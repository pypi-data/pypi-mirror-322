from typing import Type, TypeVar, Optional, Callable, Union

from nonebot import get_plugin_config
from pydantic import VERSION, BaseModel

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2

class ConfigError(RuntimeError):
    def __init__(self, msg: Optional[str]):
        self.msg = msg

    def __str__(self):
        return self.msg or ""


_conf = {}


if PYDANTIC_V2:
    BaseSettings = BaseModel

    from pydantic import ValidationError

    def default_error_msg(e: ValidationError) -> str:
        for raw in e.errors():
            if raw["type"] == "missing":
                required_loc = '/'.join(raw["loc"])
                return f"请设置{required_loc}，否则本插件无法正常工作"
        return str(e)
else:
    from pydantic import ValidationError, MissingError, BaseSettings
    from pydantic.error_wrappers import ErrorWrapper

    def default_error_msg(e: ValidationError | ErrorWrapper) -> str:
        for raw in e.raw_errors:
            if isinstance(raw.exc, MissingError):
                return f"请设置{raw.loc_tuple()[0].upper()}，否则本插件无法正常工作"
            elif isinstance(raw.exc, ValidationError):
                return default_error_msg(raw.exc)
        return str(e)


T = TypeVar("T", bound=BaseSettings)


def load_conf(t_conf: Type[T], error_msg: Union[str, Callable[[ValidationError], str]] = default_error_msg) -> T:
    global _conf
    if t_conf not in _conf:
        try:
            _conf[t_conf] = get_plugin_config(t_conf)
        except ValidationError as e:
            if callable(error_msg):
                error_msg = error_msg(e)
            raise ConfigError(error_msg) from e
    return _conf[t_conf]

__all__ = ("ConfigError", "load_conf")
