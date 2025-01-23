# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import numpy as np
from astartool.number import equals_zero, equals_zero_all
from numpy.linalg import inv

from astar_math.linear_algebra.matrix import solve_mat

npa = np.array


class TestMat(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def run_solve(self, a, b):
        return solve_mat(a, b)

    def test_square(self):
        a = npa([[1]])
        b = npa(([2]))
        _, base, vec = self.run_solve(a, b)
        # print(base)
        # print(vec)
        self.assertEqual(base.shape, (1, 0))
        self.assertEqual(vec, npa([[2]]))

    def test_square2(self):
        """
        非齐次线性方程组r==n
        :return:
        """
        a = npa([[1, 1], [0, 1]])
        b = npa(([[0], [1]]))
        _, base, vec = self.run_solve(a, b)
        # print(base)
        # print(vec)
        # print(inv(a).dot(b))
        self.assertEqual(base.shape, (2, 0))
        self.assertTrue(np.allclose(vec, npa([[-1], [1]])))

    def test_square2_0(self):
        """
        齐次线性方程组r==n
        :return:
        """
        a = npa([[1, 1], [0, 1]])
        b = npa(([[0], [0]]))
        _, base, vec = self.run_solve(a, b)
        self.assertEquals(base.shape, (2, 0))
        self.assertTrue(np.allclose(vec, npa([[0], [0]])))

    def test_square2_1(self):
        """
        齐次线性方程组r<n
        :return:
        """
        a = npa([[1, 1], [0, 0]])
        b = npa(([[0], [0]]))
        _, base, vec = self.run_solve(a, b)
        # print(base)
        self.assertEquals(base.shape, (2, 1))
        self.assertTrue(np.isclose(base[0, 0] + base[1, 0], 0))

    def test_zhihudemo(self):
        A = np.array([[1, 2, -1, 3], [2, 4, -2, 5], [-1, -2, 1, -1]])
        b = np.array([2, 1, 4])
        _, base, vec = self.run_solve(A, b)
        self.assertTrue(np.allclose(base, np.array([[-2, 1, 0, 0], [1, 0, 1, 0]]).T))
        self.assertTrue(np.allclose(vec, np.array([[-7, 0, 0, 3]]).T))

    def test_homogeneous_linear_equations(self):
        A = npa([[4.11466e+05, 2.22534e+05, 6.34000e+02, 1.06436e+05, 5.75640e+04,
                  1.64000e+02, 6.49000e+02, 3.51000e+02, 1.00000e+00],
                 [3.72036e+05, 2.67890e+05, 6.02000e+02, 1.58826e+05, 1.14365e+05,
                  2.57000e+02, 6.18000e+02, 4.45000e+02, 1.00000e+00],
                 [2.90820e+05, 2.81912e+05, 5.24000e+02, 1.94805e+05, 1.88838e+05,
                  3.51000e+02, 5.55000e+02, 5.38000e+02, 1.00000e+00],
                 [2.12742e+05, 2.67600e+05, 4.46000e+02, 1.97001e+05, 2.47800e+05,
                  4.13000e+02, 4.77000e+02, 6.00000e+02, 1.00000e+00],
                 [1.52817e+05, 2.47801e+05, 3.83000e+02, 1.83540e+05, 2.97620e+05,
                  4.60000e+02, 3.99000e+02, 6.47000e+02, 1.00000e+00],
                 [1.91780e+05, 1.30720e+05, 4.30000e+02, 5.21820e+04, 3.55680e+04,
                  1.17000e+02, 4.46000e+02, 3.04000e+02, 1.00000e+00],
                 [1.17936e+05, 9.67680e+04, 3.36000e+02, 4.10670e+04, 3.36960e+04,
                  1.17000e+02, 3.51000e+02, 2.88000e+02, 1.00000e+00],
                 [7.88970e+04, 7.86240e+04, 2.73000e+02, 3.38130e+04, 3.36960e+04,
                  1.17000e+02, 2.89000e+02, 2.88000e+02, 1.00000e+00]])
        b = np.zeros(8)
        _, base, vec = self.run_solve(A, b)
        self.assertTrue(equals_zero_all(A @ (base + vec), 1E-8))
