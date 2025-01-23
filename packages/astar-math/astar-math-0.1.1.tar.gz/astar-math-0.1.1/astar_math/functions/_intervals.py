import itertools
import numbers
from abc import ABCMeta, abstractmethod
from typing import Iterable, List

import numpy as np
from astartool.error import ParameterTypeError

npa = np.array

__all__ = [
    'BaseIntervals',
    'Intervals',
    'IntervalType',
    'ListIntervals',
    'DiscreteBaseIntervals',
    'ContinuousBaseIntervals',
    'R',
    'Z',
    'N',
    'EMPTY'
]


class IntervalType:
    Discrete = 1
    Continuous = 2
    Open = 3
    Closed = 4


class BaseIntervals:
    def __init__(self, boundary=None, continuous=True, open_or_closed=(IntervalType.Closed, IntervalType.Open), values=None):
        if boundary is None:
            boundary = np.empty(0)
        if isinstance(boundary, (list, tuple)):
            boundary = npa(boundary)
        if isinstance(boundary, np.ndarray):
            len_boundary = len(boundary)
            assert len_boundary in {0, 2}
            if len_boundary == 2:
                assert boundary[1] >= boundary[0]
            self.boundary = boundary

        self.discrete_or_continuous = IntervalType.Continuous if continuous else IntervalType.Discrete
        self.open_or_closed = open_or_closed
        if self.is_discrete():
            if values is not None:
                self.use_values = True
                self.values = set(values)
            else:
                self.use_values = False
                self.values = None
        else:
            self.use_values = False
            self.values = None

    def is_discrete(self):
        return self.discrete_or_continuous == IntervalType.Discrete

    def is_continuous(self):
        return self.discrete_or_continuous == IntervalType.Continuous

    def is_valid(self):
        return self.is_empty() or self.boundary[1] > self.boundary[0] or \
            (self.open_or_closed == (IntervalType.Closed, IntervalType.Closed) and self.boundary[0] == self.boundary[1])

    def is_empty(self):
        if self.is_continuous():
            return len(self.boundary) == 0 or \
                (self.boundary[0] == self.boundary[1] and
                 (self.open_or_closed[0] == IntervalType.Open or self.open_or_closed[1] == IntervalType.Open))
        else:
            if self.use_values and len(self.values) == 0:
                return True
            elif len(self.boundary) > 0:
                # 避免inf的情况
                if (np.isinf(self.boundary[0]) and np.sign(self.boundary[0]) < 0) or (np.isinf(self.boundary[1]) and np.sign(self.boundary[1]) > 0):
                    return False
                if int(self.boundary[0]) == int(self.boundary[1]):
                    return True
                return False
            else:
                return True

    @abstractmethod
    def intersects(self, other):
        pass

    @abstractmethod
    def intersection(self, other):
        pass

    @abstractmethod
    def union(self, other):
        pass

    @abstractmethod
    def sub(self, other):
        pass

    @abstractmethod
    def contains(self, item):
        pass

    def __and__(self, other):
        return self.intersection(other)

    def __or__(self, other):
        return self.union(other)

    def __contains__(self, item):
        return self.contains(item)


