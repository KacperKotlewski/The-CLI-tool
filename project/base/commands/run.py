from typing import Any
import typing
from common.CLI.commands import Command
from common.CLI import options as o
from common.CLI.module import CLImodule

class Run(Command):
    name:str='run'
    short_desc:str='Run the tool on the given file'
    details:str="run <file> [options]"
    options:typing.List[o.Option]=[]
    # arguments:typing.List[a.Argument]=[
    #     a.Argument(
    #         name='file',
    #         type=a.ArgumentTypes.required,
    #     )
    # ]
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def __call__(self, module:CLImodule, args:typing.List[str]) -> Any:
        stripped_args = args[1:]
        self.run(stripped_args)