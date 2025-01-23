import itertools
from abc import ABCMeta
from functools import reduce
from numbers import Number
from typing import Iterable

import numpy as np
from astartool.error import ParameterTypeError
from scipy.special import factorial

from astar_math.functions._intervals import R, ListIntervals, BaseIntervals, IntervalType


class Function:
    def __init__(self, function=None, *, expression='', name='', domain_of_definition=R):
        if function is None:
            self.functions = []
            self.expression = expression
            self.name = name
        elif isinstance(function, Function):
            self.functions = function.functions
            self.expression = function.expression
            self.name = function.name
        elif callable(function):
            self.functions = [function]
            self.expression = expression
            self.name = name
        elif isinstance(function, Iterable):
            self.functions = list(function)
            self.expression = expression
            self.name = name
        else:
            self.functions = [function]
            self.expression = expression
            self.name = name
        self.domain_of_definition = domain_of_definition

    def taylor(self, x0, n=2, eps=1e-10):
        """
        泰勒展开
        :param x0:
        :param n:
        :return:
        """
        res = []
        diff_func = [self]
        poly = Polynomial({1: 1, 0: -x0}, domain_of_definition=self.domain_of_definition)
        poly_item = 1
        for i in range(n):
            diff_func_item = diff_func[-1]
            item = poly_item * (diff_func_item.get(x0) / factorial(i, True))
            poly_item = poly * poly_item
            diff_func_item = diff_func[-1].derivative()
            diff_func.append(diff_func_item)
            res.append(item)
        return sum(res, Polynomial({}, domain_of_definition=self.domain_of_definition))

    def maclaurin(self, n=2, eps=1e-10):
        """
        麦克劳林展开
        :param n:
        :param eps:
        :return:
        """
        return self.taylor(0, n, eps)

    def get(self, x, *args, **kwargs):
        if isinstance(x, (np.ndarray, Number)):
            return reduce(lambda a, b: a + b, map(lambda f: f(x) if callable(f) else f, self.functions))
        elif isinstance(x, Function):
            expression = self.to_string("(" + x.expression + ")")
            return Function([lambda inner_x: self.get(x(inner_x))], expression=expression)
        elif callable(x):
            return Function([lambda inner_x: self.get(x(inner_x))])
        else:
            raise ParameterTypeError("x type error")

    def __call__(self, x, *args, **kwargs):
        return self.get(x, *args, **kwargs)

    def __add__(self, other):
        return self.add(other, inplace=False)

    def __iadd__(self, other):
        return self.add(other, inplace=True)

    def __neg__(self):
        return self.neg(inplace=False)

    def __sub__(self, other):
        return self.sub(other, inplace=False)

    def __isub__(self, other):
        return self.sub(other, inplace=False)

    def __mul__(self, other):
        return self.mul(other, inplace=False)

    def __imul__(self, other):
        return self.mul(other, inplace=True)

    def __truediv__(self, other):
        return self.div(other, inplace=False)

    def __idiv__(self, other):
        return self.div(other, inplace=True)

    def __pow__(self, power, modulo=None):
        return self.pow(power, modulo, inplace=False)

    def __radd__(self, other):
        return self.add(other, inplace=False)

    def __rsub__(self, other):
        return -self.sub(other, inplace=False)

    def __rmul__(self, other):
        return self.mul(other, inplace=False)

    def add(self, other, *, inplace=False):
        if isinstance(other, Number) or callable(other):
            if inplace:
                if isinstance(other, Function):
                    self.functions.extend(other.functions)
                    self.expression = self.expression + "+(" + other.expression + ")"
                elif isinstance(other, Number):
                    if other > 0:
                        self.expression = self.expression + "+{other}".format(other=other)
                    else:
                        self.expression = self.expression + "-{other}".format(other=-other)
                    self.functions.append(other)
                else:
                    self.functions.append(other)
                    self.expression = ""
                return self
            elif isinstance(other, Function):
                if isinstance(other, Function):
                    new_func = self.functions + other.functions
                    expression = self.expression + other.expression
                elif isinstance(other, Number):
                    if other > 0:
                        expression = self.expression + "+{other}".format(other=other)
                    else:
                        expression = self.expression + "-{other}".format(other=-other)
                    new_func = self.functions + [other]
                else:
                    new_func = self.functions + [other]
                    expression = ""
                return Function(new_func, expression=expression)
        else:
            raise ParameterTypeError("错误的数据类型, 加数应该是callable类型或者数字类型")

    def sub(self, other, *, inplace=False):
        if isinstance(other, Number):
            return self.add(-other, inplace=inplace)
        elif isinstance(other, Function):
            return self.add(-other, inplace=inplace)
        elif callable(other):
            return self.add(lambda x: -other(x), inplace=inplace)
        else:
            raise ParameterTypeError("错误的数据类型, 减数应该是callable类型或者数字类型")

    def neg(self, *, inplace=False):
        li = []
        for other in self.functions:
            if isinstance(other, Number):
                li.append(-other)
            elif isinstance(other, Function):
                li.append(-other)
            elif callable(other):
                li.append(lambda x: -other(x))
            else:
                raise ParameterTypeError("错误的数据类型, 负数应该是callable类型或者数字类型")
        if inplace:
            self.functions = li
            self.expression = "-({})".format(self.expression)
            return self
        else:
            return Function(li, expression="-({})".format(self.expression))

    def mul(self, other, *, inplace=False, unfolding='false', max_term=10):
        if isinstance(other, Function):
            if unfolding == 'auto':
                if len(self.functions) * len(other.functions) <= max_term:
                    unfolding = 'true'
                else:
                    unfolding = 'false'
            if unfolding == 'true':
                li = list(map(lambda x, y: x * y, itertools.product(self.functions, other.functions)))
            else:
                li = []
                for each in self.functions:
                    li.append(lambda x: each(x) * other(x) if callable(each) else lambda x: each * other(x))
        elif callable(other):
            li = []
            for each in self.functions:
                li.append(lambda x: each(x) * other(x) if callable(each) else lambda x: each * other(x))
        elif isinstance(other, Number):
            li = []
            for each in self.functions:
                li.append(lambda x: each(x) * other if callable(each) else lambda x: each * other)
        else:
            raise ParameterTypeError("错误的数据类型, 乘数应该是callable类型或者数字类型")

        if inplace:
            self.functions = li
            if isinstance(other, Function):
                self.expression = "({expression})*({other})".format(expression=self.expression, other=other.expression)
            elif isinstance(other, Number):
                self.expression = "({other})*({expression})".format(expression=self.expression, other=other)
            else:
                self.expression = ''
            return self
        else:
            expression = self.expression
            if isinstance(other, Function):
                expression = "({expression})*({other})".format(expression=expression, other=other.expression)
            elif isinstance(other, Number):
                expression = "({other})*({expression})".format(expression=expression, other=other)
            else:
                expression = ''
            return Function(li, expression=expression)

    def pow(self, power, modulo=None, *, inplace=False):
        if inplace:
            self.functions = [lambda x: pow(self.get(x), power, modulo)]
            self.expression = ''
            return self
        else:
            return Function([lambda x: pow(self.get(x), power, modulo)])

    def div(self, other, *, inplace=False):
        if isinstance(other, Function):
            x_1 = other ** (-1)
        elif callable(other):
            x_1 = lambda x: 1 / other(x)
        elif isinstance(other, (np.ndarray, Number)):
            x_1 = 1 / other
        else:
            raise ParameterTypeError("错误的数据类型, 除数应该是callable类型或者数字类型")
        return self.mul(x_1, inplace=inplace)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        functions = []
        for item in self.functions:
            if isinstance(item, Function):
                functions.append(item.derivative(delta_t, eps, inplace=False))
            elif callable(item):
                functions.append(lambda x: (item(x + delta_t) - item(x)) / delta_t)
            elif isinstance(item, (np.ndarray, Number)):
                pass
            else:
                raise ParameterTypeError("错误的数据类型")
        if inplace:
            self.functions = functions
            return self
        else:
            return Function(functions)

    def to_string(self, symbol='x'):
        return self.expression

    def __str__(self):
        return self.to_string('x')

    def __repr__(self):
        return str(self)


