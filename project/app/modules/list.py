import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory
from common.utils.string_manipulation import fit_in_space
from common.CLI.module.root_module import RootModule
from common.CLI.interface import UserInterface
from common.CLI.abstract_handler import AbstractHandler

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
class list_elements(Command):
    _elements_to_list = {
        'interfaces': 'List user interfaces.',
    }
    
    def print_when_no_element(self) -> None:
        ui:UserInterface = self._ui
        ui.message(f"\nElements to list:")
        
        max_key_len = max([len(key) for key in self._elements_to_list.keys()])
        for key, value in self._elements_to_list.items():
            ui.message(fit_in_space([key, value], [max_key_len], space_before=2, space_between=10))
            
    def print_elements_with_representation(self, name:str, elements: AbstractHandler) -> None:
        ui:UserInterface = self._ui
        if len(elements) == 0:
            ui.message(f"No elements found.")
        else:
            ui.message(f"{name.capitalize()}:")
            maxlen = max([len(element) for element in elements])
            ui.message("\n".join(elements.stylized_representation(first_str_length=maxlen, space_after=10, space_before=2)))
            
    def print_when_element_on_list(self, element:str) -> None:
        elements_to_print = None
        if element == 'interfaces':
            root_mod:RootModule = self.root_module
            elements_to_print = root_mod.interface_handler
            
            
        if elements_to_print is not None:
            if isinstance(elements_to_print, AbstractHandler):
                return self.print_elements_with_representation(element, elements_to_print)
            
        ui:UserInterface = self._ui
        ui.message(f"No elements found.")
    
    def command(self, *args, **kwargs) -> None:
        ui:UserInterface = self._ui
        element = kwargs.get('element', None)        
        
        if element == 'list':
            self.print_help_usage_action()
            self.print_when_no_element()
                
        elif element in self._elements_to_list:
            self.print_when_element_on_list(element)
            
        else:
            print(f"ERROR: Element '{element}' is not recognized.\n")
            self.print_help_usage_action()