from inspect import isclass
import time
import typing
from common.CLI.interface import interface, UserInterface

from blessed import Terminal
import colorama

@interface(
    name = "colorama",
    description = "CLI interface with colorama support."
)
class ColoramaInterface(UserInterface):
    """
    CLI interface class with colorama support.
    """
    
    def __init__(self, **data):
        super().__init__(**data)
        
        self._colorama = colorama
        self._term = Terminal
        
    
    def strip_msg(self, message: str) -> str:
        if message.strip().endswith(":"):
            message = ":".join(message.split(":")[:-1])
        return message
    
    def prompt(self, message: str, required:bool=False, return_none:bool=False) -> str:
        if required and return_none:
            raise ValueError("required and return_none cannot be both True")
        
        if message is None:
            message = "Enter value"
        message = self.strip_msg(message)
        
        while True:
            input_ = input(f'{message}: ')
            if input_ != "" or (not required and input_ == "" and not return_none):
                return input_
            elif not required and input_ == "" and return_none:
                return None
            else:
                print("Value is required")
    
    def confirm(self, message: str) -> bool:
        message = self.strip_msg(message)
        input_ = input(f'{message} (y/n): ')
        return input_.lower() == "y"
    
    def init_terminal(self) -> Terminal:
        term = self._term()
        colorama = self._colorama
        colorama.init()
        return term
    
    def choose(self, message: str, choices: typing.List[str], required:bool=False) -> str:
        message = self.strip_msg(message)
        
        current_option = 0
        anchor = 0
        flag_to_small_printed = False
        
        term = self.init_terminal()
        
        with term.cbreak(), term.hidden_cursor():
            while True:     
                start_index = 0
                
                term_height = term.height - 1
                if message is not None and len(message) > 0:
                    term_height -= 1
                    
                if term_height <3:
                    if not flag_to_small_printed:
                        print(term.clear)
                        print("Terminal window is too small, resize terminal window.", end="")
                        flag_to_small_printed = True
                    time.sleep(0.1)
                    continue
                else:
                    flag_to_small_printed = False
                    
                print(term.clear)
                if message is not None and len(message) > 0:
                    print(f"{colorama.Fore.LIGHTYELLOW_EX}{colorama.Back.BLACK}{message}")
                
                # anchor is first displayed option, current_option is the selected option, term_height is the height of the terminal
                anchor_min_index = max(0, anchor)
                anchor_max_index = min(len(choices), anchor + term_height)
                
                curent_index = anchor + current_option
                
                if current_option < anchor_min_index:
                    anchor = current_option
                elif current_option >= anchor_max_index:
                    anchor = current_option - term_height + 1
                    
                #start_index is the first displayed option, end_index is the last displayed option
                
                start_index = max(0, anchor)
                end_index = min(len(choices), anchor + term_height)           

                
                for i, option in enumerate(choices[start_index:end_index]):
                    value = f"  {option}"
                    if i+start_index == current_option:
                        value = f"  ► {colorama.Fore.RED}{colorama.Back.WHITE} {option} {colorama.Style.RESET_ALL} ◄"
                        
                    print(f"{colorama.Fore.WHITE}{colorama.Back.BLACK}{value}{colorama.Fore.WHITE}{colorama.Back.BLACK}")

                regular = f"{colorama.Fore.LIGHTMAGENTA_EX}{colorama.Back.BLACK}"
                highlight = f"{colorama.Back.MAGENTA}{colorama.Fore.LIGHTBLACK_EX}"
                print(f"{regular}Use {highlight}arrow{regular} keys to navigate, press '{highlight}Enter{regular}' to select, to exit '{highlight}Escape{regular}' or '{highlight}Ctrl+C{regular}'.", end=f"{colorama.Style.RESET_ALL}")
                
                               
                try:
                    key = term.inkey()

                    if key.name == 'KEY_UP':
                        current_option = (current_option - 1) % len(choices)
                    elif key.name == 'KEY_DOWN':
                        current_option = (current_option + 1) % len(choices)
                    elif key.name == 'KEY_ENTER':
                        print(f"{colorama.Fore.RESET}{colorama.Back.RESET}")
                        return curent_index+1
                    elif key.name == 'KEY_ESCAPE' and not required:
                        print(f"{colorama.Fore.RESET}{colorama.Back.RESET}")
                        return None
                except KeyboardInterrupt:
                    print(f"{colorama.Fore.RESET}{colorama.Back.RESET}")
                    exit(0)
                        

                
    def message(self, message: str) -> None:
        message = self.strip_msg(message)
        term = self.init_terminal()
        print(f"{colorama.Fore.LIGHTWHITE_EX}{colorama.Back.BLACK}{message}{colorama.Style.RESET_ALL}")

    def clear(self) -> None:
        print(colorama.clear)
    
    # def get_input(self) -> str:
    #     return input()