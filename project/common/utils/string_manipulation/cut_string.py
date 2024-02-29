def cut_strings_to_words(string:str, taken:int, total:int):
    words = string.split()
    lines = []
    current_line = ' ' * taken
    for word in words:
        
        # split the word if it's too long
        while len(word) > total:
            lines.append(current_line + word[:total-2])
            word = word[total-2:]
            current_line = ' ' * taken
        
        # add the word to the current line if it fits  
        if len(current_line) + len(word) + 1 <= total:
            current_line += ' ' + word
            
        # start a new line if it doesn't fit
        else:
            lines.append(current_line)
            current_line = ' ' * taken + word
                
    lines.append(current_line)
    return '\n'.join(lines)