

import unittest


import unittest
import numpy as np
from astartool.number import equals_zero_all

from astar_math.numbers import Complex

npa = np.array


class TestMat(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_complex(self):
        a = Complex([1, 3, 2])
        b = complex(1, 2)
        c = a + b
        self.assertTrue(np.allclose(c.v, [5, 2]))



