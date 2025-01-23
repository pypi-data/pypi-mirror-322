# -*- coding: utf-8 -*-

from astar_math.linear_algebra.matrix import solve_mat
import numpy as np


def random_matrix(shape, axis=None, equal_number=None):
    """
    根据约束生成矩阵
    :param shape:
    :param axis:
    :param equal_number:
    :return:
    """
    if isinstance(shape, int):
        shape = (shape, shape)
    assert len(shape) == 2
    if equal_number is None:
        return np.random.random(shape)
    if axis is None:
        if isinstance(equal_number, (int, float)):
            equal_number = np.repeat(equal_number, shape[0] + shape[1])
        else:
            assert len(equal_number) == shape[0] + shape[1]

        mat_h = np.zeros((shape[0], shape[0] * shape[1]))
        mat_v = np.zeros((shape[0], shape[0] * shape[1]))
        for i in range(shape[0]):
            mat_h[i, i * shape[1]:i * shape[1] + shape[1]] = np.ones(shape[1])

        for i in range(shape[0]):
            mat_v[i, i::shape[1]] = np.ones(shape[0])

        mat = np.vstack((mat_v, mat_h))
        _, fai, fai_star = solve_mat(mat, equal_number)
        fai[np.allclose(fai, 0)] = 0
        fai_star[np.allclose(fai_star, 0)] = 0
        random = np.random.randint(-30, 30, size=(fai.shape[1], 1))
        new_mat = np.reshape(fai @ random + fai_star, shape)
        return new_mat
    elif axis == 0:
        if isinstance(equal_number, (int, float)):
            equal_number = np.repeat(equal_number, shape[0])
        else:
            assert len(equal_number) == shape[0]
        mat = np.zeros((shape[0] * shape[1], shape[0]))
        for i in range(shape[0]):
            mat[i, i * shape[1]:i * shape[1] + shape[1]] = np.ones(shape[1])
        _, fai, fai_star = solve_mat(mat, equal_number)
        fai[np.allclose(fai, 0)] = 0
        fai_star[np.allclose(fai_star, 0)] = 0
        random = np.random.randint(-30, 30, size=(fai.shape[1], 1))
        new_mat = np.reshape(fai @ random + fai_star, shape)
        return new_mat
    elif axis == 1:
        if isinstance(equal_number, (int, float)):
            equal_number = np.repeat(equal_number, shape[1])
        else:
            assert len(equal_number) == shape[1]
        mat = np.zeros((shape[0] * shape[1], shape[0]))
        for i in range(shape[0]):
            mat[i, i::shape[1]] = np.ones(shape[0])
        _, fai, fai_star = solve_mat(mat, equal_number)
        fai[np.allclose(fai, 0)] = 0
        fai_star[np.allclose(fai_star, 0)] = 0
        random = np.random.randint(-30, 30, size=(fai.shape[1], 1))
        new_mat = np.reshape(fai @ random + fai_star, shape)
        return new_mat
