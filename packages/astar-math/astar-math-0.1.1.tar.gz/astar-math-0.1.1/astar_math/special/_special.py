from astartool.error import ParameterValueError
import numpy as np
from functools import reduce

from scipy.special import comb

npa = np.array


def combs(n):
    """
    获取贾宪三角第n行
    :param n: 行号
    :return:
    """
    if n <= 0:
        raise ParameterValueError("param n must > 0")
    elif n <= 2:
        return np.ones(n)
    else:
        mid = (n + 1) // 2
        arange = np.cumsum(np.ones(mid)) - 1
        res = np.empty(n)
        res[:mid] = comb(n-1, arange)
        res[-mid:] = res[mid - 1::-1]
        return res
