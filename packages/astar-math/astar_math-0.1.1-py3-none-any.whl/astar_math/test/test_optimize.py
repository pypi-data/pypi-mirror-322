# -*- coding: utf-8 -*-
import time
import unittest
from unittest import TestCase
import numpy as np
from scipy.optimize import fsolve

from astar_math.optimize import solve_nonlinear_equations

npa = np.array


def f(X):
    x = X[0]
    y = X[1]
    return [x ** 2 / 4 + y ** 2 - 1,
            (x - 0.2) ** 2 - y - 3]


class TestSpecial(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_solve_nonlinear_equations_str(self):
        result = solve_nonlinear_equations(f, [0, 0])
        self.assertTrue(np.allclose(f(result), np.zeros_like(result)))
        print(result)

    def test_solve_nonlinear_equations_func(self):
        result = solve_nonlinear_equations(f, [0, 0], fsolve)
        self.assertTrue(np.allclose(f(result), np.zeros_like(result)))
        print(result)
