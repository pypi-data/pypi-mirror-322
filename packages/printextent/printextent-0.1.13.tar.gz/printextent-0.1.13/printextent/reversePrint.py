def reversePrint(text: str) -> str:
    """

    Usage
    -----
    Acts like a normal print statement but reverses the text being printed.\n

    Parameters
    ----------
    text : str\n
    The text you want to be reversed.

    Returns
    -------
    Returns out the finished product into the terminal.
        
    """

    string_ = text
    final_string = ""

    def reverse(string_1: str):
        if not string_1:
            return ""
        else:
            front_part = reverse(string_1[1:])
            back_part = string_1[0]
            front_part + back_part + string_[:-len(string_1)]

        return front_part + back_part[0]

    reverse_text = reverse(string_)
    reverse_text = reverse_text.split()

    for index in reverse_text:
        final_string += f"{index} "
    return print(final_string)
    