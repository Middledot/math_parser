from typing import Dict, Union

OPERATORS = ["^", "**", "*", "/", "+", "-"]
MAPPED_OPERATORS = [
    ("^", "**"),
    ("*", "/"),
    ("+", "-"),
]

NumberType = Union[int, float]

def _resolve_simple_eq(op, num1, num2) -> NumberType:
    if op == "*":
        return num1*num2
    elif op in ["**", "^"]:
        return num1**num2
    elif op == "+":
        return num1+num2
    elif op == "-":
        return num1-num2
    elif op == "/":
        return num1/num2

def resolve_expr(expr: str, **keys: Dict[str, str]) -> NumberType:
    keys = {
        " ": "",
        "÷": "/",
        "×": "*",
        "½": "(1/2)",
        "⅓": "(1/3)",
        "⅔": "(2/3)",
        "¼": "(1/4)",
        "¾": "(3/4)",
        "⅕": "(1/5)",
        "⅖": "(2/5)",
        "⅗": "(3/5)",
        "⅘": "(4/5)",
        "⅙": "(1/6)",
        "⅚": "(5/6)",
        "⅐": "(1/7)",
        "⅛": "(1/8)",
        "⅜": "(3/8)",
        "⅝": "(5/8)",
        "⅞": "(7/8)",
        "⅑": "(1/9)",
        "⅒": "(1/10)",
        **keys
    }
    for k, v in keys.items():
        expr = expr.replace(k, str(v))

    listable = []
    c_num = ""

    for index, char in enumerate(expr):
        if char == "(":
            start = index
            end = None
            find = expr[index:]
            unclosed = 0
            for sub_i, sub_c in enumerate(find):
                if sub_c == ")":
                    unclosed -= 1
                elif sub_c == "(":
                    unclosed += 1

                if unclosed == 0:
                    end = sub_i+index
                    break

            new = list(expr)
            new[start:end+1] = [str(resolve_expr(''.join(i for i in new[start+1:end])))]
            new = ''.join(i for i in new)
            return resolve_expr(new)

        if char.isdigit():
            c_num += char
        elif char == ".":
            before = None
            if index-1 > -1:
                before = expr[index-1]

            if before is None or before in OPERATORS:
                c_num += "0"+char
            elif before.isdigit():
                c_num += char

        if char == "-":
            before = None
            if index-1 > -1:
                before = expr[index-1]

            if before is None or before in OPERATORS:  # begginning of the exp OR there's already a minus sign
                c_num = "-"
            elif before.isdigit():  # it's a minus sign, not a negative
                listable.append(c_num)
                listable.append("-")
                c_num = ""

        if char == "+":
            before = None
            if index-1 > -1:
                before = expr[index-1]

            if before is None or before == "+":
                c_num = ""
            elif before.isdigit():
                listable.append(c_num)
                listable.append("+")
                c_num = ""

        if char == "*":
            before = None
            if index-1 > -1:
                before = expr[index-1]
            after = None
            if index-1 > -1:
                after = expr[index+1]

            if before == "*":
                listable.append(c_num+"*")
                c_num = ""
            elif after == "*":
                listable.append(c_num)
                c_num = "*"
            else:
                listable.append(c_num)
                listable.append("*")
                c_num = ""

        if char == "/":
            listable.append(c_num)
            listable.append("/")
            c_num = ""

        if char == "^":
            listable.append(c_num)
            listable.append("^")
            c_num = ""

    if c_num:
        listable.append(c_num)

    return resolve_from_listable(listable)

def to_num_type(string) -> NumberType:
    try:
        res = float(string)
    except ValueError:
        return int(string)
    else:
        if round(res) == res:
            res = int(res)
        return res

def resolve_from_listable(listable) -> NumberType:
    for ops in MAPPED_OPERATORS:
        while True:
            shortest_res = {}
            for op in ops:
                try:
                    ind = listable.index(op)
                except ValueError:
                    continue
                else:
                    shortest_res[ind] = op

            if not shortest_res:
                break

            smallest = min(shortest_res.keys())
            the_op = shortest_res[smallest]

            num1, num2 = to_num_type(listable[smallest-1]), to_num_type(listable[smallest+1])

            result = to_num_type(str(_resolve_simple_eq(the_op, num1, num2)))

            listable[smallest-1:smallest+2] = [result]

    return listable[0]
