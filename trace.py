import numpy as np
from sympy import *

# Declare Lambda Lengths #
e_12, e_13, e_14, e_15, e_23, e_24, e_25, e_34, e_45 = symbols('e_12 e_13 e_14 e_15 e_23 e_24 e_25 e_34 e_45')

# Declare Signs of Triangles #
T_13, T_15, T_23, T_25, T_34, T_45 = symbols('T_13 T_15 T_23 T_25 T_34 T_45')

# Matrix Representation of Peripheral Curve 1 #
A1 = Matrix([[e_12, T_34 * e_25], [0, e_15]])
B1 = Matrix([[e_15, T_23 * e_45], [0, e_14]])
C1 = Matrix([[e_14, T_25 * e_34], [0, e_13]])
D1 = Matrix([[e_13, T_45 * e_23], [0, e_12]])

print("Representation of Peripheral 1: ", expand(A1 * B1 * C1 * D1))

# Matrix Representation of Peripheral Curve 2 #
A2 = Matrix([[e_25, T_34 * e_15], [0, e_12]])
B2 = Matrix([[e_12, T_45 * e_13], [0, e_23]])
C2 = Matrix([[e_23, T_15 * e_34], [0, e_24]])
D2 = Matrix([[e_24, T_13 * e_45], [0, e_25]])

print("Representation of Peripheral 2: ", expand(A2 * B2 * C2 * D2))

# Matrix Representation of Peripheral Curve 3 #
A3 = Matrix([[e_34, T_15 * e_24], [0, e_23]])
B3 = Matrix([[e_23, T_45 * e_12], [0, e_13]])
C3 = Matrix([[e_13, T_25 * e_14], [0, e_34]])

print("Representation of Peripheral 3: ", expand(A3 * B3 * C3))

# Matrix Representation of Peripheral Curve 4 #
