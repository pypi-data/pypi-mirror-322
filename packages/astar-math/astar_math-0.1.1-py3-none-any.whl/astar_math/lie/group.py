import copy
from abc import ABCMeta

import numpy as np

from liepack.liepack import RN as LiePackRN, SO as LiePackSO, SP as LiePackSP, LieGroup as LiePackGroup

__all__ = [
    'LieGroup',
    'RN',
    'SO',
    'SP',
    'SE',
    'SIM'
]


class LieGroup(LiePackGroup, metaclass=ABCMeta):
    pass


class RN(LieGroup, LiePackRN):
    pass


class SO(LieGroup, LiePackSO):
    pass


class SP(LieGroup, LiePackSP):
    pass


class SE(LieGroup):
    abelian = False

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("Required input 'shape' (pos 1) or 'LieGroup' (pos 1) not found")

        if isinstance(args[0], LieGroup):
            obj = copy.copy(args[0])
            return obj

        if isinstance(args[0], int):
            obj = super(LieGroup, cls).__new__(cls, args[0] + 1, **kwargs)
            shape = args[0] + 1
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
            np.copyto(obj, np.eye(shape))
        return obj

    def Identity(self):
        from astar_math.lie.lie import group2algebra, exp
        g = group2algebra(self)(self.get_dimension())
        np.copyto(self, exp(g))

    def random(self):
        from astar_math.lie.lie import group2algebra, exp
        g = group2algebra(self)(self.get_dimension())
        g.random()
        np.copyto(self, exp(g))

    def get_dimension(self):
        return int(self.shape[0] - 1)


class SIM(LieGroup):
    abelian = False

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("Required input 'shape' (pos 1) or 'LieGroup' (pos 1) not found")

        if isinstance(args[0], LieGroup):
            obj = copy.copy(args[0])
            return obj

        if isinstance(args[0], int):
            obj = super(LieGroup, cls).__new__(cls, args[0] + 1, **kwargs)
            shape = args[0] + 1
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
            np.copyto(obj, np.eye(shape))
        return obj

    def Identity(self):
        from astar_math.lie.lie import group2algebra, exp
        g = group2algebra(self)(self.get_dimension())
        np.copyto(self, exp(g))

    def random(self):
        from astar_math.lie.lie import group2algebra, exp
        g = group2algebra(self)(self.get_dimension())
        g.random()
        np.copyto(self, exp(g))

    def get_dimension(self):
        return int(self.shape[0] - 1)
