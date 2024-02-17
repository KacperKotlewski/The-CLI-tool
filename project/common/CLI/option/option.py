from .option_abstract import OptionAbstract, OptionType
import typing

class Option(OptionAbstract):
    """
    Option class is a class that represents an option that has a key and a value.

    Args:
        name (str): The name of the option.
        key (typing.List[KeyModel]): The key of the option.
        description (str): The description of the option.
        default_value (typing.Optional[str]): The default value of the option.
    """
    
    def __init__(self, default_value: typing.Optional[str] = None, **data) -> None:
        if default_value is not None:
            self.value = default_value
        super().__init__(**data)
        
    def _validate_key(self) -> None:
        self._validate_key_existence()
        return super()._validate_key()
