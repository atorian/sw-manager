from rune import Rune, RuneBuilder
import json

stat_names = {
    1: 'hp',
    2: 'hp%',
    3: 'atk',
    4: 'atk%',
    5: 'def',
    6: 'def%',
    8: 'spd',
    9: 'cr',
    10: 'cd',
    11: 'res',
    12: 'acc',
}

rune_sets = {
    1: "Energy",
    2: "Guard",
    3: "Swift",
    4: "Blade",
    5: "Rage",
    6: "Focus", 
    7: "Endure", 
    8: "Fatal", 
    10: "Despair", 
    11: "Vampire", 
    13: "Violent", 
    14: "Nemesis", 
    15: "Will", 
    16: "Shield", 
    17: "Revenge", 
    18: "Destroy", 
    19: "Fight", 
    20: "Determination", 
    21: "Enhance", 
    22: "Accuracy", 
    23: "Tolerance", 
}

classes = {
    1: 'common',
    2: 'magic',
    3: 'rare',
    4: 'hero',
    5: 'legendary',
}

rune_cls = {
    5: 'L',
    4: 'H',
    3: 'R',
    2: 'M',
    1: 'C',
}


def _stat_name(stat):
    stat_id = stat[0]
    return stat_names[stat_id]


def _stat_val(stat):
    return int(stat[1]) + int(stat[3])


def map_rune(raw) -> Rune:
    builder = RuneBuilder()

    builder.id(int(raw['rune_id']))

    builder.slot(int(raw['slot_no']))
    builder.set(rune_sets[int(raw['set_id'])])
    builder.level(raw['upgrade_curr'])
    builder.grade(raw["class"])
    builder.cls(rune_cls[raw["rank"]])

    builder.add_primary_stat(
        stat_names[raw['pri_eff'][0]],
        int(raw['pri_eff'][1])
    )

    if raw['prefix_eff'][0]:
        builder.add_prefix_stat(
            stat_names[raw['prefix_eff'][0]],
            raw['prefix_eff'][1]
        )

    for stat in raw['sec_eff']:
        builder.add_sub_stat(
            _stat_name(stat),
            _stat_val(stat),
            switched=stat[2] == 1,
            grind=int(stat[3])
        )

    return builder.make()


def load_profile(path):
    with open(path, 'r') as f:
        profile = json.load(f)

    runes = list(map(map_rune, profile['runes']))

    for unit in profile['unit_list']:
        runes.extend(map(map_rune, unit['runes']))

    return runes
