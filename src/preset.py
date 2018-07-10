from __future__ import division
from abc import abstractmethod
from typing import NamedTuple, List
from rune import Rune, RuneSet


class Condition(object):
    @abstractmethod
    def fulfilment(self, value):
        pass


class Between(Condition):
    def __init__(self, min=0, max=100000):
        self._min = min
        self._max = max

    def fulfilment(self, value):

        if self._min <= value <= self._max:
            return 1
        elif value <= self._min:
            return value / self.value
        # > max
        return 1 - (value - self.value) / self.value

    @property
    def value(self):
        return (self._max + self._min) / 2


class Min(Condition):
    def __init__(self, value):
        if value > 0:
            self._value = value
        else:
            raise Exception('value must be > 0')

    def fulfilment(self, value):
        return value / self._value if value >= self._value else 0

    @property
    def value(self):
        return self._value


class Max(Condition):
    def __init__(self, value):
        if value > 0:
            self._value = value
        else:
            raise Exception('value must be > 0')

    def fulfilment(self, value):
        if value == self._value:
            return 1
        elif value < self._value:
            return value / self._value
        else:
            return 1 - (value - self._value) / self._value

    @property
    def value(self):
        return self._value


class Around(Condition):
    def __init__(self, value):
        if value > 0:
            self._value = value
        else:
            raise Exception('value must be > 0')

    def fulfilment(self, value):

        # if value > self._value:
        #     n = 1.3
        #     return 1 + 1 / (value / self._value + 1) ** n

        return value / self._value

    @property
    def value(self):
        return self._value


class Stat(NamedTuple):
    name: str
    condition: Condition
    primary: bool = False


class Preset:
    def __init__(self, monster):
        self._monster = monster
        self._include_sets = []
        self._exclude_sets = []
        self._stats = []

    @property
    def stats(self) -> List[Stat]:
        return self._stats

    @property
    def focus(self) -> Stat:
        return self.stats[0]

    @property
    def monster(self):
        return self._monster

    def include(self, *args):
        self._include_sets = args

    def exclude(self, *args):
        self._exclude_sets = args

    @property
    def excluded_sets(self):
        return self._exclude_sets

    @property
    def allowed_sets(self):
        allowed = []
        for rune_set in self._include_sets:
            allowed += [rune_set] * rune_set.size

        allowed += [RuneSet('*', 2)] * (6 - len(allowed))

        return allowed

    def expect(self, *args):
        self._stats += args

    def no_brocken_sets(self):
        pass

    def is_suitable_rune(self, rune: Rune):

        if rune.is_locked:
            return False

        if rune.lvl < 12:
            return False

        if len(self._exclude_sets) > 0 and rune.set in self._exclude_sets:
            return False

        if len(self._include_sets) > 0 and rune.set not in self._include_sets:
            slots_needed = sum(set.size for set in self._include_sets)
            if slots_needed == 6:
                return False

        return True

    def build_value(self, stats):
        return [(stat.name, stat.condition.fulfilment(stats[stat.name])) for stat in self._stats]
