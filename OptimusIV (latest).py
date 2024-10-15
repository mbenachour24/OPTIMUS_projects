import asyncio
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests
import matplotlib.pyplot as plt
import random
import time
import logging

# Configuration globale du logger
def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Supprimer tous les handlers existants pour éviter la duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler pour le fichier
    file_handler = logging.FileHandler('journalofficiel.log', 'a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler pour le terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info("Logger configuration complete without duplication.")

# Appeler la configuration du logger
configure_logger()

# Ajout d'une configuration distincte pour enregistrer dans un autre fichier
file_specific_handler = logging.FileHandler('OFFICIALJOURNAL2.log', 'a')
file_specific_handler.setLevel(logging.DEBUG)
file_specific_formatter = logging.Formatter('%(message)s')
file_specific_handler.setFormatter(file_specific_formatter)

# Ajout du handler spécifique
logger = logging.getLogger()
logger.addHandler(file_specific_handler)

# Constants
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
CITIZEN_PRESSURE_MIN = 1
CITIZEN_PRESSURE_MAX = 10
SIMULATION_DAYS = 365
MAX_CASSATIONS = 3

class Norm:
    def __init__(self, norm_id, text, valid, complexity, norm_type="ordinaire"):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.norm_type = norm_type
        self.history = []
        logging.info(f"Norm {self.id}: Initialized with complexity {complexity} and validity {valid}")

    def update_complexity(self, adjustment):
        old_complexity = self.complexity
        self.complexity = max(COMPLEXITY_MIN, min(COMPLEXITY_MAX, self.complexity + adjustment))
        logging.info(f"Norm {self.id}: Updated complexity from {old_complexity} to {self.complexity}")
        self.history.append(('complexity', self.complexity, time.time()))

    def invalidate(self):
        self.valid = False
        logging.info(f"Norm {self.id}: Invalidated")
        self.history.append(('valid', self.valid, time.time()))

    def validate(self):
        self.valid = True
        logging.info(f"Norm {self.id}: Validated")
        self.history.append(('valid', self.valid, time.time()))

    def get_history(self):
        logging.info(f"Norm {self.id}: Getting history")
        return self.history

    def __str__(self):
        return f"Norm(id={self.id}, text={self.text}, valid={self.valid}, complexity={self.complexity})"

class Law(Norm):
    pass

class Regulation(Norm):
    pass

class Case:
    def __init__(self, case_id, text, norm_id, constitutional, complexity):
        self.id = case_id
        self.text = text
        self.norm_id = norm_id
        self.constitutional = constitutional
        self.complexity = complexity
        self.history = []
        self.cassation_count = 0
        self.status = {
            "first_instance": False,
            "appeal": False,
            "cassation": 0  # Track the number of cassations
        }
        self.final_outcome = None
        logging.info(f"Case {self.id}: A new case is brought to the Courts")

    def apply_precedent(self, precedent):
        self.constitutional = precedent
        logging.info(f"Case {self.id}: Applied precedent, reaffirmed validity status of norm: {self.constitutional}")
        self.history.append(('constitutional', self.constitutional, time.time()))

    def update_complexity(self, adjustment):
        old_complexity = self.complexity
        self.complexity = max(COMPLEXITY_MIN, min(COMPLEXITY_MAX, self.complexity + adjustment))
        logging.info(f"Case {self.id}: Updated complexity from {old_complexity} to {self.complexity}")
        self.history.append(('complexity', self.complexity, time.time()))

    def process_in_first_instance(self):
        if not self.status["first_instance"]:
            self.status["first_instance"] = True
            logging.info(f"Case {self.id}: Processing in First Instance Court")
            self.final_outcome = self.simulate_hearing()
            return self.final_outcome
        return None

    def process_in_appeal(self):
        if not self.status["appeal"]:
            self.status["appeal"] = True
            logging.info(f"Case {self.id}: Processing in Appeal Court")
            self.final_outcome = self.simulate_hearing()
            return self.final_outcome
        return None

    def process_in_cassation(self):
        if self.status["cassation"] < MAX_CASSATIONS:
            self.status["cassation"] += 1
            logging.info(f"Case {self.id}: Processing in Court of Cassation, cassation count: {self.status['cassation']}")
            cassation_outcome = self.simulate_hearing()
            if cassation_outcome == "accepted":
                self.final_outcome = "accepted"
                return "accepted"
            elif cassation_outcome == "rejected":
                self.status["appeal"] = False  # Reset appeal status
                return "rejected"
        return None

    def simulate_hearing(self):
        return random.choice(["accepted", "rejected"])

    def get_history(self):
        logging.info(f"Case {self.id}: Getting history")
        return self.history

    def __str__(self):
        return f"Case(id={self.id}, text={self.text}, norm_id={self.norm_id}, constitutional={self.constitutional}, complexity={self.complexity})"

class Court:
    def __init__(self, court_name):
        self.court_name = court_name
        logging.info(f"{self.court_name} Court: Initialized")

    def file_case(self, case):
        logging.info(f"{self.court_name} Court: Case {case.id} filed")
        logging.info(f"Case {case.id}: Filed in {self.court_name} court")

    def conduct_hearing(self, case):
        logging.info(f"{self.court_name} Court: Conducted hearing for case {case.id}")
        logging.info(f"Case {case.id}: Hearing conducted in {self.court_name} court")

    def render_judgment(self, case):
        judgment = random.choice(["accepted", "rejected"])
        logging.info(f"{self.court_name} Court: Rendered judgment for case {case.id}: {judgment}")
        logging.info(f"Case {case.id}: Judgment rendered in {self.court_name} court: {judgment}")
        return judgment

class PoliticalSystem:
    def __init__(self):
        self.norm_pool = []
        self.norm_counter = 0
        self.norm_ids = set()
        self.regulation_pool = []
        self.regulation_counter = 0
        self.action = "decision"
        self.judicial_system = None

    def generate_norms(self):
        new_norm = self.create_norm()
        if new_norm and new_norm.id not in self.norm_ids:
            self.norm_pool.append(new_norm)
            self.norm_counter += 1
            self.norm_ids.add(new_norm.id)
            logging.info(f"{self.get_body_name()}: Generated new {self.get_norm_type()}")
            if isinstance(new_norm, Law):
                self.judicial_system.control_norm_constitutionality(new_norm, "CONTRÔLE OBLIGATOIRE A PRIORI")

    def create_norm(self):
        raise NotImplementedError("Must be implemented by subclasses")

    def produce_norms_decision(self):
        if self.has_decision():
            new_norms = []
            for _ in range(2):
                new_norm = self.create_norm()
                if new_norm and new_norm.id not in self.norm_ids:
                    self.norm_pool.append(new_norm)
                    self.norm_counter += 1
                    self.norm_ids.add(new_norm.id)
                    if isinstance(new_norm, Law):
                        self.judicial_system.control_norm_constitutionality(new_norm, "CONTRÔLE DE CONSTITUTIONNALITÉ OBLIGATOIRE A PRIORI")
                    new_norms.append(new_norm)
                    logging.info(f"{self.get_body_name()}: Created new {self.get_norm_type()} by political decision")
            return new_norms
        return []

    def has_decision(self):
        return self.action == "decision"

    def send_expectations(self, citizen_pressure):
        expectations = [norm.text for norm in self.norm_pool[-3:]]
        if citizen_pressure > 3:
            expectations.append("Prioritize Norm Enforcement")
        logging.info(f"{self.get_body_name()}: Expectations sent based on citizen pressure: {citizen_pressure}")
        return expectations

    def receive_stabilization(self, stabilized_norms):
        for norm in stabilized_norms:
            logging.info(f"{self.get_body_name()}: Norm {norm.id} stabilized")
        logging.info(f"{self.get_body_name()}: The norms are being applied: stabilization")

    def make_regulations(self, citizen_pressure):
        raise NotImplementedError("Must be implemented by subclasses")

    def perform_actions(self):
        actions = [norm.text for norm in self.norm_pool[-3:]]
        logging.info(f"{self.get_body_name()}: Performed actions: {actions}")
        return actions

    def random_event(self):
        events = ["Economic Boom", "Economic Crisis", "Social Movement", "Natural Disaster", "nek mochta t3awej", "mostfa", "elections", "covid-19"]
        event = random.choice(events)
        logging.info(f"{self.get_body_name()}: Random event occurred: {event}")
        return event

    def reform_norm(self, norm_id):
        for norm in self.norm_pool:
            if norm.id == norm_id:
                new_complexity = random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
                norm.complexity = new_complexity
                norm.valid = random.choice([True, False])
                logging.info(f"{self.get_body_name()}: Norm {norm.id} reformed with new complexity {new_complexity} and validity {norm.valid}")
                self.judicial_system.control_norm_constitutionality(norm)
                break

    def get_body_name(self):
        raise NotImplementedError("Must be implemented by subclasses")

    def get_norm_type(self):
        raise NotImplementedError("Must be implemented by subclasses")

class Parliament(PoliticalSystem):
    def create_norm(self):
        return Law(
            norm_id=self.norm_counter,
            text=f'Law {self.norm_counter}',
            valid=random.choice([True, False]),
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )

    def make_regulations(self, citizen_pressure):
        return []  # Parliament doesn't make regulations

    def get_dissolved(self):
        """Dissolve the parliament and prepare for new elections."""
        self.norm_pool = []
        self.norm_counter = 0
        self.norm_ids.clear()
        logging.info(f"PARLIAMENT: The National Assembly has been dissolved. All laws are reset.")

    def get_body_name(self):
        return "PARLIAMENT"

    def get_norm_type(self):
        return "LAW"

class Government(PoliticalSystem):
    def __init__(self, prime_minister=""):
        super().__init__()
        self.prime_minister = prime_minister
        self.in_emergency_state = False  # State to track emergency status
        self.article_49_3_count = 0  # Track the usage of Article 49.3
        logging.info(f"GOVERNMENT: Initialized under Prime Minister {self.prime_minister}")

    def get_body_name(self):
        return "GOVERNMENT"

    def create_norm(self):
        regulation = Regulation(
            norm_id=self.regulation_counter,
            text=f'Regulation {self.regulation_counter}',
            valid=True,  # Regulations are assumed valid initially
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.regulation_counter += 1
        return regulation

    def make_regulations(self, citizen_pressure):
        regulations = []
        if citizen_pressure > 3 and self.norm_pool:
            norm = random.choice(self.norm_pool)
            regulation_a = Regulation(
                norm_id=self.regulation_counter,
                text=f"Regulation {self.regulation_counter} based on Law {norm.id}",
                valid=True,
                complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
            )
            regulation_b = Regulation(
                norm_id=self.regulation_counter + 1,
                text=f"Regulation {self.regulation_counter + 1} based on Law {norm.id}",
                valid=True,
                complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
            )
            regulations.extend([regulation_a, regulation_b])
            self.regulation_counter += 2
            self.regulation_pool.extend([regulation_a, regulation_b])
            logging.info(f"GOVERNMENT: Made regulations based on citizen pressure: {[regulation_a.text, regulation_b.text]}")
        return regulations

    def handle_emergency_state(self):
        """Manage actions during emergency state."""
        self.in_emergency_state = True
        logging.info(f"GOVERNMENT: State of emergency declared. Special measures in effect.")

    def lift_emergency_state(self):
        """Lift the emergency state and return to normal operation."""
        self.in_emergency_state = False
        logging.info(f"GOVERNMENT: State of emergency lifted. Returning to normal operations.")

    def use_49_3(self, law):
        """Simulate the use of Article 49.3 to pass a law without a vote."""
        self.article_49_3_count += 1
        law.adopted_without_vote = True
        logging.info(f"GOVERNMENT: Used 49.3 to adopt Law {law.id} without vote.")
        self.judicial_system.control_norm_constitutionality(law)
        
        # Check if engagement of responsibility and censure should be activated
        if self.article_49_3_count % 5 == 0:
            self.engagement_of_responsibility()

    def engagement_of_responsibility(self):
        """Simulate engagement of government's responsibility and potential censure."""
        if random.random() < 0.2:  # 20% chance of censure
            logging.info(f"GOVERNMENT: Engagement of responsibility failed. Government censured.")
            self.judicial_system.censure_government()
        else:
            logging.info(f"GOVERNMENT: Engagement of responsibility succeeded. Government not censured.")

    def get_norm_type(self):
        return "REGULATION"

class President(PoliticalSystem):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.iteration_count = 0
        self.dissolution_count = 0
        logging.info(f"PRESIDENT: President {self.name} inaugurated")

    def create_regulation_to_veto_law(self, law):
        """Create a regulation to veto a specific law."""
        regulation = Regulation(
            norm_id=self.regulation_counter,
            text=f"Regulation {self.regulation_counter} to veto Law {law.id}",
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.regulation_counter += 1
        logging.info(f"PRESIDENT: Created regulation {regulation.text} to veto Law {law.id}")
        return regulation

    def attempt_veto(self, laws):
        """Attempt to veto a law every 15 iterations."""
        self.iteration_count += 1
        if self.iteration_count % 15 == 0 and laws:
            law_to_veto = random.choice(laws)
            veto_regulation = self.create_regulation_to_veto_law(law_to_veto)
            logging.info(f"PRESIDENT: Vetoed law {law_to_veto.id} with regulation {veto_regulation.text}")
            return veto_regulation, law_to_veto
        return None, None
    
    def dissolve_assembly(self, parliament):
        """Dissolve the National Assembly and reconstitute without elections, limited to once."""
        if self.dissolution_count < 1:
            parliament.get_dissolved()
            parliament.reconstitute()
            self.dissolution_count += 1
            logging.info("PRESIDENT: Dissolved the National Assembly and reconstituted it without elections.")
        else:
            logging.info("PRESIDENT: Dissolution limit reached, cannot dissolve again.")

    def request_referendum(self, law):
        """Request a referendum on a specific law."""
        outcome = random.choice(["approved", "rejected"])
        logging.info(f"PRESIDENT: Requested a referendum on {law.text}. Outcome: {outcome}")
        return outcome

    def appoint_prime_minister(self, government, new_pm_name):
        """Appoint a new Prime Minister."""
        government.prime_minister = new_pm_name
        logging.info(f"PRESIDENT: Appointed {new_pm_name} as Prime Minister")

    def initiate_emergency_state(self, government):
        """Initiate an emergency state for handling crises."""
        government.handle_emergency_state()
        logging.info("PRESIDENT: Declared a state of emergency due to a national crisis.")

    def lift_emergency_state(self, government):
        """Lift the emergency state and return to normal operations."""
        government.lift_emergency_state()
        logging.info("PRESIDENT: State of emergency lifted, returning to normal operations.")

    def propose_amendment(self, law_text):
        """Propose an amendment to the constitution or law."""
        amendment = f"Amendment: {law_text}"
        logging.info(f"PRESIDENT: Proposed amendment: {amendment}")
        return amendment

    def coordinate_with_prime_minister(self, government):
        """Coordinate with the Prime Minister on policies."""
        logging.info(f"PRESIDENT: Coordinated with Prime Minister {government.prime_minister} on national policies.")

    def get_body_name(self):
        """Return the name of the body, i.e., PRESIDENT."""
        return "PRESIDENT"

    def get_norm_type(self):
        """Return the type of norms the President creates, which are EXECUTIVE ORDERS."""
        return "EXECUTIVE ORDER"

class PrimeMinister(Government):
    def __init__(self, name):
        super().__init__(prime_minister=name)
        self.name = name
        logging.info(f"PRIME MINISTER: Prime Minister {self.name} appointed")

    def get_body_name(self):
        return "PRIME MINISTER"

    def create_norm(self):
        return None  # The Prime Minister oversees the Government but does not directly create norms

    def get_norm_type(self):
        return "POLICY DECISION"

    def form_new_government(self):
        """Form a new government by appointing new ministers."""
        self.norm_pool = []  # Clear all existing regulations
        self.regulation_pool = []  # Clear all existing regulations
        logging.info(f"PRIME MINISTER {self.name}: Formed a new government with new policies and regulations.")

    def resign(self):
        """Handle resignation of the Prime Minister."""
        logging.info(f"PRIME MINISTER {self.name}: Resigned from office.")

    def appoint_ministers(self):
        """Appoint new ministers to the government."""
        ministers = ["Minister of Finance", "Minister of Education", "Minister of Health"]
        for minister in ministers:
            logging.info(f"PRIME MINISTER {self.name}: Appointed {minister}.")

    def activate_49_3(self, law):
        """Prime Minister activates Article 49.3 for a law."""
        logging.info(f"PRIME MINISTER {self.name}: Activated 49.3 for Law {law.id}.")
        self.use_49_3(law)

    def handle_censure(self):
        """Handle the scenario when the government is censured."""
        logging.info(f"PRIME MINISTER {self.name}: Government censured. Preparing resignation and new government formation.")
        self.resign()
        self.form_new_government()

class JudicialSystem:
    def __init__(self, parliament, government, president):
        self.case_pool = []
        self.case_counter = 0
        self.case_ids = set()
        self.parliament = parliament
        self.government = government
        self.president = president
        self.precedents = {}
        self.valid_rules = []
        self.caseload = 0
        self.judicial_decisions = 0
        self.norms_constitutionality = {}

        # Initialize subsystems here
        self.first_instance = FirstInstance("First Instance")
        self.appeal_court = Appeal("Appeal")
        self.cassation_court = Cassation("Court of Cassation")
        self.constitutional_council = Court("Constitutional Council")

    def control_norm_constitutionality(self, norm, check_type="CONTRÔLE DE CONSTITUTIONNALITÉ"):
        if norm.id in self.norms_constitutionality:
            is_constitutional = self.norms_constitutionality[norm.id]
        else:
            if check_type == "CONTRÔLE OBLIGATOIRE A PRIORI" and norm.norm_type == "ordinaire":
                # Simulate constitutionality check for ordinary laws
                is_constitutional = random.choice([True, False])
            else:
                is_constitutional = norm.valid
            self.norms_constitutionality[norm.id] = is_constitutional

        logging.info(f"JudicialSystem: {check_type} for norm {norm.id}: {'constitutional' if is_constitutional else 'unconstitutional'}")
        if not is_constitutional:
            self.remove_norm(norm)
            logging.info(f"Norm {norm.id}: Abrogated and canceled due to unconstitutionality")
        return is_constitutional

    def remove_norm(self, norm):
        if isinstance(norm, Law):
            self.parliament.norm_pool.remove(norm)
        elif isinstance(norm, Regulation):
            self.government.norm_pool.remove(norm)

    def control_regulation_legality(self, regulation):
        is_legal = random.choice([True, False])
        logging.info(f"JudicialSystem: Legality check for regulation {regulation.id}: {'legal' if is_legal else 'illegal'}")
        if not is_legal:
            law_id = int(regulation.text.split("Law ")[-1])
            law_to_check = next((law for law in self.parliament.norm_pool if law.id == law_id), None)
            if law_to_check:
                self.control_norm_constitutionality(law_to_check)
        return is_legal

    def inspect_veto_legality(self, law):
        is_legal = random.choice([True, False])
        logging.info(f"JudicialSystem: Veto legality check for law {law.id}: {'legal' if is_legal else 'illegal'}")
        if not is_legal:
            self.remove_norm(law)
            logging.info(f"Law {law.id}: Veto deemed illegal and law remains invalidated")
        else:
            self.control_norm_constitutionality(law, "CONTRÔLE DE CONSTITUTIONNALITÉ POST-VETO")

    def generate_case(self):
        if self.parliament.norm_pool or self.government.norm_pool:
            norm = random.choice(self.parliament.norm_pool + self.government.norm_pool)
            if self.case_counter not in self.case_ids:
                new_case = Case(
                    case_id=self.case_counter,
                    text=f'Case {self.case_counter} referencing {norm.text}',
                    norm_id=norm.id,
                    constitutional=self.control_norm_constitutionality(norm),
                    complexity=norm.complexity
                )
                self.case_pool.append(new_case)
                self.case_ids.add(self.case_counter)
                self.case_counter += 1
                logging.info(f"JudicialSystem: Generated new case: {new_case}")

    def control_political_actions(self, political_actions):
        for action in political_actions:
            new_norm = Law(
                norm_id=self.parliament.norm_counter,
                text=action,
                valid=True,
                complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
            )
            if new_norm.id not in self.parliament.norm_ids:
                self.parliament.norm_pool.append(new_norm)
                self.parliament.norm_counter += 1
                self.parliament.norm_ids.add(new_norm.id)
                is_constitutional = self.control_norm_constitutionality(new_norm)
                action_result = "annulled due to unconstitutionality" if not is_constitutional else "deemed constitutional"
                logging.info(f"JudicialSystem: Political act '{action}' {action_result}")

    def process_cases(self):
        for case in self.case_pool[:]:
            self.first_instance.file_case(case)
            self.first_instance.conduct_hearing(case)
            judgment = self.first_instance.render_judgment(case)
            case.final_outcome = judgment

            if case.final_outcome == "rejected":
                self.appeal_court.file_case(case)
                self.appeal_court.conduct_hearing(case)
                judgment = self.appeal_court.render_judgment(case)
                case.final_outcome = judgment

                if case.final_outcome == "rejected":
                    while case.cassation_count < MAX_CASSATIONS:
                        case.cassation_count += 1
                        self.cassation_court.file_case(case)
                        self.cassation_court.conduct_hearing(case)
                        judgment = self.cassation_court.render_judgment(case)
                        case.final_outcome = judgment

                        if case.final_outcome == "rejected" and case.cassation_count < MAX_CASSATIONS:
                            self.appeal_court.file_case(case)
                            self.appeal_court.conduct_hearing(case)
                            judgment = self.appeal_court.render_judgment(case)
                            case.final_outcome = judgment

                            if case.final_outcome == "accepted":
                                break

                    if case.cassation_count == MAX_CASSATIONS and case.final_outcome == "rejected":
                        logging.info(f"JudicialSystem: Case {case.id} rejected after too many cassations")

            self.apply_precedent(case)
            self.set_precedent(case)
            logging.info(f"Case {case.id}: Processed with outcome: {case.final_outcome}")
            self.case_pool.remove(case)

    def set_precedent(self, case):
        self.precedents[case.norm_id] = case.final_outcome
        logging.info(f"JudicialSystem: Set precedent for norm {case.norm_id}: {case.final_outcome}")

    def apply_precedent(self, case):
        if case.norm_id in self.precedents:
            case.apply_precedent(self.precedents[case.norm_id])
            logging.info(f"JudicialSystem: Applied precedent to case {case.id}: {case.final_outcome}")

    def address_expectations(self, expectations, citizen_pressure):
        self.caseload += citizen_pressure
        for expectation in expectations:
            if expectation in [norm.text for norm in self.parliament.norm_pool + self.government.norm_pool]:
                logging.info(f"JudicialSystem: Applying {expectation} to relevant cases")

    async def produce_judicial_decisions(self, iteration):
        if self.caseload > 0 and self.valid_rules:
            decisions_made = min(self.caseload, 5)
            self.judicial_decisions += decisions_made
            self.caseload -= decisions_made
            logging.info(f"JudicialSystem: Produced {decisions_made} judicial decisions during iteration {iteration}. Remaining caseload: {self.caseload}")
        else:
            logging.info("JudicialSystem: No decisions made due to lack of cases or valid rules")
        await asyncio.sleep(0.1)

    def question_prioritaire_de_constitutionnalite(self, citizen_pressure):
        if citizen_pressure > 7:
            logging.info("JudicialSystem: Triggered 'Question Prioritaire de Constitutionnalite' due to high citizen pressure")

    def stabilize_norms(self, norms):
        for norm in norms:
            logging.info(f"Norm {norm.id}: Reinforced through consistent application")

    def apply_decisions(self, decisions):
        for decision in decisions:
            logging.info(f"JudicialSystem: Applying political decision '{decision.text}'")

    def is_legal(self):
        return bool(self.valid_rules)

    def receive_rules(self, rules):
        self.valid_rules.extend(rules)
        for rule in rules:
            logging.info(f"Law {rule} est entrée en vigueur")

    def calculate_backlog(self):
        backlog_length = len(self.case_pool)
        logging.info(f"JudicialSystem: Backlog length: {backlog_length}")
        return self.caseload

    def censure_government(self):
        """Handle the censure of the government."""
        logging.info(f"JudicialSystem: The government has been censured. A new Prime Minister must be appointed.")
        self.president.appoint_prime_minister(self.government, "New Prime Minister")

class FirstInstance(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"FirstInstance Court: Initialized {court_name} court")

class Appeal(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"Appeal Court: Initialized {court_name} court")

class Cassation(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"Cassation Court: Initialized {court_name} court")

class Society:
    norms = {}
    regulations = {}

    def __init__(self, use_fixed_seed=True):
        if use_fixed_seed:
            random.seed(1)
        self.president = President("Jean Dupont")
        self.prime_minister = PrimeMinister("Alice Martin")
        self.government = Government(prime_minister=self.prime_minister.name)
        self.parliament = Parliament()
        self.judicial_system = JudicialSystem(self.parliament, self.government, self.president)
        self.parliament.judicial_system = self.judicial_system
        self.government.judicial_system = self.judicial_system
        self.iteration = 0
        self.caseload_history = []
        self.normative_inflation_history = []
        self.temporal_gap_history = []
        self.history = []

    def check_constitutionality(self, norm, current_iteration):
        try:
            if norm.id not in Society.norms or Society.norms[norm.id]['last_checked_iteration'] != current_iteration:
                is_constitutional = self.judicial_system.control_norm_constitutionality(norm)
                Society.norms[norm.id] = {'constitutional': is_constitutional, 'last_checked_iteration': current_iteration}
            else:
                logging.info(f"Norm {norm.id}: Already checked in this iteration")
        except Exception as e:
            logging.info(f"Norm {norm.id}: Error checking constitutionality: {str(e)}")

    def check_legality(self, regulation, current_iteration):
        try:
            if regulation.id not in Society.regulations or Society.regulations[regulation.id]['last_checked_iteration'] != current_iteration:
                is_legal = self.judicial_system.control_regulation_legality(regulation)
                Society.regulations[regulation.id] = {'legal': is_legal, 'last_checked_iteration': current_iteration}
            else:
                logging.info(f"Regulation {regulation.id}: Already checked in this iteration")
        except Exception as e:
            logging.info(f"Regulation {regulation.id}: Error checking legality: {str(e)}")

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            logging.info(f"\n\n--- DAY {self.iteration} ---\n")

            citizen_pressure = random.randint(CITIZEN_PRESSURE_MIN, CITIZEN_PRESSURE_MAX)
            event = self.parliament.random_event()
            citizen_pressure = self.adjust_citizen_pressure(event, citizen_pressure)

            self.parliament.generate_norms()
            self.government.generate_norms()

            vetoed_regulation, vetoed_law = self.president.attempt_veto(self.parliament.norm_pool)
            if vetoed_regulation and vetoed_law:  # Check if both regulation and law exist
                self.judicial_system.inspect_veto_legality(vetoed_law)

            self.judicial_system.generate_case()
            self.judicial_system.process_cases()

            expectations = self.parliament.send_expectations(citizen_pressure)
            self.judicial_system.address_expectations(expectations, citizen_pressure)
            
            regulations = self.government.make_regulations(citizen_pressure)
            for regulation in regulations:
                self.check_legality(regulation, self.iteration)
                
            self.judicial_system.apply_decisions(regulations)

            new_rules = self.parliament.perform_actions()
            self.judicial_system.receive_rules(new_rules)
            await self.judicial_system.produce_judicial_decisions(self.iteration)

            political_actions = self.parliament.perform_actions()
            self.judicial_system.control_political_actions(political_actions)

            if random.random() < 0.1:  # 10% chance to reform a norm each day
                norm_to_reform = random.choice(self.parliament.norm_pool)
                self.parliament.reform_norm(norm_to_reform.id)

            self.track_histories()
            self.print_status()

        await self.finalize_simulation()


    def adjust_citizen_pressure(self, event, citizen_pressure):
        adjustments = {
            "Economic Boom": random.randint(1, 5),
            "Economic Crisis": -random.randint(1, 5),
            "Social Movement": random.randint(2, 7),
            "Natural Disaster": random.randint(1, 3),
            "nek mochta t3awej": random.randint(2, 5)
        }
        return citizen_pressure + adjustments.get(event, 0)

    def track_histories(self):
        self.caseload_history.append(self.judicial_system.caseload)
        self.normative_inflation_history.append(len(self.parliament.norm_pool) + len(self.government.norm_pool))
        self.temporal_gap_history.append(self.parliament.norm_counter + self.government.norm_counter - self.judicial_system.caseload)
        self.history.append({
            'iteration': self.iteration,
            'norms': [norm.__dict__ for norm in self.parliament.norm_pool + self.government.norm_pool],
            'decisions': self.judicial_system.valid_rules.copy(),
            'judicial_decisions': self.judicial_system.judicial_decisions
        })

    def print_status(self):
        normative_inflation = self.parliament.norm_counter + self.government.norm_counter
        caseload = self.judicial_system.caseload
        temporal_gap = normative_inflation - caseload
        logging.info(f"Society: Normative Inflation: {normative_inflation}, Caseload: {caseload}, Temporal Gap: {temporal_gap}")
        logging.info(f"Society: Processing up to 5 cases per day, total processed: {self.judicial_system.judicial_decisions}")

    async def finalize_simulation(self):
        self.parliament.generate_norms()
        self.government.generate_norms()
        for norm in self.parliament.norm_pool + self.government.norm_pool:
            self.judicial_system.control_norm_constitutionality(norm, "CONTRÔLE DE CONSTITUTIONNALITÉ")

        await asyncio.sleep(0.1)
        self.calculate_correlations()
        self.plot_results()
        self.perform_granger_test()

    def calculate_correlations(self):
        caseload_array = np.array(self.caseload_history)
        normative_inflation_array = np.array(self.normative_inflation_history)
        temporal_gap_array = np.array(self.temporal_gap_history)

        pearson_caseload_normative_inflation = np.corrcoef(caseload_array, normative_inflation_array)[0, 1]
        pearson_caseload_temporal_gap = np.corrcoef(caseload_array, temporal_gap_array)[0, 1]
        pearson_normative_inflation_temporal_gap = np.corrcoef(normative_inflation_array, temporal_gap_array)[0, 1]

        logging.info(f'Society: Pearson correlation between Caseload and Normative Inflation: {pearson_caseload_normative_inflation}')
        logging.info(f'Society: Pearson correlation between Caseload and Temporal Gap: {pearson_caseload_temporal_gap}')
        logging.info(f'Society: Pearson correlation between Normative Inflation and Temporal Gap: {pearson_normative_inflation_temporal_gap}')

    def plot_results(self):
        plt.figure(figsize=(9, 6))

        plt.subplot(2, 2, 1)
        plt.plot(range(1, len(self.caseload_history) + 1), self.caseload_history, label='Caseload')
        plt.xlabel('Iteration')
        plt.ylabel('Caseload')
        plt.title('Caseload over Time')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(range(1, len(self.normative_inflation_history) + 1), self.normative_inflation_history, label='Normative Inflation', color='red')
        plt.xlabel('Iteration')
        plt.ylabel('Number of Norms')
        plt.title('Normative Inflation over Time')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(range(1, len(self.temporal_gap_history) + 1), self.temporal_gap_history, label='Temporal Gap')
        plt.xlabel('Iteration')
        plt.ylabel('Temporal Gap (Norms - Caseload)')
        plt.title('Temporal Gap over Time')
        plt.legend()

        plt.suptitle('Caseload, Normative Inflation, and Temporal Gap Analysis')
        plt.tight_layout()
        plt.show()

    def perform_granger_test(self):
        data = np.column_stack((self.normative_inflation_history, self.caseload_history))
        max_lag = 10
        test_result = grangercausalitytests(data, max_lag, verbose=True)
        for lag, test in test_result.items():
            logging.info(f"Society: Lag {lag} - F-test: {test[0]['ssr_ftest']}, P-value: {test[0]['ssr_ftest'][1]}")

async def main():
    society = Society()
    await society.simulate()

asyncio.run(main())
