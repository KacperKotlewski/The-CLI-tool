
from common.models.base import BaseModel
from ._with_help_class import BaseWithPropertyHelp
import typing
import enum

class ArgumentLikeBase(BaseModel):
    name: str = None