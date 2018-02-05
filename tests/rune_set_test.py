import unittest
from rune import RuneSet

class TestRune(unittest.TestCase):

    def test_RuneSet_comparison_1(self):
        vio = RuneSet('Violent', 2)
        will = RuneSet('Will', 2)
        any = RuneSet('*', 2)
        combo = [vio, any]

        self.assertEqual(1, combo.count(will))

    def test_RuneSet_comparison_2(self):
        will = RuneSet('Will', 2)
        combo = [RuneSet('*', 2)]

        self.assertTrue(RuneSet('*', 2) in combo)
        self.assertTrue(will in combo)

    def test_RuneSet_removal(self):
        vio = RuneSet('Violent', 2)
        will = RuneSet('Will', 2)
        any = RuneSet('*', 2)
        combo = [vio, any]
        combo.remove(will)

        self.assertEqual(0, combo.count(will))
        self.assertEqual(1, len(combo))
