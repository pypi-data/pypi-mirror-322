def errorUserPrint(text: str) -> str:
    """
    
    Usage
    -----
    Acts like a normal print statement but with a error notice before the error text in a red color setting.\n
    An example statement would be like so:\n
    [ERROR]: This is an informational message that can let users know about a situation regarding something that is wrong.\n
    (The [ERROR]: is already added to the message.)

    Parameters
    ----------
    text : str\n
    The text you want to be typed out.
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    code = "\033[1;31m"
    endcode = "\033[0m"
    return print(code + f"[ERROR]: {text}{endcode}")
