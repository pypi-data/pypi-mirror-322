# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import numpy as np
from skfuzzy.fuzzymath import fuzzy_mult, fuzzy_sub, fuzzy_add, fuzzy_div
from skfuzzy.membership import trapmf, trimf, gaussmf
from astartool.error import ParameterError

npa = np.array
npl = np.linalg
npr = np.random


class FuzzyObject(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