class DiscreteBaseIntervals(BaseIntervals):
    def __init__(self, boundary=None, open_or_closed=(IntervalType.Closed, IntervalType.Open), values=None):
        super().__init__(boundary, False, open_or_closed, values)

    def __repr__(self):
        return f"DiscreteBaseIntervals<{str(self)}>"

    def __str__(self):
        if self.use_values:
            s = "{" + ",".join(map(str, self.values)) + "}"
        else:
            left = "(" if self.open_or_closed[0] == IntervalType.Open else "["
            right = ")" if self.open_or_closed[1] == IntervalType.Open else "]"
            s = f"{left}{self.boundary[0]}, {self.boundary[1]}{right}" if not self.use_values else "{}"
        return s

    def intersects(self, other):
        if self.is_empty() or other.is_empty():
            return False
        if self.use_values and other.use_values:
            return len(self.values.intersects(other.values)) > 0
        elif self.use_values:
            cmp_left = (lambda it, y: it >= y) if other.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
            cmp_right = (lambda it, y: it <= y) if other.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
            return np.any([cmp_left(each, other.boundary[0]) and cmp_right(each, other.boundary[1]) for each in self.values])
        elif other.use_values:
            cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
            cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
            return np.any([cmp_left(each, self.boundary[0]) and cmp_right(each, self.boundary[1]) for each in other.values])
        else:
            (a, b), type1 = self.boundary, self.open_or_closed[1]
            (c, d), type2 = other.boundary, other.open_or_closed[0]
            if a > c:
                a, b, c, d, type1, type2 = c, d, a, b, type2, type1
            if b > c:
                return True
            if b == c and type2 == IntervalType.Closed and type1 == IntervalType.Closed:
                return True
            return False

    def intersection(self, other):
        if self.is_empty() or other.is_empty():
            return DiscreteBaseIntervals()
        if other.is_discrete():
            if self.use_values and other.use_values:
                return DiscreteBaseIntervals(values=self.values.intersects(other.values))
            elif self.use_values:
                cmp_left = (lambda it, y: it >= y) if other.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
                cmp_right = (lambda it, y: it <= y) if other.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
                return DiscreteBaseIntervals(values=[each for each in self.values if cmp_left(each, other.boundary[0]) and cmp_right(each, other.boundary[1])])
            elif other.use_values:
                cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
                cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
                return DiscreteBaseIntervals(values=[each for each in other.values if cmp_left(each, self.boundary[0]) and cmp_right(each, self.boundary[1])])
            else:
                (a, b), type1 = self.boundary, self.open_or_closed[1]
                (c, d), type2 = other.boundary, other.open_or_closed[0]
                if a > c:
                    a, b, c, d, type1, type2 = c, d, a, b, type2, type1
                if b > c:
                    return DiscreteBaseIntervals(boundary=(c, b), open_or_closed=(type2, type1))
                if b == c and type2 == IntervalType.Closed and type1 == IntervalType.Closed:
                    return DiscreteBaseIntervals(values=[b])

        raise NotImplemented

    def union(self, other):
        if self.is_empty():
            return other
        if other.is_empty():
            return self

        if other.is_discrete():
            if self.use_values and other.use_values:
                return DiscreteBaseIntervals(values=self.values.union(other.values))
        raise NotImplemented

    def sub(self, other):
        if isinstance(other, numbers.Number):
            if self.use_values:
                return DiscreteBaseIntervals(values=self.values - {other})
            else:
                raise NotImplemented
        elif isinstance(other, BaseIntervals):
            if self.use_values:
                cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
                cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
                return DiscreteBaseIntervals(values={each for each in self.values if cmp_left(each, other.boundary[0]) and cmp_right(each, other.boundary[1])})
            else:
                raise NotImplemented
        raise NotImplemented

    def contains(self, item):
        if isinstance(item, numbers.Number):
            if self.use_values:
                return item in self.values
            else:
                item = int(item)
                cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
                cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
                return np.all(cmp_left(item, self.boundary[0])) and np.all(cmp_right(item, self.boundary[1]))

        elif isinstance(item, Iterable):
            if self.use_values:
                return len(self.values.intersects(item)) != 0
            else:
                item = npa(list(item)).astype(int)
                cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
                cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
                return np.all(cmp_left(item, self.boundary[0])) and np.all(cmp_right(item, self.boundary[1]))
        elif isinstance(item, BaseIntervals):
            if self.use_values:
                return len(self.values.intersects(item)) != 0
            else:
                raise NotImplemented
        raise ParameterTypeError

    def __eq__(self, other):
        if not other.is_discrete():
            return False
        if self.use_values != other.use_values:
            return False
        if self.use_values:
            return self.values == other.values
        return self.boundary == other.boundary


