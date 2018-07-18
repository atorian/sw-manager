import unittest

from swarfarm.api import map_unit, LeadAbility, Unit, Meta, Stat, Element, Area, Skill, map_skill, SkillMeta, Target, \
    Iteration, PhisicalDmg, AtbBoost, Cleanse, Strip, Debuf

BERNARD = {
    "id": 368,
    "url": "https://swarfarm.com/api/v2/monsters/368/",
    "com2us_id": 11513,
    "family_id": 11500,
    "name": "Bernard",
    "base_stars": 4,
    "image_filename": "unit_icon_0005_2_4.png",
    "element": "Wind",
    "archetype": "Support",
    "obtainable": True,
    "can_awaken": True,
    "is_awakened": True,
    "awaken_bonus": "Leader Skill",
    "skills": [
        408,
        417,
        418
    ],
    "skill_ups_to_max": 10,
    "leader_skill": {
        "id": 44,
        "url": "https://swarfarm.com/api/v2/leader-skills/44/",
        "attribute": "Attack Power",
        "amount": 30,
        "area": "Element",
        "element": "Wind"
    },
    "homunculus_skills": [],
    "base_hp": 5610,
    "base_attack": 226,
    "base_defense": 380,
    "speed": 111,
    "crit_rate": 15,
    "crit_damage": 50,
    "resistance": 15,
    "accuracy": 0,
    "raw_hp": 63,
    "raw_attack": 38,
    "raw_defense": 64,
    "max_lvl_hp": 10380,
    "max_lvl_attack": 417,
    "max_lvl_defense": 703,
    "awakens_from": 367,
    "awakens_to": None,
    "awaken_mats_fire_low": 0,
    "awaken_mats_fire_mid": 0,
    "awaken_mats_fire_high": 0,
    "awaken_mats_water_low": 0,
    "awaken_mats_water_mid": 0,
    "awaken_mats_water_high": 0,
    "awaken_mats_wind_low": 0,
    "awaken_mats_wind_mid": 0,
    "awaken_mats_wind_high": 0,
    "awaken_mats_light_low": 0,
    "awaken_mats_light_mid": 0,
    "awaken_mats_light_high": 0,
    "awaken_mats_dark_low": 0,
    "awaken_mats_dark_mid": 0,
    "awaken_mats_dark_high": 0,
    "awaken_mats_magic_low": 0,
    "awaken_mats_magic_mid": 0,
    "awaken_mats_magic_high": 0,
    "source": [
        {
            "id": 17,
            "url": "https://swarfarm.com/api/v2/monster-sources/17/",
            "name": "Tamor Desert",
            "description": "",
            "farmable_source": True
        },
        {
            "id": 7,
            "url": "https://swarfarm.com/api/v2/monster-sources/7/",
            "name": "Wind Scroll",
            "description": "",
            "farmable_source": False
        },
        {
            "id": 38,
            "url": "https://swarfarm.com/api/v2/monster-sources/38/",
            "name": "Mystical Scroll or Crystal Summon",
            "description": "",
            "farmable_source": False
        },
        {
            "id": 39,
            "url": "https://swarfarm.com/api/v2/monster-sources/39/",
            "name": "Unknown Scroll or Social Summon",
            "description": "",
            "farmable_source": False
        }
    ],
    "fusion_food": False,
    "resources": {
        "Wikia": "http://summonerswar.wikia.com/wiki/Griffon_(Wind)",
        "summonerswar.co": "http://summonerswar.co/wind-griffon-bernard",
        "SummonersWarMonsters.com": "http://www.summonerswarmonsters.com/wind/bernard"
    },
    "homunculus": False,
    "craft_cost": None,
    "craft_materials": []
}


