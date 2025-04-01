import random

# Classe mère pour les Systèmes
class System:
    def __init__(self, name):
        self.name = name
        self.population = 0
        self.resources = {'wood': 0, 'stone': 0, 'metal': 0, 'food': 0}

    def produce_resources(self):
        pass

    def consume_resources(self):
        pass

    def reproduce(self):
        # Reproduction augmente la population
        new_population = self.population + random.randint(1, 5)
        print(f"{self.name}: Population increased from {self.population} to {new_population}")
        self.population = new_population

# Système Food
class FoodSystem(System):
    def __init__(self):
        super().__init__('Food System')
        self.roles = {'hunters': 5, 'gatherers': 5}

    def produce_resources(self):
        # Les chasseurs ramènent de la viande, les cueilleurs ramènent des fruits/légumes
        meat = self.roles['hunters'] * random.randint(1, 3)
        fruits = self.roles['gatherers'] * random.randint(1, 3)
        wood = (self.roles['hunters'] + self.roles['gatherers']) * random.randint(0, 1)  # Both hunt/gather wood
        self.resources['food'] += meat + fruits
        self.resources['wood'] += wood
        print(f"{self.name} produced {meat} units of meat, {fruits} units of fruits, and {wood} units of wood.")

    def specialize(self):
        # Augmentation de la spécialisation
        if self.population > 10:
            new_hunters = random.randint(1, 3)
            self.roles['hunters'] += new_hunters
            self.roles['gatherers'] += random.randint(1, 3)
            print(f"{self.name} specialized: {new_hunters} more hunters added.")

# Système Shelter
class ShelterSystem(System):
    def __init__(self):
        super().__init__('Shelter System')
        self.roles = {'miners': 5, 'builders': 5}

    def produce_resources(self):
        # Les mineurs extraient des ressources, les builders utilisent ces ressources
        stone = self.roles['miners'] * random.randint(1, 2)
        metal = self.roles['miners'] * random.randint(0, 1)
        wood = (self.roles['miners'] + self.roles['builders']) * random.randint(0, 1)  # Both miners and builders gather wood
        self.resources['stone'] += stone
        self.resources['metal'] += metal
        self.resources['wood'] += wood
        print(f"{self.name} produced {stone} units of stone, {metal} units of metal, and {wood} units of wood.")

    def specialize(self):
        # Spécialisation des rôles avec une population croissante
        if self.population > 10:
            new_miners = random.randint(1, 3)
            self.roles['miners'] += new_miners
            self.roles['builders'] += random.randint(1, 3)
            print(f"{self.name} specialized: {new_miners} more miners added.")

# Couplage structurel
class Society:
    def __init__(self):
        self.food_system = FoodSystem()
        self.shelter_system = ShelterSystem()

    def exchange_resources(self):
        # Les systèmes échangent du bois et des métaux
        wood_shared = min(self.food_system.resources['wood'], self.shelter_system.resources['wood'])
        metal_shared = min(self.food_system.resources['metal'], self.shelter_system.resources['metal'])
        
        self.food_system.resources['wood'] -= wood_shared
        self.shelter_system.resources['wood'] += wood_shared
        
        self.food_system.resources['metal'] -= metal_shared
        self.shelter_system.resources['metal'] += metal_shared
        
        print(f"Exchanged {wood_shared} units of wood and {metal_shared} units of metal between systems.")

    def iterate_generation(self):
        # Reproduction pour les deux systèmes
        self.food_system.reproduce()
        self.shelter_system.reproduce()
        
        # Spécialisation des rôles en fonction de la population
        self.food_system.specialize()
        self.shelter_system.specialize()
        
        # Les systèmes produisent leurs ressources
        self.food_system.produce_resources()
        self.shelter_system.produce_resources()
        
        # Échange de ressources entre systèmes
        self.exchange_resources()

    def simulate(self, iterations=5):
        # Simulation de plusieurs itérations
        for i in range(iterations):
            print(f"\n--- Iteration {i + 1} ---")
            self.iterate_generation()

# Initialisation de la société et simulation
society = Society()
society.simulate()