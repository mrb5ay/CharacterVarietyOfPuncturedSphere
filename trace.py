import numpy as np
from sympy import *

# Declare Lambda Lengths #
e_12, e_13, e_14, e_15, e_23, e_24, e_25, e_34, e_45 = symbols('e_12 e_13 e_14 e_15 e_23 e_24 e_25 e_34 e_45')

# Declare Signs of Triangles #
T_13, T_15, T_23, T_25, T_34, T_45 = symbols('T_13 T_15 T_23 T_25 T_34 T_45')


# Constructs a matrix, so I don't have to write it all the way out
def m(a, b, c, d):
    return Matrix([[a, b], [c, d]])


# Matrix Representation of Peripheral Curve 1 #
def trace_l1():
    A1 = Matrix([[e_12, T_34 * e_25], [0, e_15]])
    B1 = Matrix([[e_15, T_23 * e_45], [0, e_14]])
    C1 = Matrix([[e_14, T_25 * e_34], [0, e_13]])
    D1 = Matrix([[e_13, T_45 * e_23], [0, e_12]])
    result = expand(A1 * B1 * C1 * D1)
    return result


# Matrix Representation of Peripheral Curve 2 #
def trace_l2():
    A2 = Matrix([[e_25, T_34 * e_15], [0, e_12]])
    B2 = Matrix([[e_12, T_45 * e_13], [0, e_23]])
    C2 = Matrix([[e_23, T_15 * e_34], [0, e_24]])
    D2 = Matrix([[e_24, T_13 * e_45], [0, e_25]])
    result = expand(A2 * B2 * C2 * D2)
    return result


# Matrix Representation of Peripheral Curve 3 #
def trace_l3():
    A3 = Matrix([[e_34, T_15 * e_24], [0, e_23]])
    B3 = Matrix([[e_23, T_45 * e_12], [0, e_13]])
    C3 = Matrix([[e_13, T_25 * e_14], [0, e_34]])
    result = expand(A3 * B3 * C3)
    return result


# Matrix Representation of Peripheral Curve 4 #
def trace_l4():
    A4 = Matrix([[e_45, T_13 * e_25], [0, e_24]])
    B4 = Matrix([[e_24, T_15 * e_23], [0, e_34]])
    C4 = Matrix([[e_34, T_25 * e_13], [0, e_14]])
    D4 = Matrix([[e_14, T_23 * e_15], [0, e_45]])
    result = expand(A4 * B4 * C4 * D4)
    return result


# Matrix Representation of Peripheral Curve 5 #
def trace_l5():
    A5 = Matrix([[e_25, T_13 * e_24], [0, e_45]])
    B5 = Matrix([[e_45, T_23 * e_14], [0, e_15]])
    C5 = Matrix([[e_15, T_34 * e_12], [0, e_25]])
    result = expand(A5 * B5 * C5)
    return result


def trace_l1_l2():
    A6 = Matrix([[e_23, T_15 * e_34], [0, e_24]])
    B6 = Matrix([[e_24, T_13 * e_45], [0, e_25]])
    C6 = Matrix([[e_15, 0], [T_34 * e_12, e_25]])
    D6 = Matrix([[e_15, T_23 * e_45], [0, e_14]])
    E6 = Matrix([[e_14, T_25*e_34], [0, e_13]])
    F6 = Matrix([[e_23, 0], [T_45*e_12, e_13]])
    result = expand(A6 * B6 * C6 * D6 * E6 * F6)
    return result


def trace_l3_l4():
    A7 = Matrix([[e_23, T_15 * e_34], [0, e_24]])
    B7 = Matrix([[e_45, 0], [T_13 * e_25, e_24]])
    C7 = Matrix([[e_14, 0], [T_23 * e_15, e_45]])
    D7 = Matrix([[e_14, T_25 * e_34], [0, e_13]])
    E7 = Matrix([[e_23, 0], [T_45 * e_12, e_13]])
    result = expand(A7 * B7 * C7 * D7 * E7)
    return result


def trace_l2_l3():
    A8 = m(e_25, 0, T_34 * e_15, e_12)
    B8 = m(e_24, 0, T_13*e_45, e_25)
    C8 = m(e_24, T_15*e_23, 0, e_34)
    D8 = m(e_13, 0, T_25*e_14, e_34)
    E8 = m(e_13, T_45*e_23, 0, e_12)
    result = expand(A8 * B8 * C8 * D8 * E8)
    return result


# Takes in a trace function, then prints out the entries in new lines
def print_trace(f):
    trace_result = f()
    top_left = trace_result.row(0).col(0)[0]
    top_right = trace_result.row(0).col(1)[0]
    bottom_left = trace_result.row(1).col(0)[0]
    bottom_right = trace_result.row(1).col(1)[0]
    print("Top left ", top_left)
    print("Top right ", top_right)
    print("Bottom left ", bottom_left)
    print("Bottom right ", bottom_right)


print_trace(trace_l2_l3)
