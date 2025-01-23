import unittest

import numpy as np

from astar_math.functions import polynomial, fourier, gaussian, Arcsin, Arctan
from astar_math.functions import Arccos

npa = np.array


class TestArccos(unittest.TestCase):
    def setUp(self) -> None:
        self.arccos = Arccos()

    def test_arccos(self):
        y = lambda x: -1 / np.sqrt(1 - x * x)
        diff = self.arccos.derivative()
        t = np.linspace(-1, 1, 100)
        yt = y(t)
        diff_t = diff(t)
        # print("y(t)", yt)
        # print("diff(t)", diff_t)
        self.assertTrue(np.allclose(yt, diff_t))


class TestArcsin(unittest.TestCase):
    def setUp(self) -> None:
        self.arcsin = Arcsin()

    def test_arcsin(self):
        y = lambda x: 1 / np.sqrt(1 - x * x)
        diff = self.arcsin.derivative()
        t = np.linspace(-1, 1, 100)
        yt = y(t)
        diff_t = diff(t)
        # print("y(t)", yt)
        # print("diff(t)", diff_t)
        # print(diff)
        self.assertTrue(np.allclose(yt, diff_t))


class TestArctan(unittest.TestCase):
    def setUp(self) -> None:
        self.arctan = Arctan()

    def test_arctan(self):
        y = lambda x: 1 / (1 + x * x)
        diff = self.arctan.derivative()
        t = np.linspace(-1, 1, 100)
        yt = y(t)
        diff_t = diff(t)
        # print("y(t)", yt)
        # print("diff(t)", diff_t)
        # print(diff)
        self.assertTrue(np.allclose(yt, diff_t))

