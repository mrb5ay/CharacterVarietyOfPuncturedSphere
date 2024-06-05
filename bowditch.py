import numpy as np
from sympy import *
from itertools import permutations

from triangle import Triangle, Edge, Vertex

# Define global variables
v = 0
e = 0
original_e = 0
t = 0
pyramidal_coords = 0


###############################################################
# Initial Set Up.
# Params: Signs of the Triangles (A12, A13, A23, B12, B13, B23)
###############################################################
def set_up(triangle_signs=(1, 1, 1, 1, 1, 1)):
    global e, original_e, t, v, pyramidal_coords
    # Initialize Vertices #
    v1 = Vertex("1")
    v2 = Vertex("2")
    v3 = Vertex("3")
    vA = Vertex("A")
    vB = Vertex("B")

    v = {"1": v1, "2": v2, "3": v3, "A": vA, "B": vB}

    # Initialize Edges #
    e_12 = Edge(v1, v2)
    e_13 = Edge(v1, v3)
    e_23 = Edge(v2, v3)
    e_A1 = Edge(vA, v1)
    e_A2 = Edge(vA, v2)
    e_A3 = Edge(vA, v3)
    e_B1 = Edge(vB, v1)
    e_B2 = Edge(vB, v2)
    e_B3 = Edge(vB, v3)

    e = {"12": e_12, "13": e_13, "23": e_23, "A1": e_A1, "A2": e_A2, "A3": e_A3,
         "B1": e_B1, "B2": e_B2, "B3": e_B3}

    set_left_and_right_edges()

    original_e = e.copy()

    # Initialize Triangles #
    T_A12 = Triangle(epsilon=triangle_signs[0], v=[v1, v2, vA])
    T_A13 = Triangle(epsilon=triangle_signs[1], v=[v1, v3, vA])
    T_A23 = Triangle(epsilon=triangle_signs[2], v=[v2, vA, v3])

    T_B12 = Triangle(epsilon=triangle_signs[3], v=[v1, v2, vB])
    T_B13 = Triangle(epsilon=triangle_signs[4], v=[v1, vB, v3])
    T_B23 = Triangle(epsilon=triangle_signs[5], v=[v2, vB, v3])

    t = {"B12": T_B12, "B23": T_B23, "A23": T_A23, "B13": T_B13, "A13": T_A13, "A12": T_A12}

    X_1, X_2, X_3, Y_1, Y_2, Y_3 = symbols("X_1 X_2 X_3 Y_1 Y_2 Y_3", real=True, positive=True)

    pyramidal_coords = {"X_1": X_1, "X_2": X_2, "X_3": X_3, "Y_1": Y_1, "Y_2": Y_2, "Y_3": Y_3}

    return e, t, v


def set_left_and_right_edges():
    global e
    e_12 = e["12"]
    e_13 = e["13"]
    e_23 = e["23"]
    e_A1 = e["A1"]
    e_A2 = e["A2"]
    e_A3 = e["A3"]
    e_B1 = e["B1"]
    e_B2 = e["B2"]
    e_B3 = e["B3"]

    for edge in e.values():
        edge.left = []
        edge.right = []

    # Determine which Edges are Left & Right #
    # For automatically determining Left-Hand and Right-Hand Turns for Trace Formula

    # Left and Right for Ai #
    e_A1.right.append(e_A3)
    e_A1.left.append(e_A2)

    e_A2.right.append(e_A1)
    e_A2.left.append(e_A3)

    e_A3.right.append(e_A2)
    e_A3.left.append(e_A1)

    # Left and Right for Bi #
    e_B1.left.append(e_B3)
    e_B1.right.append(e_B2)

    e_B2.left.append(e_B1)
    e_B2.right.append(e_B3)

    e_B3.left.append(e_B2)
    e_B3.right.append(e_B1)

    # Rest of Orientations for T_A12 #
    e_12.right.append(e_A2)
    e_A2.left.append(e_12)
    e_12.left.append(e_A1)
    e_A1.right.append(e_12)

    # Rest of Orientations for T_B12 #
    e_12.left.append(e_B2)
    e_B2.right.append(e_12)
    e_12.right.append(e_B1)
    e_B1.left.append(e_12)

    # Rest of Orientations for T_A13 #
    e_13.right.append(e_A1)
    e_A1.left.append(e_13)
    e_13.left.append(e_A3)
    e_A3.right.append(e_13)

    # Rest of Orientations for T_B13 #
    e_13.left.append(e_B1)
    e_B1.right.append(e_13)
    e_13.right.append(e_B3)
    e_B3.left.append(e_13)
    # Rest of Orientations for T_A23 #
    e_23.right.append(e_A3)
    e_A3.left.append(e_23)
    e_23.left.append(e_A2)
    e_A2.right.append(e_23)
    # Rest of Orientations for T_B23 #
    e_23.right.append(e_B3)
    e_B3.left.append(e_23)
    e_23.left.append(e_B2)
    e_B2.right.append(e_23)


