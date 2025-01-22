def asciiPrint(art: list):
    """

    Usage
    -----
    Prints out ascii art created by the user.\n
    (Each index of the list would be one row of the art piece.)

    Parameters
    ----------
    art : list\n
    The ascii art you want to print out.

    Returns
    -------
    Returns out the finished product into the terminal.
        
    """

    for line in art:
        print(line)
