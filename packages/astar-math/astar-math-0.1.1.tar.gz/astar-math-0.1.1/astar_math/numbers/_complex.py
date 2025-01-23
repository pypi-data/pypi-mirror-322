import numbers
from typing import Iterable

import numpy as np
from astartool.error import ParameterTypeError, ParameterValueError

from astar_math.lie.matrix import skew_symmetric

npa = np.array


class Complex:
    def __init__(self, number=None, dim=None, s=None, v=None, *, dtype=None):
        if number is not None:
            if isinstance(number, Complex):
                self._complex = number._complex
            elif isinstance(number, Iterable):
                self._complex = npa(list(number), dtype=dtype)
            elif isinstance(number, (np.complex128, complex)):
                self._complex = npa([number.real, number.imag], dtype=dtype)
            elif isinstance(number, numbers.Number):
                self._complex = npa([number], dtype=dtype)
            else:
                raise ParameterTypeError('error type: complex')
        elif s is not None and v is not None:
            self._complex = np.zeros(len(v) + 1, dtype=dtype)
            self._complex[0] = s
            self._complex[1:] = v
        else:
            self._complex = npa([0, 0])

        if dim is None:
            self.dim = len(self._complex)
        else:
            self.dim = dim
            len_complex = len(self._complex)
            if len_complex < self.dim:
                self._complex = np.hstack((self._complex, [0] * (self.dim - len_complex)))
            elif len_complex > dim:
                raise ParameterValueError('error value: dim. dim > length of complex')

    def __add__(self, other):
        """
        四元数加法
        :param other:
        :return:
        """
        if isinstance(other, Complex):
            q = other
        elif isinstance(other, (list, np.ndarray, numbers.Number, complex, np.complex128)):
            q = Complex(other, dim=self.dim)
        else:
            raise ParameterTypeError("parameter error")

        return Complex(self._complex + q._complex)

    def __sub__(self, other):
        """
        四元数减法
        :param other:
        :return:
        """
        if isinstance(other, Complex):
            q = other
        elif isinstance(other, (list, np.ndarray, numbers.Number, complex, np.complex128)):
            q = Complex(other, dim=self.dim)
        else:
            raise ParameterTypeError("parameter error")

        return Complex(self._complex - q._complex)

    def __mul__(self, other):
        """
        四元数乘法
        :param other:
        :return:
        """
        if isinstance(other, Complex):
            m = other
        elif isinstance(other, (list, np.ndarray)):
            m = Complex(other)
        else:
            raise ParameterTypeError("parameter error")
        return Complex(s=self.s * m.s - self.v.dot(m.v),
                       v=self.s * m.v + m.s * self.v + skew_symmetric(self.v) @ m.v)

    @property
    def s(self):
        return self._complex[0]

    @property
    def v(self):
        return self._complex[1:]
