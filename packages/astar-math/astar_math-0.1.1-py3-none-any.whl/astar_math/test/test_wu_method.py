# -*- coding: utf-8 -*-
import pathlib

import numpy as np

from astar_math.wu_method.core import Polynomial

npa = np.array

power_matrix = [[0, 0, 0, 1, 2, -1],
                [-2, 1.5, -2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
                ]
coefficient_list = [-2, 3.5, -9.7]
names = ["a", "b", "c", "d", "e", "f"]
poly = Polynomial(power_matrix, coefficient_list, names)

print(poly)

a = pathlib.Path(r"D:\astar\aaa")
for p in a.rglob("*[.dat,.DAT]"):
    print(p)
