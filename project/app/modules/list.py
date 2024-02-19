import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory
from common.utils.string_manipulation import fit_in_space

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
            
    elif element in listings:
        print("ERROR: Not implemented yet.")
        
    else:
        print(f"ERROR: Element '{element}' is not recognized.\n")
        self.print_help_usage_action()