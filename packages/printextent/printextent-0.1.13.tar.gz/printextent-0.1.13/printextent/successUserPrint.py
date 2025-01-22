def successUserPrint(text: str) -> str:
    """
    
    Usage
    -----
    Acts like a normal print statement but with a success notice before the success text in a green color setting.\n
    An example statement would be like so:\n
    [SUCCESS]: This is an informational message that can let users know about a situation regarding something that went successfully.\n
    (The [SUCCESS]: is already added to the message.)

    Parameters
    ----------
    text : str\n
    The text you want to be typed out.
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    code = "\033[1;32m"
    endcode = "\033[0m"
    print(code + f"[SUCCESS]: {text}{endcode}")
    