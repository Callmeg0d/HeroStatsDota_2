import requests
import json

def hero_info():
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    heroes_data = response.json()
    return heroes_data

def get_heroes():
    response = requests.get('https://api.opendota.com/api/heroes')
    if response.status_code == 200:
        heroes_data = response.json()
        heroes = [hero['localized_name'] for hero in heroes_data]
        for i in range(len(heroes)):
            print(heroes[i],i, sep = " ")
    else:
        return []

def get_hero_versus(hero_id, hero_data):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    response = requests.get(url)
    hero_versus_data = response.json()
    versus_heroes = []
    for hero in hero_versus_data:
        versus_heroes.append({
            'hero_id': hero['hero_id'],
            'games_played': hero['games_played'],
            'wins': hero['wins'],
            'win_rate': round(hero['wins'] / hero['games_played'] * 100, 2)
        })
    sorted_versus_heroes = sorted(versus_heroes, key=lambda x: x['win_rate'], reverse=True)
    for i in range(len(sorted_versus_heroes)):
        print(sorted_versus_heroes[i])
    print()

def hero_by_name(hero_name, hero_data):
    for hero in hero_data:
        if hero['localized_name'].lower() == hero_name.lower():
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
    heroes_data = hero_info()

    while True:
        hero_name = input("Введите имя героя (для выхода введите 'exit'): ")
        if hero_name.lower() == "exit":
            break

        hero = hero_by_name(hero_name, heroes_data)
        if hero:
            versus_heroes = get_hero_versus(hero['id'], heroes_data)
            print_hero_info(hero, versus_heroes)
            get_heroes()
        else:
            print("Герой не найден.")

if __name__ == "__main__":
    main()