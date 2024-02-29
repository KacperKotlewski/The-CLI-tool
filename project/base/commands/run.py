from typing import Any
import typing
from common.CLI_old.commands import Command
from common.CLI_old import argument as a
from common.CLI_old import options as o
from common.CLI_old.module import CLImodule

class Run(Command):
    name:str='run'
    short_desc:str='Run the tool on the given file'
    details:str="run <file> [options]"
    options:typing.List[o.Option]=[
        # o.Option(
        #     name='mode',
        #     complexity=o.OptionComplexity.key_and_value,
        #     key=[
        #         o.KeyModel(key='m', type=o.OptionKeyTypes.letter),
        #         o.KeyModel(key='mode', type=o.OptionKeyTypes.phrase)
        #     ],
        #     details=['-m, --mode <mode>', 'Set the mode to run the tool in.'],
        # ),
    ]
    arguments:typing.List[a.Argument]=[
        a.Argument(
            name='file',
            type=a.ArgumentTypes.required,
        )
    ]
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def __call__(self, module:CLImodule, args:typing.List[str]) -> Any:
        stripped_args = args[1:]
        self.run(stripped_args)