"""
created by nikos at 5/2/21
"""
import gzip
import json
import os
from time import sleep

import requests
import typing

from functools import wraps

from .log import LogMixin
from .endpoint_config import EndpointConfig
# from . import EndpointModel, EndpointAPIModel, OperationModel


class StatsAPIObject(LogMixin):
    """
    Top-level dir* for to stash each endpoint, where (file_)path will also correspond to the statsapi.mlb.com/api space.
    As these are unique per object they map to a NoSQL keyspace as well
    """

    base_url_path = r'https://statsapi.mlb.com/api'
    base_file_path = os.environ.get('PYMLB_STATSAPI__BASE_FILE_PATH', './.var/local/mlb_statsapi')
    max_get_tries = int(os.environ.get('PYMLB_STATSAPI__BASE_FILE_PATH', '3'))

    # bucket = aws.S3_DATA_BUCKET

    def __init__(
        self,
        endpoint: "EndpointModel",
        api: "EndpointAPIModel",
        operation: "OperationModel",
        path_params=None,
        query_params=None
    ):
        super(StatsAPIObject, self).__init__()
        self.endpoint = endpoint
        self.api = api
        self.operation = operation
        self.path_params, self.query_params = dict((path_params or {}).items()), dict((query_params or {}).items())
        self.path = resolve_path(self.api, self.operation, path_params, query_params)
        self.keyspace = f"{self.endpoint.get_name()}/api" + self.path
        self.file_path = os.path.realpath(f"{self.base_file_path}/{self.keyspace}.json")
        self.url = self.base_url_path + self.path  # path should start with /
        # noinspection PyTypeChecker
        self.obj: typing.Union[list, dict] = None

    def __repr__(self):
        return '{cls}(endpoint={endpoint}, api={api}, path={path})'.format(
            cls=self.__class__.__name__,
            endpoint=self.endpoint.get_name(),
            api=self.api.description,
            path=self.path
        )

    def exists(self, ext: str):
        return os.path.isfile({
            'json': self.file_path,
            'json.gz': self.gz_path,
            'json.tar.gz': self.tar_gz_path
        }[ext])

    def get(self, tries: int = 0):
        try:
            response = requests.get(self.url, headers={'Accept-Encoding': 'gzip'})
            status_code = response.status_code
            assert status_code == 200, f'get {self.url} failed with status {status_code}: {response.content.decode()}'
            self.obj = response.json()
            self.obj.pop("copyright") if isinstance(self.obj, dict) and ("copyright" in self.obj.keys()) else ()
            self.log.info("got %s from %s on try %d" % (self, self.url, tries))
            return self
        except (AssertionError, requests.exceptions.ConnectionError) as e:
            with_exception = "with %s on try %d" % (e, tries + 1)
            if tries <= self.max_get_tries:
                self.log.warning("%s.get retry %s" % (self, with_exception))
                sleep(tries)
                return self.get(tries+1)
            else:
                self.log.error("%s.get failed %s" % (self, with_exception))
                raise e

    def load(self, ext='json.gz'):
        if ext == 'json':
            with open(self.file_path, 'r') as f:
                self.obj = json.load(f)
            self.log.info("loaded %s from %s" % (self, self.file_path))
        elif ext == 'json.gz':
            with gzip.open(self.gz_path, 'r') as f:  # 4. gzip
                self.obj = json.loads(f.read().decode('utf-8'))
            self.log.info("loaded %s from %s" % (self, self.gz_path))
        else:
            raise NotImplementedError("reading from %s is not supported" % ext)
        return self

    def prefix(self, ext='json.gz'):
        return f"{self.keyspace}.{ext}"

    def dumps(self, indent=0) -> str:
        return json.dumps(self.obj, indent=indent)

    def save(self):
        if not os.path.isdir(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        with open(f"{self.file_path}", 'w') as f:
            out = f.write(json.dumps(self.obj))
        self.log.debug("saved %s to %s" % (self, self.file_path))
        # os.chmod(self.file_path, stat.S_IREAD)
        return {
            "path": self.file_path,
            "out": out
        }

    def gzip(self):
        if not os.path.isdir(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        with gzip.open(self.gz_path, 'wb') as f:
            out = f.write(json.dumps(self.obj).encode('utf-8'))
        self.log.info("gzipped %s to %s" % (self, self.gz_path))
        # os.chmod(self.gz_path, stat.S_IREAD)
        return {
            "path": self.gz_path,
            "out": out
        }

    @property
    def tar_gz_path(self):
        return f"{self.file_path}.tar.gz"

    @property
    def gz_path(self):
        return f"{self.file_path}.gz"


def resolve_path(api, operation, path_params=None, query_params=None):
    path_params, query_params = path_params or {}, query_params or {}
    path = api.path
    assert isinstance(path_params, dict)
    assert isinstance(query_params, dict)
    assert path[0] == '/'

    # PATH PARAMS
    fmt_path_params = {}
    for path_param in operation.path_params:
        param_name = path_param.name
        assert not (path_param.required and (param_name not in path_params)), 'path_param %s is required' % param_name
        if param_name in path_params:
            arg_val = path_params.pop(param_name)
            if isinstance(arg_val, list):
                assert len(arg_val) == 1, 'Multiple %s not allowed, found %s' % (param_name, str(arg_val))
                arg_val = arg_val[0]
            arg_val = str(arg_val)
            if path_param.enum is not None:
                enums = {*map(str.lower, path_param.enum)}
                assert arg_val in enums, ("Unrecognized %s %s choice:'%s'. Please choose from [%s]" % (
                    operation.nickname, param_name, arg_val, ', '.join(enums)))
            fmt_path_params[param_name] = arg_val
    assert not path_params, "Unrecognized %s path_params: '%s'. Please choose from [%s]" % (
        operation.nickname, "', '".join(path_params.keys()), ", ".join([p.name for p in operation.path_params]))

    # resolve path elements
    path = os.path.join(
        path,
        *[value for param, value in fmt_path_params.items() if (r'{%s}' % param) not in path]
    ).format(**{param: value for param, value in fmt_path_params.items() if (r'{%s}' % param) in path})

    # QUERY PARAMS
    fmt_query_params = {}
    for query_param in operation.query_params:
        param_name = query_param.name
        assert not (query_param.required and (param_name not in query_params)), "%s query_param '%s' is required!" % (
            operation.nickname, param_name)
        if param_name in query_params:
            arg_val = query_params.pop(param_name)
            if isinstance(arg_val, list):
                assert (len(arg_val) == 1) or query_param.allowMultiple, (f'multiple {param_name} not allowed, got %s' % arg_val)
                arg_val = ','.join([*map(str, arg_val)])
            else:
                arg_val = str(arg_val)
            fmt_query_params[param_name] = arg_val
    assert not query_params, "Unrecognized %s query_params: '%s'. Please choose from [%s]" % (
        operation.nickname, "', '".join(query_params.keys()), ", ".join([qp.name for qp in operation.query_params]))
    queries = [f'{p}={v}' for p, v in sorted(fmt_query_params.items(), key=lambda x: x[0])]
    if queries:
        path += ('?' + '&'.join(queries))

    return path


def configure_api(func):
    """
    A decorator that adds the path (.apis[].path) to kwargs, and optionally sets another name to look for under either
     apis[].description or apis[].operations[].nickname, which should match. When name does not match the function,
     consider this an indication of misnaming in beta-statsapi.
    """
    arg_path = 'path'
    endpoint_name = func.__module__.split('.')[-1]
    api_name = func.__name__
    func_params = func.__code__.co_varnames
    func_cfg = EndpointConfig().config[endpoint_name][api_name]

    @wraps(func)
    def wrapper(*args, **kwargs):
        path_in_args = arg_path in func_params and func_params.index(arg_path) < len(args)
        path_in_kwargs = arg_path in kwargs
        kwargs['name'] = func_cfg.get('name', api_name)
        if path_in_kwargs or path_in_args:
            return func(*args, **kwargs)
        else:
            kwargs[arg_path] = func_cfg['path']
            return func(*args, **kwargs)

    return wrapper


# def upload_file(method: callable, path_params: dict = None, query_params: dict = None, force: bool = False):
#     obj: StatsAPIObject = method(path_params=path_params, query_params=query_params)
#     res = {
#         "bucket": obj.bucket,
#         "prefix": obj.prefix(),
#         "endpoint": obj.endpoint.get_name(),
#         "path_params": obj.path_params,
#         "query_params": obj.query_params,
#         "force": force
#     }
#     if force or (not aws.S3().exists(obj.bucket, obj.prefix())):
#         obj.get().gzip()
#         obj.upload_file()
#         res.update({
#             "size": os.path.getsize(obj.gz_path),
#         })
#     return res
