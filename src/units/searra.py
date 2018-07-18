from preset import Preset, Stat, Around, Between
from rune import RuneSets

print(RuneSets.Violent)

searra = Preset('Seara')
searra.include(RuneSets.Violent, RuneSets.Will)
searra.expect(
    Stat('spd', Between(min=208, max=220)),
    Stat('acc', Between(min=65, max=85)),
    Stat('hp', Around(25000)),
    Stat('atk', Around(2500)),
)

# find all builds where first stat is satissfied
# then of just found find where stat 2 is collected
