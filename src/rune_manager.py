from itertools import permutations
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
import math
from functools import reduce
from typing import List
import traceback
from preset import Preset
from build import Build
from rune import Rune, PROCS, MAX_VALUES

logging.basicConfig(filename='optimze.log', level=logging.DEBUG)

thread_pool = ProcessPoolExecutor(3)

class NoAvailableRunes(Exception):
    pass


class NotAvailableSets(Exception):
    pass


BUILD_DIRECTIONS = list(permutations((2, 4, 6, 1, 3, 5)))


def assemble(runes, slots, build: Build) -> Build:
    slot = slots[0]

    next_builds = sorted(
        [(r.set, build.equip(r)) for r in runes[slot] if build.is_suitable(r)],
        key=lambda pair: pair[1].value,
        reverse=True,
    )

    logging.info('num builds # {}'.format(len(next_builds)))

    if len(next_builds):

        builds_by_sets = {}
        # todo: max sets = sets include + 3
        allowed_sets = set()
        for rune_set in build.preset.allowed_sets:
            if rune_set.name != '*' and rune_set not in build.preset.excluded_sets:
                allowed_sets.add(rune_set.name)

        sets_count = sum([1 if rune_set != '*' else 3 for rune_set in allowed_sets])

        # if no broken sets ????
        # max_sets
        for rune_set, next_build in next_builds:
            if builds_by_sets.get(rune_set) is None and sets_count > 0:
                builds_by_sets[rune_set] = next_build

            if len(builds_by_sets.keys()) >= sets_count:
                sets_count -= 1

        if len(slots[1:]) > 0:
            best_build = build
            for next_build in builds_by_sets.values():
                try:
                    next_build = assemble(
                        runes=runes,
                        slots=slots[1:],
                        build=next_build
                    )

                    best_build = pick_best(next_build, best_build) if next_build else best_build

                except NoAvailableRunes:
                    continue

            return best_build
        else:
            return reduce(
                lambda a, b: pick_best(a, b),
                builds_by_sets.values()
            )

    raise NoAvailableRunes('No suitable runes for slot {}'.format(slot))


class BuildStrategy(object):

    def __init__(self, stat2, stat4, stat6, procs={}):
        self._stats = (stat2, stat4, stat6)
        self._procs = procs

        self._MIN_VALUABLE_PROCS = math.ceil(54 / self.procs_required) if self.procs_required else 0
        self._STATS_REQ = list(reversed(sorted(procs.items(), key=lambda x: x[1])))

    def runes(self):
        return self._stats

    def count(self, stat):
        return self._stats.count(stat)

    @property
    def procs(self):
        return self._procs

    @property
    def procs_required(self):
        return int(sum(map(math.fabs, self._procs.values())))

    def __eq__(self, other):
        return ''.join(self._stats) == ''.join(other._stats)

    def __iter__(self):
        return self._stats.__iter__()

    def __repr__(self):
        return '{}-{}-{}/{}'.format(
            self._stats[0],
            self._stats[1],
            self._stats[2],
            self.procs_required,
        )

    def assemble(self, preset, runes) -> Build:
        print('building {} with strategy {}'.format(preset.monster.name, self))

        strategy_runes = {
            1: list([r for r in runes[1] if self.is_suitable(r)]),
            2: list([r for r in runes[2] if self.is_suitable(r)]),
            3: list([r for r in runes[3] if self.is_suitable(r)]),
            4: list([r for r in runes[4] if self.is_suitable(r)]),
            5: list([r for r in runes[5] if self.is_suitable(r)]),
            6: list([r for r in runes[6] if self.is_suitable(r)]),
        }
        best_build = Build(preset)

        if self.can_build(strategy_runes):

            futures = []
            for build_order in BUILD_DIRECTIONS:
                futures.append(
                    thread_pool.submit(
                        assemble,
                        runes=strategy_runes,
                        slots=build_order,
                        build=Build(preset)
                    )
                )

            for next_build in as_completed(futures):
                best_build = pick_best(best_build, next_build.result())

            return best_build
        else:
            print('cant build this monster using {} strategy'.format(self))

        return best_build

    def can_build(self, runes):
        return bool(len(runes[2])) and \
               bool(len(runes[4])) and \
               bool(len(runes[6])) and \
               bool(len(runes[1])) and \
               bool(len(runes[3])) and \
               bool(len(runes[5]))

    def is_suitable(self, rune: Rune):
        if rune.slot in (2, 4, 6):
            if not self._stats[int(rune.slot / 2) - 1] in rune.primary.name:
                return False

        procs = 0
        for stat in self._STATS_REQ:
            procs += rune.procs.get(stat[0], 0)

        return procs >= 4


