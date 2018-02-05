MAX_VALUES = {
    '6': {
        'hp': {'base': 360, 'up': 120, 'max': 2448},
        'hp%': {'base': 11, 'up': 3, 'max': 63},
        'atk': {'base': 22, 'up': 8, 'max': 160},
        'atk%': {'base': 11, 'up': 3, 'max': 63},
        'def': {'base': 22, 'up': 8, 'max': 160},
        'def%': {'base': 11, 'up': 3, 'max': 63},
        'spd': {'base': 7, 'up': 2, 'max': 42},
        'cr': {'base': 7, 'up': 3, 'max': 58},
        'cd': {'base': 11, 'up': 4, 'max': 80},
        'res': {'base': 12, 'up': 3, 'max': 64},
        'acc': {'base': 12, 'up': 3, 'max': 64},
    },
    '5': {
        'hp': {'base': 270, 'up': 105, 'max': 2088},
        'hp%': {'base': 8, 'up': 2.45, 'max': 51},
        'atk': {'base': 15, 'up': 7, 'max': 135},
        'atk%': {'base': 8, 'up': 2.45, 'max': 51},
        'def': {'base': 15, 'up': 7, 'max': 135},
        'def%': {'base': 8, 'up': 2.45, 'max': 51},
        'spd': {'base': 5, 'up': 2, 'max': 39},
        'cr': {'base': 5, 'up': 2.45, 'max': 47},
        'cd': {'base': 8, 'up': 3.33, 'max': 65},
        'res': {'base': 9, 'up': 2.45, 'max': 51},
        'acc': {'base': 9, 'up': 2.45, 'max': 51}
    }
}


class RuneSet(object):

    def __init__(self, name, size):
        self._name = name
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    def __eq__(self, other):
        if self._name == '*' or other._name == '*':
            return True
        else:
            return self._name == other.name and self._size == other.size

    def __repr__(self):
        return 'RuneSet {} {}'.format(self._name, self._size)


RUNE_SETS = {
    "Energy": RuneSet("Energy", 2),
    "Guard": RuneSet("Guard", 2),
    "Swift": RuneSet("Swift", 4),
    "Blade": RuneSet("Blade", 2),
    "Rage": RuneSet("Rage", 4),
    "Focus": RuneSet("Focus", 2),
    "Endure": RuneSet("Endure", 2),
    "Fatal": RuneSet("Fatal", 4),
    "Despair": RuneSet("Despair", 4),
    "Vampire": RuneSet("Vampire", 4),
    "Violent": RuneSet("Violent", 4),
    "Nemesis": RuneSet("Nemesis", 2),
    "Will": RuneSet("Will", 2),
    "Shield": RuneSet("Shield", 2),
    "Revenge": RuneSet("Revenge", 2),
    "Destroy": RuneSet("Destroy", 2),
    "Fight": RuneSet("Fight", 2),
    "Determination": RuneSet("Determination", 2),
    "Enhance": RuneSet("Enhance", 2),
    "Accuracy": RuneSet("Accuracy", 2),
    "Tolerance": RuneSet("Tolerance", 2),
}


class Stats(object):
    def __init__(self, primary, sub_stats, prefix=None):
        self._primary = primary
        self._prefix = prefix
        self._subs = sub_stats

    def __it__(self):
        if (self._prefix):
            return ([self._primary, self._prefix] + self._subs.values()).__iter__()
        else:
            return ([self._primary] + self._subs.values()).__iter__()

    @property
    def primary(self):
        return self._primary

    @property
    def prefix(self):
        return self._prefix

    @property
    def sub_stats(self):
        return self._subs

    def __getitem__(self, stat_name):
        if self._primary.name == stat_name:
            return self._primary
        elif (self._prefix and self._prefix.name == stat_name):
            return self._prefix
        else:
            for s in self._subs:
                if stat_name == s.name:
                    return s

        return RuneStat(name='none', value=0)


class RuneStat(object):
    def __init__(self, name: str, value: int, grind: int = 0, switched=False):
        self._name = name
        self._value = value
        self._grind = grind
        self._is_switched = switched

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def is_switched(self):
        return self._is_switched

    def is_grinded(self):
        return self._grind > 0

    @property
    def grind(self):
        return self._grind

    def __str__(self):
        return "{0} {1}".format(self._name, self._value)

    def __repr__(self):
        return "RuneStat: {0} {1}".format(self._name, self._value)


