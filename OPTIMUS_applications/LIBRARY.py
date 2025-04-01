import time
import random

class Livre:
    def __init__(self, titre):
        self.titre = titre
        self.est_rangé = False
        self.est_prêté = False

class Rangement:
    def __init__(self):
        self.livres = []
    
    def ranger_livre(self, livre):
        if not livre.est_prêté:  # On ne peut ranger un livre que s'il n'est pas prêté
            livre.est_rangé = True
            self.livres.append(livre)
            print(f"Le livre '{livre.titre}' est rangé.")

class Prêt:
    def __init__(self):
        self.livres_prêtés = []
    
    def prêter_livre(self, livre):
        if not livre.est_prêté and not livre.est_rangé:  # On ne prête que des livres non rangés
            livre.est_prêté = True
            self.livres_prêtés.append(livre)
            print(f"Le livre '{livre.titre}' est prêté.")

class Recherche:
    def __init__(self, livres_disponibles):
        self.livres_disponibles = livres_disponibles

    def rechercher_livre(self, titre):
        for livre in self.livres_disponibles:
            if livre.titre == titre:
                print(f"Le livre '{titre}' a été trouvé.")
                return livre
        print(f"Le livre '{titre}' est introuvable.")
        return None

class Bibliothèque:
    def __init__(self):
        self.livres = [Livre("La Méthode OPTIMUS"), Livre("Théorie des Systèmes"), Livre("L'Autopoïèse Juridique")]
        self.rangement = Rangement()
        self.prêt = Prêt()
        self.recherche = Recherche(self.livres)
        self.iterations = 0

    def simulate(self, max_iterations=200, interval=1):
        while self.iterations < max_iterations:
            print(f"\n--- Itération {self.iterations + 1} ---")
            
            # Choisir aléatoirement une action pour simuler l'évolution dynamique
            action = random.choice(["recherche_rangement", "recherche_prêt"])
            
            if action == "recherche_rangement":
                livre = self.recherche.rechercher_livre("La Méthode OPTIMUS")
                if livre:
                    self.rangement.ranger_livre(livre)
            
            elif action == "recherche_prêt":
                livre = self.recherche.rechercher_livre("Théorie des Systèmes")
                if livre:
                    self.prêt.prêter_livre(livre)
            
            # Logique supplémentaire si besoin pour gérer les autres livres
            livre_autopoiese = self.recherche.rechercher_livre("L'Autopoïèse Juridique")
            if livre_autopoiese and not livre_autopoiese.est_rangé:
                self.rangement.ranger_livre(livre_autopoiese)

            # Affichage de l'état des systèmes
            print(f"Livres rangés : {[livre.titre for livre in self.rangement.livres]}")
            print(f"Livres prêtés : {[livre.titre for livre in self.prêt.livres_prêtés]}")

            # Pause entre les itérations pour simuler le passage du temps
            time.sleep(interval)

            # Incrémenter le compteur d'itérations
            self.iterations += 1

# Simulation avec un intervalle de 1 seconde entre chaque itération
bibliothèque = Bibliothèque()
bibliothèque.simulate(max_iterations=200, interval=1)