def find_strategies(preset: Preset) -> List[BuildStrategy]:
    slot_2_stats = ('spd', 'hp', 'atk', 'def')
    slot_4_stats = ('cr', 'cd', 'hp', 'atk', 'def')
    slot_6_stats = ('res', 'acc', 'hp', 'atk', 'def')

    required_stats = list(stat.name for stat in preset.stats)

    useful_2_slot = list(stat for stat in required_stats if (stat in slot_2_stats or stat + '%' in slot_2_stats))
    useful_4_slot = list(stat for stat in required_stats if (stat in slot_4_stats or stat + '%' in slot_4_stats))
    useful_6_slot = list(stat for stat in required_stats if (stat in slot_6_stats or stat + '%' in slot_6_stats))

    results = []
    for stat_2 in useful_2_slot:
        for stat_4 in useful_4_slot:
            for stat_6 in useful_6_slot:
                s = BuildStrategy(
                    stat_2, stat_4, stat_6,
                    _count_procs(
                        preset.monster.stats,
                        preset.stats,
                        (stat_2, stat_4, stat_6)
                    )
                )

                # there are max 54 procs on 6 legendary runes with prefixes
                # if s not in results and s.procs_required <= 54:
                if s.procs_required <= 54:
                    results.append(s)

    return sorted(results, key=lambda b: b.procs_required)


def _count_procs(base_stats, expected_stats, runes246):
    procs = {}
    for stat in expected_stats:
        base = base_stats.get(stat.name)
        if stat.name in ('hp', 'def', 'atk'):
            main_stat = MAX_VALUES['6'][stat.name + '%']['max'] * base / 100 if stat.name in runes246 else 0
            procs[stat.name] = math.ceil(
                (stat.condition.value - base - MAX_VALUES['6'][stat.name]['max'] - main_stat * runes246.count(
                    stat.name)) / (
                        base / 100 * PROCS[6][stat.name + '%']['max'])
            )
        else:
            main_stat = MAX_VALUES['6'][stat.name]['max'] if stat.name in runes246 else 0
            procs[stat.name] = math.ceil(
                (stat.condition.value - base - main_stat * runes246.count(stat.name)) / PROCS[6][stat.name]['max']
            )

    return procs



def pick_best(build_a: Build, build_b: Build, focus_stat:str = 'avg') -> Build:
    stats_fulfilled_a = sum(1 for v in build_a.stat_value if v >= 1)
    stats_fulfilled_b = sum(1 for v in build_b.stat_value if v >= 1)

    if stats_fulfilled_a > stats_fulfilled_b:
        return build_a
    elif stats_fulfilled_a < stats_fulfilled_b:
        return build_b
    else:

        return build_a if build_a.value > build_b.value else build_b


class RuneManager(object):
    def __init__(self, runes=[]):
        self._runes = runes
        self._restrictions = {}

    def optimize(self, presets=()):
        builds = []
        # add restrictions
        for preset in presets:
            # try:
                yield self._find_build(preset)
                # builds.append(self._find_build(preset))
            # except Exception as e:
            #     print(e)
            #     pass
        # return builds

    def _find_build(self, preset):

        suitable_runes = [rune for rune in self._runes if not rune.is_locked and rune.set in preset.allowed_sets]

        runes_graph = {
            1: list([r for r in suitable_runes if r.slot == 1]),
            2: list([r for r in suitable_runes if r.slot == 2]),
            3: list([r for r in suitable_runes if r.slot == 3]),
            4: list([r for r in suitable_runes if r.slot == 4]),
            5: list([r for r in suitable_runes if r.slot == 5]),
            6: list([r for r in suitable_runes if r.slot == 6]),
        }

        best_build = Build(preset)
        all_strategies = find_strategies(preset)
        procs_per_strategy = sorted(set([s.procs_required for s in all_strategies]))[:2]
        build_strategies = [s for s in all_strategies if s.procs_required in procs_per_strategy]

        for strategy in build_strategies:
            try:
                best_build = pick_best(best_build, strategy.assemble(preset, runes_graph))
            except Exception as err:
                print('err', err)
                traceback.print_exc()

        best_build.lock()

        return best_build
