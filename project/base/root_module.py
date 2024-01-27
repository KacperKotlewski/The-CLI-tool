from typing import Any
from common.CLI.module import CLImodule, ModuleType
from common.CLI import options as o
from .config import ROOT_MODULE_NAME

import typing
import sys

class RootModule(CLImodule):
    module_name: str = ROOT_MODULE_NAME
    module_type: ModuleType = ModuleType.root
    
    options: typing.List[o.Option] = [
        o.Option(
            name='help',
            complexity=o.OptionComplexity.key_only,
            key=[
                o.KeyModel(key='h', type=o.OptionKeyTypes.letter),
                o.KeyModel(key='help', type=o.OptionKeyTypes.phrase)
            ],
            details=['-h, --help','Show this help message.'],
            action = lambda self : self.print_help()
        ),
    ]
    
    user_args: typing.List[str] = None
    script_name: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.user_args = sys.argv[1:]
        self.script_name = sys.argv[0]
    
    def __call__(self) -> Any:
        if len(self.user_args) == 0:
            print(f"\nUse \"{self.script_name} -h\" or \"{self.script_name} --help\" for help and information\n")
        else:
            self.run(self.user_args)
            
    def run(self, args: typing.List[str]) -> None:
        if len(args) == 0:
            raise ValueError("No options passed")
        
        for arg in args:
            if arg.startswith("-"):
                option = self.get_option_by_key(arg)
                
            if option is None:
                raise ValueError(f"option {arg} not found")
            
            if option.complexity != o.OptionComplexity.key_only:
                pass
            if option.is_action_set():
                option(self)
        
    def print_help(self) -> None:
        print(f"\nUsage:\n{self.script_name} [OPTIONS] COMMAND [ARGS]")
        print(f'{self.get_help_info()}')