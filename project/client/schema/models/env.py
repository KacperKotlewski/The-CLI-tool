import typing
from common.models.base import BaseModel
from .info import SchemaInfo
from .elements import SchemaElement
from ..versions import Version

class EnvSchema(BaseModel):
    schematizerVersion: Version = None
    schemaInfo: typing.Optional[SchemaInfo] = None
    elements: typing.List[SchemaElement] = list()
    
    def __repr__(self) -> str:
        return f"EnvSchema(schematizerVersion={self.schematizerVersion}, schemaInfo={self.schemaInfo}, elements={self.elements})"
    
    def __str__(self) -> str:
        return f'''EnvSchema
Version: {self.schematizerVersion.value}
---
{self.schemaInfo}
---'''
