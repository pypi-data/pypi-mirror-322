# -*- coding: utf-8 -*-
from typing import List

import numpy as np
from astartool.error import ParameterError

from astar_math.fuzzy.number import ContinuousFuzzyNumber, TrapezoidalFuzzyNumber, DiscreteFuzzyNumber

npa = np.array
npl = np.linalg
npr = np.random


class DiscreteFuzzyMatrix:
    def __init__(self, matrix):
        self.matrix = []
        if isinstance(matrix, np.ndarray):
            shape = matrix.shape
            assert len(shape) == 2
            m, n = shape
            for i in range(m):
                raw = []
                for j in range(n):
                    if isinstance(matrix[i, j], float):
                        item = DiscreteFuzzyNumber(matrix[i, j], [1, ])
                    elif isinstance(matrix[i, j], DiscreteFuzzyNumber):
                        item = matrix[i, j]
                    else:
                        raise ParameterError
                    raw.append(item)
                self.matrix.append(raw)
            self.matrix = npa(self.matrix)

    def __mul__(self, other):
        if isinstance(other, DiscreteFuzzyMatrix):
            return self * other.matrix
        elif isinstance(other, np.ndarray):
            assert self.matrix.shape[1] == other.shape[0]
            m, n = self.matrix.shape
            n, p = other.shape
            result = np.empty((m, p))
            for i in range(m):
                for j in range(n):
                    for k in range(p):
                        result[i, k] = self.matrix[i, j] * other[j, k]
            return result

        raise ParameterError


class ContinuousFuzzyMatrix:
    def __init__(self, matrix=None, size=None):
        self.matrix = []
        self.init_matrix(matrix)
        if size is None:
            self.size = len(self.matrix), len(self.matrix[0])
        else:
            self.size = size

    def __mul__(self, other):
        if isinstance(other, ContinuousFuzzyMatrix):
            return self * other.matrix
        elif isinstance(other, np.ndarray):
            assert self.matrix.shape[1] == other.shape[0]
            m, n = self.matrix.shape
            n, p = other.shape
            result = np.empty((m, p))
            for i in range(m):
                for j in range(n):
                    for k in range(p):
                        result[i, k] = self.matrix[i, j] * other[j, k]
            return result

        raise ParameterError

    @property
    def shape(self):
        return self.size

    def init_matrix(self, matrix):
        if isinstance(matrix, np.ndarray):
            shape = matrix.shape
            assert len(shape) == 2
            m, n = shape
            for i in range(m):
                raw = []
                for j in range(n):
                    if isinstance(matrix[i, j], float):
                        item = ContinuousFuzzyNumber(matrix[i, j], lambda x: int(x == matrix[i, j]))
                    elif isinstance(matrix[i, j], ContinuousFuzzyNumber):
                        item = matrix[i, j]
                    else:
                        raise ParameterError
                    raw.append(item)
                self.matrix.append(raw)
            self.matrix = npa(self.matrix)


class TrapezoidalFuzzyMatrix(ContinuousFuzzyMatrix):
    def __init__(self, matrix=None, size=None):
        self.a, self.b, self.c, self.d = None, None, None, None
        super().__init__(matrix, size)

    @property
    def shape(self):
        return self.size

    def init_matrix(self, matrix):
        if isinstance(matrix, list):
            matrix = npa(matrix)
        if isinstance(matrix, np.ndarray):
            shape = matrix.shape
            assert len(shape) == 2
            m, n = shape
            for i in range(m):
                raw = []
                for j in range(n):
                    if isinstance(matrix[i, j], TrapezoidalFuzzyNumber):
                        item = matrix[i, j]
                    else:
                        raise ParameterError
                    raw.append(item)
                self.matrix.append(raw)
            self.matrix = npa(self.matrix)

            self.a = npa([[self.matrix[i, j].inner_params[0] for j in range(n)] for i in range(m)])
            self.b = npa([[self.matrix[i, j].inner_params[1] for j in range(n)] for i in range(m)])
            self.c = npa([[self.matrix[i, j].inner_params[2] for j in range(n)] for i in range(m)])
            self.d = npa([[self.matrix[i, j].inner_params[3] for j in range(n)] for i in range(m)])

    def level_set(self, gamma=0):
        return gamma * (self.b - self.a) + self.a, self.c - gamma * (self.c - self.d)
