from .option_abstract import OptionAbstract, OptionType

import typing

class Argument(OptionAbstract):
    """
    Argument class is a class that represents an argument that has a value and can have a key.
    
    Args:
        name (str): The name of the argument.
        key (typing.List[KeyModel]): The key of the argument.
        description (str): The description of the argument.
        default_value (typing.Optional[str]): The default value of the argument.
    """
    _type = OptionType.argument
    
    def __init__(self, default_value: typing.Optional[str] = None, **data) -> None:
        if default_value is not None:
            self.value = default_value
        super().__init__(**data)