class ContinuousBaseIntervals(BaseIntervals):
    def __init__(self, boundary=None, open_or_closed=(IntervalType.Closed, IntervalType.Open)):
        super().__init__(boundary, True, open_or_closed, values=None)

    def __repr__(self):
        return f"ContinuousBaseIntervals<{str(self)}>"

    def __str__(self):
        left = "(" if self.open_or_closed[0] == IntervalType.Open else "["
        right = ")" if self.open_or_closed[1] == IntervalType.Open else "]"
        return f"{left}{self.boundary[0]}, {self.boundary[1]}{right}" if not self.is_empty() else "{}"

    def intersects(self, other):
        if self.is_empty() or other.is_empty():
            return False
        (a, b), type1 = self.boundary, self.open_or_closed[1]
        (c, d), type2 = other.boundary, other.open_or_closed[0]
        if a > c:
            a, b, c, d, type1, type2 = c, d, a, b, type2, type1
        if b > c:
            return True
        if b == c and type2 == IntervalType.Closed and type1 == IntervalType.Closed:
            return True
        return False

    def intersection(self, other):
        if self.is_empty() or other.is_empty():
            return ContinuousBaseIntervals()
        if other.is_continuous():
            interval = ContinuousBaseIntervals()
            (a, b), (ta, tb) = self.boundary, self.open_or_closed
            (c, d), (tc, td) = other.boundary, other.open_or_closed
            if a > c or (a == c and tc == IntervalType.Closed):
                a, b, c, d, ta, tb, tc, td = c, d, a, b, tc, td, ta, tb
            if b > c:
                if b > d or (b == d and tb == IntervalType.Closed):
                    interval.open_or_closed = (tc, td)
                    interval.boundary = npa([c, d])
                else:
                    interval.open_or_closed = (tc, tb)
                    interval.boundary = npa([c, b])
                return interval
            elif b == c and tb == IntervalType.Closed and tc == IntervalType.Closed:
                interval.boundary = npa([b, c])
                interval.open_or_closed = (IntervalType.Closed, IntervalType.Closed)
                return interval
            return interval
        raise NotImplemented

    def contains(self, item):
        if isinstance(item, numbers.Number):
            cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
            cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
            return (cmp_left(item, self.boundary[0])) and (cmp_right(item, self.boundary[1]))

        elif isinstance(item, Iterable):
            cmp_left = (lambda it, y: it >= y) if self.open_or_closed[0] == IntervalType.Closed else (lambda it, y: it > y)
            cmp_right = (lambda it, y: it <= y) if self.open_or_closed[1] == IntervalType.Closed else (lambda it, y: it < y)
            return np.all(cmp_left(item, self.boundary[0])) and np.all(cmp_right(item, self.boundary[1]))

        elif isinstance(item, BaseIntervals):
            cmp_left = (lambda it, y: it >= y) if not (self.open_or_closed[0] == IntervalType.Open and item.open_or_closed[0] == IntervalType.Closed) else (lambda it, y: it > y)
            cmp_right = (lambda it, y: it <= y) if not (self.open_or_closed[1] == IntervalType.Open and item.open_or_closed[1] == IntervalType.Closed) else (lambda it, y: it < y)
            return np.all(cmp_left(item.boundary[0], self.boundary[0])) and np.all(cmp_right(item.boundary[1], self.boundary[1]))

        raise ParameterTypeError

    def union(self, other):
        if isinstance(other, ContinuousBaseIntervals):
            interval = ContinuousBaseIntervals()
            (a, b), (ta, tb) = self.boundary, self.open_or_closed
            (c, d), (tc, td) = other.boundary, other.open_or_closed
            if a > c or (a == c and tc == IntervalType.Closed):
                a, b, c, d, ta, tb, tc, td = c, d, a, b, tc, td, ta, tb
            if b > c:
                if b > d or (b == d and tb == IntervalType.Closed):
                    interval.open_or_closed = (ta, tb)
                    interval.boundary = npa([a, b])
                else:
                    interval.open_or_closed = (ta, td)
                    interval.boundary = npa([a, d])
                return interval
            elif b == c and (tb == IntervalType.Closed or tc == IntervalType.Closed):
                interval.boundary = npa([a, d])
                interval.open_or_closed = (ta, td)
                return interval
            else:
                from . import ListIntervals
                return ListIntervals([self, other])

        raise ParameterTypeError

    def sub(self, other):
        if isinstance(other, ContinuousBaseIntervals):
            (a, b), (ta, tb) = self.boundary, self.open_or_closed
            (c, d), (tc, td) = other.boundary, other.open_or_closed

            if b < c or (b == c and tb == IntervalType.Open):
                # a, b, c, d的情况
                return ContinuousBaseIntervals(self.boundary, open_or_closed=self.open_or_closed)
            elif b == c and tc == IntervalType.Closed:
                # a, b, c, d的情况
                return ContinuousBaseIntervals(self.boundary, open_or_closed=(self.open_or_closed[0], IntervalType.Open))

            if a > d or (a == d and ta == IntervalType.Open):
                # c, d, a, b 的情况
                return ContinuousBaseIntervals(self.boundary, open_or_closed=self.open_or_closed)
            elif a == d and td == IntervalType.Closed:
                # c, d, a, b 的情况
                return ContinuousBaseIntervals(self.boundary, open_or_closed=(IntervalType.Open, self.open_or_closed[1]))

            if c >= a:
                if d <= b:
                    # a, c, d, b 的情况
                    from . import ListIntervals
                    ca = ContinuousBaseIntervals((a, c), open_or_closed=(self.open_or_closed[0], IntervalType.Closed if other.open_or_closed[0] == IntervalType.Open else IntervalType.Open))
                    cb = ContinuousBaseIntervals((d, b), open_or_closed=(IntervalType.Closed if other.open_or_closed[1] == IntervalType.Open else IntervalType.Open, self.open_or_closed[1]))

                    if not ca.is_empty():
                        if not ca.is_empty():
                            return ListIntervals([ca, cb])
                        else:
                            return ca
                    else:
                        return cb
                else:
                    # a, c, b, d 的情况
                    return ContinuousBaseIntervals((a, c), open_or_closed=(self.open_or_closed[0], IntervalType.Closed if other.open_or_closed[1] == IntervalType.Open else IntervalType.Open))
            else:
                if d <= b:
                    # c, a, d, b 的情况
                    return ContinuousBaseIntervals((d, b), open_or_closed=(IntervalType.Closed if other.open_or_closed[1] == IntervalType.Open else IntervalType.Open, self.open_or_closed[1]))
                else:
                    # c, a, b, d 的情况
                    return ContinuousBaseIntervals()

        raise ParameterTypeError

    def __eq__(self, other):
        return isinstance(other, ContinuousBaseIntervals) and self.open_or_closed == self.open_or_closed and self.boundary == other.boundary


