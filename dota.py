import requests
from pydantic import BaseModel
import json
from http import HTTPStatus

API_OPENDOTA = "https://api.opendota.com"

url = "https://api.opendota.com/api/heroes"

class HeroData(BaseModel):
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str

try:
    response = requests.get(url)
    response.raise_for_status()
    heroes_data = response.json()
    validated_data = [HeroData(**hero) for hero in heroes_data] #все ключи-значения
except requests.exceptions.RequestException as e:
    print(f"Сетевая ошибка: {e}")
except ValueError as e:
    print(f"Ошибка при обработке JSON: {e}")

def name_by_id(some_info_about_hero):
    hero_id = some_info_about_hero["hero_id"]
    for i in range(len(heroes_data)):
        if heroes_data[i]["id"] == hero_id:
            return(heroes_data[i]["localized_name"])

class HeroMatchup(BaseModel):
    hero_id: int
    games_played: int
    wins: int
    win_rate: float

def get_hero_versus(hero_id, hero_data):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    try:
        response = requests.get(url)
        response.raise_for_status()
        hero_versus_data = response.json()
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
        print(sorted_versus_heroes[0])
        print(name_by_id(sorted_versus_heroes[0]))
        print(sorted_versus_heroes[1])
        print(name_by_id(sorted_versus_heroes[1]))
        print("Герой наиболее слаб против:")
        print(sorted_versus_heroes[-1])
        print(name_by_id(sorted_versus_heroes[-1]))
        print(sorted_versus_heroes[-2])
        print(name_by_id(sorted_versus_heroes[-2]))
        print()
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return []
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        return []

def hero_by_name(hero_name, hero_data):
    for hero in hero_data:
        if hero["localized_name"].lower() == hero_name.lower():
            return hero
    return None

def print_hero_info(hero):
    if hero:
        print(f"Информация о герое {hero['localized_name']}:")
        print(f"Полномочия героя: {hero['roles']}")
        print(f"Основной аттрибут: {hero['primary_attr']}")
        print(f"Тип атаки: {hero['attack_type']}")
        print()

def main():
    print("Программа выдаёт 2 лучших и худших героев против введённого, их статистику матчей, а также некоторые характеристики введённого героя.")
    while True:
        hero_name = input("Введите имя героя, чтобы узнать его статистику и характеристики (для выхода введите 'exit'): ")
        if hero_name.lower() == "exit":
            break
        hero = hero_by_name(hero_name, heroes_data)
        if hero:
            versus_heroes = get_hero_versus(hero['id'], heroes_data)
            print_hero_info(hero)
        else:
            print("Герой не найден.")

if __name__ == "__main__":
    main()
