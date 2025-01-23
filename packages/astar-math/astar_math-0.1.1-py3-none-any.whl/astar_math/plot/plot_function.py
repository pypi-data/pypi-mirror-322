# -*- coding: utf-8 -*-

import numpy as np
from astartool.error import ParameterError
from matplotlib import pylab as plt

from astar_math.functions import Function

npa = np.array


def plot_function(function: Function, interval, points=10, *args, handle=plt, **kwargs):
    """
    绘制多项式
    :param function: 多项式对象
    :param interval: 绘制的区间（左右均为闭区间）
    :param points: 绘制的点数
    :param args: matplotlib参数
    :param handle: 绘图句柄
    :param kwargs: matplotlib参数
    :return:
    """
    x = np.linspace(interval[0], interval[1], points)
    if isinstance(function, Function):
        function = function
    elif callable(function):
        function = Function(function)
    else:
        raise ParameterError
    res = handle.plot(x, function(x), *args, **kwargs)
    return res
