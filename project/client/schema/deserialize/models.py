import pydantic
import typing
from .. import models

class ParseData(pydantic.BaseModel):
    line: str
    line_count: int
    schema_model: typing.Union[models.Schema, models.SchemaInfo, models.SchemaElement]
    flag: typing.Optional[bool] = None