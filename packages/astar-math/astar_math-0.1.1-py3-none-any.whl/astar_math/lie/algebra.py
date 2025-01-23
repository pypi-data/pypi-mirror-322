import copy
from abc import ABCMeta
from copy import deepcopy

import numpy as np
from liepack.liepack import LieAlgebra as LiePackAlgebra, so as liepackso, sp as liepacksp, rn as liepackrn

__all__ = [
    'LieAlgebra',
    'so',
    'rn',
    'sp',
    'se',
    'sim'
]

from numpy.random import uniform


class LieAlgebra(LiePackAlgebra, metaclass=ABCMeta):
    def bracket(self, s2: LiePackAlgebra):
        new_obj = deepcopy(self)
        new_obj.set_vector((self @ s2 - s2 @ self).get_vector())
        return new_obj


class so(LieAlgebra, liepackso):
    pass


class sp(LieAlgebra, liepacksp):
    pass


class rn(LieAlgebra, liepackrn):
    pass


class se(LieAlgebra):

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("Required input 'shape' (pos 1) or 'LieAlgebra' (pos 1) not found")

        if isinstance(args[0], LieAlgebra):
            obj = copy.copy(args[0])
            return obj

        if isinstance(args[0], int):
            obj = super(se, cls).__new__(cls, args[0] + 1, **kwargs)
        else:
            raise ValueError("Input 'shape' (pos 1) must be of 'int' type")

        if len(args) > 1:
            if isinstance(args[1], np.ndarray):
                np.copyto(obj, args[1])
            elif isinstance(args[1], list):
                for ii in range(len(args[1])):
                    for jj in range(len(args[1])):
                        obj[ii, jj] = args[1][ii][jj]
        else:
            np.copyto(obj, np.zeros(obj.shape))

        return obj

    def random(self):
        r"""
        Initializes a random element in the Lie algebra.
        """
        v = [uniform(0, 1) for _ in range(self.get_dimension() * 2)]
        self.set_vector(v)

    def get_vector(self):
        return np.hstack((self.rho(), self.phi()))

    def get_dimension(self):
        return int(self.shape[0] - 1)

    def set_vector(self, vector):
        n = self.get_dimension()
        rho = vector[:n]
        phi = vector[n:]
        son = so(n)
        son.set_vector(phi)
        obj = np.zeros((n + 1, n + 1))
        obj[:n, :n] = son
        obj[:n, n] = rho
        np.copyto(self, obj)

    def rho(self):
        n = self.get_dimension()
        return self[:n, n]

    def phi(self):
        n = self.get_dimension()
        son = so(n, self[:n, :n])
        return son.get_vector()


class sim(LieAlgebra):
    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("Required input 'shape' (pos 1) or 'LieAlgebra' (pos 1) not found")

        if isinstance(args[0], LieAlgebra):
            obj = copy.copy(args[0])
            return obj

        if isinstance(args[0], int):
            obj = super(sim, cls).__new__(cls, args[0] + 1, **kwargs)
        else:
            raise ValueError("Input 'shape' (pos 1) must be of 'int' type")

        if len(args) > 1:
            if isinstance(args[1], np.ndarray):
                np.copyto(obj, args[1])
            elif isinstance(args[1], list):
                for ii in range(len(args[1])):
                    for jj in range(len(args[1])):
                        obj[ii, jj] = args[1][ii][jj]
        else:
            np.copyto(obj, np.zeros(obj.shape))

        return obj

    def random(self):
        r"""
        Initializes a random element in the Lie algebra.
        """
        v = [uniform(0, 1) for _ in range(self.get_dimension() * 2 + 1)]
        self.set_vector(v)

    def get_vector(self):
        return np.hstack((self.rho(), self.phi(), self.sigma()))

    def get_dimension(self):
        return int(self.shape[0] - 1)

    def set_vector(self, vector):
        n = self.get_dimension()
        rho = vector[:n]
        phi = vector[n:2 * n]
        sig = vector[2 * n]
        son = so(n)
        son.set_vector(phi)
        obj = np.zeros((n + 1, n + 1))
        obj[:n, :n] = son + sig * np.eye(n)
        obj[:n, n] = rho
        np.copyto(self, obj)

    def rho(self):
        n = self.get_dimension()
        return self[:n, n]

    def phi(self):
        n = self.get_dimension()
        son = so(n, self[:n, :n])
        return son.get_vector()

    def sigma(self):
        return self[0, 0]
