from preset import Preset, Stat, Min, Around
from rune import RUNE_SETS
from monster import Monster

copper = Preset(monster=Monster(name='copper', stats={
    'hp': 9555,
    'atk': 483,
    'def': 692,
    'spd': 98,
    'res': 40
}))
copper.include(RUNE_SETS['Guard'])
copper.exclude(RUNE_SETS['Violent'])
copper.expect(
    Stat('cr', Min(70)),
    Stat('cd', Around(200)),
    Stat('def', Min(2000)),
    Stat('res', Around(70)),
)