# ######################################################
# # Diagonal switch
# # Switch_sign determines which sign is greater in the Kashaev diagonal switch formula.
# # Switch_sign also determines the signs of the new triangles (in the case that the old triangles disagreed).
# # Functions labeled with v2 follow the opposite relabeling strategy (i.e. (A j)(B i) rather than (A i)(B j) )
# ######################################################
def switch_e12(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["1"] = v["A"]
    new_v["2"] = v["B"]
    new_v["A"] = v["1"]
    new_v["B"] = v["2"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["13"] = e["A3"]
    new_e["23"] = e["B3"]
    new_e["A1"] = e["A1"]
    new_e["A2"] = e["B1"]
    new_e["A3"] = e["13"]
    new_e["B1"] = e["A2"]
    new_e["B2"] = e["B2"]
    new_e["B3"] = e["23"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A13"] = t["A13"]
    new_t["A23"] = t["B13"]
    new_t["B13"] = t["A23"]
    new_t["B23"] = t["B23"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A12"].sign == t["B12"].sign:
        new_lambda_length = (e["A1"].length * e["B2"].length + e["A2"].length * e["B1"].length) / e["12"].length
        new_endpoints = [i for i in t["A12"].v + t["B12"].v if i not in e["12"].endpoints]
        new_e["12"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["A12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["1"]])
        new_t["B12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["2"]])

    # Break into cases. If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["A1"].length * e["B2"].length - e["A2"].length * e["B1"].length) / e["12"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A12"].v + t["B12"].v if i not in e["12"].endpoints]
        new_e["12"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["A12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["B12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["2"]])
        else:
            new_t["A12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["B12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["2"]])

    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


def switch_e12_v2(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["1"] = v["B"]
    new_v["2"] = v["A"]
    new_v["A"] = v["2"]
    new_v["B"] = v["1"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["13"] = e["B3"]
    new_e["23"] = e["A3"]
    new_e["A1"] = e["B2"]
    new_e["A2"] = e["A2"]
    new_e["A3"] = e["23"]
    new_e["B1"] = e["B1"]
    new_e["B2"] = e["A1"]
    new_e["B3"] = e["13"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A13"] = t["B23"]
    new_t["A23"] = t["A23"]
    new_t["B13"] = t["B13"]
    new_t["B23"] = t["A13"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A12"].sign == t["B12"].sign:
        new_lambda_length = (e["A1"].length * e["B2"].length + e["A2"].length * e["B1"].length) / e["12"].length
        new_endpoints = [i for i in t["A12"].v + t["B12"].v if i not in e["12"].endpoints]
        new_e["12"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["A12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["1"]])
        new_t["B12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["2"]])

    # Break into cases. If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["A1"].length * e["B2"].length - e["A2"].length * e["B1"].length) / e["12"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A12"].v + t["B12"].v if i not in e["12"].endpoints]
        new_e["12"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["A12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["B12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["2"]])
        else:
            new_t["A12"] = Triangle(epsilon=t["B12"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["B12"] = Triangle(epsilon=t["A12"].sign, v=[v["A"], v["B"], v["2"]])

    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


def switch_e23(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["2"] = v["A"]
    new_v["3"] = v["B"]
    new_v["A"] = v["2"]
    new_v["B"] = v["3"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["12"] = e["A1"]
    new_e["13"] = e["B1"]
    new_e["A1"] = e["12"]
    new_e["A2"] = e["A2"]
    new_e["A3"] = e["B2"]
    new_e["B1"] = e["13"]
    new_e["B2"] = e["A3"]
    new_e["B3"] = e["B3"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A12"] = t["A12"]
    new_t["A13"] = t["B12"]
    new_t["B12"] = t["A13"]
    new_t["B13"] = t["B13"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A23"].sign == t["B23"].sign:
        new_lambda_length = (e["A2"].length * e["B3"].length + e["B2"].length * e["A3"].length) / e["23"].length
        new_endpoints = [i for i in t["A23"].v + t["B23"].v if i not in e["23"].endpoints]
        new_e["23"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["A23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["2"]])
        new_t["B23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["3"]])

    # If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["A2"].length * e["B3"].length - e["A3"].length * e["B2"].length) / e["23"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A23"].v + t["B23"].v if i not in e["23"].endpoints]
        new_e["23"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["A23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["2"]])
            new_t["B23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["3"]])
        else:
            new_t["A23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["2"]])
            new_t["B23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["3"]])

    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


def switch_e23_v2(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["2"] = v["B"]
    new_v["3"] = v["A"]
    new_v["A"] = v["3"]
    new_v["B"] = v["2"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["12"] = e["B1"]
    new_e["13"] = e["A1"]
    new_e["A1"] = e["13"]
    new_e["A2"] = e["B3"]
    new_e["A3"] = e["A3"]
    new_e["B1"] = e["12"]
    new_e["B2"] = e["B2"]
    new_e["B3"] = e["A2"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A12"] = t["B13"]
    new_t["A13"] = t["A13"]
    new_t["B12"] = t["B12"]
    new_t["B13"] = t["A12"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A23"].sign == t["B23"].sign:
        new_lambda_length = (e["A2"].length * e["B3"].length + e["B2"].length * e["A3"].length) / e["23"].length
        new_endpoints = [i for i in t["A23"].v + t["B23"].v if i not in e["23"].endpoints]
        new_e["23"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["A23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["2"]])
        new_t["B23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["3"]])

    # Break into cases. If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["A2"].length * e["B3"].length - e["A3"].length * e["B2"].length) / e["23"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A23"].v + t["B23"].v if i not in e["23"].endpoints]
        new_e["23"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["A23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["2"]])
            new_t["B23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["3"]])
        else:
            new_t["A23"] = Triangle(epsilon=t["B23"].sign, v=[v["A"], v["B"], v["2"]])
            new_t["B23"] = Triangle(epsilon=t["A23"].sign, v=[v["A"], v["B"], v["3"]])

    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


def switch_e13(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["1"] = v["B"]
    new_v["3"] = v["A"]
    new_v["A"] = v["3"]
    new_v["B"] = v["1"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["12"] = e["B2"]
    new_e["23"] = e["A2"]
    new_e["A1"] = e["B3"]
    new_e["A2"] = e["23"]
    new_e["A3"] = e["A3"]
    new_e["B1"] = e["B1"]
    new_e["B2"] = e["12"]
    new_e["B3"] = e["A1"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A12"] = t["B23"]
    new_t["A23"] = t["A23"]
    new_t["B12"] = t["B12"]
    new_t["B23"] = t["A12"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A13"].sign == t["B13"].sign:
        new_lambda_length = (e["A1"].length * e["B3"].length + e["B1"].length * e["A3"].length) / e["13"].length
        new_endpoints = [i for i in t["A13"].v + t["B13"].v if i not in e["13"].endpoints]
        new_e["13"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["B13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["1"]])
        new_t["A13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["3"]])

    # Break into cases. If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["B1"].length * e["A3"].length - e["A1"].length * e["B3"].length) / e["13"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A13"].v + t["B13"].v if i not in e["13"].endpoints]
        new_e["13"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["B13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["A13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["3"]])
        else:
            new_t["B13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["A13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["3"]])

    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


def switch_e13_v2(switch_sign=False):
    global e, t, v
    # Rename the vertices according to their new role
    # in the pyramidal triangulation.
    new_v = v.copy()
    new_v["1"] = v["A"]
    new_v["3"] = v["B"]
    new_v["A"] = v["1"]
    new_v["B"] = v["3"]

    for key in new_v.keys():
        new_v[key].name = key

    # Rename the edges according to their new role
    # in the pyramidal triangulation
    new_e = e.copy()

    new_e["12"] = e["A2"]
    new_e["23"] = e["B2"]
    new_e["A1"] = e["A1"]
    new_e["A2"] = e["12"]
    new_e["A3"] = e["B1"]
    new_e["B1"] = e["A3"]
    new_e["B2"] = e["23"]
    new_e["B3"] = e["B3"]

    # Rename the triangles according to their new role
    # in the pyramidal triangulation
    new_t = t.copy()

    new_t["A12"] = t["A12"]
    new_t["A23"] = t["B12"]
    new_t["B12"] = t["A23"]
    new_t["B23"] = t["B23"]

    # Compute the lambda length for the new edge.
    # Break into cases. If both signs are positive, ....
    if t["A13"].sign == t["B13"].sign:
        new_lambda_length = (e["A1"].length * e["B3"].length + e["B1"].length * e["A3"].length) / e["13"].length
        new_endpoints = [i for i in t["A13"].v + t["B13"].v if i not in e["13"].endpoints]
        new_e["13"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        new_t["B13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["1"]])
        new_t["A13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["3"]])

    # Break into cases. If the signs are different....
    # Manually enter whether signs of new triangles are same or switched
    else:
        new_lambda_length = (e["A3"].length * e["B1"].length - e["B3"].length * e["A1"].length) / e["13"].length
        if switch_sign:
            new_lambda_length = new_lambda_length * -1
        print("Assuming", new_lambda_length, "is greater than 0.")
        new_endpoints = [i for i in t["A13"].v + t["B13"].v if i not in e["13"].endpoints]
        new_e["13"] = Edge(v_1=new_endpoints[0], v_2=new_endpoints[1], lambda_length=new_lambda_length)

        if switch_sign:
            new_t["B13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["A13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["3"]])
        else:
            new_t["B13"] = Triangle(epsilon=t["A13"].sign, v=[v["A"], v["B"], v["1"]])
            new_t["A13"] = Triangle(epsilon=t["B13"].sign, v=[v["A"], v["B"], v["3"]])
    e = new_e
    t = new_t
    v = new_v
    set_left_and_right_edges()


############################################################################################################
#
# Report the lambda lengths, signs of triangles, Tetrahedral Coords, and Expressions for Signs of Punctures
#
############################################################################################################
def report_lengths_and_signs():
    global e, t, v
    print()
    print("~~~~ REPORT LENGTHS AND SIGNS ~~~")
    print()
    print("Edge lengths (Original Labeling | New Labeling : Length ): ")
    for edge in e:
        print("e", [x.name for x in e[edge].endpoints], "=", "e'_", edge, ": ", e[edge].length)

    print("Triangle signs: ")
    for triangle in t:
        print("T'_", triangle, ": ", t[triangle].sign)

    signs = (t["A12"].sign, t["A13"].sign, t["A23"].sign, t["B12"].sign, t["B13"].sign, t["B23"].sign)
    print(signs)

    print("Coordinates (New labeling): ")
    X1 = simplify(e["23"].length * e["A1"].length)
    print("X_1'", X1)
    X2 = simplify(e["13"].length * e["A2"].length)
    print("X_2'", X2)
    X3 = simplify(e["12"].length * e["A3"].length)
    print("X_3'", X3)
    Y1 = simplify(e["23"].length * e["B1"].length)
    print("Y_1'", Y1)
    Y2 = simplify(e["13"].length * e["B2"].length)
    print("Y_2'", Y2)
    Y3 = simplify(e["12"].length * e["B3"].length)
    print("Y_3'", Y3)

    epsilon_A12 = t["A12"].sign
    epsilon_A13 = t["A13"].sign
    epsilon_A23 = t["A23"].sign
    epsilon_B12 = t["B12"].sign
    epsilon_B13 = t["B13"].sign
    epsilon_B23 = t["B23"].sign
    # Print out the inequalities coming from the top right entry of peripheral curves
    print("Sign of Punctures (after switch): ")
    vA = factor(epsilon_A23 * X1 + epsilon_A13 * X2 + epsilon_A12 * X3)
    vB = factor(epsilon_B23 * Y1 + epsilon_B13 * Y2 + epsilon_B12 * Y3)
    v1 = factor(epsilon_B13 * Y3 * X1 + epsilon_B12 * Y2 * X1
                + epsilon_A13 * X3 * Y1 + epsilon_A12 * X2 * Y1)
    v2 = factor(epsilon_B23 * Y3 * X2 + epsilon_B12 * Y1 * X2
                + epsilon_A23 * X3 * Y2 + epsilon_A12 * X1 * Y2)
    v3 = factor(epsilon_B23 * Y2 * X3 + epsilon_B13 * Y1 * X3
                + epsilon_A23 * X2 * Y3 + epsilon_A13 * X1 * Y3)
    print("vA: ", vA)
    print("vB: ", vB)
    print("v1: ", v1)
    print("v2: ", v2)
    print("v3: ", v3)

    print("Helpful identities: ")
    print("v1 + v2 + v3 = ", simplify(v1 + v2 + v3))
    print("v1 + v2 - v3 = ", simplify(v1 + v2 - v3))
    print("v1 + v3 - v2 = ", simplify(v1 + v3 - v2))
    print("v2 + v3 - v1 = ", simplify(v2 + v3 - v1))


# Takes in the triangles which the curve travels through (in order)
# The same triangle should be listed at the beginning and end
# Returns the trace of the curve.
def trace_formula(triangles, verbose=False):
    global e, t, v
    # Get the list of edges which the s.c.c intersects
    edge_list = []
    for i in range(len(triangles) - 1):
        next_edge = list(set(triangles[i].v) & set(triangles[i + 1].v))
        next_edge = next_edge[0].name + next_edge[1].name
        try:
            edge_list.append(e[next_edge])
        except KeyError:
            edge_list.append(e[next_edge[::-1]])
    if verbose:
        print("")
        print("Edges Crossed: ", edge_list)
        print("")
    # Get the matrices for the formula
    matrix_list = []
    edge_product = 1
    for j in range(len(edge_list)):
        edge_product = edge_product * edge_list[j].length
        k = (j + 1) % len(edge_list)
        # Get the third edge (which the curve does not intersect) of the triangle
        other_edge = list(set(edge_list[j].endpoints).symmetric_difference(set(edge_list[k].endpoints)))
        other_edge = other_edge[0].name + other_edge[1].name
        try:
            other_edge = e[other_edge]
        except KeyError:
            other_edge = e[other_edge[::-1]]

        # If it makes a left-hand turn:
        if edge_list[k] in edge_list[j].left:
            matrix_list.append(
                Matrix([[edge_list[j].length, triangles[k].sign * other_edge.length], [0, edge_list[k].length]]))
        # If it makes a right-hand turn:
        elif edge_list[k] in edge_list[j].right:
            matrix_list.append(
                Matrix([[edge_list[k].length, 0], [triangles[k].sign * other_edge.length, edge_list[j].length]]))
        # If something was wrong with the given s.c.c. path:
        else:
            print("Error. Edge ", edge_list[k], " is not adjacent to edge ", edge_list[j])
    if verbose:
        print("")
        print("Matrices in Product: ", matrix_list)
        print("")
    matrix_representation = Matrix([[1, 0], [0, 1]])
    for m in matrix_list:
        matrix_representation = matrix_representation * m
    matrix_representation = expand(matrix_representation / edge_product)
    matrix_representation = substitute_pyramidal_coords(matrix_representation)

    if verbose:
        print("")
        print("Resulting  matrix is")
        print("")
        print(matrix_representation)
    print("")
    print("Trace: ")
    print(Trace(matrix_representation).simplify())
    print("")


# Gets the signs after switches
def get_signs_after_switches(signs):
    set_up(triangle_signs=signs)
    print("Switch e_12")
    switch_e12()
    report_signs()
    set_up(triangle_signs=signs)
    switch_e12(switch_sign=True)
    report_signs()
    set_up(triangle_signs=signs)
    print("Switch e_13")
    switch_e13()
    report_signs()
    set_up(triangle_signs=signs)
    switch_e13(switch_sign=True)
    report_signs()
    set_up(triangle_signs=signs)
    print("Switch e_23")
    switch_e23()
    report_signs()
    set_up(triangle_signs=signs)
    switch_e23(switch_sign=True)
    report_signs()


def report_signs():
    signs = (t["A12"].sign, t["A13"].sign, t["A23"].sign, t["B12"].sign, t["B13"].sign, t["B23"].sign)
    print(signs)


# Get the traces of curves
def get_traces_of_special_curves(verbose=False):
    print("============")
    print("gamma_A1")
    print("============")
    trace_formula([t["A12"], t["A23"], t["A13"], t["B13"], t["B12"], t["A12"]], verbose=verbose)

    print("============")
    print("gamma_B1")
    print("============")
    trace_formula([t["B12"], t["A12"], t["A13"], t["B13"], t["B23"], t["B12"]], verbose=verbose)

    print("============")
    print("gamma_A2")
    print("============")
    trace_formula([t["A12"], t["B12"], t["B23"], t["A23"], t["A13"], t["A12"]], verbose=verbose)

    print("============")
    print("gamma_B2")
    print("============")
    trace_formula([t["B12"], t["A12"], t["A23"], t["B23"], t["B13"], t["B12"]], verbose=verbose)

    print("============")
    print("gamma_A3")
    print("============")
    trace_formula([t["A23"], t["A12"], t["A13"], t["B13"], t["B23"], t["A23"]], verbose=verbose)

    print("============")
    print("gamma_B3")
    print("============")
    trace_formula([t["B23"], t["A23"], t["A13"], t["B13"], t["B12"], t["B23"]], verbose=verbose)

    print("============")
    print("gamma_12")
    print("============")
    trace_formula([t["B12"], t["B23"], t["A23"], t["A12"], t["A13"], t["B13"], t["B12"]], verbose=verbose)

    print("============")
    print("gamma_13")
    print("============")
    trace_formula([t["B13"], t["B23"], t["A23"], t["A13"], t["A12"], t["B12"], t["B13"]], verbose=verbose)

    print("============")
    print("gamma_23")
    print("============")
    trace_formula([t["A12"], t["A23"], t["A13"], t["B13"], t["B23"], t["B12"], t["A12"]], verbose=verbose)
    print("")


def substitute_pyramidal_coords(expr):
    global original_e, t, v
    # Use the original edge lengths to substitute in the pyramidal coords
    e = original_e
    e_12, e_13, e_23, e_A1, e_A2, e_A3, e_B1, e_B2, e_B3 = e["12"].length, e["13"].length, e["23"].length, \
                                                           e["A1"].length, e["A2"].length, e["A3"].length, \
                                                           e["B1"].length, e["B2"].length, e["B3"].length

    X_1, X_2, X_3, Y_1, Y_2, Y_3 = pyramidal_coords["X_1"], pyramidal_coords["X_2"], pyramidal_coords["X_3"], \
                                   pyramidal_coords["Y_1"], pyramidal_coords["Y_2"], pyramidal_coords["Y_3"]

    res_expr = expr.subs([(e_A1 * e_23, X_1),
                          (e_A2 * e_13, X_2),
                          (e_A3 * e_12, X_3),
                          (e_B1 * e_23, Y_1),
                          (e_B2 * e_13, Y_2),
                          (e_B3 * e_12, Y_3)])

    res_expr = res_expr.subs([(e_A1 / e_B1, X_1 / Y_1),
                              (e_B1 / e_A1, Y_1 / X_1),
                              (e_A2 / e_B2, X_2 / Y_2),
                              (e_B2 / e_A2, Y_2 / X_2),
                              (e_A3 / e_B3, X_3 / Y_3),
                              (e_B3 / e_A3, Y_3 / X_3)])
    return res_expr


# set_up((1, 1, 1, 1, 1, -1))
# print("Before switch ....")
# get_traces_of_special_curves()
# switch_e12()
# print("After switch ....")
# get_traces_of_special_curves()
get_signs_after_switches((1, 1, 1, 1, 1, -1))
