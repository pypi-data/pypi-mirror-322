def repeatInput(question: str, answ_list: list) -> str:
    """
    
    Usage
    -----
    Acts like a normal input statements but repeats until a valid selection is chosen.

    Parameters
    ----------
    question : string\n
    The question to ask the user.
    
    answ_list : list\n
    The answer bank for the user to choose from.

    Returns
    -------
    Returns out the finished chosen answer.

    """
    input_answ = None
    while input_answ not in answ_list:
        print(question)
        count = 0
        for answ in answ_list:
            count += 1
            print(f"{count}. {answ}")
        
        input_answ = input("> ")
        if input_answ in answ_list: break
        else: print("\033[1;33m[WARNING]: That is not a valid selection. Please select an answer from the provided list.\033[0m")
    
    return input_answ
