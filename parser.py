
import re

def _process_small_eq(op, num1, num2):
    if op == "+":
        return num1+num2
    elif op == "-":
        return num1-num2
    elif op == "*":
        return num1*num2
    elif op == "/":
        return num1/num2
    elif op == "**":
        return num1**num2
    elif op == "^":
        return num1**num2
    #elif op == "":
    #    return num1+num2

def resolve_expr(exp):
    _ops = [["^", "ergs"], ["*", "/"], ["+", "-"]]# "%"]
    exp = exp.replace(" ", "")
    n_exp = exp
    for c, i in enumerate(list(exp)):
        if i == "(":
            p = 0
            for ce, ie in enumerate(exp[c:]):
                if ie == "(":
                    p += 1
                elif ie == ")":
                    p -= 1
                if p == 0:
                    n_exp = n_exp.replace(exp[c:][:ce+1], resolve_expr(exp[c+1:][:ce-1]))
                    continue

    ops = _ops.copy()

    for c, o in enumerate(_ops):
        amt = 0
        for i in o:
            if i not in n_exp:
                ops[c].remove(i)
                print(ops[c])
                amt -= 1
                
    print("final: ", ops)
    for o in ops:
        print(o)
        for i in o:
            print(i)
            before = n_exp
            c = 0
            while True:
                c += 1
                res = re.search(f"([0-9.]+\{i}[0-9.]+)", n_exp)
                if res != None:
                    res = res.group()
                    print(res)
                    x, y = res.split(i)
                    x, y = int(x), int(y)
                    simpl = str(_process_small_eq(i, x, y))
                    print("simplified: ", simpl)
                    n_exp = n_exp.replace(res, simpl)
                if n_exp == before:
                    break
                else:
                    before = n_exp

    return n_exp

print("answer: ", resolve_expr("3+0.7142857142857143*-4"))
#print("answer: ", resolve_expr("3+ (5/ 7*2-6)"))
