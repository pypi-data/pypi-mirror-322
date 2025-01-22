def warnUserPrint(text: str) -> str:
    """
    
    Usage
    -----
    Acts like a normal print statement but with a warning notice before the warning text in a yellow color setting.\n
    An example statement would be like so:\n
    [WARNING]: This is an informational message that can let users know about a situation regarding something that can go poetentially wrong.\n
    (The [WARNING]: is already added to the message.)

    Parameters
    ----------
    text : str\n
    The text you want to be typed out.
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    code = "\033[1;33m"
    endcode = "\033[0m"
    return print(code + f"[WARNING]: {text}{endcode}")
