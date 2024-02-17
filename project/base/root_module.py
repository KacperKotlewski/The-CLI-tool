from typing import Any
from common.CLI_old.module import CLImodule, ModuleType
from common.CLI_old import options as o
from common.CLI_old import commands as c
from .config import ROOT_MODULE_NAME
from client.schema.versions import Version
from . import commands as baseCommands

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
            action = lambda self,args : self.print_help()
        ),
        o.Option(
            name='version',
            complexity=o.OptionComplexity.key_only,
            key=[
                o.KeyModel(key='v', type=o.OptionKeyTypes.letter),
                o.KeyModel(key='version', type=o.OptionKeyTypes.phrase)
            ],
            details=['-v, --version', 'Show version of the tool'],
            action= lambda self, args : self.print_version(),
        ),
    ]
    
    commands: typing.List[c.Command] = [
        baseCommands.Run(),
        baseCommands.Deserialize(),
        baseCommands.Serialize(),
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
                self.run_option(arg, args)
            else:
                command = self.get_command(arg)
                
                if command is None:
                    raise ValueError(f"command {arg} not found")
                
                command(self, args)
                break
                
        
    def print_help(self) -> None:
        print(f"\nUsage:\n{self.script_name} [OPTIONS] COMMAND [ARGS]")
        print(f'{self.get_details()}')
        
    def print_version(self) -> None:
        print(f"\nVersion: {Version.getLatest().value}\n")