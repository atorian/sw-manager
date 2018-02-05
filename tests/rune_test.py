import unittest
from rune import Rune, MetaInfo, Stats, RuneStat, RUNE_SETS

class TestRune(unittest.TestCase):

    def test_Rune(self):
        meta = MetaInfo(slot=1, set=RUNE_SETS['Violent'], lvl=9, grade=6)

        stats = Stats(
            primary=RuneStat('atk', 94),
            prefix=RuneStat('cr', 4),
            sub_stats=(
                RuneStat('acc', 6),
                RuneStat('atk%', 11),
                RuneStat('cd', 12),
            ),
        )
        rune = Rune(1, meta, stats)

        self.assertEqual(94, rune['atk'])
        self.assertEqual(6, rune['acc'])
        self.assertEqual(11, rune['atk%'])
        self.assertEqual(12, rune['cd'])
        self.assertEqual(4, rune['cr'])
        self.assertEqual(160, rune.as_lvl_15()['atk'])
        self.assertEqual(118, rune.as_lvl_12()['atk'])
