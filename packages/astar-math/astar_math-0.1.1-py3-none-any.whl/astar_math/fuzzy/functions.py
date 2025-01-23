# -*- coding: utf-8 -*-

import numpy as np

from astar_math.fuzzy.intervals import FuzzyInterval
from astar_math.fuzzy.matrix import TrapezoidalFuzzyMatrix
from astar_math.fuzzy.number import TrapezoidalFuzzyNumber
from astar_math.linear_algebra.matrix import solve_mat

npa = np.array


def solve_fuzzy_matrix(a: TrapezoidalFuzzyMatrix, b: TrapezoidalFuzzyMatrix):
    """
    梯形模糊方程组求解
    :param a: 模糊矩阵
    :param b: 模糊向量
    :return:
    """
    a0_low = a.a
    a0_up = a.c
    a1_low = a.b
    a1_up = a.d
    b0_low = b.a
    b0_up = b.c
    b1_low = b.b
    b1_up = b.d

    f, x0_low_1, x0_low_2 = solve_mat(a0_up, b0_low)
    x0_low = x0_low_1 if f else x0_low_2
    f, x0_up_1, x0_up_2 = solve_mat(a0_low, b0_up)
    x0_up = x0_up_1 if f else x0_up_2
    f, x1_low_1, x1_low_2 = solve_mat(a1_up, b1_low)
    x1_low = x1_low_1 if f else x1_low_2
    f, x1_up_1, x1_up_2 = solve_mat(a1_low, b1_up)
    x1_up = x0_up_1 if f else x0_up_2

    result = TrapezoidalFuzzyMatrix(
        [[TrapezoidalFuzzyNumber(x=None, a=a, b=b, c=c, d=d)] for a, b, d, c in zip(x0_low, x0_up, x1_low, x1_up)])
    return result


def fuzzy_real_system_of_linear_equation(a: np.ndarray, b: (np.ndarray, list)):
    """
    Solution to Fuzzy System of Linear Equations with Crisp Coefficients
    D. Behera & S. Chakraverty
    :param a: m x n 实数矩阵
    :param b: np.array or list
    :return:
    """
    if isinstance(b, list):
        b = npa(b)
    if len(b.shape) == 1:
        b = np.expand_dims(b, axis=1)

    b_mat = np.zeros((len(b), 2))
    if isinstance(b[0][0], FuzzyInterval):
        for i, row in enumerate(b):
            for each in row:
                b_mat[i, :] = each.x
    else:
        b_mat = b
    f, x_add_1, x_add_2 = solve_mat(a, (b_mat[:, 0] + b_mat[:, 1]))
    x_add = x_add_1 if f else x_add_2
    f, x_sub_1, x_sub_2 = solve_mat(np.abs(a), (b_mat[:, 0] - b_mat[:, 1]))
    x_sub = x_sub_1 if f else x_sub_2
    x_low = (x_add + x_sub) / 2
    x_up = (x_add - x_sub) / 2
    return npa([[FuzzyInterval([low, up])] for (low, up) in zip(x_low, x_up)])

# def solve_fuzzy(a: (TrapezoidalFuzzyMatrix, np.ndarray), b: TrapezoidalFuzzyMatrix):
#     for i in range(b.shape[0]):
#         for j in range(b.shape[1]):
#             assert isinstance(b.matrix[i][j], TrapezoidalFuzzyNumber)
#
#     if isinstance(a, TrapezoidalFuzzyMatrix):
#         return solve_fuzzy_a(a, b)
#     elif isinstance(a, np.ndarray):
#         return fuzzy_real_system_of_linear_equation(a, b)
#     else:
#         raise NotImplemented()
