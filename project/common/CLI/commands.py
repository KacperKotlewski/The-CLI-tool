import enum

from . import options as o

from ._with_options_class import BaseWithOptions
from ._with_help_class import BaseWithHelp
import typing

class Command(BaseWithOptions):
    command: str = None
    value: typing.Optional[typing.List[str]] = None
    short_desc: str
    details: str
    action: typing.Callable = None
    
    def __init__(self, **data):
        super().__init__(**data)
        # self.options.append(o.Option(
        #     name='help',
        #     complexity=o.OptionComplexity.key_only,
        #     key=[
        #         o.KeyModel(key='h', type=o.OptionKeyTypes.letter),
        #         o.KeyModel(key='help', type=o.OptionKeyTypes.phrase)
        #     ],
        #     details=['-h, --help', 'Show this help message.'],
        # ))
        
    def print_help(self):
        pass
        # print(f'{self.help_info}')
        # print(f'\nOptions:\n{self.get_help_info()}\n')