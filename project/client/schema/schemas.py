import pydantic
import typing
import enum

class SchemaInfo(pydantic.BaseModel):
    name: str
    description: str
    version: str
    author: str
    license: str
    
class SchemaFieldTypes(enum.Enum):
    string = "string"
    integer = "int"
    boolean = "bool"
    float = "float"
    password = "password"
    uuid = "uuid"
    regex = "regex"
    base64 = "base64"
    
class SchemaField(pydantic.BaseModel):
    name: str
    example: typing.Optional[str]
    description: typing.Optional[str]
    hint: typing.Optional[str]
    type: SchemaFieldTypes
    required: bool = False
    regex: typing.Optional[str]
    generate: bool = False
    user: bool = True
    default: typing.Optional[str]
    
class SchemaTextTypes(enum.Enum):
    header = "header"
    section = "section"
    subsection = "subsection"
    message = "message"
    space = "space"
    divider = "divider"
    
class SchemaText(pydantic.BaseModel):
    type: SchemaTextTypes
    text: typing.Optional[str]
    
SchemaElement = typing.Union[SchemaField, SchemaText]

class EnvSchema(pydantic.BaseModel):
    schematizerVersion: str
    schemaInfo: SchemaInfo
    typing.List[SchemaElement]
