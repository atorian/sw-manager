from preset import Preset, Stat, Min, Around, Between
from rune import RUNE_SETS
from monster import Monster

copper = Preset(monster=Monster(name='copper', stats={
    'hp': 9555,
    'atk': 483,
    'def': 692,
    'spd': 98,
    'res': 40
}))
copper.include(RUNE_SETS['Guard'], RUNE_SETS['Blade'])
copper.exclude(RUNE_SETS['Violent'])
copper.expect(
    Stat('cr', Between(70, 80)),
    Stat('cd', Around(250)),
    Stat('def', Min(2000)),
    Stat('atk', Around(800)),
)
