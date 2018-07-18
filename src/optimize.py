from rune_manager import RuneManager
from swarfarm import load_profile
import units
import time
from pathlib import Path

if __name__ == "__main__":

    file = Path() / 'atorian-1757319.json'
    print(file.absolute())
    runes = load_profile(file.absolute())

    manager = RuneManager(runes)

    start = time.time()
    presets = [
        units.searra,
        units.theomars,
        units.copper,
    ]

    for build in manager.optimize(presets):
        print(build.monster.name)
        print('hp', build.stats['hp'])
        print('atk', build.stats['atk'])
        print('def', build.stats['def'])
        print('spd', build.stats['spd'])
        print('cr', build.stats['cr'])
        print('cd', build.stats['cd'])
        print('res', build.stats['res'])
        print('acc', build.stats['acc'])

        for rune in sorted([r for r in build.runes if r], key=lambda r: r.slot):
            if rune:
                print(rune.slot, rune.grade * '\u2b50', rune.set.name)
                print(str(rune.stats.primary))
                if rune.stats.prefix:
                    print(str(rune.stats.prefix))
                else:
                    print('-')

                for stat in rune.stats.sub_stats:
                    print(str(stat))

        end = time.time()
        print('time', end - start)
        print('-----')
        start = time.time()
