import types

from astartool.error import ParameterValueError, MethodNotFoundError

__all__ = [
    'solve_nonlinear_equations'
]


def solve_nonlinear_equations(callback, x0=None, method: (str, types.FunctionType) = 'fsolve', *args, **kwargs):
    """
    求解非线性方程
    :param callback: 回调函数
    :param x0: 初值
    :param method: 计算方法, 默认调用fsolve计算
    :param args:
    :param kwargs:
    :return:
    """
    if x0 is None:
        raise ParameterValueError("param `x0` error, x0 must be given by user")
    if isinstance(method, str):
        if method.lower() == 'fsolve':
            from scipy.optimize import fsolve
            return fsolve(callback, x0, *args, **kwargs)
    elif callable(method):
        return method(callback, x0, *args, **kwargs)
    raise MethodNotFoundError("method is not Found")

