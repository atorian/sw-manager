from preset import Preset, Stat, Around, Between, Max
from rune import RUNE_SETS
from monster import Monster

theomars = Preset(monster=Monster(name='Theomars', stats={
    'hp': 10875,
    'atk': 823,
    'def': 593,
    'spd': 100,
    'cr': 30,
}))
theomars.include(RUNE_SETS['Violent'], RUNE_SETS['Will'])
theomars.expect(
    Stat('spd', Between(min=190, max=210)),
    Stat('cr', Between(min=60, max=70)),
    Stat('cd', Around(150)),
    Stat('atk', Around(2000)),
    Stat('hp', Around(20000)),
)
