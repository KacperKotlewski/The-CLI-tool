import enum
import typing
import pydantic
    
class SchemaTextTypes(enum.Enum):
    header = "Header"
    section = "Section"
    subsection = "Subsection"
    message = "Message"
    space = "Space"
    divider = "Divider"
    
class SchemaText(pydantic.BaseModel):
    type: SchemaTextTypes
    text: typing.Optional[str] = None