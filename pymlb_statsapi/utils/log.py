"""
created by nikos at 5/2/21
"""

import logging

root = logging.getLogger("mlb_statsapi")
root.setLevel(logging.INFO)
# root.propagate = os.environ.get('AIRFLOW_CTX_EXECUTION_DATE') is None
root.propagate = False
logging_format = [
    # '[%(asctime)s]',
    "{%(filename)s:%(lineno)d}",
    "%(name)s",
    "%(threadName)s",
    "%(levelname)s",
    "-",
    "%(message)s",
]
formatter = logging.Formatter(" ".join(logging_format))

loggers = {}


class LogMixin:
    _log = None

    @property
    def log(self):
        if self._log is None:
            self._log = get_logger(self)
        return self._log


# noinspection PyPep8Naming
def get_logger(logMixin: LogMixin):
    global loggers
    name = logMixin.__class__.__module__ + "." + logMixin.__class__.__name__
    if loggers.get(name) is None:
        loggers[name] = logging.root.getChild(name)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        loggers[name].addHandler(console)
    return loggers[name]
