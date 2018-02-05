from abc import abstractmethod
from typing import List
from preset import Preset
from turn_order import TurnOrder
from time import sleep
from build import Build


class RuneManager(object):
    def __init__(self, runes=[]):
        self._runes = runes
        self._monsters = []
        self._turn_order = []

    def add_monster(self, preset: Preset):
        self._monsters.append(preset)

    def restrict_turn_order(self, order_constraint: TurnOrder):
        self._turn_order.append(order_constraint)

    def optimize(self):
        builds = []
        for preset in self._monsters:
            builds.append(self._find_build(preset))

        return builds

    def _filter_runes(self, slot, filter):
        return (r for r in self._runes if r.slot == slot and filter(r))

    def _find_build(self, preset):

        runes = [rune.as_equipped(preset.monster) for rune in self._runes if preset.is_suitable_rune(rune)]

        slot1 = list(r for r in runes if r.slot == 1)
        slot2 = list(r for r in runes if r.slot == 2)
        slot3 = list(r for r in runes if r.slot == 3)
        slot4 = list(r for r in runes if r.slot == 4)
        slot5 = list(r for r in runes if r.slot == 5)
        slot6 = list(r for r in runes if r.slot == 6)

        print('slot1', len(slot1))
        print('slot2', len(slot2))
        print('slot3', len(slot3))
        print('slot4', len(slot4))
        print('slot5', len(slot5))
        print('slot6', len(slot6))

        print(len(slot1) * len(slot2) * len(slot3) * len(slot4) * len(slot5) * len(slot6))
        # for rune in self._runes:
        #     for ra in slot1:
        #         if rune.id == ra.id:
        #             print(rune.slot, rune.grade * '\u2b50', rune.set.name)
        #             print(str(rune.stats.primary))
        #             if rune.stats.prefix:
        #                 print(str(rune.stats.prefix))
        #             else:
        #                 print('-')
        #
        #             for stat in rune.stats.sub_stats:
        #                 print(str(stat))
        #
        #             print('-' * 10)
        # return

        c = 0

        build = Build(preset.monster, [])

        for r1 in slot1:
            sa_1 = preset.get_sets_allowed()
            sa_1.remove(r1.set)
            for r2 in slot2:
                sa_2 = sa_1[:]
                sa_2.remove(r2.set)
                for r3 in slot3:
                    if r3.set in sa_2:
                        sa_3 = sa_2[:]
                        sa_3.remove(r3.set)
                        for r4 in slot4:
                            if r4.set in sa_3:
                                sa_4 = sa_3[:]
                                sa_4.remove(r4.set)
                                for r5 in slot5:
                                    if r5.set in sa_4:
                                        sa_5 = sa_4[:]
                                        sa_5.remove(r5.set)
                                        for r6 in slot6:
                                            if r6.set in sa_5:
                                                c += 1

                                                nextBuild = Build(preset.monster, (r1, r2, r3, r4, r5, r6))
                                                build = preset.pick_best(build, nextBuild)
                                                if nextBuild == build:
                                                    print('hp', build.hit_points)
                                                    print('atk', build.attack)
                                                    print('def', build.defense)
                                                    print('spd', build.speed)
                                                    print('cr', build.crit_rate)
                                                    print('cd', build.crit_dmg)
                                                    print('res', build.resistance)
                                                    print('acc', build.accuracy)
                                                    print('-' * 10)

        print('total builds:', c)

        return build
