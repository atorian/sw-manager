
class TurnOrder(object):
    def __init__(self, members, speed_sync=False):
        pass

class Team(object):

    def __init__(self, members, turn_order=None, lead=None, speed_sync=False):
        self._members = members
        self._order = turn_order
        self._lead = lead
        self._speed_sync = speed_sync

    def is_ok(self, *args):
        pass

class AO(Team):
    def get_prio(self):
        return

class AD(Team):
    pass

class GWO(Team):
    pass

class GWD(Team):
    pass

class Raid(Team):
    pass

class Beast(Team):
    pass

class Cairos(Team):
    pass

class TOA(Team):
    pass
