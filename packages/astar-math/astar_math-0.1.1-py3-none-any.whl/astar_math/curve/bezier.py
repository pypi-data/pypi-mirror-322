import numpy as np

from astar_math.special import combs


def bezier(ctrl, start, end, n=20):
    """

    :param start: 起始点
    :param end: 终点
    :param ctrl: 控制点
    :param n: 插入点数
    :return: x, y
    """
    len_ctrl = len(ctrl)
    coef = np.repeat([combs(len_ctrl + 2)], 2, axis=0)
    ti = np.linspace(0, 1, n)
    t = np.repeat([ti], len_ctrl + 1, axis=0)
    t_1 = (1 - t)[::-1, :]

    # axis0 表示阶数， 分别表示t的0次幂， 1次幂， ... len_ctrl+2次幂
    # axis1 表示第几个点
    t_star = np.vstack((np.ones(n), np.cumprod(t, axis=0)))
    t_1_star = np.vstack((np.cumprod(t_1, axis=0)[::-1, :], np.ones(n)))

    points = np.vstack((start, ctrl, end))
    res = (t_star * t_1_star).T @ (coef.T * points)
    return res[:, 0], res[:, 1]
