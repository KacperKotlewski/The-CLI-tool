import typing
from common.models.base import BaseModel
from .info import SchemaInfo
from .elements import SchemaElement
from ..versions import Version

class EnvSchema(BaseModel):
    schematizerVersion: Version = None
    schemaInfo: SchemaInfo = None
    elements: typing.List[SchemaElement] = list()
