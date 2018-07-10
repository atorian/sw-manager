from preset import Preset, Stat, Around, Between
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
    Stat('spd', Between(min=208, max=220)),
    Stat('acc', Between(min=65, max=85)),
    Stat('hp', Around(25000)),
    Stat('atk', Around(2500)),
)

# find all builds where first stat is satissfied
# then of just found find where stat 2 is collected
