# political_systems.py
import logging
import random
from norms import Law, Regulation

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

    def perform_actions(self):
        actions = [norm.text for norm in self.norm_pool[-3:]]
        logging.info(f"{self.get_body_name()}: Performed actions: {actions}")
        return actions

    def random_event(self):
        events = ["Economic Boom", "Economic Crisis", "Social Movement", "Natural Disaster", "Election"]
        event = random.choice(events)
        logging.info(f"{self.get_body_name()}: Random event occurred: {event}")
        return event

    def reform_norm(self, norm_id):
        for norm in self.norm_pool:
            if norm.id == norm_id:
                new_complexity = random.randint(1, 10)
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
            complexity=random.randint(1, 10)
        )

    def get_body_name(self):
        return "PARLIAMENT"

    def get_norm_type(self):
        return "LAW"

    def get_dissolved(self):
        """Dissolve the parliament and reset norms."""
        self.norm_pool = []
        self.norm_counter = 0
        self.norm_ids.clear()
        logging.info("PARLIAMENT: The National Assembly has been dissolved. All laws are reset.")

class Government(PoliticalSystem):
    def __init__(self, prime_minister=""):
        super().__init__()
        self.prime_minister = prime_minister
        self.in_emergency_state = False
        self.article_49_3_count = 0
        logging.info(f"GOVERNMENT: Initialized under Prime Minister {self.prime_minister}")

    def get_body_name(self):
        return "GOVERNMENT"

    def create_norm(self):
        regulation = Regulation(
            norm_id=self.regulation_counter,
            text=f'Regulation {self.regulation_counter}',
            valid=True,  # Regulations are assumed valid initially
            complexity=random.randint(1, 10)
        )
        self.regulation_counter += 1
        return regulation

    def use_49_3(self, law):
        """Use Article 49.3 to pass a law without a vote."""
        self.article_49_3_count += 1
        law.adopted_without_vote = True
        logging.info(f"GOVERNMENT: Used 49.3 to adopt Law {law.id} without vote.")
        self.judicial_system.control_norm_constitutionality(law)

    def handle_emergency_state(self):
        """Declare an emergency state."""
        self.in_emergency_state = True
        logging.info(f"GOVERNMENT: State of emergency declared.")

    def lift_emergency_state(self):
        """Lift the emergency state."""
        self.in_emergency_state = False
        logging.info(f"GOVERNMENT: State of emergency lifted.")

    def get_norm_type(self):
        return "REGULATION"

class President(PoliticalSystem):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.dissolution_count = 0
        logging.info(f"PRESIDENT: President {self.name} inaugurated")

    def attempt_veto(self, laws):
        """Attempt to veto a law every 15 iterations."""
        if laws:
            law_to_veto = random.choice(laws)
            logging.info(f"PRESIDENT: Vetoed law {law_to_veto.id}")
            return law_to_veto
        return None

    def dissolve_assembly(self, parliament):
        """Dissolve the National Assembly once."""
        if self.dissolution_count < 1:
            parliament.get_dissolved()
            self.dissolution_count += 1
            logging.info("PRESIDENT: Dissolved the National Assembly.")
        else:
            logging.info("PRESIDENT: Dissolution limit reached.")

    def get_body_name(self):
        return "PRESIDENT"

    def get_norm_type(self):
        return "EXECUTIVE ORDER"

class PrimeMinister(Government):
    def __init__(self, name):
        super().__init__(prime_minister=name)
        self.name = name
        logging.info(f"PRIME MINISTER: Prime Minister {self.name} appointed")

    def resign(self):
        """Handle resignation of the Prime Minister."""
        logging.info(f"PRIME MINISTER {self.name}: Resigned from office.")