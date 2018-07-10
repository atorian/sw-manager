import unittest
from team import TeamManager


class TestStrategies(unittest.TestCase):

    def test_sets_priorities(self):
        manager = TeamManager()

        manager.add_team('searra', 'tiana', 'galleon', 'malaka', prio=10, lead='spd_24', speed_sync=True)
        manager.add_team('searra', 'tiana', 'malaka', prio=10, lead='spd_24', speed_sync=True)
        manager.add_team('galleon', 'tiana', 'zairos', prio=5, lead='spd_24', speed_sync=True)
        manager.add_team('searra', 'eladriel', 'chasun', lead='wind_hp_50')

        self.assertEqual(manager.prioritize()[0:5], ['tiana', 'searra', 'malaka', 'galleon', 'zairos'])