class Const(Function):
    def __init__(self, number, *, domain_of_definition=R):
        if callable(number):
            number = number(0)
        super().__init__([number], domain_of_definition=domain_of_definition)
        self.number = number

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Const(0, domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "{}".format(self.number)

    def __str__(self):
        return self.to_string('x')


class Polynomial(Function):
    """
    多项式
    """

    def __init__(self, polynomial=None, coefficient=None, exponent=None, *, domain_of_definition=R):
        """
        coefficient: 系数
        exponent: 指数
        """
        if polynomial is not None:
            if isinstance(polynomial, Polynomial):
                self.polynomial_dict = polynomial.polynomial_dict
            elif isinstance(polynomial, dict):
                self.polynomial_dict = polynomial
            else:
                raise ParameterTypeError("参数类型错误")
        elif coefficient is not None:
            if exponent is not None:
                self.polynomial_dict = dict(zip(exponent, coefficient))
            else:
                self.polynomial_dict = dict(zip(range(len(coefficient)), coefficient))
        else:
            self.polynomial_dict = {}
        super().__init__([self], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    @property
    def coefficient(self):
        return list(self.polynomial_dict.values())

    @property
    def exponent(self):
        return list(self.polynomial_dict.keys())

    def mul(self, other, *, inplace=False, unfolding='false', max_term=10):

        if isinstance(other, Number):
            polynomial_dict = {k: other * v for k, v in self.polynomial_dict.items()}
            if inplace:
                self.polynomial_dict = polynomial_dict
                return self
            else:
                return Polynomial(polynomial_dict, domain_of_definition=self.domain_of_definition)
        elif isinstance(other, Polynomial):
            new_poly = {}
            for (k1, v1), (k2, v2) in itertools.product(self.polynomial_dict.items(), other.polynomial_dict.items()):
                k = k1 + k2
                new_poly[k] = new_poly.get(k, 0) + v1 * v2
            if inplace:
                self.polynomial_dict = new_poly
                return self
            else:
                return Polynomial(new_poly)
        else:
            return super().mul(other, inplace=inplace, unfolding=unfolding, max_term=max_term)

    def diff(self, eps=1e-8):
        """
        导函数
        """
        return Polynomial({k - 1: k * v for k, v in self.polynomial_dict.items() if not (-eps < k < eps)}, domain_of_definition=self.domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return self.diff(eps)

    def get(self, x):
        """
        获得x对应的值
        """
        if isinstance(x, (Number, np.ndarray)):
            y = np.zeros_like(x)
            for k, v in self.polynomial_dict.items():
                y += v * x ** k
            return y
        else:
            return super().get(x)

    def simplify(self, eps=1e-8):
        """
        化简多项式，删去系数为0的项
        :param eps: 判断0的精度
        :return:
        """
        self.polynomial_dict = {k: v for k, v in self.polynomial_dict.items() if not (-eps < v < eps)}

    def __iadd__(self, other):
        if isinstance(other, Polynomial):
            for k, v in other.polynomial_dict.items():
                if k in self.polynomial_dict:
                    self.polynomial_dict[k] += v
                else:
                    self.polynomial_dict[k] = v
        elif isinstance(other, Number):
            if 0 in self.polynomial_dict:
                self.polynomial_dict += other
            else:
                self.polynomial_dict[0] = other

        else:
            raise ParameterTypeError("错误的数据类型")

    def __isub__(self, other):
        if isinstance(other, Polynomial):
            for k, v in other.polynomial_dict.items():
                if k in self.polynomial_dict:
                    self.polynomial_dict[k] -= v
                else:
                    self.polynomial_dict[k] = -v
        elif isinstance(other, Number):
            if 0 in self.polynomial_dict:
                self.polynomial_dict -= other
            else:
                self.polynomial_dict[0] = -other
        else:
            raise ParameterTypeError("错误的数据类型")

    def __add__(self, other):
        poly = self.polynomial_dict.copy()
        if isinstance(other, Polynomial):
            for k, v in other.polynomial_dict.items():
                if k in poly:
                    poly[k] += v
                else:
                    poly[k] = v
        elif isinstance(other, Number):
            if 0 in poly:
                poly[0] += other
            else:
                poly[0] = other
        elif isinstance(other, Function) or callable(other):
            return super().add(other)
        else:
            raise ParameterTypeError("错误的数据类型")
        return Polynomial(poly)

    def __radd__(self, other):
        return self.add(other, inplace=False)

    def __sub__(self, other):
        poly = self.polynomial_dict.copy()
        if isinstance(other, Polynomial):
            for k, v in other.polynomial_dict.items():
                if k in poly:
                    poly[k] -= v
                else:
                    poly[k] = -v
        elif isinstance(other, Number):
            if 0 in poly:
                poly[0] -= other
            else:
                poly[0] = -other
        elif isinstance(other, Function) or callable(other):
            return super().sub(other, inplace=False)
        else:
            raise ParameterTypeError("错误的数据类型")
        return Polynomial(poly)

    def to_string(self, symbol='x'):
        res = [(k, v) for k, v in self.polynomial_dict.items()]
        res.sort()
        s = []
        for p, c in self.polynomial_dict.items():
            if np.isclose(c, 1):
                c_str = '1' if p == 0 else ''
            elif np.isclose(c, -1):
                c_str = '-'
            elif np.isclose(c, 0):
                continue
            else:
                c_str = "{c}".format(c=c)

            if np.isclose(p, 0):
                p_str = ''
            elif np.isclose(p, 1):
                p_str = '{symbol}'.format(symbol=symbol)
            elif p > 0:
                p_str = '{symbol}^{p}'.format(symbol=symbol, p=p)
            else:
                p_str = '{symbol}^({p})'.format(symbol=symbol, p=p)
            s.append(c_str + p_str)

        s_str = '+'.join(s)
        return s_str.replace("+-", "-")

    def __str__(self):
        return self.to_string('x')


class TrigonometricFunction(Function, metaclass=ABCMeta):
    pass


class Sin(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.sin(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Cos(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "sin({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Cos(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.cos(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return -Sin(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "cos({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Tan(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.tan(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Sec(domain_of_definition=self.domain_of_definition) * Sec(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "tan({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Sec(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.sec(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Sec(domain_of_definition=self.domain_of_definition) * Tan(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "sec({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Csc(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.csc(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return -Cot(domain_of_definition=self.domain_of_definition) * Csc(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "csc({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Cot(TrigonometricFunction):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.cot(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Csc(domain_of_definition=self.domain_of_definition) * Csc(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "cot({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Arcsin(Function):
    def __init__(self, *, domain_of_definition=ListIntervals(BaseIntervals([-1, 1], open_or_closed=(IntervalType.Closed, IntervalType.Closed)))):
        super().__init__([lambda x: np.arcsin(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Function(lambda x: 1 / np.sqrt(1 - x * x), domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "arcsin({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Arccos(Function):
    def __init__(self, *, domain_of_definition=ListIntervals(BaseIntervals([-1, 1], open_or_closed=(IntervalType.Closed, IntervalType.Closed)))):
        super().__init__([lambda x: np.arccos(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Function(lambda x: -1 / np.sqrt(1 - x * x), domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "arccos({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Arctan(Function):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.arctan(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Polynomial({-1: 1}, domain_of_definition=self.domain_of_definition).get(Polynomial({2: 1, 0: 1}))

    def to_string(self, symbol='x'):
        return "arctan({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Power(Function):
    def __init__(self, a, *, domain_of_definition=R):
        self.a = a
        super().__init__([lambda x: np.power(a, x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return np.log(self.a) * Power(self.a, domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "{a}^({symbol})".format(a=self.a, symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Exp(Power):
    def __init__(self, *, domain_of_definition=R):
        super(Exp, self).__init__(np.e, domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Exp(domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "exp({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Log(Function):
    def __init__(self, a, *, domain_of_definition=ListIntervals(BaseIntervals([0, np.inf], open_or_closed=(IntervalType.Open, IntervalType.Open)))):
        self.a = a
        super().__init__([lambda x: np.log(x) / np.log(a)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        return Polynomial({-1: np.log(self.a)}, domain_of_definition=self.domain_of_definition)

    def to_string(self, symbol='x'):
        return "log{a}({symbol})".format(a=self.a, symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Ln(Log):
    def __init__(self, *, domain_of_definition=ListIntervals(BaseIntervals([0, np.inf], open_or_closed=(IntervalType.Open, IntervalType.Open)))):
        super().__init__([lambda x: np.log(x)], domain_of_definition=domain_of_definition)

    def to_string(self, symbol='x'):
        return "ln({symbol})".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')


class Abs(Function):
    def __init__(self, *, domain_of_definition=R):
        super().__init__([lambda x: np.abs(x)], expression=self.to_string('x'), domain_of_definition=domain_of_definition)

    def to_string(self, symbol='x'):
        return "|{symbol}|".format(symbol=symbol)

    def __str__(self):
        return self.to_string('x')

    def derivative(self, delta_t=1e-8, eps=1e-10, *args, inplace=False, **kwargs):
        left_set = ListIntervals(BaseIntervals((-np.inf, 0), open_or_closed=(IntervalType.Open, IntervalType.Open)))
        right_set = ListIntervals(BaseIntervals((0, np.inf), open_or_closed=(IntervalType.Open, IntervalType.Open)))
        return Const(-1, domain_of_definition=left_set & self.domain_of_definition) + Const(1, domain_of_definition=right_set & self.domain_of_definition)


self = Polynomial({1: 1})
