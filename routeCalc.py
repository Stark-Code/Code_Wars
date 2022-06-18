import re
import sys


def checkSolution(expression):
    if re.match(r"^(?:-?\d+)\.*\d*$", expression):  # Check for solution
        return True


def populateMatch(m):
    return [m.group(i) for i in range(1, 4)]


def recursiveEval(expression):
    print(f"Evaluating: {expression}")
    if checkSolution(expression):
        return float(expression)
    # -?\d +\.?\d * e?-?\d *)([*$])(-?\d +\.?\d * e?-?\d *
    x = re.search(r"(-?\d+\.?\d*(?:e-\d*)?)([*$])(-?\d+\.?\d*(?:e-\d*)?)", expression)
    if x:
        match = populateMatch(x)
        print(match)
        if match[1] == "*":
            result = float(match[0]) * float(match[2])
        else:  # Division
            result = float(match[0]) / float(match[2])
        evaluatedExpression = expression[:x.span()[0]] + str(result) + expression[x.span()[1]:]
        return recursiveEval(evaluatedExpression)
    else:
        y = re.search(r"(-?\d+\.?\d*(?:e-\d*)?)([+-])(-?\d+\.?\d*(?:e-\d*)?)", expression)
        if y:
            match = populateMatch(y)
            print(match)
            if match[1] == "+":
                result = float(match[0]) + float(match[2])
            else:  # Subtraction
                result = float(match[0]) - float(match[2])
            evaluatedExpression = expression[:y.span()[0]] + str(result) + expression[y.span()[1]:]
            return recursiveEval(evaluatedExpression)


def calculate(expression):
    if checkSolution(expression):
        return float(expression)
    if re.search(r"[^0-9e+\-*$]", expression):  # Check for invalid characters
        return '400: Bad request'
    elif not re.search(r"^(?:-?\d+.?\d*)(?:[*$+-])(?:-?\d+.?\d*)*$", expression):  # Check for invalid expressions
        return '400: Bad request (Expression Invalid)'
    return recursiveEval(expression)

e1 = "32e3*6"
e2 = "5+8-8*2$4"
e3 = "5e-4+2"
r1 = calculate(e3)
print(r1)


# print(float("2e-10"))












#
# eNeg = re.search(r'(-?\d+)e-(\d+)', component)
#         if eNeg:
#             print(eNeg)
#             print(eNeg.group(1))
#             print(eNeg.group(2))
#             _result = int(eNeg.group(1))
#             for _ in range(int(eNeg.group(2))):
#                 _result /= 10
#             return _result
#         else:
#             return float(e.group(1))