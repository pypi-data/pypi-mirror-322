from liepack.liepack import exp as liepack_exp
from liepack.liepack import *

from astar_math.lie.algebra import *
from astar_math.lie.group import *


def algebra2group(g):
    r"""
    Returns the Lie group corresponding to an input Lie algebra element.

    :param g: An element of Lie algebra :math:`\mathfrak{g}`.
    :return: :math:`\mathfrak{g}`'s group, :math:`G`.
    """
    if isinstance(g, rn):
        return RN
    if isinstance(g, so):
        return SO
    if isinstance(g, sp):
        return SP
    if isinstance(g, se):
        return SE
    if isinstance(g, sim):
        return SIM
    if isinstance(g, LieAlgebra):
        return LieGroup


def group2algebra(G):
    r"""
    Returns the Lie algebra corresponding to an input Lie group element.

    :param G: An element of Lie group :math:`G`.
    :return: :math:`G`'s algebra, :math:`\mathfrak{g}`.
    """
    if isinstance(G, RN):
        return rn
    if isinstance(G, SO):
        return so
    if isinstance(G, SP):
        return sp
    if isinstance(G, SE):
        return se
    if isinstance(G, SIM):
        return sim
    if isinstance(G, LieGroup):
        return LieAlgebra


def bch(X: LieAlgebra, Y: LieAlgebra, k=1):
    # BCH公式
    # https://www.zhihu.com/question/529656229
    assert k in (1, 2)
    d1 = X.bracket(Y)
    res = X + Y
    if k == 1:
        res += 0.5 * d1
    elif k == 2:
        d2 = (X + d1 / 6.0).bracket(Y)
        d3 = X.bracket(-2 * d1 / 3 + d2)
        res += 0.5 * d2 + 0.25 * d3
    return res
