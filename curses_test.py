from blessed import Terminal
import colorama
import time

def main():
    
    term = Terminal()

    # Inicjalizacja colorama
    colorama.init()
    saved_text_color = colorama.Fore.RESET
    saved_bg_color = colorama.Back.RESET

    # Zdefiniuj listę opcji
    options = [f'Opcja {i}' for i in range(1, 60)]
    current_option = 0
    top_text = "Select an option:"
    
    anchor = 0
    flag_to_small_printed = False

    with term.cbreak(), term.hidden_cursor():
        while True:     
            start_index = 0
            
            term_height = term.height - 1
            if top_text is not None and len(top_text) > 0:
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
            if top_text is not None and len(top_text) > 0:
                print(f"{colorama.Fore.LIGHTYELLOW_EX}{colorama.Back.BLACK}{top_text}")
            
            # anchor is first displayed option, current_option is the selected option, term_height is the height of the terminal
            anchor_min_index = max(0, anchor)
            anchor_max_index = min(len(options), anchor + term_height)
            
            if current_option < anchor_min_index:
                anchor = current_option
            elif current_option >= anchor_max_index:
                anchor = current_option - term_height + 1
                
            #start_index is the first displayed option, end_index is the last displayed option
            
            start_index = max(0, anchor)
            end_index = min(len(options), anchor + term_height)           

            
            for i, option in enumerate(options[start_index:end_index]):
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
                    current_option = (current_option - 1) % len(options)
                elif key.name == 'KEY_DOWN':
                    current_option = (current_option + 1) % len(options)
                elif key.name == 'KEY_ENTER':
                    print(f"{saved_bg_color}{saved_text_color}")
                    return current_option
                elif key.name == 'KEY_ESCAPE':
                    print(f"{saved_bg_color}{saved_text_color}")
                    return None
            except KeyboardInterrupt:
                print(f"{saved_bg_color}{saved_text_color}")
                return None

if __name__ == "__main__":
    print(main())
