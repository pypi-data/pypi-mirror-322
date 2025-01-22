def typewritePrint(text: str):
    """
    
    Usage
    -----
    Acts like a normal print statement but with a typewriter effect.

    Parameters
    ----------
    text : string\n
    The text you want to be typed out.
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    import sys, time

    for letter in text:
        time.sleep(0.03)
        sys.stdout.write(letter)
        sys.stdout.flush()
    print("")
