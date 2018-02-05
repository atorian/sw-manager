class Build(object):
    def __init__(self, monster, runes=[]):
        self._monster = monster
        self._runes = runes
        self._stats = {}

        for stat in ['hp', 'atk', 'def', 'spd', 'cr', 'cd', 'res', 'acc']:
            self._stats[stat] = monster.stats[stat] + sum(r[stat] for r in runes)

    @property
    def runes(self):
        return self._runes

    @property
    def sets(self):
        print('_runes', self._runes)
        used_rune_sets = [rune.set for rune in self._runes]
        print('used_rune_sets', used_rune_sets)
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
    def attack(self):
        return self._stats['atk']

    @property
    def defense(self):
        return self._stats['def']

    @property
    def hit_points(self):
        return self._stats['hp']

    @property
    def speed(self):
        return self._stats['spd']

    @property
    def crit_rate(self):
        return self._stats['cr']

    @property
    def crit_dmg(self):
        return self._stats['cd']

    @property
    def resistance(self):
        return self._stats['res']

    @property
    def accuracy(self):
        return self._stats['acc']

    @property
    def dmg(self, skill):
        pass
