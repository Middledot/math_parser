import re

from typing import Union, Optional, Dict, List, Tuple

def _resolve_simple_eq(op, num1, num2):
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

def _op_in_expr(expr, op):
    return any(o in expr for o in op)

def resolve_expr(expr: str, **keys: Dict[str, str]) -> Union[int, float]:
    # the only regex here
    IS_FLOAT: str = r"^-?\d+(?:\.\d+)$"

    ops: List[Tuple[str]] = [
        ("^", "**"),
        ("*", "/"),
        ("+", "-"),
    ]
    all_ops: List[str] = [
        "^",
        "**",
        "*",
        "/",
        "+",
        "-",
    ]
    keys = {
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
        **keys
    }
    for k, v in keys.items():
        expr = expr.replace(k, str(v))

    paren: int = 0
    p_first: Optional[int] = None
    p_last: Optional[int] = None

    first_current_num: Optional[int] = None
    first_num_ready: Optional[bool] = False
    sec_current_num: Optional[int] = None
    current_op: Optional[int] = None
    actual_op: Optional[int] = None

    to_replace: Dict[str, str] = {}
    if "(" in expr and ")" in expr:
        for index, char in enumerate(expr):
            if char == "(":
                paren += 1
                if paren == 1:
                    p_first = index+1
            if char == ")":
                paren -= 1
                if paren == 0:
                    p_last = index
                    to_replace[f"{p_first}:{p_last}"] = resolve_expr(expr[p_first:p_last])
                    p_first, p_last = None, None

    _exp = list(expr)

    for k, v in to_replace.items():
        _begin = int(k.split(':')[0])-1
        _end = int(k.split(':')[1])+1

        _exp[_begin:_end] = list(str(v))
    expr = str(''.join(_exp))

    to_replace = {}

    if (re.match(IS_FLOAT, expr) is None or expr.isdigit()) and ("(" not in expr and ")" not in expr):
        for o in ops:
            if _op_in_expr(expr, o):
                current_op = o
                break

        check_for_min = True
        for ind, _char in enumerate(expr):
            if (_char.isdigit() or
                _char == "." or
                (
                    check_for_min == True and
                    _char == "-" and
                    (
                        (first_current_num is None and expr[(ind-1 if ind-1 != -1 else ind)] in all_ops) or
                        (first_current_num is not None and sec_current_num is None and expr[ind-1] in all_ops)
                    )
                )
            ):
                if not first_num_ready:
                    if first_current_num == None:
                        first_current_num = _char
                    else:
                        first_current_num = first_current_num+_char
                else:
                    if sec_current_num == None:
                        sec_current_num = _char
                    else:
                        sec_current_num = sec_current_num+_char
                if _char == "-":
                    check_for_min = False
            else:
                check_for_min = True

            if (
                _char in current_op or # It's an operator in use
                _char in all_ops or # and (sec_current_num != None)) or # It's another operator
                (_char == "-" and check_for_min is not False) or
                ind == len(expr)-1 # End of the string
            ):
                if _char == "-":
                    if check_for_min is False:
                        continue

                if not first_num_ready and first_current_num != None:
                    first_num_ready = True
                    actual_op = _char
                else:
                    eq = f"{first_current_num}{actual_op}{sec_current_num}"
                    eq_res = _resolve_simple_eq(actual_op, float(first_current_num), float(sec_current_num))
                    new_str = expr.replace(eq, str(eq_res))
                    return resolve_expr(new_str)
            elif _char in all_ops and (sec_current_num != None):
                pass

    try:
        res = int(float(expr))
    except ValueError:
        if re.match(IS_FLOAT, str(float(expr))) is not None:
            res = float(expr)
        else:
            return resolve_expr(expr)
    return res
