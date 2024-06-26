import requests
class HeroesStorage:
    def __init__(self):
        self.heroes_data = []

    def set(self, url):
        response = requests.get(url)
        self.heroes_data = response.json()

    def get(self):
        self.set("https://api.opendota.com/api/heroes")
        return self.heroes_data

heroes_storage = HeroesStorage()
heroes_data = heroes_storage.get()
