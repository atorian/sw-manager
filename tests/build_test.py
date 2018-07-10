import unittest

from build import Build
from preset import Between, Around, Stat
from src import Preset, Monster
from tests import make_rune
from units import searra


class TestBuild(unittest.TestCase):

    def setUp(self):
        self._preset = Preset(monster=Monster(name='Dummy', stats={
            'hp': 10000,
            'atk': 800,
            'def': 600,
            'spd': 100,
            'acc': 25
        }))
        self._preset.expect(
            Stat('spd', Between(min=200, max=220)),
            Stat('atk', Around(1600)),
            Stat('hp', Around(20000)),
            Stat('acc', Between(min=50, max=75))
        )

    def test_build_value_is_0_for_build_without_runes(self):
        build = Build(self._preset)
        self.assertEqual(0, build.value)

    def test_build_value_is_not_0_when_rune_equipped(self):
        build = Build(self._preset)
        rune = make_rune(
            slot=1,
            set='Violent',
            grade=6,
            lvl=12,
            primary=('atk', 118),
            sub_stats=(
                ('spd', 10),
                ('acc', 5),
                ('atk%', 10),
                ('hp%', 10),
            )
        )
        self.assertEqual(0.54, round(build.equip(rune).value, 3))

    def test_build_stats(self):
        build = Build(
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
        self.assertEqual(75, build.stats['acc'])



if __name__ == '__main__':
    unittest.main()
