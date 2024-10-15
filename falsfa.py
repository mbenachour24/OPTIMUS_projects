import time
import random

class Agent:
    def __init__(self, name):
        self.name = name
        self.energy = 100  # Chaque agent a un certain niveau d'énergie pour la discussion
        self.mood = random.choice(['constructive', 'destructive'])  # Chaque agent est constructif ou destructif
    
    def speak(self):
        if self.mood == 'constructive':
            print(f"{self.name} dit quelque chose de constructif.")
        else:
            print(f"{self.name} dit quelque chose de destructif.")
        
        self.energy -= 10  # Chaque intervention consomme de l'énergie
        if self.energy <= 0:
            print(f"{self.name} est épuisé.")
    
    def recharge(self):
        self.energy = 100
        print(f"{self.name} recharge son énergie.")
    
    def switch_mood(self):
        self.mood = 'constructive' if self.mood == 'destructive' else 'destructive'
        print(f"{self.name} change d'humeur en {self.mood}.")
    
    def status(self):
        return {"name": self.name, "energy": self.energy, "mood": self.mood}


class FalsfaSystem:
    def __init__(self):
        self.agents = []
        self.iteration = 0
    
    def add_agent(self, agent):
        self.agents.append(agent)
        print(f"L'agent {agent.name} a rejoint la discussion.")
    
    def simulate_iteration(self):
        print(f"\nIteration {self.iteration}")
        for agent in self.agents:
            agent.speak()
            if random.random() > 0.7:
                agent.switch_mood()  # Random switch mood
            
            if agent.energy <= 0:
                agent.recharge()
        
        self.iteration += 1
        time.sleep(2)  # Pause pour simuler le passage du temps entre les itérations
    
    def run_simulation(self, iterations=5):
        for _ in range(iterations):
            self.simulate_iteration()


# Initialisation du système Falsfa++
system = FalsfaSystem()

# Ajout des agents de la conversation
system.add_agent(Agent("Mohamed"))
system.add_agent(Agent("Maude"))
system.add_agent(Agent("Habib"))

# Lancer la simulation pour 5 itérations
system.run_simulation(5)
