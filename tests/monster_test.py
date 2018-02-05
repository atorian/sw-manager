import unittest
from monster import Monster

class TestUnit(unittest.TestCase):

    def test_Monster_name(self):
        unit = Monster(name='Copper', stats={
            'hp': 9555,
            'atk': 483,
            'def': 692,
            'spd': 98,
            'res': 40
        })
        self.assertEqual(unit.name, 'Copper')


if __name__ == '__main__':
    unittest.main()
