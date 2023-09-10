import numpy as np
from sympy import *

a, b, c, d, e, f, g, h = symbols('a b c d e f g h')

print(expand(c * (a + b - a + c*d + e*d) + c*e*d))

A = Matrix([[a, b], [c, d]])
B = Matrix([[e, f], [g, h]])

print(A)
print(B)
print(A * B)

e_t1, y_e1 = symbols('e_t1, y_e1')

print(factor(e_t1 * y_e1 + y_e1 * y_e1))
