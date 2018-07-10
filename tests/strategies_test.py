import unittest
from units import theomars, searra, copper
from rune_manager import find_strategies, BuildStrategy


class TestStrategies(unittest.TestCase):

    def test_find_theo_strategies(self):
        strategies = find_strategies(theomars)
        print('theomars', strategies)
        self.assertIn(BuildStrategy('spd', 'cd', 'hp'), strategies)
        self.assertIn(BuildStrategy('spd', 'cd', 'atk'), strategies)

    def test_find_searra_strategies(self):
        strategies = find_strategies(searra)
        print('searra', strategies)
        self.assertIn(BuildStrategy('spd', 'hp', 'atk'), strategies)
        self.assertIn(BuildStrategy('atk', 'hp', 'atk'), strategies)

    def test_find_copper_strategies(self):
        strategies = find_strategies(copper)
        print('copper', strategies)
        self.assertIn(BuildStrategy('def', 'cd', 'def'), strategies)
