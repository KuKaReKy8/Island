import random



class Island:
    type_zone = ('forest', 'field', 'mountain')
    weather = ('snowy', 'sunny', 'windy', 'dry')
    type_predators = {'волк': [17, 29, 21, 'волк'],
                      'медведь': [13, 21, 29, "медведь"],
                      'лиса': [18, 32, 23, "лиса"]}
    type_herbivores = {'заяц': [18, 34, 17, "заяц"],
                       'ёж': [10, 20, 14, "ёж"],
                       'кабан': [16, 25, 18, "кабан"]}
    type_plants = {'папоротник': ['папоротник', 3],
                   'клевер': ['клевер', 1],
                   'сыть': ['сыть', 2]}
    zones = []

    @staticmethod
    def generate_zone():
        num_of_zones = 5
        for _ in range(num_of_zones):
            _generate_type_zone = random.choice(Island.type_zone)
            _generate_weather = random.choice(Island.weather)
            _generate_zone = Zone(_generate_type_zone, _generate_weather)
            Island.zones.append(_generate_zone)
            num_of_predators = random.randint(1, 10)
            num_of_herbivores = random.randint(1, 20)
            num_of_plants = random.randint(1, 100)
            for _ in range(num_of_predators):
                _generate_zone.generate_predators()
            for _ in range(num_of_herbivores):
                _generate_zone.generate_herbivores()
            for _ in range(num_of_plants):
                _generate_zone.generate_plants()
        print(_generate_zone.population)


class Zone:
    def __init__(self, zone, weather):
        self.zone = zone
        self.weather = weather
        self.population = {'predators': [], 'herbivores': [], 'plants': []}


    def generate_predators(self):
        _predator = random.choice(list(Island.type_predators.keys()))
        self.population['predators'].append(Predators(Island.type_predators[_predator]))


    def generate_herbivores(self):
        _herbivore = random.choice(list(Island.type_herbivores.keys()))
        self.population['herbivores'].append(Herbivore(Island.type_herbivores[_herbivore]))


    def generate_plants(self):
        _plant = random.choice(list(Island.type_plants.keys()))
        self.population['plants'].append(Plant(Island.type_plants[_plant]))


class Animal:
    def __init__(self, description):
        self.name = description[3]
        self.age = 0
        self.speed = description[0]
        self.fatigue = 0
        self.hunger = 0
        self.fatigue_limit = description[1]
        self.hunger_limit = description[2]


class Herbivore(Animal):
    age_limit_herbivore = 12


class Predators(Animal):
    age_limit_predator = 15


class Plant:
    age_limit_plant = 5

    def __init__(self, descrription):
        self.name = descrription[0]
        self.food = descrription[1]
        self.age = 0

Island.generate_zone()
