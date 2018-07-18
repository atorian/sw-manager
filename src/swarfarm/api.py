import sys
from enum import Enum
from typing import NamedTuple, List, Optional, Dict, Union
import simplejson as json
import requests

URL = 'https://swarfarm.com/api/v2/monsters/'


def fetch_units(url):
    response = requests.get(url)
    data = response.json()
    return data['results'], data['next']


def export_units():
    pass


class Element(str, Enum):
    WIND = 'wind'
    FIRE = 'fire'
    WATER = 'water'
    LIGHT = 'light'
    DARK = 'dark'


class Stat(str, Enum):
    HP = 'hp'
    ATK = 'atk'
    DEF = 'def'
    SPD = 'spd'
    CR = 'cr'
    CD = 'cd'
    RES = 'res'
    ACC = 'acc'

class Target(str, Enum):
    SELF = 'self'
    NOT_SELF = 'not_self'
    ALLY = 'ally'
    AOE_ALLY = 'aoe_ally'
    ENEMY = 'enemy'
    AOE_ENEMY = 'aoe_enemy'

class Area(str, Enum):
    ARENA = 'arena'
    GUILD = 'guild'
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


class Debuf(NamedTuple):
    duration: int
    target: Optional[Target] = None
    irresistible: bool = False
    chance: Optional[int] = 100


class Dot(Debuf):
    duration: int
    target: Optional[Target] = None
    irresistible: bool = False
    chance: Optional[int] = 100
    quantity: int = 1


class Buf(NamedTuple):
    duration: int
    target: Optional[Target] = None


class Heal(NamedTuple):
    amount: int
    target: Optional[Target] = None


class Iteration(NamedTuple):
    enemy_dmg: Optional[Union[PhisicalDmg, str]] = None
    atb_boost: Optional[Union[AtbBoost, int]] = None
    cleanse: Optional[Union[Cleanse, "all"]] = None
    strip: Optional[Union[Strip, "all"]] = None
    haste: Optional[Union[Buf, int]] = None
    def_break: Optional[Union[Debuf, int]] = None
    atk_break: Optional[Union[Debuf, int]] = None
    unrecoverable: Optional[Union[Debuf, int]] = None
    stun: Optional[Union[Debuf, int]] = None
    dot: Optional[Debuf] = None
    heal: Optional[Heal] = None
    atk_buf: Optional[Buf] = None
    def_buf: Optional[Buf] = None
    cr_buf: Optional[Buf] = None
    anti_cr: Optional[Buf] = None
    glancing: Optional[Debuf] = None
    branding: Optional[Debuf] = None


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
    'HP': Stat.HP,
    'Attack Power': Stat.ATK,
    'Defense': Stat.DEF,
    'Critical Rate': Stat.CR,
    'Critical DMG': Stat.CD,
    'Accuracy': Stat.ACC,
    'Resistance': Stat.RES,
    'Attack Speed': Stat.SPD,
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


BUFFS ={
    'Increase SPD': 'haste',
    "Increase DEF": 'def_buf',
    'Increase ATK': 'atk_buf',
    'Increase CRI Rate': 'crit_buf',
    'Increase CRI Resist': 'anti_crit',
    'Recovery': 'hot',
    'Counter': 'counter',
    'Revenge': 'revenge',
    'Immunity': 'immunity',
    'Invincible': 'invincibility',
    'Reflect DMG': 'reflect',
    'Shield': 'shield',
    'Endure': 'endure',
    'Defend': 'defend',
    'Protect Soul': 'soul_protection',
}
DEBUFFS = {
    'Decrease ATK': 'atk_break',
    'Decrease DEF': 'def_break',
    'Decrease SPD': 'slow',
    'Disturb HP Recovery': 'unrecoverable',
    'Continuous DMG': 'dot',
    'Glancing Hit': 'glancing',
    'Beneficial Effects Blocked': 'block_buf',
    'Bomb': 'bomb',
    'Provoke':'provoke',
    'Sleep': 'sleep',
    'Freeze': 'freeze',
    'Stun': 'stun',
    'Silence':'silence',
    'Brand': 'brand',
    'Oblivious':'oblivious'
}

attribute = (
    'Ignore DEF',
    'AOE',
)

