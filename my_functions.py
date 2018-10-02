"""
My functions
"""

def myinput(arg, content):
    """
    Takes input values and makes the user repeat if they enter the wrong data type
    """
    if arg == "float":
        exitTrigger = False
        while exitTrigger == False:
            try:
                floatVal = float(input(content))
                if not floatVal:
                    pass
                else:
                    return floatVal
                    exitTrigger = True
            except ValueError:
                print("That was not a number!")

    if arg == "int":
        exitTrigger = False
        while exitTrigger == False:
            try:
                intVal = int(input(content))
                if not intVal:
                    pass
                else:
                    return intVal
                    exitTrigger = True
            except ValueError:
                print("That was not an integer!")

    if arg == "str":
        exitTrigger = False
        while exitTrigger == False:
            try:
                strVal = input(content)
                if not strVal:
                    pass
                else:
                    return strVal
                    exitTrigger = True
            except ValueError:
                print("You didn't type anything!")
