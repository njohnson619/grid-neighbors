import logging
import sys
from typing import cast, Any


# DEBUG is 10 and 5 is already registered by other libs, so something in between
# https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
_TRACE = 7
def _trace(self: logging.Logger, message: Any, *args, **kwargs) -> None:
    if self.isEnabledFor(_TRACE):
        self._log(_TRACE, message, args, **kwargs)

def _trace_root(message, *args, **kwargs):
    logging.log(_TRACE, message, *args, **kwargs)

logging.addLevelName(_TRACE, "TRACE")
setattr(logging, "TRACE", _TRACE)
setattr(logging.getLoggerClass(), "trace", _trace)
setattr(logging, "trace", _trace_root)


class TraceLogger(logging.Logger):
    def trace(self, msg, *args, **kwargs):
        pass

def create_logger(name: Any = None, level: Any = None) -> TraceLogger:
    log = cast(TraceLogger, logging.getLogger(name or "MyLogger"))
    log.propagate = False
    log.setLevel(level or logging.INFO)
    if not log.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("{asctime}: {levelname:<8s}{thread!s:<15.15s} [{name:<15.15s}] {message:s}", style="{")
        )
        log.addHandler(handler)
    return log

def set_global_log_level(level: int):
    # TODO: remove when dependencies are configured correctly. for now, force same level
    #   across all loggers to avoid missing any helpful logs
    all_loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for l in all_loggers:
        l.setLevel(level)