other = {
    'Increase ATB': 'atb_boost',
    'Decrease ATB': 'atb_reduce',
    'Cleanse': 'cleanse',
    'Heal': 'heal',
    'Revive': 'revive',
    'Remove Buff': 'strip',
    'Additional Turn': 'grant_turn',
    'Detonate Bomb': 'detonate',
    'Steal Buff': 'steal_buf',
    'Reduce Cooltime': 'reduce_cooltime',
    'Increase Cooltime': 'increase_cooltime',
    'Self-Heal': 'heal',
    # 'Multiple Hits',
    # 'Auto Effect':,
    'Anti-Revive': 'anti_revive',
    'Transfer Debuff': 'transfer_debuf',
    'Additional Attack': 'extra_hit',
    'Increase Buff Duration': 'increase_buff_duration',
    'Decrease Debuff Duration': 'decrease_buff_duration',
    'Self-Harm',
    'Elemental Advantage',
    'Ally Attack',
    'Destroy HP',
    'Team Attack',
    'Decrease Damage',
    'Increase Debuff Duration',
    'Reduce incoming DMG',
    'Redistribute HP',
    'Prevent Resurrect',
    'Threat',
    'Ignore Damage Reduction',
    'Guaranteed Critical Hit',
    'Debuff Bonus Damage',
}

def map_interation(skill):
    target = Target.ENEMY if not skill['aoe'] else Target.AOE_ENEMY

    effects = {}

    if any(skill["scales_with"]):
        effects['enemy_dmg'] = map_multiplier(skill['multiplier_formula'])

    for effect in skill['effects']:
        if effect['effect']['name'] == 'Increase ATB':
            effects['atb_boost'] = effect['quantity']
        elif effect['effect']['name'] == 'Cleanse':
            effects['cleanse'] = 'all' if effect['all'] else Cleanse(amount=effect['quantity'])
        elif effect['effect']['name'] == 'Remove Buff':
            effects['strip'] = 'all' if effect['all'] else Strip(amount=effect['quantity'])
        elif effect['effect']['name'] == 'Increase SPD':
            effects['haste'] = effect['quantity']
        elif effect['effect']['name'] == 'Decrease DEF':
            effects['def_break'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance']
            )
        elif effect['effect']['name'] == 'Decrease ATK':
            effects['atk_break'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Continuous DMG':
            effects['dot'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Stun':
            effects['stun'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Disturb HP Recovery':
            effects['unrecoverable'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Heal':
            effects['heal'] = Heal(
                amount=effect['quantity'],
                target=target
            )
        elif effect['effect']['name'] == 'Increase ATK':
            effects['atk_buf'] = Buf(
                duration=effect['quantity'],
                target=target
            )
        elif effect['effect']['name'] == 'Increase DEF':
            effects['def_buf'] = Buf(
                duration=effect['quantity'],
                target=target
            )
        elif effect['effect']['name'] == 'Increase CRI Rate':
            effects['cr_buf'] = Buf(
                duration=effect['quantity'],
                target=target
            )
        elif effect['effect']['name'] == 'Glancing Hit':
            effects['glancing'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Debuff Bonus Damage':
            effects['branding'] = Debuf(
                duration=effect['quantity'],
                chance=None if effect['chance'] == 100 else effect['chance'],
                target=target
            )
        elif effect['effect']['name'] == 'Increase CRI Resist':
            effects['branding'] = Buf(
                duration=effect['quantity'],
                target=target
            )
        else:
            raise Exception('Uknown effect {}'.format(str(effect['effect'])))

    return Iteration(**effects)


def map_skill(skill: dict) -> Union[Skill, Passive]:
    target = Target.ENEMY if not skill['aoe'] else Target.AOE_ENEMY

    cooldown = skill['cooltime'] if skill['cooltime'] else None
    if 'Cooltime Turn -1' in skill['level_progress_description']:
        cooldown -= skill['level_progress_description'].count('Cooltime Turn -1')

    try:
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
    except Exception as e:
        print(e)
        print(skill)
        sys.exit()


def fetch_skill(id):
    return requests.get(f"https://swarfarm.com/api/v2/skills/{id}/").json()


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

    next = URL
    units = []

    while next:
        data, next = fetch_units(next)
        units.extend(
            [map_unit(u) for u in data if u['can_awaken'] and u['is_awakened'] and not u['archetype'] == 'Material']
        )

    print(json.dumps({u.meta.name:u for u in units}, namedtuple_as_object=True))
