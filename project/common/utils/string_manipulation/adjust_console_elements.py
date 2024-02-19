import typing
from ..settings_classes import Representation
# from ..string_manipulation import to_words, spaced_fit
from .cut_string import cut_strings_to_words as to_words
from .spaced_text import spaced_fit

def fit_in_space(strings:typing.List[str], total_space:int=None, space_before:int=None, space_between:int=None, str_length:typing.List[typing.Optional[int]]=list()) -> None:
    """
    fit_in_space Adjusts the strings to fit in the total space.
    
    Args:
        strings (typing.List[str]): The strings to adjust.
        total_space (int): The total space. Default is None (uses Representation.total_space()).
        space_before (int): The space before the model. Default is None (uses Representation.space_before()).
        space_between (int): The space between the strings. Default is None (uses Representation.space_between()).
        str_length (typing.List[str|None]): The fixed length of the strings. Default is list().
    """
    
    if len(strings) < 1:
        raise ValueError("Need at least one string.")
    elif len(strings) <= 2:
        if space_before is None:
            space_before = Representation.space_upfront()
        if total_space is None:
            total_space = Representation.total_space()
        if space_between is None:
            space_between = Representation.space_between()
            
        if len(strings) == 1:
                
            if str_length[0] is None:
                str_length[0] = len(strings[0])
                
            return " " * space_before + strings[0].ljust(str_length[0])
        
        elif len(strings) == 2:                
            text = fit_in_space([strings[0]], total_space, space_before, space_between, [str_length[0]])
            
            space_before_second = len(text)
            
            if str_length[1] is None:
                str_length[1] = len(strings[1])
                
            # if second_str_length is None:
            #     second_str_length = min(str_length[1], (total_space - space_before_second))
                
                
            text +=" " *space_between + spaced_fit(strings[1], space_before_second, total_space)[space_before_second:]
            
            return text
    else:
        # populate str_length with None
        while len(str_length) < len(strings):
            str_length.append(None)
            
        #divide last one and the rest
            
        last_str = strings[-1]
        last_str_length = str_length[-1]
        
        other_strs = strings[:-1]
        other_strs_length = str_length[:-1]
        
        # fit the rest
        text = fit_in_space(other_strs, total_space, space_before, space_between, other_strs_length)
        
        # fit the last one
        return fit_in_space([text, last_str], total_space, space_before, space_between, [len(text), last_str_length])
        
        
        