from preset import Preset, Stat, Min, Around, Between
from rune import RuneSets

copper = Preset('Copper')
copper.include(RuneSets.Guard, RuneSets.Blade)
copper.exclude(RuneSets.Violent)
copper.expect(
    Stat('cr', Between(70, 80)),
    Stat('cd', Around(250)),
    Stat('def', Min(2000)),
    Stat('atk', Around(800)),
)
