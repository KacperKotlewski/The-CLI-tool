import typing
from common.models.base import BaseModel

class BaseWithHelp(BaseModel):
    details: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_details()
        
    def _validate_details(self) -> None:
        raise BaseException("_validate_details not implemented yet")

class BaseWithPropertyHelp(BaseWithHelp):
    details: typing.List[str] = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate_details(self) -> None:
        if not isinstance(self.details, list):
            raise ValueError(f"Help info {self.details} is not a list")
        
        if len(self.details) != 2:
            raise ValueError(f"Help info {self.details} is not a list of length 2,\n - First element should be an string of usage for example: \"-h, --help\"\n - Second element should be an string of help info for example: \"Show this help message.\"")
        
        if not all(isinstance(arg, str) for arg in self.details):
            raise ValueError(f"Help info {self.details} is not a list of strings")

    
