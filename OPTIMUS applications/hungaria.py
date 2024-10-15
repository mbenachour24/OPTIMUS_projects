import random
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, filename='hungarian_crisis.log', filemode='a', format='%(message)s')

COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
SIMULATION_DAYS = 100

# Constants reflecting the crisis dynamics
JUDICIAL_WEAKENING_PROBABILITY = 0.7  # 70% chance that a norm will reduce judicial power
POLITICAL_OVERREACH_PROBABILITY = 0.6  # 60% chance that political norms bypass judicial checks

# Norm Class
class Norm:
    def __init__(self, norm_id, text, valid=True, complexity=1):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.undermines_judiciary = False
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        self.valid = False
        self.log_event("Repealed due to unconstitutionality")
        
    def log_event(self, message):
        logging.info(f"Norm {self.id}: {message}")
        print(f"Norm {self.id}: {message}")

# Case Class to represent judicial cases
class Case:
    def __init__(self, case_id, text, norm):
        self.id = case_id
        self.text = text
        self.norm = norm
        self.constitutional = norm.valid
        self.log_event("Filed in the judicial system")

    def log_event(self, message):
        logging.info(f"Case {self.id}: {message}")
        print(f"Case {self.id}: {message}")

# PoliticalSystem with increased aggressiveness in norm production
class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0
        self.norms = []

    def make_decision(self):
        self.norm_counter += 1
        norm_text = f'Norm {self.norm_counter}: Legal Reform'
        valid = random.choice([True, False])
        complexity = random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        norm = Norm(norm_id=self.norm_counter, text=norm_text, valid=valid, complexity=complexity)

        # Political overreach produces norms that limit the judiciary
        if random.random() < POLITICAL_OVERREACH_PROBABILITY:
            norm.undermines_judiciary = True
            norm.log_event("This norm limits judicial independence!")
        else:
            norm.log_event("Produced without limiting the judiciary.")

        self.norms.append(norm)
        logging.info(f"Political System produced: {norm.text}")
        return norm

# JudicialSystem with reduced autonomy
class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.cases = []
        self.judicial_power = 1.0  # Start with full power, but this will reduce

    def weaken_judicial_power(self, norm):
        if norm.undermines_judiciary and random.random() < JUDICIAL_WEAKENING_PROBABILITY:
            self.judicial_power -= 0.1  # Judicial power decreases over time
            logging.info(f"Judicial System: Power reduced by 10%. Current power: {self.judicial_power * 100}%")
            return True
        return False

    def check_constitutionality(self, norm):
        if self.judicial_power <= 0.3:  # If judicial power is too weak, invalid norms might pass
            logging.info(f"Judicial System: Too weak to fully check constitutionality of {norm.id}.")
        elif not norm.valid:
            norm.invalidate()
            norm.log_event("Constitutionality check: Unconstitutional.")
        else:
            norm.log_event("Constitutionality check: Constitutional.")

    def produce_cases(self, norm):
        if not norm.valid:
            logging.info(f"Judicial System: Cannot create case based on invalid norm {norm.id}")
            return None

        self.case_counter += 1
        case = Case(
            case_id=self.case_counter,
            text=f'Case {self.case_counter} referencing {norm.text}',
            norm=norm
        )
        self.cases.append(case)
        logging.info(f"Judicial System produced: {case.text}")
        return case

# Society Class to simulate the Hungarian crisis
class Society:
    def __init__(self):
        self.political_system = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            logging.info(f"\n\n--- DAY {self.iteration} ---\n")

            # Simulate political events and norm production
            event = random.choice(["Constitutional Amendment", "Court Packing", "Executive Overreach"])
            logging.info(f"Political System: Random event occurred: {event}")

            # Political system creates a norm
            norm = self.political_system.make_decision()

            # Judicial system checks constitutionality and weakens power if necessary
            if self.judicial_system.weaken_judicial_power(norm):
                logging.info(f"Judicial System: Weakened by the political norm {norm.id}.")

            self.judicial_system.check_constitutionality(norm)
            self.judicial_system.produce_cases(norm)

            logging.info(f"Society: Iteration {self.iteration} - Judicial Power: {self.judicial_system.judicial_power * 100}%\n")
            await asyncio.sleep(0.1)  # Simulate time

# Running the simulation for the Hungarian model
async def main():
    society = Society()
    await society.simulate()

asyncio.run(main())
