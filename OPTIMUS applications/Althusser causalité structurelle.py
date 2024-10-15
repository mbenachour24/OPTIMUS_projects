import random
import numpy as np

class System:
    def __init__(self, name):
        self.name = name
        self.internal_state = 1.0  # état interne du système
        self.external_influence = 0.0  # influence externe des autres systèmes

    def update_internal_state(self):
        # L'état interne évolue en fonction de son propre fonctionnement et de l'influence externe
        # Un simple exemple avec un facteur aléatoire pour simuler une dynamique interne
        self.internal_state += random.uniform(-0.1, 0.1) + self.external_influence
        self.internal_state = max(0, min(self.internal_state, 10))  # Garder l'état dans un intervalle [0, 10]

    def receive_external_influence(self, influence):
        # Fonction pour recevoir des influences externes provenant d'autres systèmes
        self.external_influence = influence

class CausalityModel:
    def __init__(self):
        # Créer les systèmes différenciés : juridique, politique, économique
        self.juridical_system = System("Juridique")
        self.political_system = System("Politique")
        self.economic_system = System("Économique")

    def calculate_influence(self):
        # Calculer l'influence mutuelle entre systèmes selon des pondérations spécifiques
        # Cela pourrait être paramétré selon les contextes (normes, réformes, etc.)
        influence_juridique = (0.4 * self.political_system.internal_state + 0.6 * self.economic_system.internal_state)
        influence_politique = (0.3 * self.juridical_system.internal_state + 0.7 * self.economic_system.internal_state)
        influence_economique = (0.5 * self.juridical_system.internal_state + 0.5 * self.political_system.internal_state)

        # Retourner les influences mutuelles
        return influence_juridique, influence_politique, influence_economique

    def run_simulation(self, steps=50):
        for step in range(steps):
            print(f"\n--- Step {step+1} ---")

            # Calculer les influences croisées
            influence_juridique, influence_politique, influence_economique = self.calculate_influence()

            # Appliquer les influences externes sur chaque système
            self.juridical_system.receive_external_influence(influence_juridique)
            self.political_system.receive_external_influence(influence_politique)
            self.economic_system.receive_external_influence(influence_economique)

            # Mettre à jour les états internes de chaque système
            self.juridical_system.update_internal_state()
            self.political_system.update_internal_state()
            self.economic_system.update_internal_state()

            # Afficher les états internes des systèmes à chaque étape
            print(f"Système juridique: {self.juridical_system.internal_state:.2f}")
            print(f"Système politique: {self.political_system.internal_state:.2f}")
            print(f"Système économique: {self.economic_system.internal_state:.2f}")

# Lancer la simulation de causalité structurelle
causality_model = CausalityModel()
causality_model.run_simulation()