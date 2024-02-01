import enum
import typing
from common.models.base import BaseModel
    
# class SchemaTextOnlyTypes(enum.Enum):
#     header = "Header"
#     section = "Section"
#     subsection = "Subsection"
#     message = "Message"

# class SchemaTextSpacerTypes(enum.Enum):
#     space = "Space"
#     divider = "Divider"
    
# class SchemaTextTypes(enum.Enum):
#     header = SchemaTextOnlyTypes.header
#     section = SchemaTextOnlyTypes.section
#     subsection = SchemaTextOnlyTypes.subsection
#     message = SchemaTextOnlyTypes.message
#     space = SchemaTextSpacerTypes.space
#     divider = SchemaTextSpacerTypes.divider

class SchemaTextTypes(enum.Enum):
    header = "Header"
    section = "Section"
    subsection = "Subsection"
    message = "Message"
    space = "Space"
    divider = "Divider"
    
class SchemaTextSpacerTypes(enum.Enum):
    space = SchemaTextTypes.space
    divider = SchemaTextTypes.divider

class SchemaText(BaseModel):
    type: SchemaTextTypes = None
    text: typing.Optional[str] = None
    
    def __str__(self) -> str:
        if self.type == SchemaTextSpacerTypes.space:
            return f"\n"
        elif self.type == SchemaTextSpacerTypes.divider:
            return f"----------"
        else:
            return f"{self.text}"