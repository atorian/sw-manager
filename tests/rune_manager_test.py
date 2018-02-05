import unittest
from rune_manager import RuneManager
from preset import Preset, Stat, Min, Around
from monster import Monster
from team import Team
from rune import Rune, RuneBuilder
from turn_order import TurnOrder
from units import copper
from random import randint

used_ids = []

def make_rune(slot=1, set="Energy", grade=6, lvl=12, primary=None, prefix=None, sub_stats=None):
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
    builder.add_primary_stat(*primary)
    if prefix:
        builder.add_prefix_stat(*prefix)

    for stat in sub_stats:
        builder.add_sub_stat(*stat)

    return builder.make()


class TestRuneManager(unittest.TestCase):

    @unittest.skip
    def test_manager_preserves_order(self):
        rune_builder = RuneBuilder()
        runes = (
            make_rune(
                slot=1,
                set='Violent',
                grade=6,
                lvl=12,
                primary=('atk', 118),
                sub_stats=(
                    ('cr', 15),
                    ('cd', 18),
                    ('atk%', 10),
                    ('hp%', 8),
                )
            ),
            make_rune(
                slot=1,
                set='Blade',
                grade=6,
                lvl=12,
                primary=('atk', 118),
                sub_stats=(
                    ('cr', 15),
                    ('cd', 18),
                    ('atk%', 10),
                    ('hp%', 8),
                )
            ),
            make_rune(
                slot=2,
                set='Guard',
                grade=6,
                lvl=12,
                primary=('def%', 63),
                sub_stats=(
                    ('cr', 8),
                    ('cd', 24),
                    ('atk%', 10),
                    ('res', 8),
                )
            ),
            make_rune(
                slot=3,
                set='Guard',
                grade=6,
                lvl=12,
                primary=('def', 118),
                sub_stats=(
                    ('cr', 8),
                    ('cd', 16),
                    ('hp%', 10),
                    ('def%', 16),
                )
            ),
            make_rune(
                slot=4,
                set='Blade',
                grade=6,
                lvl=12,
                primary=('cd', 80),
                sub_stats=(
                    ('cr', 8),
                    ('res', 8),
                    ('hp%', 10),
                    ('def%', 24),
                )
            ),
            make_rune(
                slot=5,
                set='Guard',
                grade=6,
                lvl=12,
                primary=('hp', 2040),
                sub_stats=(
                    ('cr', 8),
                    ('cd', 24),
                    ('hp%', 10),
                    ('res', 8),
                )
            ),
            make_rune(
                slot=6,
                set='Guard',
                grade=6,
                lvl=12,
                primary=('def%', 63),
                sub_stats=(
                    ('cr', 8),
                    ('cd', 18),
                    ('hp%', 16),
                    ('res', 8),
                )
            ),
        )

        manager = RuneManager(runes)

        preset = Preset(monster=Monster(name='copper', stats={
            'hp': 9555,
            'atk': 483,
            'def': 692,
            'spd': 98,
            'res': 40
        }))
        preset.include(blade, guard)
        preset.exclude(violent)
        preset.expect(
            Stat(name='cr', condition=Min(70)),
            Stat(name='def', condition=Around(2000))
        )

        manager.add_monster(preset)

        builds = list(manager.optimize())
        self.assertEqual(1, len(list(builds)))

        build = builds[0]

        print(build)
        self.assertEqual(1, build.sets.count('Blade'))
        self.assertEqual(2, build.sets.count('Guard'))

        self.assertEqual(build.attack, 697.6)
        self.assertEqual(build.defense, 1958.72)
        self.assertEqual(build.crit_rate, 70)
        self.assertEqual(build.crit_dmg, 230)
        self.assertEqual(build.hit_points, 16754.7)
        self.assertEqual(build.speed, 98)
        self.assertEqual(build.resistance, 40)
        self.assertEqual(build.accuracy, 0)


if __name__ == '__main__':
    unittest.main()
