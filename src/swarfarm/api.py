from collections import namedtuple
from enum import Enum
from typing import NamedTuple, List, Optional, Dict, Union

import requests

URL = 'https://swarfarm.com/api/v2/monsters/'


def fetch_units(page=None):
    params = {'page': page} if page else None
    response = requests.get(URL, params=params)
    data = response.json()
    return data['results'], data['next']


def export_units():
    pass


class Element(Enum):
    WIND = 'wind'
    FIRE = 'fire'
    WATER = 'water'
    LIGHT = 'light'
    DARK = 'dark'


class Stat(Enum):
    HP = 'hp'
    ATK = 'atk'
    DEF = 'def'
    SPD = 'spd'
    CR = 'cr'
    CD = 'cd'
    RES = 'res'
    ACC = 'acc'


class Target(Enum):
    SELF = 'self'
    NOT_SELF = 'not_self'
    ALLY = 'ally'
    AOE_ALLY = 'aoe_ally'
    ENEMY = 'enemy'
    AOE_ENEMY = 'aoe_enemy'


class Area(Enum):
    ARENA = 'arena'
    GUILD_WAR = 'guild_war'
    DUNGEON = 'dungeon'
    ELEMENT = 'element'


class LeadAbility(NamedTuple):
    element: Optional[Element]
    stat: Stat
    area: Optional[Area]
    value: float


class Meta(NamedTuple):
    name: str
    element: Element
    image: str


class PhisicalDmg(NamedTuple):
    multiplier: str
    target: Optional[Target]
    ignore_def: bool = False


class AtbBoost(NamedTuple):
    value: int
    target: Optional[Target] = None


class Cleanse(NamedTuple):
    amount: Union[int, "all"]


class Strip(NamedTuple):
    amount: Union[int, "all"]


class Iteration(NamedTuple):
    enemy_dmg: Optional[Union[PhisicalDmg, str]] = None
    atb_boost: Optional[AtbBoost] = None
    cleanse: Optional[Union[Cleanse, "all"]] = None
    strip: Optional[Union[Strip, "all"]] = None


class SkillMeta(NamedTuple):
    name: str
    description: str
    image: str


class Skill(NamedTuple):
    meta: SkillMeta
    cooldown: Optional[int]
    target: Target
    iterations: List[Iteration]


class Passive(NamedTuple):
    id: int


SWARFARM_LEAD_STAT = {
    'Attack Power': Stat.ATK,
    'HP': Stat.HP,
    'Critical Rate': Stat.CR
}

SWARFARM_TARGET = {
    367: Target.ENEMY,
    368: Target.ENEMY,
    582: Target.ENEMY,
    583: Target.ENEMY,
}


class Unit(NamedTuple):
    meta: Meta
    stats: Dict[Stat, int]
    skills: List[Skill]
    lead: LeadAbility

    @property
    def name(self) -> str:
        return self.meta.name

    @property
    def element(self) -> Element:
        return self.meta.element


def map_leader_skill(lead) -> LeadAbility:
    return LeadAbility(
        element=Element(lead['element'].lower()) if lead['element'] else None,
        stat=SWARFARM_LEAD_STAT[lead['attribute']],
        value=int(lead['amount']) / 100,
        area=None if not lead['area'] or lead['area'] == 'General' else Area(lead['area'].lower()),
    )


SWARFARM_MULTIPLIER_PLACEHOLDERS = {
    '{ATK}': 'self.atk',
    '{DEF}': 'self.def',
    '{SPD}': 'self.spd',
    '{HP}': 'self.hp',
    '{TARGET SPD}': 'target.spd',
}

SWARFARM_EFFECTS = {
    'Increase ATB': 'atb_boost',
}


def map_multiplier(formula: str) -> str:
    for source, target in SWARFARM_MULTIPLIER_PLACEHOLDERS.items():
        formula = formula.replace(source, target)

    return formula


def map_interation(skill):
    target = SWARFARM_TARGET[skill['used_on'][0]]
    if target == Target.ENEMY and skill['aoe']:
        target = Target.AOE_ENEMY

    if len(skill['effects']) == 0:
        return Iteration(
            enemy_dmg=map_multiplier(skill['multiplier_formula'])
        )

    effects = {}
    for effect in skill['effects']:
        if effect['effect']['name'] == 'Increase ATB':
            effects['atb_boost'] = AtbBoost(
                value=effect['quantity']
            )
        elif effect['effect']['name'] == 'Cleanse':
            effects['cleanse'] = 'all' if effect['all'] else Cleanse(amount=effect['quantity'])
        elif effect['effect']['name'] == 'Remove Buff':
            effects['strip'] = 'all' if effect['all'] else Strip(amount=effect['quantity'])

    return Iteration(**effects)


def map_skill(skill: dict) -> Union[Skill, Passive]:
    target = SWARFARM_TARGET[skill['used_on'][0]]
    if target == Target.ENEMY and skill['aoe']:
        target = Target.AOE_ENEMY

    cooldown = skill['cooltime'] if skill['cooltime'] else None
    if 'Cooltime Turn -1' in skill['level_progress_description']:
        cooldown -= skill['level_progress_description'].count('Cooltime Turn -1')

    return Skill(
        meta=SkillMeta(
            name=skill['name'],
            description=skill['description'],
            image=skill['icon_filename']
        ),
        cooldown=cooldown,
        target=target,
        iterations=[map_interation(skill)] * skill['hits']
    )


def fetch_skill(id):
    return requests.get('https://swarfarm.com/api/v2/skills/{}/'.format(str(id))).json()


def map_unit(raw_unit):
    return Unit(
        meta=Meta(
            name=raw_unit['name'],
            element=Element(raw_unit['element'].lower()),
            image=raw_unit['image_filename']
        ),
        stats={
            Stat.HP: raw_unit['max_lvl_hp'],
            Stat.ATK: raw_unit['max_lvl_attack'],
            Stat.DEF: raw_unit['max_lvl_defense'],
            Stat.SPD: raw_unit['speed'],
            Stat.CR: raw_unit['crit_rate'],
            Stat.CD: raw_unit['crit_damage'],
            Stat.RES: raw_unit['resistance'],
            Stat.ACC: raw_unit['accuracy'],
        },
        lead=map_leader_skill(raw_unit['leader_skill']) if raw_unit.get('leader_skill') else None,
        skills=[map_skill(fetch_skill(skill)) for skill in raw_unit['skills']]
    )


if __name__ == '__main__':
    data, next = fetch_units()

    units = [map_unit(u) for u in data if u['can_awaken'] and u['is_awakened'] and not u['archetype'] == 'Material']

    print(units)
