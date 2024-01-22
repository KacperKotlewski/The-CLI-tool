from common.CLI.base_class import CLI_Handler
from common.CLI.argument_classes import Argument, ArgumentComplexity, ArgumentKeyTypes, ArgumentValueTypes, KeyModel, ValueModel

import typing

import enum

class userInterfaces(enum.Enum):
    cli = "cli"
    web = "web"

class baseCLI(CLI_Handler):
    arguments = [
        Argument(
            name='help',
            complexity=ArgumentComplexity.key_only,
            key=[
                KeyModel(key='h', type=ArgumentKeyTypes.letter),
                KeyModel(key='help', type=ArgumentKeyTypes.phrase)
            ],
            help_info=f'-h, --help\t\t- show help info'
        ),
        Argument(
            name='client interface',
            complexity=ArgumentComplexity.key_and_value,
            key=[
                KeyModel(key='c', type=ArgumentKeyTypes.letter),
                KeyModel(key='client', type=ArgumentKeyTypes.phrase)
                ],
            value=ValueModel(value='client interface', type=ArgumentValueTypes.single),
            help_info=f'-c, --client [{", ".join([ui.value for ui in userInterfaces])}]\t\t- set client interface'
        ),
    ]
    module_name: str = 'base'
    
    arguments: typing.List[Argument]
    
    