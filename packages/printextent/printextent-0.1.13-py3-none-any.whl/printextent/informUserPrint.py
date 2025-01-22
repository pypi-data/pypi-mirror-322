def informUserPrint(text: str) -> str:
    """
    
    Usage
    -----
    Acts like a normal print statement but with a informational notice before the informational text in a gray color setting.\n
    An example statement would be like so:\n
    [INFO]: This is an informational message that can let users know about a situation regarding something that the user must know.\n
    (The [INFO]: is already added to the message.)

    Parameters
    ----------
    text : str\n
    The text you want to be typed out.
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    code = "\033[1;30m"
    endcode = "\033[0m"
    return print(code + f"[INFO]: {text}{endcode}")
