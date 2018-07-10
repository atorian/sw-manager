import unittest
from swarfarm.profile_reader import load_profile, map_rune

class TestProfileLoader(unittest.TestCase):

    def test_loader(self):
        runes = load_profile('/Users/hcdeveloper/src/swop/atorian-1757319.json')


        filtered = list([r for r in runes if r['spd'] == 27 and r.slot == 4])
        self.assertTrue(len(filtered), 1)
        self.assertEqual(1108, len(runes))


    def test_rune_parser_1(self):
        raw_rune = {
          "rune_id": 3136359513,
          "wizard_id": 1757319,
          "occupied_type": 1,
          "occupied_id": 2516851675,
          "slot_no": 1,
          "rank": 5,
          "class": 6,
          "set_id": 13,
          "upgrade_limit": 15,
          "upgrade_curr": 15,
          "base_value": 662530,
          "sell_value": 33126,
          "pri_eff": [
            3,
            160
          ],
          "prefix_eff": [
            0,
            0
          ],
          "sec_eff": [
            [
              10,
              6,
              0,
              0
            ],
            [
              4,
              20,
              0,
              4
            ],
            [
              8,
              12,
              0,
              3
            ],
            [
              9,
              5,
              0,
              0
            ]
          ],
          "extra": 0
        }

        rune = map_rune(raw_rune)

        self.assertEqual(3136359513, rune.id)
        self.assertEqual('Violent', rune.set.name)
        self.assertEqual(24, rune['atk%'])
        self.assertEqual(15, rune['spd'])
        self.assertEqual(5, rune['cr'])
        self.assertEqual(6, rune['cd'])

    def test_rune_parser_2(self):
        raw_rune = {
          "rune_id": 3820232250,
          "wizard_id": 1757319,
          "occupied_type": 1,
          "occupied_id": 1474153324,
          "slot_no": 3,
          "rank": 5,
          "class": 6,
          "set_id": 3,
          "upgrade_limit": 15,
          "upgrade_curr": 12,
          "base_value": 380400,
          "sell_value": 19020,
          "pri_eff": [
            5,
            118
          ],
          "prefix_eff": [
            6,
            6
          ],
          "sec_eff": [
            [
              11,
              6,
              1,
              0
            ],
            [
              8,
              16,
              0,
              0
            ],
            [
              2,
              12,
              0,
              5
            ],
            [
              12,
              5,
              0,
              0
            ]
          ],
          "extra": 0
        }

        rune = map_rune(raw_rune)

        self.assertEqual(3820232250, rune.id)
        self.assertEqual('Swift', rune.set.name)
        self.assertEqual(6, rune['def%'])
        self.assertEqual(6, rune['res'])
        self.assertEqual(16, rune['spd'])
        self.assertEqual(17, rune['hp%'])
        self.assertEqual(5, rune['acc'])


    def test_rune_parser_2(self):
        raw_rune = {
          "rune_id": 3820232250,
          "wizard_id": 1757319,
          "occupied_type": 1,
          "occupied_id": 1474153324,
          "slot_no": 3,
          "rank": 5,
          "class": 6,
          "set_id": 3,
          "upgrade_limit": 15,
          "upgrade_curr": 12,
          "base_value": 380400,
          "sell_value": 19020,
          "pri_eff": [
            5,
            118
          ],
          "prefix_eff": [
            6,
            6
          ],
          "sec_eff": [
            [
              11,
              6,
              1,
              0
            ],
            [
              8,
              16,
              0,
              0
            ],
            [
              2,
              12,
              0,
              5
            ],
            [
              12,
              5,
              0,
              0
            ]
          ],
          "extra": 0
        }

        rune = map_rune(raw_rune)

        self.assertEqual(3820232250, rune.id)
        self.assertEqual('Swift', rune.set.name)
        self.assertEqual(6, rune['def%'])
        self.assertEqual(6, rune['res'])
        self.assertEqual(16, rune['spd'])
        self.assertEqual(17, rune['hp%'])
        self.assertEqual(5, rune['acc'])
