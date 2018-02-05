from rune_manager import RuneManager
from swarfarm import load_profile
import units
import time

runes = load_profile('/Users/hcdeveloper/src/swop/atorian-1757319.json')

manager = RuneManager(runes)
# manager.add_monster(units.copper)
manager.add_monster(units.searra)

start = time.time()

builds = list(manager.optimize())

end = time.time()
print('time', end - start)
# print('Copper')
# print(builds[0])

build = builds[0]
print('Searra')
print('hp', build.hit_points)
print('atk', build.attack)
print('def', build.defense)
print('spd', build.speed)
print('cr', build.crit_rate)
print('cd', build.crit_dmg)
print('res', build.resistance)
print('acc', build.accuracy)

print('')
#
# for rune in build.runes:
#     print(rune.slot, rune.grade * '\u2b50', rune.set.name)
#     print(str(rune.stats.primary))
#     if rune.stats.prefix:
#         print(str(rune.stats.prefix))
#     else:
#         print('-')
#
#     for stat in rune.stats.sub_stats:
#         print(str(stat))

