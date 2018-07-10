class Team(object):
    def __init__(self, prio, members, lead=None, speed_sync=False):
        self._members = members
        self._prio = prio
        self._lead = lead
        self._speed_sync = speed_sync

    @property
    def priority(self):
        return self._prio

    @property
    def members(self):
        return self._members


class TeamManager:

    def __init__(self, teams=None):
        self._teams = teams if teams is not None else []

    def add_team(self, *units, prio=1, lead=None, speed_sync=False):
        self._teams.append(
            Team(prio, units, lead=lead, speed_sync=speed_sync)
        )

    def branch(self):
        return TeamManager(self._teams)

    def prioritize(self):
        prios = {}
        for team in self._teams:
            for unit in team.members:
                prios[unit] = prios.get(unit, 0) + team.priority

        return sorted(prios, key=prios.__getitem__, reverse=True)