class Intervals(metaclass=ABCMeta):
    def __init__(self, intervals: (BaseIntervals, Iterable[BaseIntervals]) = None, simple=False):
        if isinstance(intervals, Intervals):
            self.intervals = intervals.intervals.copy()
        elif isinstance(intervals, BaseIntervals):
            self.intervals = [intervals]
        elif isinstance(intervals, Iterable):
            self.intervals: List[BaseIntervals] = list(intervals)
            for each in self.intervals:
                assert isinstance(each, BaseIntervals)

        self.is_simple = simple

    def __repr__(self):
        return f"Intervals<{str(self)}>"

    def __str__(self):
        return "[" + ','.join(map(str, self.intervals)) + "]"

    def is_empty(self, simplify=True):
        if not self.is_simple:
            res = self.simplify(inplace=simplify)
            return len(res.intervals) == 0
        else:
            return len(self.intervals) == 0

    @abstractmethod
    def union(self, other, inplace=False, simple=True):
        pass

    @abstractmethod
    def intersection(self, other, inplace=False, simple=True):
        pass

    @abstractmethod
    def sub(self, other, inplace=False, simple=True):
        pass

    @abstractmethod
    def simplify(self, inplace=True):
        pass

    def __and__(self, other):
        return self.intersection(other)

    def __iand__(self, other):
        return self.intersection(other, inplace=True)

    def __sub__(self, other):
        return self.sub(other, inplace=False)

    def __isub__(self, other):
        return self.sub(other, inplace=True)

    def __or__(self, other):
        return self.union(other)

    def __ior__(self, other):
        return self.union(other, inplace=True)


