# -*- coding: utf-8 -*-

import numpy as np
from astartool.error import ParameterError

npa = np.array


def gaussian(x, params, *args, **kwargs):
    """
    高斯函数
    :param x:
    :param params: 高斯函数参数，要求是 a0, mu0, sigma0, a1, mu1, sigma1, ...格式
    :param args:
    :param kwargs:
    :return:
    """
    x = npa(x)
    params_matrix = npa(params).reshape((-1, 3))
    func = lambda p, q, z: p * np.exp(-((x - q) / z) ** 2)
    return sum(map(func, params_matrix[:, 0], params_matrix[:, 1], params_matrix[:, 2]))


def polynomial(x, params, *args, **kwargs):
    """
    多项式函数
    :param x:
    :param params: 指数从0开始，params有多少个值，最高次幂就是几
    :return:
    """
    y = 0
    x = npa(x)
    params = params[::-1]
    for k in params:
        y = y * x + k
    return y


def fourier(x, params, *args, **kwargs):
    """
    傅里叶函数
    :param x:
    :param params: a0, w, a1, b1, a2, b2, ...
    :param args:
    :param kwargs:
    :return:
    """
    if len(params) % 2:
        raise ParameterError("参数应该是偶数个")
    x = npa(x).reshape((1, -1))
    a0 = params[0]
    w = params[1]
    a = params[2::2]
    b = params[3::2]
    alpha = np.cumsum(np.ones_like(a)).reshape((-1, 1))
    t = (w * alpha) @ x
    res = a0 + a @ np.cos(t) + b @ np.sin(t)
    return res


if __name__ == '__main__':
    y = polynomial([1, 2], [3, -2, 1])  # x**2-2*x+3
    assert np.isclose(y[0], 2.0) and np.isclose(y[1], 3.0)

    x = npa([1, 2, 3, 4])
    y = fourier(x, [1, 2, 3, 4])  # 1 + 3cos(2x) + 4sin(2x)

    assert np.allclose(y, 1 + 3 * np.cos(2 * x) + 4 * np.sin(2 * x))

    x = npa([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    y = fourier(x, [1, 2, 3, 4, -5, -6])  # 1 + 3cos(2x) + 4sin(2x) - 5cos(2*2x) - 6sin(2*2x)
    assert np.allclose(y, 1 + 3 * np.cos(2 * x) + 4 * np.sin(2 * x) - 5 * np.cos(4 * x) - 6 * np.sin(4 * x))

    x = npa([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    y = gaussian(x, [0.5, 2, 1, 3, 1, 4])  # 0.5 * exp(-((x - 2)) ** 2) + 3 * exp(-((x - 1) / 4) ** 2)
    assert np.allclose(y, 0.5 * np.exp(-(x - 2) ** 2) + 3 * np.exp(-((x - 1) / 4) ** 2))


