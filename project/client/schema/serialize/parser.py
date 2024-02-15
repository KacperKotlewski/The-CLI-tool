from .. import models
from ..versions import Version
import typing
import re

def parse_env_to_elements(env: str) -> typing.List[models.SchemaElement]:
    elements: typing.List[models.SchemaElement] = list()
    
    
    for line in env.splitlines():
        if line.startswith("#"):
            elements.append(models.SchemaText(type=models.SchemaTextTypes.message, text=line[1:].strip()))
            
        elif "=" in line:
            comment = None
            key, value = line.split("=", 1)
            if "#" in value:
                value, comment = value.split("#", 1)
                
            element = models.SchemaField(og_name=key, default=value.strip())
            
            if comment is not None:
                element.description = comment
            elements.append(element)
    
    return elements

def build_schema(schemaInfo: models.SchemaInfo, elements: typing.List[models.SchemaElement]) -> models.Schema:
    schematizerVersion = Version.getLatest()
    schema = models.Schema(schematizerVersion = schematizerVersion, schemaInfo = schemaInfo, elements = elements)
    schema.isValid()
    return schema