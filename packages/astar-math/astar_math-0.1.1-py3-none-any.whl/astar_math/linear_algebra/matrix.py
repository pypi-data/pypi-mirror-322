# -*- coding: utf-8 -*-

import numpy as np
from numpy.linalg import matrix_rank
from scipy.linalg import pinv, inv, lu


__author__ = 'A.Star'


def solve_mat(a: np.ndarray, b: np.ndarray):
    """
    求解ax=b
    :param a:
    :param b:
    :return:
    flag:是否为齐次线性方程组, 若是：
        result1: 表示非0解基础解系，若len=0,则无非0解
        result2: 表示0解，若无，表示无解
    """
    size_x, size_y = a.shape
    if len(b.shape) == 1:
        vector_b = np.expand_dims(b, 1)
    else:
        vector_b = b
    assert size_x == vector_b.shape[0]
    rank_a = matrix_rank(a)
    if np.allclose(b, 0):
        # 齐次线性方程组
        if rank_a < size_y:
            # 存在无穷解
            A_mat = a
            index = np.argmax(~np.isclose(A_mat, 0), axis=1)
            pivot_variable = np.ones(size_y, dtype=bool)
            pivot_variable[index] = False
            free_variable = ~pivot_variable
            free_variable_index = np.where(free_variable)[0]
            fai = np.empty((size_y, size_y - rank_a))
            for i, free_ind in enumerate(free_variable_index):
                fai_i = np.zeros((size_y, 1))
                fai_i[free_ind, 0] = 1
                fai_i[pivot_variable, :1] = inv(A_mat[:rank_a, pivot_variable]) @ (
                    -A_mat[:rank_a, free_ind:free_ind + 1])
                fai[:, i] = fai_i[:, 0]
            return True, fai, np.zeros((size_y, 1))
        else:
            # 仅仅存在0解
            return True, np.empty((size_y, 0)), np.zeros((size_y, 1))
    else:
        # 非齐次线性方程组
        extend_a = np.hstack((a, vector_b))
        rank_ex = matrix_rank(extend_a)
        if rank_a < rank_ex:
            # 无解
            return False, np.empty((size_y, 0)), np.empty((size_y, 0))
        elif rank_a == size_x:
            # 存在1解
            P, L, U = lu(extend_a)
            A_mat = U[:rank_ex, :-1]
            b_mat = U[:rank_ex, -1:]
            index = np.argmax(~np.isclose(A_mat, 0), axis=1)
            pivot_variable = np.zeros(size_y, dtype=bool)
            pivot_variable[index] = True

            fai_star = np.zeros((size_y, 1))
            fai_star[pivot_variable, :1] = inv(A_mat[:rank_a, pivot_variable]) @ b_mat
            fai = np.empty((size_y, 0))
            return False, fai, fai_star
        else:
            # 存在多解
            P, L, U = lu(extend_a)
            A_mat = U[:rank_ex, :-1]
            b_mat = U[:rank_ex, -1:]
            index = np.argmax(~np.isclose(A_mat, 0), axis=1)
            pivot_variable = np.zeros(size_y, dtype=bool)
            pivot_variable[index] = True
            free_variable = ~pivot_variable
            fai_star = np.zeros((size_y, 1))
            fai_star[pivot_variable, :1] = pinv(A_mat[:, pivot_variable]) @ b_mat
            free_variable_index = np.where(free_variable)[0]
            fai = np.zeros((size_y, size_y - rank_a))
            for i, free_ind in enumerate(free_variable_index):
                fai_i = np.zeros((size_y, 1))
                fai_i[free_ind, 0] = 1
                fai_i[pivot_variable, :1] = inv(A_mat[:rank_a, pivot_variable]) @ (
                    -A_mat[:rank_a, free_ind:free_ind + 1])
                fai[:, i] = fai_i[:, 0]
            return False, fai, fai_star
