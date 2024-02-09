import random
import keyboard


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
    current_month = 1

    @staticmethod
    def generate_zone():
        num_of_zones = 1
        for _ in range(num_of_zones):
            _generate_type_zone = random.choice(Island.type_zone)
            _generate_weather = random.choice(Island.weather)
            _generate_zone = Zone(_generate_type_zone, _generate_weather, _)
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

    @staticmethod
    def main_cycle():
        Island.generate_zone()
        x = True
        while x:
            if keyboard.is_pressed("esc"):
                x = False
            print(f'\nТекущий месяц {Island.current_month}\n')
            for _zone in Island.zones:
                _zone.life_cycle()
            Island.current_month += 1
            if Island.current_month >= 60:
                x = False


class Zone:
    def __init__(self, zone, weather, zone_id):
        self.zone = zone
        self.weather = weather
        self.population = {'predators': [], 'herbivores': [], 'plants': []}
        self.zone_id = zone_id

    def generate_predators(self):
        _predator = random.choice(list(Island.type_predators.keys()))
        self.population['predators'].append(Predators(Island.type_predators[_predator], self.zone_id))
        print(f'Появился {_predator}')

    def generate_herbivores(self):
        _herbivore = random.choice(list(Island.type_herbivores.keys()))
        self.population['herbivores'].append(Herbivore(
            description=Island.type_herbivores[_herbivore],
            zone_id=self.zone_id))
        print(f'Появился {_herbivore}')

    def generate_plants(self):
        _plant = random.choice(list(Island.type_plants.keys()))
        self.population['plants'].append(Plant(Island.type_plants[_plant]))
        print(f'Появился {_plant}')

    def life_cycle(self):
        print(f'Количество хищников в зоне {self.zone_id}: {len(self.population["predators"])}')
        for _pred in self.population['predators']:
            if _pred.dead():
                print(f'\n{_pred.name} умерло!\n')
                self.population['predators'].remove(_pred)
                continue
            _pred.implement_frame_pred()
            print(f'Текущий хищник: {_pred.name} возрастом {_pred.month}')
        print(f'Количество травоядных в зоне {self.zone_id}: {len(self.population["herbivores"])}')
        for _herb in self.population['herbivores']:
            if _herb.dead():
                print(f'\n{_herb.name} умерло!\n')
                self.population['herbivores'].remove(_herb)
                continue
            _herb.implement_frame_herb()
            print(f'Текущее травоядное: {_herb.name} возрастом {_herb.month}')
        print(f'Количество растений в зоне {self.zone_id}: {len(self.population["plants"])}')
        for _plant in self.population['plants']:
            if _plant.dead():
                print(f'\n{_plant.name} умерло!\n')
                self.population['plants'].remove(_plant)
                continue
            _plant.month += 1
            print(f'Текущее растение: {_plant.name} возрастом {_plant.month}')


class Animal:
    def __init__(self, description, zone_id):
        self.name = description[3]
        self.month = 0
        self.speed = description[0]
        self.fatigue = 0
        self.hunger = 0
        self.fatigue_limit = description[1]
        self.hunger_limit = description[2]
        self.month_limit = random.randint(120, 180)
        self.zone_id = zone_id
        self._desription = description

    def _sleep(self):
        fatigue_recovery = random.randint(4, 7)
        self.fatigue -= fatigue_recovery

    def dead(self):
        if self.hunger >= self.hunger_limit \
                or self.fatigue >= self.fatigue_limit \
                or self.month_limit <= self.month:
            return True
        else:
            return False

    def _check_huger(self):
        if self.hunger >= 0.7 * self.hunger_limit:
            return True
        else:
            return False

    def raise_vital_stats(self):
        self.month += 1
        self.fatigue += random.randint(2, 5)
        self.hunger += random.randint(3, 6)


class Herbivore(Animal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.food = random.randint(3, 6)

    def _eat(self):
        for _zone in Island.zones:
            if self.zone_id == _zone.zone_id:
                _plant = _zone.population['plants'][0]
                self.hunger -= _plant.food
                _zone.population['plants'].remove(_plant)

    def _reproduction(self):
        for _zone in Island.zones:
            if self.zone_id == _zone.zone_id:
                _herb = Herbivore(description=self._desription, zone_id=self.zone_id)
                _zone.population['herbivore'].append(_herb)
                print(f'\nРодилось {_herb.name}')

    def implement_frame_herb(self):
        if self.month >= 5:
            self._sleep()
            if self._check_huger():
                self._eat()
            if self.month % 7 == 0:
                if random.randint(0, 1):
                    self._reproduction()
        self.raise_vital_stats()


class Predators(Animal):
    def _hunt(self):
        for _zone in Island.zones:
            if self.zone_id == _zone.zone_id:
                if _zone.population['herbivores']:
                    _herb = _zone.population['herbivores'][0]
                    self.hunger -= _herb.food
                    _zone.population['herbivores'].remove(_herb)

    def _reproduction(self):
        for _zone in Island.zones:
            if self.zone_id == _zone.zone_id:
                _pred = Predators(description=self._desription, zone_id=self.zone_id)
                _zone.population['predators'].append(_pred)
                print(f'\nРодилось {_pred.name}\n')

    def implement_frame_pred(self):
        if self.month >= 5:
            self._sleep()
            if self._check_huger():
                self._hunt()
            if self.month % 7 == 0:
                if random.randint(0, 1):
                    self._reproduction()
        self.raise_vital_stats()


class Plant:
    def __init__(self, description):
        self.name = description[0]
        self.food = description[1]
        self.month = 0
        self.month_limit_plant = random.randint(70, 100)

    def dead(self):
        if self.month_limit_plant == self.month:
            return True
        else:
            return False

Island.main_cycle()