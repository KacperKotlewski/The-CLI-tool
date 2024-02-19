import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory, OptionBuilder, OptionHandler

create = Module(
    name = "create",
    description = "Create new elements in the project.",
    help_str = "This command creates a new module in the project.",
)

@command(
    name = "env",
    description = "Create a new .env file.",
    help_str = "Create a new .env file in the project.",
    option_handler = [
         OptionFactory.argument(
            name='input',
            keys=['-i', '--input'],
            description='Input schema file to deserialize.',
            required=True
        ),
        OptionFactory.option(
            name='output',
            keys=['-o', '--output'],
            description='Output filename for .env file.',
            required=False
        ),
    ]
)
def env_create(self: Command, *args) -> Command:
    input_file = self.get_value('input')
    output_file = self.get_value('output')
    
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist")
        sys.exit(1)
        
    text = open(input_file, 'r').read()
    
    from client.schema.deserialize import parser
    from client.schema import models
    
    schema = parser.parse_env_schema(text)
    
    #print schema
    print(f"\nSchema: {input_file}\n\n{schema}\n\n")
    
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
    if output_file is None:
        output_file = input(f"Enter output file name (default: .env." + (f".{sname}" if sname != "" else "") + "): ").strip()
    if output_file == "":
        output_file = ".env" + (f".{sname}" if sname != "" else "") + ".deserialized"
        
    print(f"Saves to {output_file}")
        
    with open(output_file, 'w') as f:
        f.write(output_file_data)
        

create += env_create