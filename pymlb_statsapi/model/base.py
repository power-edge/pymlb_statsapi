"""
created by nikos at 4/21/21
"""

from serde import Model, fields, tags

from pymlb_statsapi.utils.log import LogMixin
from pymlb_statsapi.utils.schema_loader import sl
from pymlb_statsapi.utils.stats_api_object import StatsAPIObject


class MLBStatsAPIModel(Model):
    _instance = None
    apiVersion: fields.Str()
    src_url: fields.Str()
    swaggerVersion: fields.Str()

    @classmethod
    def read_doc_str(cls, schema_name: str):
        return sl.read_stats_schema(schema_name)

    @classmethod
    def read_doc(cls, schema_name: str):
        return sl.load_stats_schema(schema_name)

    @classmethod
    def from_doc(cls, schema_name: str = None):
        if cls._instance is None:
            cls._instance = cls.from_json(
                cls.read_doc_str(schema_name) or cls.__module__.split(".")[-1]
            )
        return cls._instance


class ResponseMessage(Model):
    code: fields.Int()
    message: fields.Optional(fields.Str)
    responseModel: fields.Optional(fields.Str)


class ItemType(Model):
    type: fields.Str()


class Parameter(Model):
    allowMultiple: fields.Bool()
    defaultValue: fields.Str()
    description: fields.Str()
    name: fields.Str()
    paramType: fields.Choice(["path", "query"])
    required: fields.Bool()
    type: fields.Str()
    items: fields.Optional(fields.Nested(ItemType))
    # optional
    items: fields.Optional(fields.Nested(ItemType))
    uniqueItems: fields.Optional(fields.Bool)
    # even more optional
    enum: fields.Optional(fields.List(fields.Str))


class OperationModel(Model):
    consumes: fields.List(fields.Str)
    deprecated: fields.Str()
    method: fields.Choice(["GET", "POST"])
    nickname: fields.Str()
    notes: fields.Str()
    parameters: fields.List(Parameter)
    produces: fields.List(fields.Str)
    responseMessages: fields.List(ResponseMessage)
    summary: fields.Str()
    type: fields.Str()

    # optional
    items: fields.Optional(fields.Nested(ItemType))
    uniqueItems: fields.Optional(fields.Bool)

    @property
    def path_params(self):
        return [param for param in self.parameters if param.paramType == "path"]

    @property
    def query_params(self):
        return [param for param in self.parameters if param.paramType == "query"]


class APIModelBase(Model):
    description: fields.Str()
    path: fields.Str()

    class Meta:
        tag = tags.Internal(tag="apis")


class EndpointAPIModel(APIModelBase):
    operations: fields.List(OperationModel)

    @property
    def operations_map(self):
        return {o.nickname: o for o in self.operations if o.method == "GET"}

    @property
    def operation(self):
        return self.operations_map[self.description]


class EndpointModel(MLBStatsAPIModel, LogMixin):
    """
    Each api in the api_docs gets an inheriting class to define methods to for the endpoint access patterns.

    Some of the api doc json files have small naming issues, therefore the @api_path wraps functions to make explicit
    the path and name to search, where the name corresponds to the api.description or the api.operation.nickname, but
    method names are corrected for misnaming in the underlying documentation.

    These methods return a StatsAPIFileObject which is endpoint/api aware, and can get, save, and load itself.
    """

    _methods = None

    apis: fields.List(EndpointAPIModel)
    api_path: fields.Str()
    basePath: fields.Str()
    consumes: fields.List(fields.Str)
    # models: fields.Dict(fields.Str, )  # very complex serde and *not* necessary for stashing responses in a data store
    produces: fields.List(fields.Str)
    resourcePath: fields.Str()

    class Meta:
        tag = tags.Internal(tag="endpoint")

    def get_name(self):
        name = self.api_path.split("/")[-1]
        return name

    @property
    def _api_path_name_map(self):
        return {(api.path, api.description): api for api in self.apis}

    @property
    def _api_description_map(self):
        return {api.description: api for api in self.apis}

    def get_api_file_object(self, **kwargs):
        path, name = kwargs["path"], kwargs["name"]
        api = self._api_path_name_map[path, name]
        operation = api.operations_map[name]
        path_params, query_params = (
            kwargs.get("path_params"),
            kwargs.get("query_params"),
        )
        return StatsAPIObject(
            endpoint=self,
            api=api,
            operation=operation,
            path_params=path_params,
            query_params=query_params,
        )
