import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory, OptionBuilder, OptionHandler
from common.utils.string_manipulation import fit_in_space

# create = Module(
#     name = "create",
#     description = "Create new elements in the project.",
#     help_str = "This command creates a new module in the project.",
# )

@command(
    name = "list",
    description = "List particular elements in the tool.",
    help_str = "List particular elements in the tool.",
    option_handler = [
        OptionFactory.argument(
            name='element',
            description='Elements to list.',
            required=True,
            keys=['-e'],
            default_value='list'
        ),
    ]
)
def list_elements(self: Command, *args) -> Command:
    listings = {
        # 'env': 'List .env files in the project.',
        # 'schema': 'List schema files in the project.',
        # 'modules': 'List module files in the project.',
        # 'commands': 'List commands available.',
        'interfaces': 'List user interfaces.',
    }
    
    element = self.get_value('element')
    
    if element == 'list':
        self.print_help_usage_action()
        
        print(f"\n{self.get_usage()}")
        print(f"\nElements to list:")
        
        max_key_len = max([len(key) for key in listings.keys()])
        for key, value in listings.items():
            print(fit_in_space([key, value], [max_key_len], space_before=2, space_between=10))
            