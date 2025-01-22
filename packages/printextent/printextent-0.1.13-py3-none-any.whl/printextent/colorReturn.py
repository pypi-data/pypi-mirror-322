def colorReturn(text, color: str=None, style: str=None, bg_color: str=None) -> str:
    """

    Usage
    -----
    A way to customize text without the print statements.\n
    Can be customized in many ways.

    Parameters
    ----------
    text : str\n
    The text you want to customize.

    color : str\n
    The color you want the text to be. -/- Options: Gray, Red, Green, Yellow, Blue, Purple, Cyan, White or Rainbow

    style : str\n
    The text style you want the text to be. -/- Options: Bold, Dimmed, Italicized or Underlined

    bg_color : str\n
    The background color you want behind the text to be. -/- Options: Gray, Red, Green, Yellow, Blue, Purple, Cyan or White

    Returns
    -------
    Returns a string with the customized text to be printed out later on.
        
    """

    colors = ["Gray", "Red", "Green", "Yellow", "Blue", "Purple", "Cyan", "White"]
    styles = ["Bold", "Dim", "Italicize", "Underline"]
    colorcodes = ["\033[0;30;48m", "\033[0;31;48m", "\033[0;32;48m", "\033[0;33;48m", "\033[0;34;48m", "\033[0;35;48m", "\033[0;36;48m", "\033[0;37;48m"]
    rbcolors = ["\033[0;31;48m", "\033[0;32;48m", "\033[0;33;48m", "\033[0;34;48m", "\033[0;35;48m", "\033[0;36;48m", "\033[0;37;48m"]
    endcode = "\033[0m"
    code = "\033[0;37;40m"

    if color != None:
        if color.capitalize() == "Rainbow":
            try:
                newtxt = ""
                rainbow_index = 0
                txt = list(text)
                for char in txt:
                    newtxt += rbcolors[rainbow_index] + char + endcode
                    rainbow_index += 1
                    if rainbow_index == 6:
                        rainbow_index = 0
                return newtxt
            except err as err:
                print(str(err))
                exit()
        else:
            try:
                if color != None:
                    if color.capitalize() not in colors:
                        raise ValueError("\033[1;31m[ERROR]:\033[0m The color specified does not exist.")
                    else:
                        colorIndex = colors.index(color.capitalize())
                        code = colorcodes[colorIndex]

                if style != None:
                    if style.capitalize() not in styles:
                        raise ValueError("\033[1;31m[ERROR]:\033[0m The style specified does not exist.")
                    else:
                        if style == "Bold":
                            code = code.replace("[0", "[1")
                        elif style == "Dim":
                            code = code.replace("[0", "[2")
                        elif style == "Italicize":
                            code = code.replace("[0", "[3")
                        elif style == "Underline":
                            code = code.replace("[0", "[4")

                if bg_color != None:
                    if bg_color.capitalize() not in colors:
                        raise ValueError("\033[1;31m[ERROR]:\033[0m The background color specified does not exist.")
                    else:
                        if bg_color == "Gray":
                            code = code.replace("48m", "40m")
                        elif bg_color == "Red":
                            code = code.replace("48m", "41m")
                        elif bg_color == "Green":
                            code = code.replace("48m", "42m")
                        elif bg_color == "Yellow":
                            code = code.replace("48m", "43m")
                        elif bg_color == "Blue":
                            code = code.replace("48m", "44m")
                        elif bg_color == "Purple":
                            code = code.replace("48m", "45m")
                        elif bg_color == "Cyan":
                            code = code.replace("48m", "46m")
                        elif bg_color == "White":
                            code = code.replace("48m", "47m")
                
                return code + text + endcode
            except ValueError as err:
                print(str(err))
                exit()
    else:
        try:
            if style != None:
                if style.capitalize() not in styles:
                    raise ValueError("\033[1;31m[ERROR]:\033[0m The style specified does not exist.")
                else:
                    if style == "Bold":
                        code = code.replace("[0", "[1")
                    elif style == "Dim":
                        code = code.replace("[0", "[2")
                    elif style == "Italicize":
                        code = code.replace("[0", "[3")
                    elif style == "Underline":
                        code = code.replace("[0", "[4")

            if bg_color != None:
                if bg_color.capitalize() not in colors:
                    raise ValueError("\033[1;31m[ERROR]:\033[0m The background color specified does not exist.")
                else:
                    if bg_color == "Gray":
                        code = code.replace("48m", "40m")
                    elif bg_color == "Red":
                        code = code.replace("48m", "41m")
                    elif bg_color == "Green":
                        code = code.replace("48m", "42m")
                    elif bg_color == "Yellow":
                        code = code.replace("48m", "43m")
                    elif bg_color == "Blue":
                        code = code.replace("48m", "44m")
                    elif bg_color == "Purple":
                        code = code.replace("48m", "45m")
                    elif bg_color == "Cyan":
                        code = code.replace("48m", "46m")
                    elif bg_color == "White":
                        code = code.replace("48m", "47m")
        
            return code + text + endcode
        except ValueError as err:
            print(str(err))
            exit()
