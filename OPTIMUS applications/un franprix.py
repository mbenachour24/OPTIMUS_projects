import time
import random

# Classe Produit
class Produit:
    def __init__(self, nom, prix, quantite, cout_restock):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.cout_restock = cout_restock  # Cost to restock each unit

    def vendre(self, quantite):
        if quantite <= self.quantite:
            self.quantite -= quantite
            return True
        else:
            print(f"Pas assez de {self.nom} en stock!")
            return False

    def restocker(self, quantite):
        """Ajoute la quantité donnée au stock"""
        self.quantite += quantite

# Classe Caisse
class Caisse:
    def __init__(self):
        self.total_caisse = 0

    def gerer_paiement(self, montant):
        self.total_caisse += montant
        return True

    def status(self, id):
        print(f"Total caisse {id}: {self.total_caisse}€")

# Classe Franprix
class Franprix:
    def __init__(self):
        self.produits = []
        self.caisses = [Caisse() for _ in range(3)]  # Trois caisses
        self.clients = []
        self.iteration = 0
        self.total_tresorerie = 0

    def ajouter_produit(self, produit):
        self.produits.append(produit)

    def ajouter_client(self, client):
        self.clients.append(client)

    def afficher_stock(self):
        print("\nStock actuel:")
        for produit in self.produits:
            print(f"{produit.nom}: {produit.quantite} unités, {produit.prix}€")

    def total_tresorerie_status(self):
        """Affiche la somme totale de toutes les caisses."""
        total = sum([caisse.total_caisse for caisse in self.caisses])
        self.total_tresorerie = total
        print(f"Total trésorerie: {self.total_tresorerie}€")

    def restock(self, threshold=5, restock_amount=10):
        """Restocks products that fall below a given threshold, deducts money from total trésorerie."""
        for produit in self.produits:
            if produit.quantite < threshold:
                cost = produit.cout_restock * restock_amount
                if self.total_tresorerie >= cost:
                    print(f"Restocking {produit.nom} with {restock_amount} units at a cost of {cost}€")
                    produit.restocker(restock_amount)
                    self.total_tresorerie -= cost
                else:
                    print(f"Pas assez d'argent dans la trésorerie pour restocker {produit.nom}!")

    def iterer(self):
        self.iteration += 1
        print(f"\n--- Iteration {self.iteration} ---")

        # Les clients achètent des produits aléatoirement
        for client in self.clients:
            produit = random.choice(self.produits)
            quantite = random.randint(1, 3)  # Quantité aléatoire entre 1 et 3
            client.ajouter_au_panier(produit, quantite)
            client.passer_a_la_caisse(random.choice(self.caisses))  # Caisse aléatoire

        # Afficher le statut des caisses et total trésorerie
        for i, caisse in enumerate(self.caisses, start=1):
            caisse.status(i)
        
        # Afficher la trésorerie totale
        self.total_tresorerie_status()

        # Restocker les produits si nécessaire
        self.restock()

    def simuler(self, iterations=5):
        for _ in range(iterations):
            self.afficher_stock()
            self.iterer()
            time.sleep(0.1)  # Pause pour simuler le temps qui passe

# Classe Client
class Client:
    def __init__(self, nom, argent):
        self.nom = nom
        self.panier = []
        self.argent = argent

    def ajouter_au_panier(self, produit, quantite):
        self.panier.append((produit, quantite))

    def passer_a_la_caisse(self, caisse):
        total = sum([produit.prix * quantite for produit, quantite in self.panier])
        if caisse.gerer_paiement(total):
            print(f"{self.nom} a payé {total}€.")
            for produit, quantite in self.panier:
                produit.vendre(quantite)
            self.panier = []
        else:
            print(f"{self.nom} n'a pas pu payer.")

# Initialisation du Franprix
franprix = Franprix()

# Ajouter des produits au stock avec un coût de restock
franprix.ajouter_produit(Produit("Pomme", 1.5, 50, 0.8))
franprix.ajouter_produit(Produit("Pain", 2.0, 30, 1.0))
franprix.ajouter_produit(Produit("Lait", 1.0, 20, 0.5))
franprix.ajouter_produit(Produit("zatla", 10, 15, 3))
franprix.ajouter_produit(Produit("chorba", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("kafteji", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("mkhara9", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("fricassé", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("savon", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("brosse à dent", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("dentifrice", 3.5, 15, 2.5))
franprix.ajouter_produit(Produit("cocaine", 90, 15, 40))

# Ajouter des clients
franprix.ajouter_client(Client("Alice", 100))
franprix.ajouter_client(Client("Bob", 100))
franprix.ajouter_client(Client("mustapha", 100))
franprix.ajouter_client(Client("mohamed", 100))
franprix.ajouter_client(Client("philippe", 100))
franprix.ajouter_client(Client("khalil", 100))
franprix.ajouter_client(Client("hamza", 100))
franprix.ajouter_client(Client("zatlyboy", 100))
franprix.ajouter_client(Client("aicha", 100))



# Simuler le Franprix pendant 10 itérations
franprix.simuler(200)