import numpy as np
from sympy import *


class Vertex:
    def __init__(self, name):
        self.name = name
        self.symbol = symbols("v_" + name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        if self.name == "A":
            return 10
        if self.name == "B":
            return 30
        return int(self.name)

    def __str__(self):
        return "v_" + self.name

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, v_1, v_2):
        self.vertices = set()
        self.vertices.update([v_1, v_2])
        self.symbol = symbols("e_" + v_1.name + v_2.name)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __str__(self):
        s = iter(self.vertices)
        return "e_" + next(s).name + next(s).name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        s = iter(self.vertices)
        return next(s).__hash__() + next(s).__hash__()


class Triangle:
    def __init__(self, epsilon=1, e=0, v=0):
        if e == 0 and v == 0:
            raise ValueError

        self.sign = epsilon

        if e != 0:
            self.edges = set()
            self.edges.update(e)
            self.vertices = e[0].vertices.union(e[1].vertices).union(e[2].vertices)
            s = iter(self.vertices)
            self.symbol = symbols("T_" + next(s).name + next(s).name + next(s).name)
        elif v != 0:
            self.vertices = set()
            self.vertices.update(v)
            self.edges = set()
            self.edges.update([Edge(v[0], v[1]), Edge(v[1], v[2]), Edge(v[0], v[2])])
            self.symbol = symbols("T_" + v[0].name + v[1].name + v[2].name)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __str__(self):
        s = iter(self.vertices)
        return "T_" + next(s).name + next(s).name + next(s).name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        s = iter(self.vertices)
        return next(s).__hash__() + next(s).__hash__() + next(s).__hash__()
