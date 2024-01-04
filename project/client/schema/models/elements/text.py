import enum
import typing
from common.models.base import BaseModel
    
class SchemaTextTypes(enum.Enum):
    header = "Header"
    section = "Section"
    subsection = "Subsection"
    message = "Message"
    space = "Space"
    divider = "Divider"
    
class SchemaText(BaseModel):
    type: SchemaTextTypes = None
    text: typing.Optional[str] = None