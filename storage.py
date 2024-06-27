class HeroesStorage:
    def __init__(self):
        self.heroes_data = []

    def set(self, heroes_data):
        self.heroes_data = heroes_data

    def get(self):
        return self.heroes_data


heroes_storage = HeroesStorage()
