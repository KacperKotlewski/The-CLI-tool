from typing import Any
import typing
from common.CLI.commands import Command
from common.CLI import argument as a
from common.CLI import options as o
from common.CLI.module import CLImodule

from client.schema.serialize import parser
from client.schema import models
import os
import sys
import requests

class Serialize(Command):
    name:str='serialize'
    short_desc:str='Serialize the given file'
    usage:str="serialize [options]"
    details:str="serialize [options]"
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
            details=['-i, --input <file>', 'Set the input file to serialize.'],
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
        
    def strip_user_msg(self, message: str) -> str:
        if message.strip().endswith(":"):
            message = ":".join(message.split(":")[:-1])
        return message
                
    def user_input_string(self, message: str) -> str:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        return input(f'{message}: ')
    
    def user_input_accept(self, message: str) -> bool:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
            
        return input(f"{message} (y/n): ").lower() == "y"
    
    def user_input_int(self, message: str) -> int:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        
        while True:
            try:
                return int(input(f"{message}: "))
            except ValueError:
                print("Invalid value. Input must be an integer number")
    
    def user_input_choice(self, choices: typing.List[str], message: str) -> str:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        
        print("Choose from the following options:")
        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice}")
        
        while True:
            try:
                choice = int(input(f"{message}: "))
                if choice < 1 or choice > len(choices):
                    raise ValueError()
                return choices[choice-1]
            except ValueError:
                print("Invalid value. Input must be a number corresponding to the option")
    
                
                
    def create_schema_info(self) -> models.SchemaInfo:
        print("Enter schema information:")
        name = self.user_input_string("Enter name of this schema: ")
        description = self.user_input_string("Enter description: ")
        version = self.user_input_string("Enter version: ")
        author = self.user_input_string("Enter author: ")
        
        licence_choice = self.user_input_choice(["Detect", "Choose established license", "Custom license", "None"], "Choose license type: ")
        
        license = None
        
        if licence_choice == "Choose established license" or licence_choice == "Detect":
            licenses = requests.get("https://api.github.com/licenses").json()
            license_names = [license["spdx_id"] for license in licenses]
            
            if licence_choice == "Choose established license":
                license = self.user_input_choice(license_names, "Choose license: ")
            elif licence_choice == "Detect":
                for root, dirs, files in os.walk("."):
                    if "LICENSE" in files:
                        with open(os.path.join(root, "LICENSE"), 'r') as f:
                            license_content = f.read()
                            
                        for lic_name in license_names:
                            if lic_name in license_content:
                                if self.user_input_accept(f"Detected license: {lic_name}\nUse this license?"):
                                    license = lic_name
                                    break
                        break
        
        elif licence_choice == "Custom license":
            license = self.user_input_string("Enter license: ")
            
        elif licence_choice == "None":
            license = "None"
            
        
        return models.SchemaInfo(
            name=name,
            description=description,
            version=version,
            author=author,
            license=license,
        )
        
        
    def run(self, args: typing.List[str]) -> None:
        super().run(args)
        
        #ask for file path
        if self.input_file is None:
            self.output_file = input("Enter file path: ")
        
        if not os.path.exists(self.output_file):
            print(f"File {self.output_file} does not exist")
            sys.exit(1)
           
        print("Serializing .env data...")
        elements = None
        with open(self.output_file, 'r') as f:
            elements = parser.parse_env_to_elements(f.read())
            
        print("Serializing finished\n")
        
        print("Now I will ask you to fill a data for the schema")
        schemaInfo = self.create_schema_info()
        
        
        
        
        self.output_file = "schema.env-serialized"
        
        parsed = parser.build_schema(schemaInfo, elements).to_text()
            
        with open(self.output_file, 'w') as f:
            f.write(parsed)
        
        
                
        
                