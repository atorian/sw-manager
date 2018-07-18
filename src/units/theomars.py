from preset import Preset, Stat, Around, Between
from rune import RuneSets

theomars = Preset('Theomars')
theomars.include(RuneSets.Violent, RuneSets.Will)
theomars.expect(
    Stat('spd', Between(min=190, max=210)),
    Stat('cr', Between(min=60, max=70)),
    Stat('cd', Around(150)),
    Stat('atk', Around(2000)),
    Stat('hp', Around(20000)),
)
