import asyncio
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Tout:
    """Classe mère orchestratrice"""
    def __init__(self):
        self.instances = []  # Toutes les instances de sous-Tout
        self.graph = nx.Graph()  # Graphe des relations entre les Touts
        print("Le Grand Tout a été créé.")

    def register(self, tout_instance):
        """Ajoute une instance de Tout à la supervision du Grand Tout"""
        self.instances.append(tout_instance)
        self.graph.add_node(tout_instance.name, level=tout_instance.level)
        print(f"{tout_instance.name} a été enregistré dans le Grand Tout.")

    def connect(self, tout1, tout2):
        """Crée une connexion entre deux Touts dans le Grand Tout"""
        self.graph.add_edge(tout1.name, tout2.name)
        tout1.connections["peers"].append(tout2)
        tout2.connections["peers"].append(tout1)
        print(f"{tout1.name} et {tout2.name} sont connectés.")

    def visualize(self):
        """Visualisation du réseau des Touts"""
        pos = nx.spring_layout(self.graph)
        levels = nx.get_node_attributes(self.graph, "level")
        node_colors = [levels[node] for node in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, node_size=500)
        plt.show()

    async def orchestrate(self, cycles=3):
        """Orchestre les interactions entre les Touts"""
        for cycle in range(1, cycles + 1):
            print(f"\n=== Cycle {cycle} ===")
            for tout in self.instances:
                if tout.connections["peers"]:
                    partner = random.choice(tout.connections["peers"])
                    if random.random() < 0.5:
                        tout.perturb(partner)
                    else:
                        tout.cooperate(partner)
                    tout.adapt()
            await asyncio.sleep(1)  # Pause pour simuler le temps qui passe


class ToutInstance:
    """Classe de chaque Tout individuel"""
    def __init__(self, name, level, grand_tout):
        self.name = name
        self.level = level
        self.attributes = {
            "floats": [random.random() for _ in range(random.randint(1, 5))],
            "ints": [random.randint(1, 100) for _ in range(random.randint(1, 5))],
            "strings": [f"Str_{i}" for i in range(random.randint(1, 5))],
        }
        self.connections = defaultdict(list)  # Liste des pairs connectés
        grand_tout.register(self)  # Enregistre cette instance dans le Grand Tout
        print(f"{self.name} créé (niveau {self.level}) avec attributs : {self.attributes}")

    def perturb(self, target_tout):
        """Perturbe un autre Tout"""
        print(f"{self.name} perturbe {target_tout.name}")
        perturbation_value = random.uniform(-10, 10)
        target_tout.attributes["floats"].append(perturbation_value)
        print(f"{target_tout.name} reçoit une perturbation de valeur {perturbation_value:.2f}")

    def cooperate(self, target_tout):
        """Coopère avec un autre Tout"""
        print(f"{self.name} coopère avec {target_tout.name}")
        self_sum = sum(self.attributes["ints"])
        target_sum = sum(target_tout.attributes["ints"])
        combined = (self_sum + target_sum) / 2
        print(f"Valeur combinée de {self.name} et {target_tout.name} : {combined:.2f}")
        return combined

    def adapt(self):
        """Adapte ses attributs en fonction des interactions"""
        mutation_factor = random.uniform(0.9, 1.1)
        for key in ["floats", "ints"]:
            self.attributes[key] = [val * mutation_factor for val in self.attributes[key]]
        print(f"{self.name} s'adapte avec un facteur de mutation de {mutation_factor:.2f}")


async def main():
    # Création du Grand Tout
    tout = Tout()

    # Ajout des Touts individuels
    grand_tout_instance = ToutInstance("Grand_Tout", level=0, grand_tout=tout)

    for i in range(5):
        new_tout = ToutInstance(f"Tout_{i+1}", level=random.randint(1, 3), grand_tout=tout)
        tout.connect(grand_tout_instance, new_tout)

    # Lancement des interactions orchestrées
    await tout.orchestrate(cycles=5)

    # Visualisation finale
    print("\n=== Visualisation finale ===")
    tout.visualize()


# Exécution du programme
asyncio.run(main())