# -*- coding: utf-8 -*-
from abc import abstractmethod
from numbers import Number

import numpy as np
from astartool.error import ParameterError
from skfuzzy import trapmf, gaussmf
from skfuzzy.fuzzymath import fuzzy_mult, fuzzy_sub, fuzzy_add, fuzzy_div

from astar_math.fuzzy.core import FuzzyObject

npa = np.array


class DiscreteFuzzyNumber(FuzzyObject):
    def __init__(self, x, a):
        super().__init__()
        self.x = x
        self.a = a

    def __mul__(self, other):
        if isinstance(other, DiscreteFuzzyNumber):
            return DiscreteFuzzyNumber(*fuzzy_mult(self.x, self.a, other.x, other.a))
        elif isinstance(other, DiscreteFuzzyNumber):
            return DiscreteFuzzyNumber(*fuzzy_mult(self.x, self.a, other, [1]))
        raise ParameterError

    def __sub__(self, other):
        if isinstance(other, DiscreteFuzzyNumber):
            return DiscreteFuzzyNumber(*fuzzy_sub(self.x, self.a, other.x, other.a))
        elif isinstance(other, float):
            return DiscreteFuzzyNumber(*fuzzy_sub(self.x, self.a, other, [1]))
        raise ParameterError

    def __add__(self, other):
        if isinstance(other, DiscreteFuzzyNumber):
            return DiscreteFuzzyNumber(*fuzzy_add(self.x, self.a, other.x, other.a))
        elif isinstance(other, float):
            return DiscreteFuzzyNumber(*fuzzy_add(self.x, self.a, other, [1]))
        raise ParameterError

    def __truediv__(self, other):
        if isinstance(other, DiscreteFuzzyNumber):
            return DiscreteFuzzyNumber(*fuzzy_div(self.x, self.a, other.x, other.a))
        elif isinstance(other, float):
            return DiscreteFuzzyNumber(*fuzzy_div(self.x, self.a, other, [1]))
        raise ParameterError


class ContinuousFuzzyNumber(FuzzyObject):
    def __init__(self, x, membership_function):
        super().__init__()
        self.x = x
        self.membership_function = membership_function
        self.inner_params = None

    @abstractmethod
    def level_set(self, gamma=0):
        assert 0 <= gamma <= 1


class TrapezoidalFuzzyNumber(ContinuousFuzzyNumber):
    """
    梯形模糊数
    """

    def __init__(self, x, a, b, c, d):
        super().__init__(x, lambda k: trapmf(k, (a, b, c, d)))
        self.inner_params = (a, b, c, d)

    def level_set(self, gamma=0):
        super().level_set(gamma)
        return [(gamma * (self.inner_params[1] - self.inner_params[0]) + self.inner_params[0],
                 self.inner_params[2] - gamma * (self.inner_params[2] - self.inner_params[3]))]

    def __add__(self, other):
        if isinstance(other, Number):
            a, b, c, d = self.inner_params
            if self.x is not None:
                return TrapezoidalFuzzyNumber(self.x + other, a + other, b + other, c + other, d + other)
            else:
                return TrapezoidalFuzzyNumber(None, a + other, b + other, c + other, d + other)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Number):
            a, b, c, d = self.inner_params
            if self.x is not None:
                return TrapezoidalFuzzyNumber(self.x + other, a - other, b - other, c - other, d - other)
            else:
                return TrapezoidalFuzzyNumber(None, a - other, b - other, c - other, d - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            a, b, c, d = self.inner_params
            if self.x is not None:
                return TrapezoidalFuzzyNumber(self.x * other, a * other, b * other, c * other, d * other)
            else:
                return TrapezoidalFuzzyNumber(None, a * other, b * other, c * other, d * other)
        return NotImplemented


class TriangularFuzzyNumber(TrapezoidalFuzzyNumber):
    """
    三角形模糊数
    """

    def __init__(self, x, a, b, c):
        super().__init__(x, a, b, c, b)


class GaussianFuzzyNumber(ContinuousFuzzyNumber):
    """
    高斯模糊数
    """

    def __init__(self, x, mean, sigma):
        super().__init__(x, lambda k: gaussmf(k, mean, sigma))
        self.inner_params = (mean, sigma)

    def level_set(self, gamma=0):
        super().level_set(gamma)
        mean, sigma = self.inner_params
        mu = np.sqrt(-np.log(gamma) * (2 * sigma * sigma))
        return [(mu - np.fabs(mean), mu + np.fabs(mean))]
