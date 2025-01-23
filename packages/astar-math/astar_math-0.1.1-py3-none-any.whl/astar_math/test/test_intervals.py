import unittest

import numpy as np

from astar_math.functions import Intervals, ListIntervals, ContinuousBaseIntervals, IntervalType, DiscreteBaseIntervals
from astar_math.functions import R, Z, N, EMPTY

npa = np.array


class TestIntervals(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        super().setUp()

    def test_equals(self):
        assert R == ListIntervals(ContinuousBaseIntervals((-np.inf, np.inf), (IntervalType.Open, IntervalType.Open)))
        assert Z == ListIntervals(DiscreteBaseIntervals((-np.inf, np.inf), (IntervalType.Open, IntervalType.Open)))
        assert N == ListIntervals(DiscreteBaseIntervals((0, np.inf), (IntervalType.Closed, IntervalType.Open)))

    def test_empty(self):
        assert ListIntervals(DiscreteBaseIntervals(values=[])).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((0, 0))).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((0.5, 0.5))).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((0.5, 0.5), open_or_closed=(IntervalType.Closed, IntervalType.Open))).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((0.5, 0.5), open_or_closed=(IntervalType.Open, IntervalType.Closed))).is_empty()
        assert not ListIntervals(ContinuousBaseIntervals((0.5, 0.5), open_or_closed=(IntervalType.Closed, IntervalType.Closed))).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((-np.inf, -np.inf))).is_empty()
        assert ListIntervals(ContinuousBaseIntervals((np.inf, np.inf))).is_empty()

    def test_union(self):
        S12 = ListIntervals(DiscreteBaseIntervals(values=[1, 2]))
        S1234 = ListIntervals(DiscreteBaseIntervals(values=[1, 2, 3, 4]))
        S345 = ListIntervals(DiscreteBaseIntervals(values=[3, 4, 5]))
        S12345 = ListIntervals(DiscreteBaseIntervals(values=[1, 2, 3, 4, 5]))
        Sinf_1 = ListIntervals(DiscreteBaseIntervals((-np.inf, 1), open_or_closed=(IntervalType.Open, IntervalType.Closed)))
        S1_inf = ListIntervals(DiscreteBaseIntervals((1, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        S0_inf = ListIntervals(DiscreteBaseIntervals((0, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))

        assert S12 | S1234 == S1234
        assert S12 | S345 == S12345

        # TODO
        # assert (ListIntervals(DiscreteBaseIntervals(values=[])).union(Z)) == Z
        # assert (ListIntervals(DiscreteBaseIntervals(values=[1, 2])).union(Z)) == Z
        # assert (ListIntervals(DiscreteBaseIntervals(values=[0, np.inf])).union(Z)) == Z
        # assert (ListIntervals(DiscreteBaseIntervals(values=[1, 2], open_or_closed=[IntervalType.Open, IntervalType.Open])).union(Z)) == Z
        # assert S0_inf | Sinf_1 == Z
        # assert  Sinf_1 | S0_inf == Z
        # assert  S0_inf | S1_inf == S0_inf
        # assert S0_inf | S1_inf == S0_inf

        CS12 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 2], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS1234 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 4], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS345 = ListIntervals(ContinuousBaseIntervals(boundary=[3, 5], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS2345 = ListIntervals(ContinuousBaseIntervals(boundary=[2, 5], open_or_closed=[IntervalType.Open, IntervalType.Closed]))
        CS12345 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 5], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CSinf_1 = ListIntervals(ContinuousBaseIntervals((-np.inf, 1), open_or_closed=(IntervalType.Open, IntervalType.Closed)))
        CS1_inf = ListIntervals(ContinuousBaseIntervals((1, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        CS0_inf = ListIntervals(ContinuousBaseIntervals((0, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        assert R | EMPTY == R
        assert CS0_inf | CSinf_1 == R
        assert CSinf_1 | CS0_inf == R
        assert CS0_inf | CS1_inf == CS0_inf
        assert CS0_inf | CS1_inf == CS0_inf
        assert CS12 | CS1234 == CS1234
        assert CS12 | CS345 == ListIntervals(CS12.intervals + CS345.intervals)
        assert CS12 | CS2345 == CS12345

    def test_intersection(self):
        S12 = ListIntervals(DiscreteBaseIntervals(values=[1, 2]))
        S1234 = ListIntervals(DiscreteBaseIntervals(values=[1, 2, 3, 4]))
        S345 = ListIntervals(DiscreteBaseIntervals(values=[3, 4, 5]))
        S12345 = ListIntervals(DiscreteBaseIntervals(values=[1, 2, 3, 4, 5]))
        Sinf_1 = ListIntervals(DiscreteBaseIntervals((-np.inf, 1), open_or_closed=(IntervalType.Open, IntervalType.Closed)))
        S1_inf = ListIntervals(DiscreteBaseIntervals((1, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        S0_inf = ListIntervals(DiscreteBaseIntervals((0, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        S01 = ListIntervals(DiscreteBaseIntervals((0, 1), open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        assert S12 & S1234 == S12
        assert S12 & S345 == EMPTY

        assert (ListIntervals(DiscreteBaseIntervals(values=[])).intersection(Z)) == EMPTY
        assert S12.intersection(Z) == S12
        assert S0_inf.intersection(Z) == S0_inf

        assert S0_inf & Sinf_1 == S01
        assert Sinf_1 & S0_inf == S01
        assert S0_inf & S1_inf == S1_inf
        assert S1_inf & S0_inf == S1_inf

        CS12 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 2], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS1234 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 4], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS345 = ListIntervals(ContinuousBaseIntervals(boundary=[3, 5], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CS2345 = ListIntervals(ContinuousBaseIntervals(boundary=[2, 5], open_or_closed=[IntervalType.Open, IntervalType.Closed]))
        CS12345 = ListIntervals(ContinuousBaseIntervals(boundary=[1, 5], open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        CSinf_1 = ListIntervals(ContinuousBaseIntervals((-np.inf, 1), open_or_closed=(IntervalType.Open, IntervalType.Closed)))
        CS1_inf = ListIntervals(ContinuousBaseIntervals((1, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        CS0_inf = ListIntervals(ContinuousBaseIntervals((0, np.inf), open_or_closed=(IntervalType.Closed, IntervalType.Open)))
        CS01 = ListIntervals(ContinuousBaseIntervals((0, 1), open_or_closed=[IntervalType.Closed, IntervalType.Closed]))
        assert R & EMPTY == EMPTY
        assert CS0_inf & CSinf_1 == CS01
        assert CSinf_1 & CS0_inf == CS01
        assert CS0_inf & CS1_inf == CS1_inf
        assert CS1_inf & CS0_inf == CS1_inf
        assert CS12 & CS1234 == CS12
        assert CS12 & CS345 == EMPTY
        assert CS12 & CS2345 == EMPTY
