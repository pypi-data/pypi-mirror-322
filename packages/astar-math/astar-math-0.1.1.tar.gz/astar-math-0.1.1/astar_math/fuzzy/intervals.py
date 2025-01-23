# -*- coding: utf-8 -*-

import numpy as np
from skfuzzy.fuzzymath import fuzzy_mult, fuzzy_sub, fuzzy_add, fuzzy_div
from skfuzzy.intervals.intervalops import *

from astar_math.fuzzy.core import FuzzyObject


npa = np.array


class FuzzyInterval(FuzzyObject):
    def __init__(self, x, mf=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x, self.mf = x, mf

    def __getitem__(self, item):
        return self.x[item]

    def __add__(self, other):
        if isinstance(other, FuzzyInterval):
            return FuzzyInterval(addval(self.x, other.x), self.mf)
        raise NotImplemented

    def __sub__(self, other):
        if isinstance(other, FuzzyInterval):
            return FuzzyInterval(subval(self.x, other.x), self.mf)
        raise NotImplemented

    def __mul__(self, other):
        if isinstance(other, FuzzyInterval):
            return FuzzyInterval(multval(self.x, other.x), self.mf)
        raise NotImplemented

    def __truediv__(self, other):
        if isinstance(other, FuzzyInterval):
            return FuzzyInterval(divval(self.x, other.x), self.mf)
        raise NotImplemented
