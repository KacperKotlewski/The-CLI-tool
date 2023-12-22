from .. import models
from . import exceptions as exc
from .. import versions
import pydantic
import typing

    
def get_key_and_value(line:str) -> typing.Tuple[str, str]:
    (key,value) = line.split(":")
    key = key.strip()
    value = value.strip()
    return (key,value)
