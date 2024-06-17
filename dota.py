import requests
import json
from http import HTTPStatus

API_OPENDOTA = "https://api.opendota.com"

url = "https://api.opendota.com/api/heroes"
try:
    response = requests.get(url)
    response.raise_for_status()
    heroes_data = response.json()
except requests.exceptions.RequestException:
    print(f"Сетевая ошибка:")


def get_heroes():
    url = "https://api.opendota.com/api/heroes"
    try:
        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:
            heroes_data = response.json()
            hero_name_and_id = []
            for hero in heroes_data:
                hero_name_and_id.append((
                    hero["localized_name"],
                    hero["id"]
                ))
        else:
            return []
    except requests.exceptions.RequestException:
        print(f"Сетевая ошибка:")
        return None

def name(s):
    k = s["hero_id"]
    for i in range(len(heroes_data)):
        if heroes_data[i]["id"] == k:
            return(heroes_data[i]["localized_name"])


def get_hero_versus(hero_id, hero_data):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    try:
        response = requests.get(url)
        hero_versus_data = response.json()
        versus_heroes = []
        for hero in hero_versus_data:
            if hero['games_played'] >= 5 :
                versus_heroes.append({
                    "hero_id": hero["hero_id"],
                    "games_played": hero["games_played"],
                    "wins": hero["wins"],
                    "win_rate": round(hero["wins"] / hero["games_played"] * 100, 2)
                })
        sorted_versus_heroes = sorted(versus_heroes, key=lambda x: x["win_rate"], reverse=True)
        print("Герой наиболее силён против:")
        print(sorted_versus_heroes[0])
        print(name(sorted_versus_heroes[0]))
        print(sorted_versus_heroes[1])
        print(name(sorted_versus_heroes[1]))
        print("Герой наиболее слаб против:")
        print(sorted_versus_heroes[-1])
        print(name(sorted_versus_heroes[-1]))
        print(sorted_versus_heroes[-2])
        print(name(sorted_versus_heroes[-2]))
        print()
    except requests.exceptions.RequestException:
        print(f"Сетевая ошибка:")
        return None

def hero_by_name(hero_name, hero_data):
    for hero in hero_data:
        if hero["localized_name"].lower() == hero_name.lower():
            return hero
    return None

def print_hero_info(hero, versus_heroes):
    if hero:
        print(f"Информация о герое {hero['localized_name']}:")
        print(f"Полномочия героя: {hero['roles']}")
        print(f"Основной аттрибут: {hero['primary_attr']}")
        print(f"Тип атаки: {hero['attack_type']}")
        print()

def main():

    while True:
        hero_name = input("Введите имя героя (для выхода введите 'exit'): ")
        if hero_name.lower() == "exit":
            break
        hero = hero_by_name(hero_name, heroes_data)
        if hero:
            get_heroes()
            versus_heroes = get_hero_versus(hero['id'], heroes_data)
            print_hero_info(hero, versus_heroes)

        else:
            print("Герой не найден.")

if __name__ == "__main__":
    main()
