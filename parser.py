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

def resolve_expr(exp, **keys):
    ops = [
        r"(-{0,1}[0-9.]+\*\*-{0,1}[0-9.]+|-{0,1}[0-9.]+\^-{0,1}[0-9.-]+)",
        r"(-{0,1}[0-9.]+\*-{0,1}[0-9.]+|-{0,1}[0-9.]+\/-{0,1}[0-9.-]+)",
        r"(-{0,1}[0-9.]+\+-{0,1}[0-9.]+|-{0,1}[0-9.]+\--{0,1}[0-9.-]+)",
    ]
    results = []

    keys = keys | {
        " ": "",
        "½": "1/2",
        "⅓": "1/3",
        "⅔": "2/3",
        "¼": "1/4",
        "¾": "3/4",
        "⅕": "1/5",
        "⅖": "2/5",
        "⅗": "3/5",
        "⅘": "4/5",
        "⅙": "1/6",
        "⅚": "5/6",
        "⅐": "1/7",
        "⅛": "1/8",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8",
        "⅑": "1/9",
        "⅒": "1/10",
    }
    for k, r in keys.items():
        exp = exp.replace(k, r)

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
