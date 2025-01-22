def listPrint(list: list, style: str="Bulletin") -> str:
    """ 
    
    Usage
    -----
    Prints out a formated list either with the set style.

    Parameters
    ----------
    list : list\n
    The list you want to be printed out.
    
    style : str\n
    The style of how the list will be laid out. -/- Options: Bulletin or Number
    
    Returns
    -------
    Returns out the finished product into the terminal.
        
    """
    if style == "Bulletin":
        for item in list: print(f"• {item}")
    elif style == "Number":
        num_count = 0
        for item in list: num_count += 1; print(f"{num_count}. {item}")