class SwarfarmApiTest(unittest.TestCase):

    def test_parse_unit(self):
        parsed = Unit(
            meta=Meta(
                name='Bernard',
                element=Element.WIND,
                image='unit_icon_0005_2_4.png',
            ),
            stats={
                Stat.HP: 10380,
                Stat.ATK: 417,
                Stat.DEF: 703,
                Stat.SPD: 111,
                Stat.CR: 15,
                Stat.CD: 50,
                Stat.RES: 15,
                Stat.ACC: 0,
            },
            lead=LeadAbility(
                element=Element.WIND,
                stat=Stat.ATK,
                value=0.3,
                area=Area.ELEMENT
            ),
            skills=[
                Skill(
                    meta=SkillMeta(
                        name='Snatch',
                        description='Attacks the enemy with razor-sharp claws. Damage increases accordingly to your Attack Speed.',
                        image='skill_icon_0002_6_0.png'
                    ),
                    target=Target.ENEMY,
                    cooldown=None,
                    iterations=[
                        Iteration(
                            enemy_dmg='self.atk*(self.spd + 90)/55'
                        )
                    ]
                ),
                Skill(
                    meta=SkillMeta(
                        name='Body Slam',
                        description='Attacks the enemy with a body slam and weakens their Attack Power and Defense for 2 turns.',
                        image='skill_icon_0002_2_1.png'
                    ),
                    target=Target.ENEMY,
                    cooldown=2,
                    iterations=[
                        Iteration(
                            enemy_dmg='5.1*self.atk',
                            def_break=2,
                            atk_break=2
                        )
                    ]
                ),
                Skill(
                    meta=SkillMeta(
                        name='Tailwind',
                        description='Increases the Attack Bar of all allies by 30%, and also increases their Attack Speed for 2 turns.',
                        image='skill_icon_0002_6_1.png'
                    ),
                    target=Target.AOE_ENEMY,
                    cooldown=3,
                    iterations=[
                        Iteration(
                            atb_boost=30,
                            haste=2,
                        )
                    ]
                )
            ],
        )
        self.assertEqual(parsed, map_unit(BERNARD))

    def test_parse_bernard_skill_1(self):
        raw_skill = {
            "id": 408,
            "com2us_id": 2503,
            "name": "Snatch",
            "description": "Attacks the enemy with razor-sharp claws. Damage increases accordingly to your Attack Speed.",
            "slot": 1,
            "cooltime": None,
            "hits": 1,
            "passive": False,
            "aoe": False,
            "max_level": 5,
            "level_progress_description": [
                "Damage +5%",
                "Damage +5%",
                "Damage +5%",
                "Damage +15%"
            ],
            "effects": [],
            "multiplier_formula": "{ATK}*({SPD} + 90)/55",
            "multiplier_formula_raw": "[[\"ATK\", \"*\", 1.0], [\"*\"], [\"ATTACK_SPEED\", \"+\", 90], [\"/\"], [55]]",
            "scales_with": [
                "ATK",
                "SPD"
            ],
            "icon_filename": "skill_icon_0002_6_0.png",
            "used_on": [
                368,
                367
            ]
        }

        snatch = Skill(
            meta=SkillMeta(
                name="Snatch",
                description="Attacks the enemy with razor-sharp claws. Damage increases accordingly to your Attack Speed.",
                image="skill_icon_0002_6_0.png",
            ),
            cooldown=None,
            target=Target.ENEMY,
            iterations=[
                Iteration(
                    enemy_dmg='self.atk*(self.spd + 90)/55'
                )
            ]
        )

        self.assertEqual(map_skill(raw_skill), snatch)

    def test_parse_bernard_skill_2(self):
        raw_skill = {
            "id": 417,
            "com2us_id": 2508,
            "name": "Body Slam",
            "description": "Attacks the enemy with a body slam and weakens their Attack Power and Defense for 2 turns.",
            "slot": 2,
            "cooltime": 3,
            "hits": 1,
            "passive": False,
            "aoe": False,
            "max_level": 5,
            "level_progress_description": [
                "Damage +10%",
                "Damage +10%",
                "Damage +10%",
                "Cooltime Turn -1"
            ],
            "effects": [
                {
                    "effect": {
                        "id": 19,
                        "url": "https://swarfarm.com/api/v2/skill-effects/19/",
                        "name": "Decrease ATK",
                        "is_buff": False,
                        "description": "Attack Power is reduced by 50%",
                        "icon_filename": "debuff_attack_down.png"
                    },
                    "aoe": False,
                    "single_target": True,
                    "self_effect": False,
                    "chance": 100,
                    "on_crit": False,
                    "on_death": False,
                    "random": False,
                    "quantity": 2,
                    "all": False,
                    "self_hp": False,
                    "target_hp": False,
                    "damage": False,
                    "note": ""
                },
                {
                    "effect": {
                        "id": 20,
                        "url": "https://swarfarm.com/api/v2/skill-effects/20/",
                        "name": "Decrease DEF",
                        "is_buff": False,
                        "description": "Defense is reduced by 70%",
                        "icon_filename": "debuff_defence_down.png"
                    },
                    "aoe": False,
                    "single_target": True,
                    "self_effect": False,
                    "chance": 100,
                    "on_crit": False,
                    "on_death": False,
                    "random": False,
                    "quantity": 2,
                    "all": False,
                    "self_hp": False,
                    "target_hp": False,
                    "damage": False,
                    "note": ""
                }
            ],
            "multiplier_formula": "5.1*{ATK}",
            "multiplier_formula_raw": "[[\"ATK\", \"*\", 5.1]]",
            "scales_with": [
                "ATK"
            ],
            "icon_filename": "skill_icon_0002_2_1.png",
            "used_on": [
                368,
                367
            ]
        }

        skill = Skill(
            meta=SkillMeta(
                name='Body Slam',
                description='Attacks the enemy with a body slam and weakens their Attack Power and Defense for 2 turns.',
                image='skill_icon_0002_2_1.png'
            ),
            target=Target.ENEMY,
            cooldown=2,
            iterations=[
                Iteration(
                    enemy_dmg='5.1*self.atk',
                    def_break=2,
                    atk_break=2
                )
            ]
        )

        self.assertEqual(map_skill(raw_skill), skill)

    def test_parse_tiana_skill_3(self):
        raw_skill = {
            "id": 1214,
            "com2us_id": 9713,
            "name": "Wind of Changes",
            "description": "Removes all harmful and beneficial effects of all allies and enemies and increases the Attack Bar of all allies by 30%. This effect can't be resisted.",
            "slot": 3,
            "cooltime": 6,
            "hits": 1,
            "passive": False,
            "aoe": True,
            "max_level": 3,
            "level_progress_description": [
                "Cooltime Turn -1",
                "Cooltime Turn -1"
            ],
            "effects": [
                {
                    "effect": {
                        "id": 17,
                        "url": "https://swarfarm.com/api/v2/skill-effects/17/",
                        "name": "Increase ATB",
                        "is_buff": True,
                        "description": "The ATK bar of ally monsters is filled by a set amount. This allows ally monsters to attack again sooner.",
                        "icon_filename": ""
                    },
                    "aoe": True,
                    "single_target": False,
                    "self_effect": False,
                    "chance": 100,
                    "on_crit": False,
                    "on_death": False,
                    "random": False,
                    "quantity": 30,
                    "all": False,
                    "self_hp": False,
                    "target_hp": False,
                    "damage": False,
                    "note": ""
                },
                {
                    "effect": {
                        "id": 34,
                        "url": "https://swarfarm.com/api/v2/skill-effects/34/",
                        "name": "Cleanse",
                        "is_buff": True,
                        "description": "Removes one or more debuffs",
                        "icon_filename": ""
                    },
                    "aoe": True,
                    "single_target": False,
                    "self_effect": False,
                    "chance": 100,
                    "on_crit": False,
                    "on_death": False,
                    "random": False,
                    "quantity": None,
                    "all": True,
                    "self_hp": False,
                    "target_hp": False,
                    "damage": False,
                    "note": ""
                },
                {
                    "effect": {
                        "id": 37,
                        "url": "https://swarfarm.com/api/v2/skill-effects/37/",
                        "name": "Remove Buff",
                        "is_buff": False,
                        "description": "Removes one or more beneficial effects from target monster(s)",
                        "icon_filename": ""
                    },
                    "aoe": True,
                    "single_target": False,
                    "self_effect": False,
                    "chance": 100,
                    "on_crit": False,
                    "on_death": False,
                    "random": False,
                    "quantity": None,
                    "all": True,
                    "self_hp": False,
                    "target_hp": False,
                    "damage": False,
                    "note": ""
                }
            ],
            "multiplier_formula": "30.0000000000000 (Fixed)",
            "multiplier_formula_raw": "[[30.0, \"FIXED\"]]",
            "scales_with": [],
            "icon_filename": "skill_icon_0010_4_4.png",
            "used_on": [
                582,
                583
            ]
        }

        wind_of_change = Skill(
            meta=SkillMeta(
                name="Wind of Changes",
                description="Removes all harmful and beneficial effects of all allies and enemies and increases the Attack Bar of all allies by 30%. This effect can't be resisted.",
                image="skill_icon_0010_4_4.png",
            ),
            cooldown=4,
            target=Target.AOE_ENEMY,
            iterations=[
                Iteration(
                    strip='all',
                    cleanse='all',
                    atb_boost=30
                )
            ]
        )

        self.assertEqual(wind_of_change, map_skill(raw_skill))
