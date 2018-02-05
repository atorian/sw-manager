from .profile_reader import load_profile
import requests


def load_monster(name):
    r = requests.get('https://swarfarm.com/api/v2/monsters', params={name: name})

    print(r.json())
