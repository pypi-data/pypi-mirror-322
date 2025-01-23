import numpy as np

from liepack.domain.liealgebras import so

npa = np.array


def skew_symmetric(a: (np.ndarray, list)):
    """
    获取反对称矩阵
    :param a:
    :return: 反对称矩阵
    """
    mat = so(len(a))
    mat.set_vector(a)
    return mat
