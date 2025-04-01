import asyncio
import random
import logging

# Configuration des logs pour tracer la simulation
logging.basicConfig(level=logging.DEBUG, filename='admin_simulation.log', filemode='a', format='%(message)s')

# Constantes de la simulation
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
SIMULATION_DAYS = 10
BUDGET_MIN = 50000
BUDGET_MAX = 200000

# Classe représentant un acte administratif
class AdministrativeAct:
    def __init__(self, act_id, text, valid=True, complexity=1):
        self.id = act_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Acte créé avec complexité {complexity} et validité {valid}")

    def invalidate(self):
        self.valid = False
        self.log_event("Acte invalidé")

    def log_event(self, message):
        log_message = f"Acte {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

# Classe représentant les décisions administratives
class AdministrativeDecision:
    def __init__(self, decision_id, act):
        self.id = decision_id
        self.act = act
        self.legal = act.valid
        self.log_event("Décision en cours d'évaluation")

    def validate(self):
        self.legal = True
        self.log_event("Décision validée")

    def invalidate(self):
        self.legal = False
        self.log_event("Décision invalidée")

    def log_event(self, message):
        log_message = f"Décision {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

# Classe représentant l'État central
class CentralGovernment:
    def __init__(self):
        self.act_counter = 0
        self.budget = random.randint(BUDGET_MIN, BUDGET_MAX)
        self.acts = []

    def create_act(self):
        self.act_counter += 1
        act = AdministrativeAct(
            act_id=self.act_counter,
            text=f'Acte Gouvernement {self.act_counter}',
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.acts.append(act)
        return act

    def allocate_budget(self, region):
        allocation = random.randint(5000, 20000)
        if self.budget >= allocation:
            self.budget -= allocation
            region.receive_funds(allocation)
            print(f"Gouvernement central alloue {allocation} € à {region.name}")
        else:
            print("Gouvernement central : Budget insuffisant pour allocation.")

    def reallocate_funds(self, department):
        """Réallocation des fonds aux départements en difficulté."""
        if self.budget > 10000 and department.resources < 5000:
            assistance = min(15000, self.budget)
            self.budget -= assistance
            department.resources += assistance
            print(f"Gouvernement central réaffecte {assistance} € au département {department.name}")
        else:
            print(f"Gouvernement central : Pas de fonds suffisants pour aider {department.name}")

# Classe représentant un préfet (niveau déconcentré)
class Prefect:
    def __init__(self, name):
        self.name = name
        self.review_counter = 0

    def check_legality(self, act):
        log_message = f"{self.name} : Contrôle de l'acte {act.id} avec complexité {act.complexity}"
        logging.info(log_message)
        print(log_message)

        if act.complexity > 6:
            act.invalidate()
        log_message = f"{self.name} : Contrôle terminé. Acte valide: {act.valid}"
        logging.info(log_message)

# Classe représentant le Conseil d'État
class ConseilEtat:
    def __init__(self):
        self.case_counter = 0

    def review_act(self, act):
        # Si l'acte est déjà invalidé par le préfet, le Conseil d'État ne peut pas le valider.
        if not act.valid:
            print(f"Conseil d'État : Acte {act.id} déjà invalidé par le préfet, aucune action possible.")
        else:
            # Le Conseil d'État vérifie la complexité de l'acte pour potentiellement l'invalider.
            if act.complexity > 8:
                act.invalidate()
                print(f"Conseil d'État : Acte {act.id} invalidé pour complexité excessive")
            else:
                print(f"Conseil d'État : Acte {act.id} validé")

    def handle_appeal(self, decision):
        """Réexamine une décision pour s'assurer de sa légalité."""
        if not decision.legal:
            decision.invalidate()
            print(f"Conseil d'État : Décision {decision.id} annulée")
        else:
            print(f"Conseil d'État : Décision {decision.id} confirmée")

# Classe représentant une région (niveau décentralisé)
class Region:
    def __init__(self, name):
        self.name = name
        self.budget = random.randint(BUDGET_MIN, BUDGET_MAX)
        self.projects = []

    def receive_funds(self, amount):
        self.budget += amount
        print(f"{self.name} a reçu {amount} €")

    def propose_project(self):
        project = f"Projet Régional {random.randint(1, 100)}"
        self.projects.append(project)
        print(f"{self.name} propose un nouveau projet : {project}")

# Classe représentant un département (niveau décentralisé)
class Department:
    def __init__(self, name):
        self.name = name
        self.resources = random.randint(30000, 100000)

    def manage_infrastructure(self):
        cost = random.randint(5000, 15000)
        if self.resources >= cost:
            self.resources -= cost
            print(f"{self.name} investit {cost} € dans l'infrastructure")
        else:
            print(f"{self.name} manque de ressources pour l'infrastructure")

# Classe représentant une commune (niveau décentralisé)
class Commune:
    def __init__(self, name):
        self.name = name
        self.population = random.randint(1000, 50000)

    def provide_local_services(self):
        print(f"{self.name} fournit des services locaux à ses {self.population} habitants")

# Classe principale orchestrant la simulation
class FrenchAdministration:
    def __init__(self):
        self.government = CentralGovernment()
        self.prefect = Prefect("Préfet de Région")
        self.conseil_etat = ConseilEtat()
        self.regions = [Region("Île-de-France"), Region("Provence-Alpes-Côte d'Azur")]
        self.departments = [Department("Hauts-de-Seine"), Department("Bouches-du-Rhône")]
        self.communes = [Commune("Paris"), Commune("Marseille")]
        self.iteration = 0  # Initialisation de l'attribut 'iteration'
        
    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            print(f"\n{'='*20} JOUR {self.iteration} {'='*20}")

            act = self.government.create_act()
            self.prefect.check_legality(act)
            self.conseil_etat.review_act(act)

            for region in self.regions:
                region.propose_project()
                self.government.allocate_budget(region)

            for department in self.departments:
                department.manage_infrastructure()
                # Réallocation des ressources en cas de difficulté financière
                self.government.reallocate_funds(department)

            for commune in self.communes:
                commune.provide_local_services()

            await asyncio.sleep(1)

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            print(f"\n{'='*20} JOUR {self.iteration} {'='*20}")

            # Le gouvernement crée un nouvel acte
            act = self.government.create_act()

            # Préfet vérifie la légalité
            self.prefect.check_legality(act)

            # Conseil d'État effectue un contrôle supplémentaire
            self.conseil_etat.review_act(act)

            # Les régions proposent des projets
            for region in self.regions:
                region.propose_project()
                self.government.allocate_budget(region)

            # Les départements gèrent des infrastructures
            for department in self.departments:
                department.manage_infrastructure()

            # Les communes fournissent des services
            for commune in self.communes:
                commune.provide_local_services()

            await asyncio.sleep(1)

        print("Simulation terminée.")

# Point d'entrée principal
async def main():
    administration = FrenchAdministration()
    await administration.simulate()

asyncio.run(main())