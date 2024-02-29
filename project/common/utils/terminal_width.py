def get_terminal_width() -> int:
    try:
        try:
            from blessed import Terminal
            term = Terminal()
            width = term.width
        except ImportError:
            import shutil
            width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
        
    return width