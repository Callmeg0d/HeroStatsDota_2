import requests
import json
from http import HTTPStatus
from schemes import HeroData
from schemes import HeroMatchup
from storage import heroes_storage

OPENDOTA_API = "https://api.opendota.com"


def get_heroes_data():
    url = f"{OPENDOTA_API}/api/heroes"
    try:
        validated_data = [HeroData(**hero) for hero in heroes_data]
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
    return heroes_data

def get_name_by_id(some_info_about_hero):
    hero_id = some_info_about_hero["hero_id"]
    heroes_data = heroes_storage.get()
    for i in range(len(heroes_data)):
        if heroes_data[i].id == hero_id:
            return heroes_data[i].localized_name

def get_hero_versus(hero_id, hero_data):
    url = f"{OPENDOTA_API}/api/heroes/{hero_id}/matchups"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return []
        
    try:
        hero_versus_data = response.json()
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        return []
        
    versus_heroes = []
    for hero in hero_versus_data:
        matchup_info = HeroMatchup(
            hero_id=hero["hero_id"],
            games_played=hero["games_played"],
            wins=hero["wins"],
            win_rate=round(hero["wins"] / hero["games_played"] * 100, 2)
        )
        if matchup_info.games_played >= 5:
            versus_heroes.append(matchup_info.dict())
    sorted_versus_heroes = sorted(versus_heroes, key=lambda x: x["win_rate"], reverse=True)
    print("Герой наиболее силён против:")
    for i in range(2):
        print(sorted_versus_heroes[i], (get_name_by_id(sorted_versus_heroes[i])))
    print("Герой наиболее слаб против:")
    for i in range(2):
        print(sorted_versus_heroes[len(sorted_versus_heroes) - i - 1], (get_name_by_id(sorted_versus_heroes[len(sorted_versus_heroes) - i - 1])))
    print()

def get_hero_by_name(hero_name, hero_data):
    for hero in hero_data:
        if hero.localized_name.lower() == hero_name.lower():
            return hero
    return None

def print_hero_info(hero):
    if not hero:
        return
    hero_info = f"""
    Информация о герое {hero.localized_name}:
    Полномочия героя: {hero.roles}
    Основной аттрибут: {hero.primary_attr}
    Тип атаки: {hero.attack_type}
    """
    print(hero_info)

def main():
    # init heroes data
    heroes_storage.set(get_heroes_data())
    
    print("Программа выдаёт 2 лучших и худших героев против введённого, их статистику матчей, а также некоторые характеристики введённого героя.")
    while True:
        hero_name = input("Введите имя героя, чтобы узнать его статистику и характеристики (для выхода введите 'exit'): ")
        if hero_name.lower() == "exit":
            break
        hero = get_hero_by_name(hero_name, heroes_storage.get())
        if hero:
            print_hero_info(hero)
            versus_heroes = get_hero_versus(hero.id, heroes_storage.get())
        else:
            print("Герой не найден.")

if __name__ == "__main__":
    main()
