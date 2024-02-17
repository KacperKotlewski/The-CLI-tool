import typing
from common.models.base import BaseModel

class BaseWithHelp(BaseModel):
    details: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_details()
        
    def _validate_details(self) -> None:
        if not isinstance(self.details, str):
            raise ValueError(f"Help info {self.details} is not a string")
    
    def get_details(self) -> str:
        return self.details
    
    def get_details_len(self) -> int:
        return len(self.details)
    
    def get_stylized_details(self, max_len:int = None) -> str:
        if not max_len is None and not isinstance(max_len, int):
            raise ValueError(f"expected INT got: {type(max_len)}")
        
        if max_len is None:
            max_len = self.get_details_len()
            
        return f"{self.details:<{max_len}s}"

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

    def get_stylized_details(self, max_len:int = None) -> str:
        if not max_len is None and not isinstance(max_len, int):
            raise ValueError(f"expected INT got: {type(max_len)}")
        
        if max_len is None:
            max_len = self.get_details_len()
            
        return f"{self.details[0]:<{max_len}s}\t\t{self.details[1]}"
    
    def get_details_len(self) -> int:
        return len(self.details[0])
    
