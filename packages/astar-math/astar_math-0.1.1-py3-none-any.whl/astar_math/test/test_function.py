import unittest

import numpy as np

from astar_math.functions import polynomial, fourier, gaussian
from astar_math.functions import Sin

npa = np.array


class TestFunction(unittest.TestCase):
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
