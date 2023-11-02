import numpy as np
from sympy import *

from triangle import Triangle, Edge, Vertex


def diagonal_switch(t1, t2, edge_set, triangle_set):
    # Get the old edge.
    # Simply find the common edge between the edge sets
    old_e = next(iter(t1.edges.intersection(t2.edges)))

    # Get the new edge.
    # Take the union of both triangles' vertex sets
    # and subtract the vertices of the old edge.
    new_endpoints = t1.vertices.union(t2.vertices) - old_e.vertices
    new_e = Edge(new_endpoints.pop(), new_endpoints.pop())

    # Update the lambda length of the edge
    # and get the signs of the new triangles.

    # First, remove the new edge from the edge set
    # so we can update the lambda lengths / signs of triangles
    edge_set.remove(new_e)
    triangle_set.remove(t1)
    triangle_set.remove(t2)

    # Extract the necessary symbols for the formula
    t1.edges.remove(old_e)
    t2.edges.remove(old_e)
    s1 = iter(t1.edges)
    s2 = iter(t2.edges)

    e1 = next(s1)
    e3 = next(s2)
    e2 = next(s1)
    e4 = next(s2)

    # Compute the new lambda length
    if t1.sign == t2.sign:

        # Break into cases. To find the edge set of the new triangles
        # just look at the union of the vertex set of the new edge
        # and two edges coming from different original triangles. Check length is 3.
        if len(new_e.vertices.union(e1.vertices).union(e3.vertices)) == 3:
            new_t1_edges = [e1, e3, new_e]
            new_t2_edges = [e2, e4, new_e]
            new_e.symbol = (e1.symbol * e3.symbol + e2.symbol * e4.symbol) / old_e.symbol
        else:
            new_t1_edges = [e1, e4, new_e]
            new_t2_edges = [e2, e3, new_e]
            new_e.symbol = (e1.symbol * e4.symbol + e2.symbol * e3.symbol) / old_e.symbol

    if t1.sign != t2.sign:
        # Break into cases. To find the edge set of the new triangles
        # just look at the union of the vertex set of the new edge
        # and two edges coming from different original triangles. Check length is 3.
        if len(new_e.vertices.union(e1.vertices).union(e3.vertices)) == 3:
            new_t1_edges = [e1, e3, new_e]
            new_t2_edges = [e2, e4, new_e]
            new_e.symbol = (e1.symbol * e3.symbol - e2.symbol * e4.symbol) / old_e.symbol
        else:
            new_t1_edges = [e1, e4, new_e]
            new_t2_edges = [e2, e3, new_e]
            new_e.symbol = (e1.symbol * e4.symbol - e2.symbol * e3.symbol) / old_e.symbol

    # Create the new triangles
    t1.edges.add(new_e)
    t2.edges.add(new_e)

    new_t1 = Triangle(epsilon=t1.sign, e=new_t1_edges)
    new_t2 = Triangle(epsilon=t2.sign, e=new_t2_edges)

    # Update the triangle set and edge set
    triangle_set.add(new_t1)
    triangle_set.add(new_t2)
    edge_set.add(new_e)

    return new_t1, new_t2, edge_set, triangle_set
