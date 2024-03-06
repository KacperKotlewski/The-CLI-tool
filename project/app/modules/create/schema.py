import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory, OptionBuilder, OptionHandler
from common.CLI.module.root_module import RootModule
from common.CLI.interface import UserInterface
import typing


from client.schema.serialize import parser
from client.schema import models
import requests

@command(
    name = "schema",
    description = "Create a new .env.schema file.",
    help_str = "Create a new .env.schema file in the project.",
    option_handler = [
         OptionFactory.argument(
            name='input',
            keys=['-i', '--input'],
            description='Input .env file to deserialize.',
            required=True
        ),
        OptionFactory.option(
            name='output',
            keys=['-o', '--output'],
            description='Output filename for .env.schema file.',
            required=False
        ),
    ]
)
class SchemaCommand(Command):   
    
    def user_input_choose_item(self, items: typing.List[models.SchemaElement], message: str, required:bool=False) -> typing.Tuple[int, models.SchemaElement]:
        strings = []
        for item in items:
            if item is None:
                strings.append("----- Empty -----")
            elif isinstance(item, typing.get_args(models.SchemaElement)):
                strings.append(item.introduce())
        choice = self._ui.choose(message, strings, required)
        
        if choice is not None:
            item = items[choice-1]
            return choice-1, item
        else:
            return None, None
    
    def user_input_choose_string(self, message: str, choices: typing.List[str]=None, required:bool=False) -> str:
        if choices is None:
            return ""
        choice = self._ui.choose(message, choices, required)
        if choice is not None:
            return choices[choice-1]
        return None
                
                
    def create_schema_info(self) -> models.SchemaInfo:
        self._ui.message("Enter schema information:")
        name = self._ui.prompt("Enter name of this schema: ")
        description = self._ui.prompt("Enter description: ")
        version = self._ui.prompt("Enter version: ")
        author = self._ui.prompt("Enter author: ")
        
        
        license = None
        
        while license is None:
            licence_choice = self.user_input_choose_string(message="Choose license type: ", choices=["Detect", "Choose established license", "Custom license", "None"])
        
            if licence_choice == "Choose established license" or licence_choice == "Detect":
                licenses = requests.get("https://api.github.com/licenses").json()
                license_names = [license["spdx_id"] for license in licenses]
                
                if licence_choice == "Choose established license":
                    license = self.user_input_choose_string(message="Choose license: ", choices=license_names)
                elif licence_choice == "Detect":
                    for root, dirs, files in os.walk("."):
                        if "LICENSE" in files:
                            with open(os.path.join(root, "LICENSE"), 'r') as f:
                                license_content = f.read()
                                
                            for lic_name in license_names:
                                if lic_name in license_content:
                                    if self._ui.confirm(f"Detected license: {lic_name}\nUse this license?"):
                                        license = lic_name
                                        break
                            break
            
            elif licence_choice == "Custom license":
                license = self._ui.prompt("Enter license: ")
                
            elif licence_choice == "None":
                license = "None"
            
        
        return models.SchemaInfo(
            name=name,
            description=description,
            version=version,
            author=author,
            license=license,
        )
            
    def edit_field(self, element: models.SchemaField) -> models.SchemaField:
        self._ui.message(f"Editing field: {element.og_name}")
                
        def inp(message: str) -> str:
            in_ = self._ui.prompt(message)
            if in_ == "":
                return None
            return in_
        
        og_name = inp("Enter field key" + f"(current: {element.og_name})")
        name = inp("Enter display name" + (f"(current: {element.name})" if element.name else ""))
        description = inp("Enter description" + (f"(current: {element.description})" if element.description else ""))
        hint = inp("Enter hint" + (f"(current: {element.hint})" if element.hint else ""))
        default = inp("Enter default value" + (f"(current: {element.default})" if element.default else ""))
        type_ = self.user_input_choose_string(message="Choose type", choices=[t.value for t in models.SchemaFieldTypes])
        regex = inp("Enter regex" + (f"(current: {element.regex})" if element.regex else ""))
        error = inp("Enter error message" + (f"(current: {element.error})" if element.error else ""))
        
        props = list()
        for prop in models.SchemaFieldProps:
            enabled = element.props is not None and prop in element.props
            answer = self._ui.confirm(f"Is {prop.value} set?" + (f" (current: {'yes' if enabled else 'no'})" if enabled else ""))
            if answer:
                props.append(prop)
                
        if len(props) == 0:
            props = None
            
        if type_ is not None and type_ > 0:
            type_ = [t for t in models.SchemaFieldTypes][type_-1]
                
        new_elem = element.__deepcopy__()
        new_elem.og_name = og_name if og_name else element.og_name
        new_elem.name = name if name else element.name
        new_elem.description = description if description else element.description
        new_elem.hint = hint if hint else element.hint
        new_elem.default = default if default else element.default
        new_elem.type = type_ if type_ else element.type
        new_elem.regex = regex if regex else element.regex
        new_elem.props = props if props else element.props
        new_elem.error = error if error else element.error
        
        return new_elem
        
    def edit_text(self, element: models.SchemaText) -> models.SchemaText:
        no_text = [models.SchemaTextTypes.space, models.SchemaTextTypes.divider]
        
        self._ui.message(f"Editing text element: {element.type.value} : {element.text if element.text else ''}")
        
        if element.type in no_text:
            new_type = self.user_input_choose_string(message="Choose new type", choices=[t.value for t in models.SchemaTextType])
            text = None
            if not new_type in no_text:
                text = self._ui.prompt(f"Enter text (current: {element.text if element.text else ''})")
            if new_type is not None:
                return models.SchemaText(type=new_type, text=text)
        else:
            new_type = self.user_input_choose_string(message="Choose what to edit", choices=["Type", "Text"])
            if new_type == "Type":
                new_type = self.user_input_choose_string(message="Choose new type", choices=[t.value for t in models.SchemaTextTypes])
                if new_type is not None:
                    return models.SchemaText(type=new_type, text=element.text)
            elif new_type == "Text":
                text = self._ui.prompt(f"Enter text (current: {element.text if element.text else ''})")
                return models.SchemaText(type=element.type, text=text)
            return element
        
    def edit_element(self, element: models.SchemaElement) -> models.SchemaElement:
        if isinstance(element, models.SchemaField):
            return self.edit_field(element)
        elif isinstance(element, models.SchemaText):
            return self.edit_text(element)
        
        
    def create_new_field(self) -> models.SchemaField:
        self._ui.message("Enter field information:")
        og_name = self._ui.prompt("Enter field (example: DATABASE_PASSWORD)", required=True)
        name = self._ui.prompt("Enter display name")
        default = self._ui.prompt("Enter default value")
        description = self._ui.prompt("Enter description")
        example = self._ui.prompt("Enter example")
        hint = self._ui.prompt("Enter hint")
        type_ = self._ui.choose("Choose type", [t.value for t in models.SchemaFieldTypes])
        regex = self._ui.prompt("Enter regex")
        error_msg = self._ui.prompt("Enter error message")
        
        props = list()
        for elem in models.SchemaFieldProps:
            answer = self._ui.confirm(f"Is {elem.value} set?")
            if answer:
                props.append(elem)
                
        if name == "":
            name = None
        if default == "":
            default = None
        if description == "":
            description = None
        if example == "":
            example = None
        if hint == "":
            hint = None
        if regex == "":
            regex = None
        if error_msg == "":
            error_msg = None
            
        if type_ is not None and type_ > 0:
            type_ = [t for t in models.SchemaFieldTypes][type_-1]
        
        model =  models.SchemaField(
            og_name=og_name,
            default=default,
            name=name,
            example=example,
            description=description,
            hint=hint,
            regex=regex,
            props=props,
            error=error_msg
        )
        
        if isinstance(type_, models.SchemaFieldTypes):
            model.type = type_
        return model
        
    def create_new_text(self) -> models.SchemaText:
        self._ui.message("Enter text information:")
        choices = [e.value for e in models.SchemaTextTypes]
        type_ = self.user_input_choose_string(message="Choose text type", choices=choices)
        if type_ is None:
            return None
        
        type_ = models.SchemaTextTypes(type_)
        if type_ in [models.SchemaTextTypes.space, models.SchemaTextTypes.divider]:
            return models.SchemaText(type=type_)
        else:
            text = self._ui.prompt("Enter text")
            return models.SchemaText(type=type_, text=text)
    
    def create_new_element(self) -> models.SchemaElement:
        choices = ["Field", "Text"]
        choice = self.user_input_choose_string(message="Choose element type", choices=choices)
        
        if choice == "Field":
            return self.create_new_field()
        elif choice == "Text":
            return self.create_new_text()
        
    def insert_element(self, element: models.SchemaElement, elements: typing.List[models.SchemaElement]) -> typing.List[models.SchemaElement]:
        index, elem = self.user_input_choose_item(elements, "Choose position")
        if index is None:
            return elements
        
        elements.insert(index, element)
        return elements
    
    def main_menu(self, schema: models.Schema) -> models.Schema:
        
        while True:
            
            choices = ["View", "Edit", "Save"]
            self._ui.message("\n\n--------- Options ---------\n")
            choice = self.user_input_choose_string(message="What do you want to do?", choices=choices, required=True)
            
            if choice == "View":
                choice = self.user_input_choose_string(message="What do you want to view?", choices=["Schema", "Elements"])
                if choice == "Schema":
                    self._ui.message("\n\n--------- Schema ---------\n")
                    self._ui.message(schema.to_text())
                    self._ui.prompt("Press key to continue")
                elif choice == "Elements":
                    self._ui.message("\n\n--------- Elements ---------\n")
                    for element in schema.elements:
                        self._ui.message(element.introduce())
                    self._ui.prompt("Press key to continue")
                
            elif choice == "Save":
                break
            
            elif choice == "Edit":               
                
                while True:
                    choices = ["Change schema info", "Edit element", "Add element", "Remove element", "Change element position"]
                    # choice = self._ui.choose(choices, "What do you want to do?")
                    choice = self.user_input_choose_string(message="What do you want to do?", choices=choices)
                    if choice == "Change schema info":
                        schema.schemaInfo = self.create_schema_info()
                        
                    elif choice == "Edit element":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to edit")
                        if index is not None:
                            schema.elements[index] = self.edit_element(element)
                        
                    elif choice == "Add element":
                        element = self.create_new_element()
                        if element is not None:
                            schema.elements = self.insert_element(element, schema.elements+[None])

                    elif choice == "Remove element":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to delete")
                        if index is not None:
                            schema.elements.pop(index)
                    
                    elif choice == "Change element position":
                        index, element = self.user_input_choose_item(schema.elements, "Choose element to change position")
                        if index is None:
                            continue
                        trimmed_list = schema.elements[:index] + schema.elements[index+1:] + [None]
                        schema.elements = self.insert_element(element, trimmed_list)
                        # filter none values
                        schema.elements = [elem for elem in schema.elements if elem is not None]
                    
                    elif choice == "Finish editing" or choice is None:
                        break
                    
                    schema.elements = [elem for elem in schema.elements if elem is not None]
                    
        return schema
        
    def command(self, *args, **kwargs) -> None:
        input_file = kwargs.get('input', None)
        output_file = kwargs.get('output', None)
        
        if not os.path.exists(input_file):
            self._ui.message(f"File {input_file} does not exist")
            sys.exit(1)
           
        self._ui.message("Serializing .env data...")
        elements = None
        with open(input_file, 'r') as f:
            elements = parser.parse_env_to_elements(f.read())
            
        self._ui.message("Serializing finished\n")
        
        self._ui.message("Now I will ask you to fill a data for the schema")
        schemaInfo = self.create_schema_info()
        
        
        schema = self.main_menu(parser.build_schema(schemaInfo, elements))
        
        sname = schema.schemaInfo.name.lower().replace(' ', '_')
        if output_file is None:
            output_file = self._ui.prompt(f"Enter output file name (default: .env" + (f".{sname}" if sname != "" else "") + ".schema): ").strip()
        if output_file == "":
            output_file = ".env" + (f".{sname}" if sname != "" else "") + ".schema"
            
        self._ui.message(f"Saves to {output_file}")
            
        with open(output_file, 'w', encoding="utf-8") as f:
            f.write(schema.to_text())