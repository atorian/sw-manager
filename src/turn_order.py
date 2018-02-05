
class TurnOrder(object):
    def __init__(self, members, speed_sync=False):
        self._members = members
        self._speed_sync = speed_sync

    def is_satisfied(self, builds):
        pass