class MetaInfo(object):

    def __init__(self, slot, set: RuneSet, lvl, grade):
        self._slot = slot
        self._set = set
        self._lvl = lvl
        self._grade = grade

    @property
    def slot(self):
        return self._slot

    @property
    def set(self):
        return self._set

    @property
    def lvl(self):
        return self._lvl

    @property
    def grade(self):
        return self._grade


class EquippedRune(object):
    def __init__(self, id, meta: MetaInfo, monster_stats, rune_stats: Stats):
        self._id = id
        self._meta = meta
        self._stats = {
            'hp': rune_stats['hp'].value + rune_stats['hp%'].value * monster_stats['hp'] / 100,
            'atk': rune_stats['atk'].value + rune_stats['atk%'].value * monster_stats['atk'] / 100,
            'def': rune_stats['def'].value + rune_stats['def%'].value * monster_stats['def'] / 100,
            'spd': rune_stats['spd'].value,
            'cr': rune_stats['cr'].value,
            'cd': rune_stats['cd'].value,
            'res': rune_stats['res'].value,
            'acc': rune_stats['res'].value,
        }
        # todo: calc possible grinds / switches

    def __getitem__(self, key):
        return self._stats[key]

    @property
    def id(self):
        return self._id

    @property
    def slot(self):
        return self._meta.slot

    @property
    def set(self):
        return self._meta.set

class Rune(object):
    def __init__(self, id: int, meta: MetaInfo, stats: Stats):
        self._id = id
        self._meta = meta
        self._stats = stats
        self._is_locked = False

    def lock(self):
        self._is_locked = True

    def unlock(self):
        self._is_locked = False

    def is_locked(self):
        return self._is_locked

    @property
    def id(self):
        return self._id

    def __getitem__(self, key):
        return self._stats[key].value

    @property
    def grade(self):
        return self._meta.grade

    @property
    def stats(self):
        return self._stats

    @property
    def slot(self):
        return self._meta.slot

    @property
    def set(self):
        return self._meta.set

    @property
    def primary(self):
        return self._stats.primary

    def _stat_value(self, stat, lvl):
        rules = MAX_VALUES.get(str(self._meta.grade)).get(stat)

        if lvl == 15:
            return rules.get('max')

        return rules.get('base') + lvl * rules.get('up')

    def as_lvl_12(self):
        return Rune(
            self._id,
            self._meta,
            Stats(
                primary=RuneStat(
                    self._stats.primary.name,
                    self._stat_value(self._stats.primary.name, 12)
                ),
                prefix=self._stats.prefix,
                sub_stats=self._stats.sub_stats
            )
        )

    def as_lvl_15(self):
        return Rune(
            self._id,
            self._meta,
            Stats(
                primary=RuneStat(
                    self._stats.primary.name,
                    self._stat_value(self._stats.primary.name, 15)
                ),
                prefix=self._stats.prefix,
                sub_stats=self._stats.sub_stats
            )
        )

    def as_equipped(self, monster):
        return EquippedRune(
            self._id,
            self._meta,
            monster.stats,
            self._stats
        )


class RuneBuilder(object):

    def __init__(self):
        self._reset()

    def _reset(self):
        self._id = None
        self._meta = {
            'set': None,
            'grade': None,
            'slot': None,
            'lvl': None,
        }

        self._stats = {
            'primary': None,
            'prefix': None,
            'sub_stats': [],
        }

    def id(self, id):
        self._id = id

    def level(self, lvl):
        self._meta['lvl'] = lvl

    def slot(self, slot):
        self._meta['slot'] = slot

    def grade(self, grade):
        self._meta['grade'] = grade

    def set(self, set_name):
        self._meta['set'] = RUNE_SETS[set_name]

    def add_primary_stat(self, name, value):
        self._stats['primary'] = (name, value)

    def add_prefix_stat(self, name, value):
        self._stats['prefix'] = (name, value)

    def add_sub_stat(self, name, value, grind=0, switched=False):
        self._stats['sub_stats'].append(
            (name, value, grind, switched)
        )

    def make(self):
        rune = Rune(
            self._id,
            MetaInfo(**self._meta),
            Stats(
                primary=RuneStat(*self._stats['primary']),
                prefix=RuneStat(*self._stats['prefix']) if self._stats['prefix'] else None,
                sub_stats=list(map(lambda args: RuneStat(*args), self._stats['sub_stats'])),
            ) if self._stats['primary'] else None
        )

        self._reset()

        return rune
