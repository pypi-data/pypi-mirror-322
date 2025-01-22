# What is it?

printextent is a Python library for customizing print statements in a different variety of ways.

printextent makes it easier to accomplish! (Either by printing or returning the customized text!)

## Installation

Via pip:

```bash
pip install printextent
```
or
```bash
python -m pip install printextent --upgrade
```

## Examples

```python
import printextent

# prints out "Hello World! This is a test sentence!" in the color blue while also being bolded.
printextent.colorPrint("Hello World! This is a test sentence!", "Blue", "Bold")

# prints out "Hello World! This is a test sentence!" in a rainbow pattern.
printextent.colorPrint("Hello World! This is a test sentence!", "Rainbow")

# prints out "Hello World! This is a test sentence!" while under a typewriter effect.
printextent.typewritePrint("Hello World! This is a test sentence!")

# prints out "Hello World! This is a test sentence!" reversed. ("!ecnetnes tset a si sihT !dlroW olleH")
printextent.reversePrint("Hello World! This is a test sentence!")

# prints out a info message regarding an important message.
printextent.informUserPrint("This is an informational message that can let users know about a situation regarding something that the user must know.")

# prints out a warning message regarding an important message.
printextent.warnUserPrint("This is an informational message that can let users know about a situation regarding something that can go poetentially wrong.")

# prints out a error message regarding an important message.
printextent.errorUserPrint("This is an informational message that can let users know about a situation regarding something that is wrong.")
```

## License

[MIT](https://choosealicense.com/licenses/mit/)