from preset import Preset, Stat, Min, Around, Between
from rune import RUNE_SETS
from monster import Monster

searra = Preset(monster=Monster(name='Searra', stats={
    'hp': 10875,
    'atk': 801,
    'def': 615,
    'spd': 100,
    'acc': 25
}))
searra.include(RUNE_SETS['Violent'], RUNE_SETS['Will'])
searra.expect(
    Stat('spd', Between(min=205, max=220)),  # 105%
    Stat('atk', Around(2000)), # 150%
    Stat('hp', Around(20000)), # 97%
    Stat('acc', Between(min=60, max=85))
)
