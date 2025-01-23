# -*- coding: utf-8 -*-
import time
import unittest
from unittest import TestCase
import numpy as np
from astartool.number import equals_zero, equals_zero_all
from astar_math.special import combs
from scipy.special import comb
from astar_math.linear_algebra.matrix import solve_mat

npa = np.array


class TestSpecial(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_combs(self):
        # n = 1000
        # print(combs(3))
        # print(combs(4))
        # print(combs(5))
        # assert np.allclose(combs(4), [1, 3, 3, 1])
        # assert np.allclose(combs(5), [1, 4, 6, 4, 1])
        # n = 1030
        # n = 30
        # n = 180000
        n = 1000000
        time_start = time.process_time_ns()
        # res = [comb(n, i) for i in range(n)]
        arange = np.cumsum(np.ones(n)) - 1
        res = comb(n - 1, arange)
        time_end1 = time.process_time_ns()
        res2 = combs(n)
        time_end2 = time.process_time_ns()
        self.assertTrue(np.allclose(res, res2))
        print("time combs is:", time_end2 - time_end1)
        print("time comb is: ", time_end1 - time_start)
        self.assertLessEqual(time_end2 - time_end1, time_end1 - time_start)
