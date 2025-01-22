def progressBarPrint(curr_percentage: int, max_percentage: int=100, color: str=None) -> str:
    """
    
    Usage
    -----
    Prints out a progression bar with no functions.
    An example of a progress bar would look like so:\n
    [######____] 60/100

    Parameters
    ----------
    curr_percentage : int\n
    The current status of percentage out of the maximum percentage.

    max_percentage : int\n
    The maximum status of percentage. -/- Default : 100

    color : str\n
    The color you want the text to be. -/- Options: Gray, Red, Green, Yellow, Blue, Purple, Cyan or White
    
    Returns
    -------
    Returns out the finished product into the terminal.

    """
    if color != None:
        colors = ["Gray", "Red", "Green", "Yellow", "Blue", "Purple", "Cyan", "White"]
        colorcodes = ["\033[30m", "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"]

        if color.capitalize() not in colors:
            raise ValueError("\033[1;31m[ERROR]:\033[0m The color specified does not exist.")
        else:
            colorIndex = colors.index(color.capitalize())
            code = colorcodes[colorIndex]
        endcode = "\033[0m"

        print(code + "[" + endcode, end="")
        for i in range(24):
            if i/24 < curr_percentage/max_percentage:
                print(code + "#" + endcode, end="")
            else:
                print(code + "_" + endcode, end="")
        print(code + "]" + endcode, end="")
    else:
        print("[", end="")
        for i in range(24):
            if i/24 < curr_percentage/max_percentage:
                print("#", end="")
            else:
                print("_", end="")
        print(f"] {curr_percentage}/{max_percentage}")
