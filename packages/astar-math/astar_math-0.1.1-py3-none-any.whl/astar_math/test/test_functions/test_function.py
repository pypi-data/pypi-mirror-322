import unittest

import numpy as np

from astar_math.functions import polynomial, fourier, gaussian
from astar_math.functions import Sin

npa = np.array


class TestFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.func = Sin()

    def test_add_number(self):
        a = 1
        res = self.func + a
        y = lambda x: np.sin(x) + 1
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_number_add_function(self):
        a = 1
        res = a + self.func
        y = lambda x: np.sin(x) + 1
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_sub_number(self):
        a = 1
        res = self.func - a
        y = lambda x: np.sin(x) - 1
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_number_sub_function(self):
        a = 1
        res = a - self.func
        y = lambda x: 1 - np.sin(x)
        t = np.linspace(0, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_mul_number(self):
        a = 2.0
        res = self.func * a
        y = lambda x: np.sin(x) * a
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_number_mul_function(self):
        a = 2.0
        res = a * self.func
        y = lambda x: a * np.sin(x)
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_power_positive_number(self):
        a = -2.0
        res = self.func ** a
        y = lambda x: np.sin(x) ** a
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_div_number(self):
        a = 2.0
        res = self.func / a
        y = lambda x: np.sin(x) / a
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))

    def test_number_div_function(self):
        a = 2.0
        res = a / self.func
        y = lambda x: a / np.sin(x)
        t = np.linspace(-10, 10, 100)
        self.assertTrue(np.allclose(res(t), y(t)))


class TestPolynomial(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_functions(self):
        y = polynomial([1, 2], [3, -2, 1])  # x**2-2*x+3
        assert np.isclose(y[0], 2.0) and np.isclose(y[1], 3.0)
        self.assertAlmostEqual(y[0], 2)
        self.assertAlmostEqual(y[1], 3)
        x = npa([1, 2, 3, 4])
        y = fourier(x, [1, 2, 3, 4])  # 1 + 3cos(2x) + 4sin(2x)
        assert np.allclose(y, 1 + 3 * np.cos(2 * x) + 4 * np.sin(2 * x))

        x = npa([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        y = fourier(x, [1, 2, 3, 4, -5, -6])  # 1 + 3cos(2x) + 4sin(2x) - 5cos(2*2x) - 6sin(2*2x)
        assert np.allclose(y, 1 + 3 * np.cos(2 * x) + 4 * np.sin(2 * x) - 5 * np.cos(4 * x) - 6 * np.sin(4 * x))

        x = npa([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        y = gaussian(x, [0.5, 2, 1, 3, 1, 4])  # 0.5 * exp(-((x - 2)) ** 2) + 3 * exp(-((x - 1) / 4) ** 2)
        assert np.allclose(y, 0.5 * np.exp(-(x - 2) ** 2) + 3 * np.exp(-((x - 1) / 4) ** 2))

    def test_maclaurin(self):
        fun = Sin()
        sin0 = fun.maclaurin(4)
        print(sin0)
