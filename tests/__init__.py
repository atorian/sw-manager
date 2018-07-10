from random import randint

from rune import RuneBuilder


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
    builder.cls('R')
    builder.add_primary_stat(*primary)
    if prefix:
        builder.add_prefix_stat(*prefix)

    for stat in sub_stats:
        builder.add_sub_stat(*stat)

    return builder.make()
