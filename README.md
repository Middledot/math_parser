# Math Parser
1 function

1 equation

23* memory leaks

1 result

<span style="font-size:0.8em;"> * exageration </span>

## Examples

It can do simple equations
```py
>>> from math_parser import resolve_expr
>>> print(resolve_expr("2^2"))
4
```

Complicated-ish expressions (brackets, order of operations)
```py
>>> from math_parser import resolve_expr
>>> print(resolve_expr("3+(5/7*2-6)"))
-1.5714285714285712
```

Variable support
```py
>>> from math_parser import resolve_expr
>>> print(resolve_expr("a*12", a=3))
36
```

One day someone's going to tell me this is [extremely inefficient](https://github.com/QwireDev/MathParser/blob/master/math_parser.py) and they'll probably be right.
