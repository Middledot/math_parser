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
        ("^"),  # TODO: , "**"),
        ("*", "/"),
        ("+", "-"),
    ]
    all_ops: List[str] = [
        "^",
        #"**",  # TODO
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

        check_for_extra_char = True
        if "^" not in current_op:
            for ind, char in enumerate(expr):
                if (char.isdigit() or
                    char == "." or
                    (
                        check_for_extra_char == True and
                        char == "-" and
                        (
                            (first_current_num is None and expr[(ind-1 if ind-1 != -1 else ind)] in all_ops) or
                            (first_current_num is not None and sec_current_num is None and expr[ind-1] in all_ops)
                        )
                    )
                ):
                    if not first_num_ready:
                        if first_current_num == None:
                            first_current_num = char
                        else:
                            first_current_num = first_current_num+char
                    else:
                        if sec_current_num == None:
                            sec_current_num = char
                        else:
                            sec_current_num = sec_current_num+char
                    if char == "-":
                        check_for_extra_char = False
                else:
                    check_for_extra_char = True

                if (
                    char in all_ops or # It's another operator # also does check for current op
                    (char == "-" and check_for_extra_char is not False) or
                    ind == len(expr)-1 # End of the string
                ):
                    if char == "-":
                        if check_for_extra_char is False:
                            continue

                    if not first_num_ready and first_current_num != None:
                        first_num_ready = True
                        actual_op = char
                    else:
                        eq = f"{first_current_num}{actual_op}{sec_current_num}"
                        eq_res = _resolve_simple_eq(actual_op, float(first_current_num), float(sec_current_num))
                        new_str = expr.replace(eq, str(eq_res))
                        return resolve_expr(new_str)
        else:
            to_eval = []  # not actual eval
            _current = 0
            def safe_list_get(l, id, default=None):
                try:
                    return l[id]
                except IndexError:
                    return default
            for ind, char in enumerate(expr):
                if (
                    char.isdigit() or
                    char == "." or(
                        check_for_extra_char == True and
                        char == "-" and
                        (
                            (expr[(ind+1 if ind+1 != len(expr)-1 else ind)].isdigit() and expr[(ind-1 if ind-1 != -1 else ind)] in all_ops) or
                            (first_current_num is not None and sec_current_num is None and expr[ind-1] in all_ops)
                        )
                    )
                ):
                    if safe_list_get(to_eval, _current) == None:
                        to_eval.append([char, None])
                    else:
                        to_eval[_current][0] = to_eval[_current][0]+char

                if (
                    char in all_ops or
                    (char == "-" and check_for_extra_char is not False) or
                    ind == len(expr)-1
                ):
                    if char == "-":
                        if check_for_extra_char is False:
                            continue

                    if char in current_op:
                        _current += 1
                        to_eval.append(["", char])
                    else:
                        if len(to_eval) == 2:
                            eq = f"{to_eval[0]}{actual_op}{to_eval[1]}"
                            eq_res = _resolve_simple_eq(actual_op, float(first_current_num), float(sec_current_num))
                            new_str = expr.replace(eq, str(eq_res))
                            return resolve_expr(new_str)
                        else:
                            full_eq = ""
                            new_nums = []
                            for _i in to_eval:
                                num = _i[0]
                                _op = _i[1]
                                if _op is None:
                                    full_eq += num
                                else:
                                    full_eq += f"{_op}{num}"
                                new_nums.append(num)
                            res = 1
                            for _ in reversed(new_nums):
                                res = float(_)**res
                            new_str = expr.replace(full_eq, str(res))
                            return resolve_expr(new_str)


    try:
        res = int(float(expr))
    except ValueError:
        if re.match(IS_FLOAT, str(float(expr))) is not None:
            res = float(expr)
        else:
            return resolve_expr(expr)
    return res
