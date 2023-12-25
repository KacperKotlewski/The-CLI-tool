import typing
import pydantic
from .info import SchemaInfo
from .elements import SchemaElement
from ..versions import Version

class EnvSchema(pydantic.BaseModel):
    schematizerVersion: Version = None
    schemaInfo: SchemaInfo = None
    elements: typing.List[SchemaElement] = list()
