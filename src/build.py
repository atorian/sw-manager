from statistics import harmonic_mean, mean
from typing import List, Tuple, NamedTuple

from preset import Preset
from rune import Rune, EquippedRune


values = {}

class Build(object):

    def __init__(self, preset: Preset, runes: List[Rune] = None):
        self._monster = preset.monster
        self._preset = preset
        self._runes = runes or [None, ] * 6
        self._stats = {}
        self._v_id = '.'.join(str(r.id) for r in self.runes)

    def fingerprint(self):
        return '-'.join([r.id for r in self._runes])

    @property
    def preset(self):
        return self._preset

    def equip(self, rune):
        # if self._runes[rune.slot - 1]:
        #     raise Exception('Rune for slot {} is already equipped'.format(rune.slot))

        new_runes = self._runes[:]
        new_runes[rune.slot - 1] = rune

        return Build(self._preset, new_runes)

    def lock(self):
        for rune in self._runes:
            if rune:
                rune.lock()

    def grind(self):
        pass

    @property
    def stats(self):
        equipped_runes = [r.as_equipped(self._monster) for r in self._runes if r]
        stats = {}
        for stat in ['hp', 'atk', 'def', 'spd', 'cr', 'cd', 'res', 'acc']:
            stats[stat] = self._monster.stats[stat] + sum(r[stat] for r in equipped_runes)

        return stats

    @property
    def focus_stat(self):
        return self.stats[self._preset.focus.name]

    def _value(self):
        global values
        if not values.get(self._v_id):
            vs = [v for s, v in self._preset.build_value(self.stats)]
            hv = harmonic_mean([max(v, 0) for v in vs]) if any(self._runes) else 0
            values[self._v_id] = (vs, hv)

        return values[self._v_id]

    @property
    def value(self):
        return self._value()[1]

    @property
    def stat_value(self):
        return self._value()[0]

    def is_suitable(self, rune: Rune):
        if rune.set in self._preset.allowed_sets:
            sets_remained = self._preset.allowed_sets
            for r in self._runes:
                if r:
                    sets_remained.remove(r.set)

            return rune.set in sets_remained

        return False

    @property
    def runes(self):
        return [rune for rune in self._runes if rune]

    @property
    def sets(self):
        used_rune_sets = [rune.set for rune in self._runes]
        sets = []
        for rune in self._runes:
            if used_rune_sets.count(rune.set) % rune.set.size == 0 and rune.set.name not in sets:
                c = used_rune_sets.count(rune.set) / rune.set.size
                while c > 0:
                    sets.append(rune.set.name)
                    c -= 1

        return sets

    @property
    def monster(self):
        return self._monster

    @property
    def is_complete(self):
        return len(self._runes) == 6
