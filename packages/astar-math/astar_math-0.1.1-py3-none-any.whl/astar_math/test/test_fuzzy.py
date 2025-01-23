# -*- coding: utf-8 -*-

import numpy as np
from astar_math.fuzzy.core import FuzzyObject
from astar_math.fuzzy.intervals import FuzzyInterval
from astar_math.fuzzy.functions import fuzzy_real_system_of_linear_equation
import unittest

npa = np.array


class RealSystemOfLinearEquation(unittest.TestCase):
    def test_a(self):
        """
        Solution to Fuzzy System of Linear Equations with Crisp Coefficients
        D. Behera & S. Chakraverty
        Ex 1:
        x1 − x2 = [α, 2−α],
        x1 + 3x2 = [4 + α, 7 − 2α].

        x1 = [11/8+5a/8, 23/8-7a/8]
        x2 = [7/8+a/8, 11/8-3a/8]
        :return:
        """
        a = npa([[1, -1], [1, 3]])
        x1 = []
        x2 = []
        alpha_array = np.linspace(0, 1, 11)
        for alpha in alpha_array:
            b = [[alpha, 2 - alpha], [4 + alpha, 7 - 2 * alpha]]
            x = fuzzy_real_system_of_linear_equation(a, b)
            x1.append(x[0][0])
            x2.append(x[1][0])
            assert np.allclose(x1[-1].x, [[11 / 8 + 5 * alpha / 8], [23 / 8 - 7 * alpha / 8]])
            assert np.allclose(x2[-1].x, [[7 / 8 + alpha / 8], [11 / 8 - 3 * alpha / 8]])
