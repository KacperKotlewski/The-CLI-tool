import typing
from common.models.base import BaseModel
from .info import SchemaInfo
from .elements import SchemaElement
from ..versions import Version

def schema_text_template (schema: 'EnvSchema') -> str:
    return f'''# dotEnv schema
# CliVersion: {schema.schematizerVersion.value}
# ---
# Name: {schema.schemaInfo.name}
# Description: {schema.schemaInfo.description}
# Version: {schema.schemaInfo.version}
# Author: {schema.schemaInfo.author}
# License: {schema.schemaInfo.license}
# ---
'''


class EnvSchema(BaseModel):
    schematizerVersion: Version = None
    schemaInfo: typing.Optional[SchemaInfo] = None
    elements: typing.List[SchemaElement] = list()
    
    def to_text(self) -> str:
                
        text = schema_text_template(self)
        
        for element in self.elements:
            if isinstance(element, typing.get_args(SchemaElement)):
                t = element.to_text()
                if t:
                    text += f"\n{t}"
            else:
                text += f"\n# {element}"
                
        return text
    
    def __repr__(self) -> str:
        return f"EnvSchema(schematizerVersion={self.schematizerVersion}, schemaInfo={self.schemaInfo}, elements={self.elements})"
    
    def __str__(self) -> str:
        return f'''EnvSchema
Version: {self.schematizerVersion.value}
---
{self.schemaInfo}
---'''