class ListIntervals(Intervals):

    def __init__(self, intervals: (BaseIntervals, Iterable[BaseIntervals]) = None, simple=False):
        super().__init__(intervals, simple)

    def simplify(self, inplace=True):
        intervals = [each for each in self.intervals if each.is_valid() and not each.is_empty()]
        if len(intervals) >= 2:
            intervals = sorted(intervals, key=lambda x: x.boundary[0])
            res = []
            current_interval: BaseIntervals = intervals[0]
            for each in intervals[1:]:
                if each.intersects(current_interval):
                    current_interval = current_interval.union(each)
                else:
                    res.append(current_interval)
                    current_interval = each
            else:
                res.append(current_interval)
            intervals = res
        if inplace:
            self.intervals = intervals
            return self
        else:
            return ListIntervals(intervals)

    def union(self, other, inplace=False, simple=True):
        if inplace:
            if isinstance(other, Intervals):
                self.intervals.extend(other.intervals)
                if simple:
                    self.simplify(inplace)
            elif isinstance(other, BaseIntervals):
                self.intervals.append(other)
                if simple:
                    self.simplify(inplace)
            elif isinstance(other, Iterable):
                self.intervals.extend(other)
                if simple:
                    self.simplify(inplace)
            else:
                raise ParameterTypeError
            return self
        else:
            if isinstance(other, ListIntervals):
                new_intervals = ListIntervals(self.intervals + other.intervals)
                if simple:
                    new_intervals.simplify(inplace)
            elif isinstance(other, BaseIntervals):
                new_intervals = ListIntervals(self.intervals + [other])
                if simple:
                    new_intervals.simplify(inplace)
            elif isinstance(other, Iterable):
                new_intervals = ListIntervals(self.intervals + other)
                if simple:
                    new_intervals.simplify(inplace)
            else:
                raise ParameterTypeError
            return new_intervals

    def sub(self, other, inplace=False, simple=True):
        if isinstance(other, ListIntervals):
            if inplace:
                self.intervals = [a.sub(b) for a, b in itertools.product(self.intervals, other.intervals)]
                if simple:
                    self.simplify(inplace)
                return self
            else:
                intervals = [a.sub(b) for a, b in itertools.product(self.intervals, other.intervals)]
                new_intervals = ListIntervals(intervals, simple)
                return new_intervals
        raise NotImplemented

    def intersection(self, other, inplace=False, simple=True):
        if inplace:
            if isinstance(other, Intervals):
                res = [a.intersection(b) for a, b in itertools.product(self.intervals, other.intervals)]
                self.intervals = res
                if simple:
                    self.simplify(inplace)
            elif isinstance(other, BaseIntervals):
                res = [a.intersection(other) for a in self.intervals]
                self.intervals = res
                if simple:
                    self.simplify(inplace)
            elif isinstance(other, Iterable):
                res = [a.intersection(b) for a, b in itertools.product(self.intervals, other)]
                self.intervals = res
                if simple:
                    self.simplify(inplace)
            else:
                raise ParameterTypeError
            return self
        else:
            if isinstance(other, Intervals):
                res = [a.intersection(b) for a, b in itertools.product(self.intervals, other.intervals)]
                result = ListIntervals(res)
                if simple:
                    result.simplify(inplace)
            elif isinstance(other, Iterable):
                res = [a.intersection(b) for a, b in itertools.product(self.intervals, other)]
                result = ListIntervals(res)
                if simple:
                    result.simplify(inplace)
            else:
                raise ParameterTypeError
            return result

    def __eq__(self, other):
        res1 = self.simplify(False)
        res2 = other.simplify(False)
        return len(res1.intervals) == len(res2.intervals) and np.all([a == b for a, b in zip(res1.intervals, res2.intervals)])


EMPTY = ListIntervals(ContinuousBaseIntervals())
R = ListIntervals(ContinuousBaseIntervals((-np.inf, np.inf), (IntervalType.Open, IntervalType.Open)))
Z = ListIntervals(DiscreteBaseIntervals((-np.inf, np.inf), (IntervalType.Open, IntervalType.Open)))
N = ListIntervals(DiscreteBaseIntervals((0, np.inf), (IntervalType.Closed, IntervalType.Open)))
