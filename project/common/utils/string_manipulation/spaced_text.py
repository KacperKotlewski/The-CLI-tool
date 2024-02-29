from .cut_string import cut_strings_to_words

def spaced_fit(text:str, spaces:int, total:int) -> str:
    l = total - spaces
    if l < 10:
        raise ValueError("Total length is less than taken length. Need at least 10 characters.")
    
    if len(text) < l:
        return ' ' * spaces + text
    
    return cut_strings_to_words(text, spaces, total)
    
    