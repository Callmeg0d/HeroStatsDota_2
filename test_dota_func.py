from dota.dota import name_by_id
from dota.dota import hero_by_name
from dota.dota import heroes_data
import pytest


@pytest.mark.parametrize("some_info_with_id, expected_result", [
    ({'hero_id': 66, 'games_played': 11, 'wins': 1, 'win_rate': 9.09}, "Chen"),
    ({'hero_id': 75, 'games_played': 19, 'wins': 13, 'win_rate': 68.42}, "Silencer"),
    ({'hero_id': 1}, "Anti-Mage"),
    ({'hero_id': 186}, None)]
)
def test_name_by_id(some_info_with_id, expected_result):
    assert name_by_id(some_info_with_id) == expected_result


@pytest.mark.parametrize("hero_name, heroes_data, expected_result", [
    ("Riki", heroes_data, {'attack_type': 'Melee','id': 32,'legs': 2,'localized_name': 'Riki','name': 'npc_dota_hero_riki',
                                                 'primary_attr': 'agi','roles': ['Carry', 'Escape', 'Disabler']}),
    ("rIKi", heroes_data, {'attack_type': 'Melee','id': 32,'legs': 2,'localized_name': 'Riki','name': 'npc_dota_hero_riki',
                                                 'primary_attr': 'agi','roles': ['Carry', 'Escape', 'Disabler']}),
    ("Pudge", heroes_data, {'attack_type': 'Melee','id': 14,'legs': 2,'localized_name': 'Pudge','name': 'npc_dota_hero_pudge',
                                                 'primary_attr': 'str','roles': ['Disabler', 'Initiator', 'Durable', 'Nuker']}),
])
def test_hero_by_name(hero_name, heroes_data, expected_result):
    assert hero_by_name(hero_name, heroes_data) == expected_result
