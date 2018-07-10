from typing import NamedTuple
import ./units

'''
AO
AD
GWO
GWD
Raid
Beast
'''

class Team(object):

    def __init__(self, members, turn_order, lead, speed_sync=False):
        self._members = members
        self._order = turn_order
        self._lead = lead
        self._speed_sync = speed_sync

    def is_ok(self, *args):
        pass


slow_bombers = Team(
    members=('tiana','galleon', 'malaka', 'searra'),
    lead='spd_24',
    spead_sync=True
)

fast_bombers = Team(
    members=('searra', 'kabilla', 'tiana', 'malaka'),
    turn_order=('kabilla', 'tiana', 'malaka', 'searra'),
    lead='searra',
    speadSync=True
)


def either_team(*args):
    pass


''' 
raid5 1 team, 
fire_beast,
wind_beast,
water_beast,
'''

manager = Optimizer(runes)
manager.add_unit(units.copper, select.MaxDmg(copper.skills[3]))
manager.add_unit(units.searra)
manager.add_unit(units.theo)
manager.add_unit(units.chasun)
manager.add_unit(units.orion, select.MaxStat('spd'))


manager.add_team(slow_bombers)
manager.add_team(fast_bombers, usage=2)
manager.add_team(
    Team(
        members=('searra', 'orion', 'eladriel'),
        turn_order('orion', 'searra', 'eladriel')
    )
)
manager.add_team(
    Team(
        members=('theo', 'vela', 'chasun'),
        turn_order=('chasun', 'theo', 'vela')
    )
)
manager.add_team(
    Team(
        members=('theo', 'vela', 'chasun'),
        turn_order=('chasun', 'theo', 'vela')
    )
)
manager.add_team(
    Team(
        members=('lushen', 'fuco', 'rigel', 'collean', 'xio ling'),
        turn_order=('collean', 'lushen', 'xio ling', 'fuco', 'rigel'),
        lead='lushen'
    )
)
manager.add_team(
    either_team(
        Team(members=('khmun', 'theo', 'rakuni'), turn_order=('theo', 'rakuni', 'khmun')),
        Team(members=('khmun', 'theo', 'rakuni'), turn_order=('rakuni', 'theo', 'khmun'))
    )
)
manager.add_team(
    Team(members=('vela', 'emma', 'buldozer'))
)
manager.add_team(
    Team(members=('racuni', 'emma', 'buldozer'))
)
manager.add_team(
    Team(members=('searra', 'chasun', 'hvadam'))
)
manager.add_team(
    either_team(
        Team(members=('khmun', 'theo', 'rakuni'), turn_order=('theo', 'rakuni', 'khmun')),
        Team(members=('khmun', 'theo', 'rakuni'), turn_order=('rakuni', 'theo', 'khmun'))
    )
)
manager.add_team(
    Team(
        members=('geminy', 'orion', 'kamya'),
        turn_order=('orion', 'geminy', 'kamya'),
        lead='geminy',
        speed_sync=true
    )
)



print(manager.priorities())


# builds = manager.optimize()

