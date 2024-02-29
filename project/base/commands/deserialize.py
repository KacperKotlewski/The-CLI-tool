from typing import Any
import typing
from common.CLI_old.commands import Command
from common.CLI_old import argument as a
from common.CLI_old import options as o
from common.CLI_old.module import CLImodule

from client.schema.deserialize import parser
from client.schema import models
import os
import sys

class Deserialize(Command):
    name:str='deserialize'
    short_desc:str='Deserialize the given file - create .env file from .env.schema file.'
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
    
    input_file: typing.Optional[str]  = None
    output_file: typing.Optional[str] = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def __call__(self, module:CLImodule, args:typing.List[str]) -> Any:
        stripped_args = args[1:]
        
        self.execute(stripped_args)
        
    def execute(self, args: typing.List[str]) -> None:
        super().execute(args)
        
        #ask for file path
        if self.input_file is None:
            self.input_file = input("Enter file path: ")
        
        if not os.path.exists(self.input_file):
            print(f"File {self.input_file} does not exist")
            sys.exit(1)
            
        text = open(self.input_file, 'r').read()
        
        schema = parser.parse_env_schema(text)
        
        #print schema
        print(f"\nSchema: {self.input_file}\n\n{schema}\n\n")
        
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
                
                if not element.is_hidden():
                    print(f"\n{element.name if element.name is not None else element.og_name}")
                    if element.description is not None:
                        print(f" {element.description}") 
                    if element.example is not None:
                        print(f" example: {element.example}")
                        
                    default = "will be generated" if element.is_generated() else element.default
                    
                    while True:
                        new_value = input(f"Enter value" + (f" (default: {default}): " if default != "" else ": "))
                        
                        if new_value != "" and element.check_regex(new_value):
                            element.default = new_value
                            break
                        elif new_value == "" and element.is_generated():
                            element.default = element.generate()
                            break
                        elif new_value == "" and element.is_required() and element.default == "":
                            print(f"Field is required")
                        else:
                            break

                elif element.is_generated():
                    element.default = element.generate()
                
                descrition_str = f" # {element.description}" if element.description is not None else ""
                output_file_data += f"{element.og_name}={element.default}{descrition_str}\n"
                
                
        sname = schema.schemaInfo.name.lower().replace(' ', '_')
        if self.output_file is None:
            self.output_file = input(f"Enter output file name (default: .env." + (f".{sname}" if sname != "" else "") + "): ").strip()
        if self.output_file == "":
            self.output_file = ".env." + (f".{sname}" if sname != "" else "") + ".deserialized"
            
        print(f"Saves to {self.output_file}")
            
        with open(self.output_file, 'w') as f:
            f.write(output_file_data)
            
        
        
                
        
                