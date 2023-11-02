import numpy as np
from sympy import *

from triangle import Triangle, Edge, Vertex
from switch import diagonal_switch

######################################################
# Initial Set Up
######################################################

# Initialize Vertices #
v1 = Vertex("1")
v2 = Vertex("2")
v3 = Vertex("3")
vA = Vertex("A")
vB = Vertex("B")

vertex_set = {v1, v2, v3, vA, vB}

# Initialize Edges #
edge_set = set()
for v in vertex_set:
    for w in vertex_set:
        if v != w:
            edge_set.add(Edge(v, w))

# Initialize Triangles #
triangle_set = set()

T_12B = Triangle(epsilon=1, v=[v1, v2, vB])
T_2B3 = Triangle(epsilon=1, v=[v2, vB, v3])
T_2A3 = Triangle(epsilon=1, v=[v2, vA, v3])
T_1B3 = Triangle(epsilon=1, v=[v1, vB, v3])
T_13A = Triangle(epsilon=1, v=[v1, v3, vA])
T_12A = Triangle(epsilon=1, v=[v1, v2, vA])

triangle_set.update([T_12B, T_2B3, T_2A3, T_1B3, T_13A, T_12A])

######################################################
# Doing Diagonal Switches
######################################################

for e in edge_set:
    globals()[e.__str__()] = e
    print(globals()[e.__str__()], globals()[e.__str__()].symbol)

T_AB2, T_AB1, edge_set, triangle_set = diagonal_switch(T_12B, T_12A, edge_set, triangle_set)

T_123, T_12A, edge_set, triangle_set = diagonal_switch(T_2A3, T_13A, edge_set, triangle_set)

T_3AB, T_23A, edge_set, triangle_set = diagonal_switch(T_AB2, T_2B3, edge_set, triangle_set)

print(edge_set)
print(triangle_set)

