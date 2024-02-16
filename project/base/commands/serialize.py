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
                
    def user_input_string(self, message: str, required:bool=False, return_none:bool=False) -> str:
        if required and return_none:
            raise ValueError("required and return_none cannot be both True")
        
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        
        while True:
            input_ = input(f'{message}: ')
            if input_ != "" or (not required and input_ == "" and not return_none):
                return input_
            elif not required and input_ == "" and return_none:
                return None
            else:
                print("Value is required")
    
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
    
    def user_input_choice(self, choices: typing.List[str], message: str, escape:bool=False) -> str:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        
        print("Choose from the following options:")
        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice}")
        if escape:
            print("Type 'escape' to cancel")
        
        while True:
            try:
                inp = input(f"{message}: ")
                if escape and inp.lower() == "escape":
                    return None
                choice = int(inp)
                if choice < 1 or choice > len(choices):
                    raise ValueError()
                return choices[choice-1]
            except ValueError:
                print("Invalid value. Input must be a number corresponding to the option")
                
    def user_input_choose_item(self, items: typing.List[models.SchemaElement], message: str, escape:bool=False, allow_empty_element:bool=False) -> typing.Tuple[int, models.SchemaElement]:
        if message is None:
            message = "Enter value"
        message = self.strip_user_msg(message)
        
        print("Choose from the following options:")
        for i, item in enumerate(items):
            if item is None:
                if allow_empty_element:
                    print(f"{i+1}. --- Empty ---")
            else:
                print(f"{i+1}. {item.introduce()}")
        if escape:
            print("Type 'escape' to cancel")
        
        while True:
            try:
                inp = input(f"{message}: ")
                if escape and inp.lower() == "escape":
                    return None, None
                choice = int(inp)
                if choice < 1 or choice > len(items):
                    raise ValueError()
                return choice-1, items[choice-1]
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
        
        while license is None:
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
        
    # def go_through_elements(self, elements: typing.List[models.SchemaElement]) -> typing.List[models.SchemaElement]:
    
    def edit_field(self, element: models.SchemaField) -> models.SchemaField:
        print(f"Editing field: {element.og_name}")
        
        inp = lambda message: self.user_input_string(message, return_none=True)
        
        og_name = inp("Enter field key" + f"(current: {element.og_name})")
        name = inp("Enter display name" + (f"(current: {element.name})" if element.name else ""))
        description = inp("Enter description" + (f"(current: {element.description})" if element.description else ""))
        hint = inp("Enter hint" + (f"(current: {element.hint})" if element.hint else ""))
        default = inp("Enter default value" + (f"(current: {element.default})" if element.default else ""))
        regex = inp("Enter regex" + (f"(current: {element.regex})" if element.regex else ""))
        error = inp("Enter error message" + (f"(current: {element.error})" if element.error else ""))
        
        props = list()
        for prop in models.SchemaFieldProps:
            enabled = element.props is not None and prop in element.props
            answer = self.user_input_accept(f"Is {prop.value} set?" + (f" (current: {'yes' if enabled else 'no'})" if enabled else ""))
            if answer:
                props.append(prop)
                
        if len(props) == 0:
            props = None
                
        new_elem = element.__deepcopy__()
        new_elem.og_name = og_name if og_name else element.og_name
        new_elem.name = name if name else element.name
        new_elem.description = description if description else element.description
        new_elem.hint = hint if hint else element.hint
        new_elem.default = default if default else element.default
        new_elem.regex = regex if regex else element.regex
        new_elem.props = props if props else element.props
        new_elem.error = error if error else element.error
        
        return new_elem
        
    def edit_text(self, element: models.SchemaText) -> models.SchemaText:
        no_text = [models.SchemaTextTypes.space, models.SchemaTextTypes.divider]
        
        print(f"Editing text element: {element.type.value} : {element.text if element.text else ''}")
        
        if element.type in no_text:
            new_type = self.user_input_choice([t.value for t in models.SchemaTextTypes if t not in no_text], "Choose new type")
            text = None
            if not new_type in no_text:
                text = self.user_input_string(f"Enter text (current: {element.text if element.text else ''})")
            return models.SchemaText(type=new_type, text=text)
        else:
            new_type = self.user_input_choice(["Type", "Text"], "Choose what to edit")
            if new_type == "Type":
                new_type = self.user_input_choice([t.value for t in models.SchemaTextTypes], "Choose new type")
                return models.SchemaText(type=new_type, text=element.text)
            elif new_type == "Text":
                text = self.user_input_string(f"Enter text (current: {element.text if element.text else ''})")
                return models.SchemaText(type=element.type, text=text)
        
    def edit_element(self, element: models.SchemaElement) -> models.SchemaElement:
        if isinstance(element, models.SchemaField):
            return self.edit_field(element)
        elif isinstance(element, models.SchemaText):
            return self.edit_text(element)
        
        
    def create_new_field(self) -> models.SchemaField:
        print("Enter field information:")
        og_name = self.user_input_string("Enter field (example: DATABASE_PASSWORD)", required=True)
        name = self.user_input_string("Enter display name", return_none=True)
        default = self.user_input_string("Enter default value")
        description = self.user_input_string("Enter description", return_none=True)
        example = self.user_input_string("Enter example", return_none=True)
        hint = self.user_input_string("Enter hint", return_none=True)
        # type_ = self.user_input_string("Enter type")
        regex = self.user_input_string("Enter regex", return_none=True)
        error_msg = self.user_input_string("Enter error message", return_none=True)
        
        props = list()
        for elem in models.SchemaFieldProps:
            answer = self.user_input_accept(f"Is {elem.value} set?")
            if answer:
                props.append(elem)
        
        return models.SchemaField(
            og_name=og_name,
            default=default,
            name=name,
            example=example,
            description=description,
            hint=hint,
            # type=type.
            regex=regex,
            props=props,
            error=error_msg
        )
        
    def create_new_text(self) -> models.SchemaText:
        print("Enter text information:")
        choices = [e.value for e in models.SchemaTextTypes]
        type_ = self.user_input_choice(choices, "Choose text type")
        type_ = models.SchemaTextTypes(type_)
        if type_ in [models.SchemaTextTypes.space, models.SchemaTextTypes.divider]:
            return models.SchemaText(type=type_)
        else:
            text = self.user_input_string("Enter text")
            return models.SchemaText(type=type_, text=text)
    
    def create_new_element(self) -> models.SchemaElement:
        choices = ["Field", "Text"]
        choice = self.user_input_choice(choices, "Choose element type", escape=True)
        
        if choice == "Field":
            return self.create_new_field()
        elif choice == "Text":
            return self.create_new_text()
        
    def insert_element(self, element: models.SchemaElement, elements: typing.List[models.SchemaElement]) -> typing.List[models.SchemaElement]:
        index, elem = self.user_input_choose_item(elements, "Choose position", allow_empty_element=True)
        if index is None:
            return None
        
        elements.insert(index, element)
        return elements
    
    def last_think_before_save(self, schema: models.Schema) -> models.Schema:
        
        while True:
            
            choices = ["View", "Edit", "Save"]
            print("\n\n--------- Options ---------\n")
            choice = self.user_input_choice(choices, "What do you want to do?")
            
            if choice == "View":
                choice = self.user_input_choice(["Schema", "Elements"], "What do you want to view?")
                if choice == "Schema":
                    print("\n\n--------- Schema ---------\n")
                    print(schema.to_text())
                    input("Press key to continue")
                elif choice == "Elements":
                    print("\n\n--------- Elements ---------\n")
                    for element in schema.elements:
                        print(element.introduce())
                    input("Press key to continue")
                
            elif choice == "Save":
                break
            
            elif choice == "Edit":               
                
                while True:
                    choices = ["Change schema info", "Edit element", "Add element", "Remove element", "Change element position", "Finish editing"]
                    choice = self.user_input_choice(choices, "What do you want to do?")
                    if choice == "Change schema info":
                        schema.schemaInfo = self.create_schema_info()
                        
                    elif choice == "Edit element":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to edit", escape=True)
                        schema.elements[index] = self.edit_element(element)
                        
                    elif choice == "Add element":
                        element = self.create_new_element()
                        schema.elements = self.insert_element(element, schema.elements+[None])

                    elif choice == "Remove element":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to delete", escape=True)
                        schema.elements.pop(index)
                    
                    elif choice == "Change element position":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to change position", escape=True)
                        if index is None:
                            continue
                        trimmed_list = schema.elements[:index] + schema.elements[index+1:] + [None]
                        schema.elements = self.insert_element(element, trimmed_list)
                        # filter none values
                        schema.elements = [elem for elem in schema.elements if elem is not None]
                    
                    elif choice == "Finish editing":
                        break
                    
                    schema.elements = [elem for elem in schema.elements if elem is not None]
                    
        return schema
        
        
        
        
        
    def run(self, args: typing.List[str]) -> None:
        super().run(args)
        
        #ask for file path
        if self.input_file is None:
            self.input_file = input("Enter file path: ")
        
        if not os.path.exists(self.input_file):
            print(f"File {self.input_file} does not exist")
            sys.exit(1)
           
        print("Serializing .env data...")
        elements = None
        with open(self.input_file, 'r') as f:
            elements = parser.parse_env_to_elements(f.read())
            
        print("Serializing finished\n")
        
        print("Now I will ask you to fill a data for the schema")
        schemaInfo = self.create_schema_info()
        
        
        schema = self.last_think_before_save(parser.build_schema(schemaInfo, elements))
        
        sname = schema.schemaInfo.name.lower().replace(' ', '_')
        if self.output_file is None:
            self.output_file = input(f"Enter output file name (default: .env" + (f".{sname}" if sname != "" else "") + ".schema): ").strip()
        if self.output_file == "":
            self.output_file = ".env" + (f".{sname}" if sname != "" else "") + ".schema"
            
        print(f"Saves to {self.output_file}")
            
        with open(self.output_file, 'w', encoding="utf-8") as f:
            f.write(schema.to_text())
        
        
                
        
                