import typing
import pydantic
from .info import SchemaInfo
from .elements import SchemaElement

class EnvSchema(pydantic.BaseModel):
    schematizerVersion: str
    schemaInfo: SchemaInfo
    typing.List[SchemaElement]
