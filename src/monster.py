


class Monster(object):
    def __init__(self, name, stats):
        self._name = name
        self._stats = {
            'cr': 15,
            'cd': 50,
            'res': 15,
            'acc': 0,
            **stats
        }

    @property
    def name(self):
        return self._name

    @property
    def stats(self):
        return self._stats
