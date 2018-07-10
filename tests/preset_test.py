import unittest
from preset import Preset, Stat, Min, Max, Between, Around
from monster import Monster
from rune import Rune, RuneBuilder, RuneSet, RUNE_SETS
from random import randint
from rune_manager import Build, pick_best

violent = RUNE_SETS['Violent']
will = RUNE_SETS['Will']
guard = RUNE_SETS['Guard']

used_ids = []


def make_rune(slot=1, set="Energy", grade=6, lvl=12, primary=None, prefix=None, sub_stats=None, cls='H'):
    builder = RuneBuilder()

    id = None

    while not id:
        _id = randint(1, 2000000)
        if _id not in used_ids:
            id = _id

    builder.id(id)
    builder.slot(slot)
    builder.level(lvl)
    builder.grade(grade)
    builder.set(set)
    builder.cls(cls)

    if primary:
        builder.add_primary_stat(*primary)

    if prefix:
        builder.add_prefix_stat(*prefix)

    if sub_stats:
        for stat in sub_stats:
            builder.add_sub_stat(*stat)

    return builder.make()


class TestPreset(unittest.TestCase):

    def setUp(self):
        self._preset = preset = Preset(monster=Monster(name='Searra', stats={
            'hp': 10875,
            'atk': 801,
            'def': 615,
            'spd': 100,
            'acc': 25
        }))
        preset.include(violent, will)
        preset.expect(
            Stat('spd', Between(min=205, max=220)),  # 105
            Stat('atk', Around(2000)),  # 150%
            Stat('hp', Around(20000)),  # 97%
            Stat('acc', Between(min=60, max=85)),  # 50%
        )

    def test_is_suitable_rune_1(self):
        preset = Preset(monster=Monster('any', stats={}))
        preset.exclude(violent)

        self.assertTrue(preset.is_suitable_rune(make_rune(slot=1, set='Guard')))

    def test_is_suitable_rune_2(self):
        preset = Preset(monster=Monster('any', stats={}))
        preset.include(violent, will)

        self.assertTrue(preset.is_suitable_rune(make_rune(slot=1, set='Violent')))
        self.assertTrue(preset.is_suitable_rune(make_rune(slot=2, set='Will')))

    def test_is_suitable_rune_3(self):
        preset = Preset(monster=Monster('any', stats={}))
        preset.include(violent, will)

        self.assertFalse(preset.is_suitable_rune(make_rune(slot=1, set='Guard')))

    def test_is_suitable_rune_6(self):
        rune = make_rune(slot=1, set='Violent', cls='L', primary=('atk%', 63), sub_stats=(
            ('spd', 8),
            ('cd', 18),
            ('hp%', 16),
            ('res', 8),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_7(self):
        rune = make_rune(slot=4, set='Violent', cls='L', primary=('hp%', 63), sub_stats=(
            ('spd', 16),
            ('def', 18),
            ('atk%', 15),
            ('def%', 15),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_8(self):
        rune = make_rune(slot=3, set='Violent', cls='L', primary=('def', 160), sub_stats=(
            ('hp%', 12),
            ('spd', 20),
            ('acc', 13),
            ('cr', 4),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_9(self):
        rune = make_rune(slot=5, set='Will', primary=('hp', 1800), prefix=('cd', 5), cls='H', sub_stats=(
            ('spd', 20),
            ('cr', 6),
            ('atk%', 6),
            ('acc', 4),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_10(self):
        rune = make_rune(slot=1, set='Violent', primary=('atk', 160), cls='H', sub_stats=(
            ('cd', 6),
            ('atk%', 24),
            ('spd', 15),
            ('cr', 5),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_11(self):
        rune = make_rune(slot=1, set='Violent', primary=('atk', 160), cls='L', sub_stats=(
            ('atk%', 16),
            ('spd', 13),
            ('acc', 9),
            ('cr', 10),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_is_suitable_rune_12(self):
        rune = make_rune(slot=1, set='Will', primary=('atk', 94), cls='L', sub_stats=(
            ('atk%', 15),
            ('cd', 5),
            ('hp%', 22),
            ('acc', 7),
        ))

        self.assertTrue(self._preset.is_suitable_rune(rune))

    def test_compare_builds_1(self):
        build_a = Build(
            self._preset,
            runes=(
                make_rune(slot=1, set='Violent', primary=('atk', 118), prefix=('acc', 6), sub_stats=(
                    ('atk%', 20),
                    ('spd', 8),
                    ('cr', 11),
                    ('hp', 19),
                )),
                make_rune(slot=2, set='Violent', primary=('atk%', 63), sub_stats=(
                    ('hp%', 6),
                    ('acc', 14),
                    ('cd', 12),
                    ('spd', 16),
                )),
                make_rune(slot=3, set='Violent', primary=('def', 160), sub_stats=(
                    ('cr', 4),
                    ('spd', 20),
                    ('acc', 13),
                    ('hp%', 12),
                )),
                make_rune(slot=4, set='Violent', primary=('hp%', 63), sub_stats=(
                    ('atk', 12),
                    ('cd', 6),
                    ('spd', 27),
                    ('hp', 256),
                )),
                make_rune(slot=5, set='Will', grade=5, primary=('hp', 1530), prefix=('atk%', 4), sub_stats=(
                    ('hp%', 4),
                    ('spd', 15),
                    ('res', 6),
                    ('atk', 9),
                )),
                make_rune(slot=6, set='Will', primary=('atk%', 63), sub_stats=(
                    ('def%', 17),
                    ('spd', 14),
                    ('acc', 8),
                    ('hp%', 10),
                )),
            )
        )
        build_b = Build(
            self._preset,
            runes=(
                make_rune(slot=1, set='Violent', primary=('atk', 118), prefix=('acc', 6), sub_stats=(
                    ('atk%', 20),
                    ('spd', 8),
                    ('cr', 11),
                    ('hp', 19),
                )),
                make_rune(slot=2, set='Violent', primary=('atk%', 63), sub_stats=(
                    ('hp%', 6),
                    ('acc', 14),
                    ('cd', 12),
                    ('spd', 16),
                )),
                make_rune(slot=3, set='Violent', primary=('def', 160), sub_stats=(
                    ('cr', 4),
                    ('spd', 20),
                    ('acc', 13),
                    ('hp%', 12),
                )),
                make_rune(slot=4, set='Violent', primary=('hp%', 63), sub_stats=(
                    ('atk', 12),
                    ('cd', 6),
                    ('spd', 27),
                    ('hp', 256),
                )),
                make_rune(slot=5, set='Will', grade=6, primary=('hp', 1800), prefix=('cd', 5), sub_stats=(
                    ('atk%', 6),
                    ('spd', 20),
                    ('acc', 4),
                    ('cr', 9),
                )),
                make_rune(slot=6, set='Will', primary=('atk%', 63), sub_stats=(
                    ('def%', 17),
                    ('spd', 14),
                    ('acc', 8),
                    ('hp%', 10),
                )),
            )
        )

        self.assertEqual(build_b, pick_best(build_a, build_b))

    def test_compare_builds_2(self):
        build_a = Build(
            self._preset,
            runes=(
                make_rune(
                    slot=1,
                    set='Will',
                    primary=('atk', 118),
                    prefix=('hp', 143),
                    sub_stats=(
                        ('res', 16),
                        ('spd', 16),
                        ('atk%', 20),
                        ('hp%', 11),
                    )
                ),
                make_rune(
                    slot=2,
                    set='Violent',
                    primary=('spd', 39),
                    prefix=('cr', 5),
                    sub_stats=(
                        ('atk%', 16),
                        ('hp%', 16),
                        ('def%', 10),
                        ('hp', 621),
                    )
                ),
                make_rune(
                    slot=3,
                    set='Violent',
                    primary=('def', 126),
                    prefix=('cd', 4),
                    sub_stats=(
                        ('spd', 12),
                        ('hp%', 19),
                        ('def%', 10),
                        ('cr', 6),
                    )
                ),
                make_rune(
                    slot=4,
                    set='Violent',
                    primary=('hp%', 47),
                    sub_stats=(
                        ('res', 20),
                        ('atk%', 17),
                        ('spd', 8),
                        ('cd', 4),
                    )
                ),
                make_rune(
                    slot=5,
                    set='Will',
                    grade=6,
                    primary=('hp', 1880),
                    sub_stats=(
                        ('spd', 15),
                        ('atk%', 21),
                        ('cr', 6),
                        ('def%', 11),
                    )
                ),
                make_rune(
                    slot=6,
                    set='Will',
                    primary=('atk%', 63),
                    prefix=('cr', 6),
                    sub_stats=(
                        ('hp%', 24),
                        ('spd', 18),
                        ('def%', 5),
                        ('cd', 9),
                    )
                ),
            )
        )
        build_b = Build(
            self._preset,
            runes=(
                make_rune(
                    slot=1,
                    set='Violent',
                    primary=('atk', 160),
                    sub_stats=(
                        ('res', 12),
                        ('acc', 15),
                        ('hp%', 17),
                        ('spd', 17),
                    )
                ),
                make_rune(
                    slot=2,
                    set='Violent',
                    primary=('atk%', 63),
                    sub_stats=(
                        ('hp%', 11),
                        ('acc', 14),
                        ('cd', 12),
                        ('spd', 16),
                    )
                ),
                make_rune(
                    slot=3,
                    set='Violent',
                    primary=('def', 160),
                    sub_stats=(
                        ('cr', 4),
                        ('spd', 20),
                        ('acc', 13),
                        ('hp%', 12),
                    )
                ),
                make_rune(
                    slot=4,
                    set='Violent',
                    primary=('hp%', 63),
                    sub_stats=(
                        ('atk%', 12),
                        ('cd', 6),
                        ('spd', 27),
                        ('hp', 256),
                    )
                ),
                make_rune(
                    slot=5,
                    set='Will',
                    grade=6,
                    primary=('hp', 1800),
                    prefix=('cd', 5),
                    sub_stats=(
                        ('spd', 15),
                        ('atk%', 21),
                        ('cr', 6),
                        ('def%', 11),
                    )
                ),
                make_rune(
                    slot=6,
                    set='Will',
                    primary=('atk%', 63),
                    sub_stats=(
                        ('def%', 17),
                        ('spd', 14),
                        ('acc', 8),
                        ('hp%', 12),
                    )
                ),
            )
        )

        self.assertEqual(build_b, pick_best(build_a, build_b))

    def test_compare_builds_3(self):
        build_a = Build(
            self._preset,
            runes=(
                make_rune(
                    slot=1,
                    set='Violent',
                    primary=('atk', 126),
                    prefix=('acc', 6),
                    sub_stats=(
                        ('atk%', 23),
                        ('spd', 8),
                        ('cr', 11),
                        ('hp%', 19),
                    )
                ),
                make_rune(
                    slot=2,
                    set='Violent',
                    primary=('atk%', 63),
                    sub_stats=(
                        ('hp%', 11),
                        ('acc', 14),
                        ('cd', 12),
                        ('spd', 16),
                    )
                ),
                make_rune(
                    slot=3,
                    set='Will',
                    primary=('def', 118),
                    prefix=('spd', 6),
                    sub_stats=(
                        ('cr', 6),
                        ('hp%', 22),
                        ('acc', 21),
                        ('res', 8),
                    )
                ),
                make_rune(
                    slot=4,
                    set='Violent',
                    primary=('hp%', 63),
                    sub_stats=(
                        ('spd', 9),
                        ('cr', 11),
                        ('atk%', 23),
                        ('acc', 9),
                    )
                ),
                make_rune(
                    slot=5,
                    set='Violent',
                    grade=5,
                    primary=('hp', 2088),
                    prefix=('atk%', 5),
                    sub_stats=(
                        ('def%', 11),
                        ('spd', 24),
                        ('res', 7),
                        ('cd', 5),
                    )
                ),
                make_rune(
                    slot=6,
                    set='Will',
                    primary=('atk%', 63),
                    prefix=('cr', 6),
                    sub_stats=(
                        ('def%', 17),
                        ('spd', 14),
                        ('acc', 8),
                        ('hp%', 12),
                    )
                )
            )
        )
        build_b = Build(
            self._preset,
            runes=(
                make_rune(
                    slot=1,
                    set='Violent',
                    primary=('atk', 160),
                    sub_stats=(
                        ('res', 12),
                        ('acc', 15),
                        ('hp%', 17),
                        ('spd', 17),
                    )
                ),
                make_rune(
                    slot=2,
                    set='Violent',
                    primary=('atk%', 63),
                    sub_stats=(
                        ('hp%', 11),
                        ('acc', 14),
                        ('cd', 12),
                        ('spd', 16),
                    )
                ),
                make_rune(
                    slot=3,
                    set='Violent',
                    primary=('def', 160),
                    sub_stats=(
                        ('cr', 4),
                        ('spd', 20),
                        ('acc', 13),
                        ('hp%', 12),
                    )
                ),
                make_rune(
                    slot=4,
                    set='Violent',
                    primary=('hp%', 63),
                    sub_stats=(
                        ('atk%', 12),
                        ('cd', 6),
                        ('spd', 27),
                        ('hp', 256),
                    )
                ),
                make_rune(
                    slot=5,
                    set='Will',
                    grade=6,
                    primary=('hp', 1800),
                    prefix=('cd', 5),
                    sub_stats=(
                        ('spd', 15),
                        ('atk%', 21),
                        ('cr', 6),
                        ('def%', 11),
                    )
                ),
                make_rune(
                    slot=6,
                    set='Will',
                    primary=('atk%', 63),
                    sub_stats=(
                        ('def%', 17),
                        ('spd', 14),
                        ('acc', 8),
                        ('hp%', 12),
                    )
                ),
            )
        )

        self.assertEqual(build_b, pick_best(build_a, build_b))

    def test_equipped_rune(self):
        rune = make_rune(slot=1, set='Violent', primary=('atk', 118), prefix=('acc', 6), sub_stats=(
            ('atk%', 20),
            ('spd', 8),
            ('cr', 11),
            ('hp', 19),
        ))

        equipped_rune = rune.as_equipped(self._preset.monster)

        self.assertEqual(equipped_rune['atk'], 278.2)
        self.assertEqual(equipped_rune['def'], 0)
        self.assertEqual(equipped_rune['cd'], 0)
        self.assertEqual(equipped_rune['spd'], 8)

    def test_Stat_Min_is_1_when_value_is_eql(self):
        condition = Min(10)
        self.assertEqual(1, condition.fulfilment(10))

    def test_Stat_Min_is_0_when_value_is_less(self):
        condition = Min(10)
        self.assertEqual(0, condition.fulfilment(9))

    def test_Stat_Min_is_proportionate_to_over_fulfillment(self):
        condition = Min(10)
        self.assertEqual(1.1, condition.fulfilment(11))
        self.assertEqual(1.5, condition.fulfilment(15))

    def test_Stat_Max_is_1_when_value_is_eql(self):
        condition = Max(10)
        self.assertEqual(1, condition.fulfilment(10))

    def test_Stat_Max_is_proportional_to_value_when_less(self):
        condition = Max(10)
        self.assertEqual(0.9, condition.fulfilment(9))

    def test_Stat_Max_is_backwards_proportional_to_value_when_greater(self):
        condition = Max(10)
        self.assertEqual(0.9, condition.fulfilment(11))

    def test_Stat_Around_is_proportinal_to_value_1(self):
        condition = Around(1000)
        self.assertEqual(1, condition.fulfilment(1000))

    def test_Stat_Around_is_proportinal_to_value_2(self):
        condition = Around(1000)
        self.assertEqual(0, condition.fulfilment(0))

    def test_Stat_Around_is_proportinal_to_value_3(self):
        condition = Around(1000)
        self.assertEqual(1.2397, round(condition.fulfilment(2000), 4))

    def test_Stat_Around_is_proportinal_to_value_4(self):
        condition = Around(1000)
        self.assertEqual(1.3039, round(condition.fulfilment(1500), 4))

    def test_Stat_Between_1(self):
        condition = Between(min=5, max=10)
        self.assertEqual(0, condition.fulfilment(0))

    def test_Stat_Between_2(self):
        condition = Between(min=5, max=10)
        self.assertEqual(1, round(condition.fulfilment(5), 3))

    def test_Stat_Between_3(self):
        condition = Between(min=5, max=10)
        self.assertEqual(1, round(condition.fulfilment(10), 3))

    def test_Stat_Between_4(self):
        condition = Between(min=60, max=85)
        self.assertEqual(1, round(condition.fulfilment(61), 4))

    def test_Stat_Between_5(self):
        condition = Between(min=60, max=85)
        self.assertEqual(1, round(condition.fulfilment(75), 4))
