import re
from string import digits

def _resolve_small_eq(op, num1, num2):
    if op == "+":
        return float(num1)+float(num2)
    elif op == "-":
        return float(num1)-float(num2)
    elif op == "*":
        return float(num1)*float(num2)
    elif op == "/":
        return float(num1)/float(num2)
    elif op == "**":
        return float(num1)**float(num2)
    elif op == "^":
        return float(num1)**float(num2)
    #elif op == "":
    #    return num1+num2

def resolve_expr(exp):
    ops = [
        r"(-{0,1}[0-9.]+\*\*-{0,1}[0-9.]+|-{0,1}[0-9.]+\^-{0,1}[0-9.-]+)",
        r"(-{0,1}[0-9.]+\*-{0,1}[0-9.]+|-{0,1}[0-9.]+\/-{0,1}[0-9.-]+)",
        r"(-{0,1}[0-9.]+\+-{0,1}[0-9.]+|-{0,1}[0-9.]+\--{0,1}[0-9.-]+)",
    ]
    results = []
    exp = exp.replace(" ", "")
    p = 0
    current = []
    for c, i in enumerate(list(exp)):
        if i == "(":
            p += 1
            if len(current) == 0:
                current.append(c)
        if i == ")":
            p -= 1
            if len(current) == 1:
                current.append(c)
            if p == 0 and len(current) == 2:
                results.append(current)
                current = []

    replacables = {f"({exp[i[0]+1:i[1]]})": exp[i[0]+1:i[1]] for i in results}
    
    for k, i in replacables.items():
        exp = exp.replace(k, resolve_expr(i))

    results = {}
    for i in ops:
        while True:
            eq = re.search(i, exp)
            if eq == None:
                break
            if eq != None:
                eq = eq.group()
                op = eq.translate(eq.maketrans("", "", digits)).strip(".")
                if len(op) > 1:
                    op = op[0]
                results[eq] = _resolve_small_eq(op, *eq.split(op))

            for k, r in results.items():
                exp = exp.replace(k, str(r))

    return float(exp)
