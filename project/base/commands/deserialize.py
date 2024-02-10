from typing import Any
import typing
from common.CLI.commands import Command
from common.CLI import argument as a
from common.CLI import options as o
from common.CLI.module import CLImodule

from client.schema.deserialize import parser
from client.schema import models
import os
import sys

class Deserialize(Command):
    name:str='deserialize'
    short_desc:str='Deserialize the given file'
    usage:str="deserialize [options]"
    details:str="deserialize [options]"
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
        o.Option(
            name="input schema file",
            complexity=o.OptionComplexity.key_and_value,
            key=[
                o.KeyModel(key='i', type=o.OptionKeyTypes.letter),
                o.KeyModel(key='input', type=o.OptionKeyTypes.phrase)
            ],
            details=['-i, --input <file>', 'Set the input file to deserialize.'],
            value = o.ValueModel(
                type=o.OptionValueTypes.single,
                value=None
            ),
            action = lambda self, args: setattr(self, 'input_file', args[0])
        ),
    ]
    arguments:typing.List[a.Argument]=[
        # a.Argument(
        #     name='input',
        #     type=a.ArgumentTypes.required,
        # ),
        # # a.Argument(
        # #     name='output',
        # #     short_desc
        # #     type=a.ArgumentTypes.required,
        # # )
    ]
    
    input_file: str = None
    output_file: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def __call__(self, module:CLImodule, args:typing.List[str]) -> Any:
        stripped_args = args[1:]
        
        self.run(stripped_args)
        
    def run(self, args: typing.List[str]) -> None:
        super().run(args)
        
        #ask for file path
        if self.input_file is None:
            self.output_file = input("Enter file path: ")
        
        if not os.path.exists(self.output_file):
            print(f"File {self.output_file} does not exist")
            sys.exit(1)
            
        text = open(self.output_file, 'r').read()
        
        schema = parser.parse_env_schema(text)
        
        #print schema
        print(f"\nSchema: {self.output_file}\n\n{schema}\n\n")
        
        output_file_data = ""
        
        for element in schema.elements:
            # print(element)
            
            if isinstance(element, models.SchemaText):
                if element.type == models.SchemaTextTypes.header:
                    size = len(element.text)
                    print(size*"-" + f"\n{element.text.upper()}\n" + size*"-" + "")
                elif element.type == models.SchemaTextTypes.section:
                    print(f"\n---- {element.text.upper()} ----")
                elif element.type == models.SchemaTextTypes.subsection:
                    print(f" {element.text.upper()} ")
                else:
                    print(f"{element}")
                    
                output_file_data += f"# {element}\n"
                    
            elif isinstance(element, models.SchemaField):
                print(f"\n{element.name}:\n {element.description}\n example: {element.example}")
                new_value = input(f"Enter value (default: {element.default}): ")
                if new_value != "":
                    element.default = new_value
                
                output_file_data += f"{element.og_name}={element.default}\n"
                
                
        # if self.output_file is None:
        #     self.output_file = input("Enter output file name (default: .env): ")
        # if self.output_file == "":
        #     self.output_file = ".env"
        self.output_file = ".env"
            
        with open(self.output_file, 'w') as f:
            f.write(output_file_data)
            
        
        
                
        
                