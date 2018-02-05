from __future__ import division
from abc import abstractmethod
from typing import NamedTuple
from rune import Rune, RuneSet
from statistics import harmonic_mean


class Condition(object):
    @abstractmethod
    def is_ok(self, build):
        pass


class Between(Condition):
    def __init__(self, min=0, max=100000):
        self._min = min
        self._max = max

    def fulfilment(self, value):
        return 1 if self._min <= value <= self._max else 0


class Min(Condition):
    def __init__(self, value):
        if value > 0:
            self._value = value
        else:
            raise Exception('value must be > 0')

    def fulfilment(self, value):
        return value / self._value if value >= self._value else 0


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


class Around(Condition):
    def __init__(self, value):
        if value > 0:
            self._value = value
        else:
            raise Exception('value must be > 0')

    def fulfilment(self, value):
        return value / self._value


class Stat(NamedTuple):
    name: str
    condition: Condition


class Build(object):
    def __init__(self, r246):
        self._main_runes = r246
        self._runes = {}

    def set_rune(self, rune):
        self._runes[rune.slot] = rune

    def is_possible_with(self, rune):
        pass


procs = {
    5: {
        'hp': {'min': 90, 'max': 300},
        'hp%': {'min': 4, 'max': 7},
        'atk': {'min': 8, 'max': 15},
        'atk%': {'min': 4, 'max': 7},
        'def': {'min': 8, 'max': 15},
        'def%': {'min': 4, 'max': 7},
        'spd': {'min': 3, 'max': 5},
        'cr': {'min': 3, 'max': 5},
        'cd': {'min': 3, 'max': 5},
        'acc': {'min': 3, 'max': 7},
        'res': {'min': 3, 'max': 7},
    },
    6: {
        'atk%': {'min': 5, 'max': 8},
        'atk': {'min': 10, 'max': 20},
        'hp%': {'min': 5, 'max': 8},
        'hp': {'min': 135, 'max': 375},
        'def%': {'min': 5, 'max': 8},
        'def': {'min': 10, 'max': 20},
        'spd': {'min': 4, 'max': 6},
        'cr': {'min': 4, 'max': 6},
        'cd': {'min': 4, 'max': 7},
        'acc': {'min': 4, 'max': 8},
        'res': {'min': 4, 'max': 8},
    }
}


class Preset:
    def __init__(self, monster):
        self._monster = monster
        self._include_sets = []
        self._exclude_sets = []
        self._stats = []

    @property
    def monster(self):
        return self._monster

    def include(self, *args):
        self._include_sets = args

    def exclude(self, *args):
        self._exclude_sets = args

    def get_sets_allowed(self):
        allowed = []
        for set in self._include_sets:
            allowed += [set] * set.size

        allowed += [RuneSet('*', 2)] * (6 - len(allowed))

        return allowed

    def get_acceptable_core_runes(self):
        return [
            ('spd', 'hp', 'atk'),
            ('atk', 'atk', 'hp'),
            ('atk', 'atk', 'atk'),
        ]

    def expect(self, *args):
        self._stats += args

    def no_brocken_sets(self):
        pass

    def _calc_diff(self):
        pass

    def is_suitable_rune(self, rune: Rune):
        if len(self._exclude_sets) > 0 and rune.set in self._exclude_sets:
            return False

        if len(self._include_sets) > 0 and rune.set not in self._include_sets:
            slots_needed = sum(set.size for set in self._include_sets)
            if slots_needed == 6:
                return False

        if len(self._stats) > 0:

            if rune.slot in (2, 4, 6):
                is_useful = False
                for stat in self._stats:
                    is_useful = is_useful or (stat.name in rune.primary.name)

                if not is_useful:
                    return False

            has_stats = 0
            prio_stats = self._stats[0:2]

            if rune.slot == 3:
                prio_stats = [s for s in self._stats if 'atk' not in s.name][0:2]

            for stat in prio_stats:
                if stat.name in ('hp', 'def', 'atk'):
                    if rune[stat.name + '%'] >= (2 * procs[rune.grade][stat.name + '%']['min']):
                        has_stats += 1
                elif rune[stat.name] >= (2 * procs[rune.grade][stat.name]['min']):
                    has_stats += 1

            if has_stats != len(prio_stats):
                return False

        return True

    def rune_satisfaction(self, rune: Rune):
        satisfaction = 0
        for stat in self._stats:
            d = 0
            if stat.name in ('hp', 'def', 'atk'):
                d = (getattr(rune.stats, stat.name + '_f') + getattr(
                    rune.stats,
                    stat.name + '_p'
                ) * self._monster.stats.get(stat.name)
                     ) / (stat.condition.value - self._monster.stats.get(stat.name)) / 100
            else:
                d += getattr(rune.stats, stat.name) / (stat.condition.value - self._monster.stats.get(stat.name))

            satisfaction += d

        return satisfaction

    def _build_value(self, build):
        fulfilment = []
        for stat in self._stats:
            if stat.name == 'hp':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.hit_points)))
            elif stat.name == 'atk':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.attack)))
            elif stat.name == 'def':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.defense)))
            elif stat.name == 'spd':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.speed)))
            elif stat.name == 'cr':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.crit_rate)))
            elif stat.name == 'cd':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.crit_dmg)))
            elif stat.name == 'acc':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.accuracy)))
            elif stat.name == 'res':
                fulfilment.append((stat.name, stat.condition.fulfilment(build.resistance)))
            else:
                print('unknown stat')

        return fulfilment

    def pick_best(self, build_a, build_b):

        if len(self._stats) > 0:
            value_a = self._build_value(build_a)
            value_b = self._build_value(build_b)

            stats_fulfilled_a = sum(1 for s, v in value_a if v >= 1)
            stats_fulfilled_b = sum(1 for s, v in value_b if v >= 1)

            if stats_fulfilled_a > stats_fulfilled_b:
                return build_a
            elif stats_fulfilled_a < stats_fulfilled_b:
                return build_b
            else:
                return build_a if harmonic_mean(v for s, v in value_a) >= harmonic_mean(v for s, v in value_b) else build_b
        else:
            return build_b
