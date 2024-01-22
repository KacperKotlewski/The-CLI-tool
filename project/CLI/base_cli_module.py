from typing import Any
from common.CLI.model import CLI_Model
from common.CLI.argument_classes import Argument, ArgumentComplexity, ArgumentKeyTypes, ArgumentValueTypes, KeyModel, ValueModel

import typing

import enum

import sys

class userInterfaces(enum.Enum):
    cli = "cli"
    web = "web"

class baseCLI(CLI_Model):
    arguments = [
        Argument(
            name='help',
            complexity=ArgumentComplexity.key_only,
            key=[
                KeyModel(key='h', type=ArgumentKeyTypes.letter),
                KeyModel(key='help', type=ArgumentKeyTypes.phrase)
            ],
            help_info=f'-h, --help\t\t- show help info',
            action = lambda self : self.print_help()
        ),
    ]
    module_name: str = 'base'
    
    arguments: typing.List[Argument]
    
    user_args: typing.List[str] = None
    script_name: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.user_args = sys.argv[1:]
        self.script_name = sys.argv[0]
    
    def __call__(self) -> Any:
        if len(self.user_args) == 0:
            print(f"{self.script_name} <commands>")
            print("\nUse -h or --help for help info")
        else:
            self.run(self.user_args)
            
    def run(self, arguments: typing.List[str]) -> None:
        pass
        
    def print_help(self) -> None:
        print(self.help_info())