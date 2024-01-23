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
            print(f"\n{self.script_name} <commands>")
            print(f"\nUse \"{self.script_name} -h\" or \"{self.script_name} --help\" for help and information\n")
        else:
            self.run(self.user_args)
            
    def run(self, args: typing.List[str]) -> None:
        if len(args) == 0:
            raise ValueError("No arguments passed")
        
        for arg in args:
            if arg.startswith("-") or arg.startswith("--"):
                argument = self.get_argument_by_key(arg.strip("-"))
            if argument is None:
                raise ValueError(f"Argument {arg} not found")
            if argument.complexity != ArgumentComplexity.key_only:
                pass
            if argument.is_action_set():
                argument(self)
        
    def print_help(self) -> None:
        print(self.help_info())