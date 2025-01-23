# -*- coding: utf-8 -*-

import numpy as np

npa = np.array


def rotate_x(theta_x):
    """
    绕x旋转theta_x弧度的旋转矩阵
    :param theta_x:
    :return:
    """
    return npa([[1, 0, 0],
                [0, np.cos(theta_x), -np.sin(theta_x)],
                [0, np.sin(theta_x), np.cos(theta_x)]])


def rotate_y(theta_y):
    """
    绕y旋转theta_y弧度的旋转矩阵
    :param theta_y:
    :return:
    """
    return npa([[np.cos(theta_y), 0, np.sin(theta_y)],
                [0, 1, 0],
                [-np.sin(theta_y), 0, np.cos(theta_y)]])


def rotate_z(theta_z):
    """
    绕z旋转theta_z弧度的旋转矩阵
    :param theta_z:
    :return:
    """
    return npa([[np.cos(theta_z), -np.sin(theta_z), 0],
                [np.sin(theta_z), np.cos(theta_z), 0],
                [0, 0, 1]])
