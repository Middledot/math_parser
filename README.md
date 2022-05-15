# Math Parser
1 function

1 equation

23* memory leaks

1 result

<span style="font-size:0.5em;"> * this may or may not be an exageration </span>

Simple parser for math expressions in strings.

## Examples

It can do simple equations
```py
>>> from math_parser import resolve_expr
>>> resolve_expr("2^2")  # simple calculations
4
>>> resolve_expr("3+(5/7*2-6)")  # complicated-ish expressions (brackets & order of operations)
-1.5714285714285712
>>> resolve_expr("a*12", a=3)  # custom variable support
36
>>> resolve_expr("½ × ⅗")  # auto-replaces supported symbols and spaces
0.3
>>> resolve_expr("1+2+3+4+5+6+7*7") 
70
>>>
```

[Source?](https://github.com/QwireDev/MathParser/blob/master/math_parser.py)
