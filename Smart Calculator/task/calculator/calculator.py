# Smart Calculator
# Author: Jason Tolbert (https://github.com/jasonalantolbert)
# Python Version: 3.8


# This program was written as part of a JetBrains Academy project.
# For more information, visit https://hyperskill.org/projects/74.


# BEGINNING OF PROGRAM

import re
from numexpr import evaluate

                
class Variable:  # contains variable creation method, existing variable dictionary, and variable format validation regex
    vars_dict = {}

    sym_format = re.compile("^[A-Za-z]+$")
    val_format = re.compile("^[0-9]+$")

    @staticmethod
    def create_var(declaration):
        try:
            symbol, value = (declaration.replace(" ", "")).split(sep="=")  # tries to split declaration on equals sign
        except ValueError:  # multiple equals signs will throw a ValueError exception
            print("Invalid assignment\n")
            return
        else:
            if not re.match(Variable.sym_format, symbol):  # validates variable name
                print("Invalid identifier\n")
                return
            elif not re.match(Variable.val_format, value):  # validates variable value
                try:
                    # if the variable value is not properly formatted, the program checks if the user is trying to
                    # set the value of the variable to the value of an existing variable, and if so, adds the new
                    # variable to the dictionary with the value of the existing variable
                    Variable.vars_dict[symbol] = Variable.vars_dict[value]
                except KeyError:
                    # a KeyError exception is raised if the value the user is
                    # trying to assign to the variable is invalid
                    print("Invalid assignment\n")
                    return
            else:
                Variable.vars_dict[symbol] = value  # adds variable to dictionary if declaration is properly formatted


def variable_resolution(expr):  # resolves variables
    if re.match("[A-Za-z] *[0-9]|[0-9] *[A-Za-z]", expr):
        # checks for invalid variable identifiers (i.e. alphanumeric strings, such as "a2a" or "n22")
        print("Invalid identifier\n")
        return "skip"

    expr_split = re.findall("[\w]+|[+-/*]|[()]+", expr)  # splits expression into list expr_split

    for key, value in Variable.vars_dict.items():   # replaces known variables in expr_split with their values
        for index, element in enumerate(expr_split):
            if key == element:
                expr_split.insert(index, value)
                expr_split.pop(index + 1)

    expr = "".join(expr_split)  # rejoins expression as expr

    if re.search("[A-Za-z]", expr):  # any alphabetic characters still in the expression are unkown variables
        print("Unknown variable\n")
        return "skip"

    return expr


def operator_resolution(expr):  # handles occurrences of *, /, and ^ operators
    if re.match("\*\*+|//+", expr):  # sequences of * or / are invalid
        return "invalid"
    else:
        expr = re.sub("/", "//", expr)  # replaces / with // for integer division
        expr = re.sub("\^", "**", expr)  # replaces ^ with ** for exponents
        return expr


def calculate(expression):  # evaluates mathematical expressions
    if re.search("[A-Za-z]", expression):  # resolves any variables if present
        expression = variable_resolution(expression)

    if re.search("[/*^]", expression):  # resolves any *, /, or ^ if present
        expression = operator_resolution(expression)

    if expression and expression != "skip":  # runs if expression is not empty or skip key
        try:  # attempts to evaluate the expression
            print(f"{evaluate(expression)}\n")
        except Exception:  # if any exception is raised, the expression is assumed to be invalid
            print("Invalid expression\n")


def commands(command):  # contains instructions for commands (e.g. /help)
    if command == "/help":
        print("\n"
              "This program evaluates mathematical expressions.\n"
              "Expressions are combinations of numbers (e.g. 1, 2, 3) and operators (e.g. +, -, *, /). "
              "For example: 1 + 2 - 3 * 4.\n"
              "Supported operators include:\n"
              "+: addition\n"
              "-: subtraction\n"
              "*: multiplication\n"
              "/: integer division\n"
              "^: power\n"
              "To evaluate an expression, simply type it and press the Enter or Return key on your keyboard.\n"
              "The program also supports variables. To create a variable, type "
              "[variable name] = [variable value] (without brackets). "
              "Once created, variables can be used in any expression.\n")
        return

    if command == "/exit":
        print("Bye!")
        exit()

    # both of the above commands will eventually leave commands(), so if the program gets to this point, the command
    # entered is invalid.
    print("Unknown command\n")
    return


def main():  # acts as master control for the rest of the program
    print("\nEnter an expression to calculate it.\n"
          "To exit, enter /exit.\n"
          "For help, enter /help.\n")
    
    while True:
        selection = input()
        if selection.startswith("/"):  # evaluates the input as a command if the input begins with a forward slash
            commands(selection)
        elif "=" in selection:  # evaluates the input as a variable assignment if the input contains an equals sign
            Variable.create_var(selection)
        else:  # otherwise, evaluates the expression
            calculate(selection)


main()  # runs main()

# END OF PROGRAM
