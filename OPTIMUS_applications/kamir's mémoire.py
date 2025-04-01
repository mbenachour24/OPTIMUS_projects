import time
import random

# Classe représentant le système politique (FLN)
class PoliticalSystem:
    def __init__(self):
        self.reforms = []  # Liste des réformes politiques
        self.repression_level = 0  # Niveau de répression
    
    def propose_reform(self):
        # Propose une réforme (économique ou politique)
        reform = {"id": len(self.reforms) + 1, "type": random.choice(["économique", "politique"]), "success": None}
        self.reforms.append(reform)
        print(f"Système politique propose une réforme: {reform['type']}")
        return reform
    
    def manage_repression(self, movements):
        # Ajuste le niveau de répression en fonction de la contestation
        if movements.is_protesting:
            self.repression_level += 1
            print(f"Niveau de répression augmenté à: {self.repression_level}")
        else:
            print("Pas de répression nécessaire pour l'instant.")
        return self.repression_level

# Classe représentant les mouvements de gauche
class LeftMovements:
    def __init__(self):
        self.is_protesting = False  # État de protestation
    
    def organize_protest(self):
        # Décide si une protestation est organisée
        self.is_protesting = random.choice([True, False])
        if self.is_protesting:
            print("Les mouvements de gauche organisent une protestation.")
        else:
            print("Les mouvements de gauche ne protestent pas.")
        return self.is_protesting

# Classe représentant la population
class Population:
    def __init__(self):
        self.is_discontent = False
    
    def respond_to_reform(self, reform):
        # La population réagit aux réformes (positivement ou négativement)
        if reform["type"] == "économique":
            reform["success"] = random.choice([True, False])
            if reform["success"]:
                print("Réforme économique acceptée par la population.")
            else:
                print("Réforme économique rejetée, augmentation du mécontentement.")
                self.is_discontent = True
        elif reform["type"] == "politique":
            reform["success"] = random.choice([True, False])
            if reform["success"]:
                print("Réforme politique réussie.")
            else:
                print("Réforme politique échoue, la population se soulève.")
                self.is_discontent = True
        return self.is_discontent

# Classe représentant la société (orchestrateur)
class Society:
    def __init__(self):
        self.political_system = PoliticalSystem()
        self.left_movements = LeftMovements()
        self.population = Population()
    
    def simulate(self, cycles=5):
        for cycle in range(cycles):
            print(f"\n--- Cycle {cycle + 1} ---")
            
            # Le système politique propose une réforme
            reform = self.political_system.propose_reform()
            
            # La population réagit à la réforme
            discontent = self.population.respond_to_reform(reform)
            
            # Les mouvements de gauche décident de protester ou non
            protest = self.left_movements.organize_protest()
            
            # Le système politique ajuste son niveau de répression
            repression = self.political_system.manage_repression(self.left_movements)
            
            # Pause pour simuler l'évolution dans le temps
            time.sleep(1)

# Exécuter la simulation
society = Society()
society.simulate(10)
