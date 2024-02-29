from .option_abstract import OptionAbstract

class Flag(OptionAbstract):
    """
    Flag class is a class that represents a flag that has a key and boolean value. Default value is False.
    
    Args:
        name (str): The name of the flag.
        key (typing.List[KeyModel]): The key of the flag.
        description (str): The description of the flag.
    """
    _value = False
    _require_argument = False
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_value()
    
    def _validate_key(self) -> None:
        self._validate_key_existence()
        return super()._validate_key()
        
    def _validate_value(self) -> None:
        """
        _validate_value validates the value of the flag.
        
        Raises:
            ValueError: If the value of the flag is not a boolean.
        """
        if self.value is not None and not isinstance(self.value, bool):
            raise ValueError(f"Flag {self.name} has value {self.value} that is not a boolean")
        
    def set_value(self, value: bool=True) -> None:
        if not isinstance(value, bool):
            raise ValueError(f"Flag {self.name} has value {value} that is not a boolean")
        self._value = value
        
    def is_set(self) -> bool:
        return self._value

    def __str__(self) -> str:
        return f"Flag: {self.name}, {self.description}, {self.value}"