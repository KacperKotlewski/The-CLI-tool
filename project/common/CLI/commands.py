import enum
from typing import Any

from . import options as o

from ._with_options_class import BaseWithOptions
from ._with_help_class import BaseWithHelp
from ._with_arguments_class import ArgumentLikeBase
import typing

class Command(BaseWithOptions, ArgumentLikeBase, BaseWithHelp):
    short_desc: str
    
    def __init__(self, **data):
        super().__init__(**data)
        self.options.insert(0, o.Option(
            name='help',
            complexity=o.OptionComplexity.key_only,
            key=[
                o.KeyModel(key='h', type=o.OptionKeyTypes.letter),
                o.KeyModel(key='help', type=o.OptionKeyTypes.phrase)
            ],
            details=['-h, --help', 'Show this help message.'],
            action=lambda self, args: self.print_help()
        ))
        
    def print_help(self):
        print(f'\nUsage:\n{self.details}')
        print(f'{self.get_details()}')
        
    def get_stylized_details(self, strlen: int) -> str:
        return super().get_stylized_details(strlen) + f'\t\t{self.short_desc}'
    
    def run(self, args: typing.List[str]) -> None:
        for arg in args:
            if arg.startswith("-"):
                self.run_option(arg, args)
            else:
                raise ValueError(f"command {arg} not found")
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError(f"Command __call__ not implemented for {self.name}")