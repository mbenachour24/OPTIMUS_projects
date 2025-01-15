import asyncio
import random
import logging
import matplotlib.pyplot as plt

# Setup enhanced logging
logging.basicConfig(level=logging.DEBUG, filename='mini_optimus.log', filemode='a', format='%(message)s')

# Constants
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
SIMULATION_DAYS = 50

class Norm:
    def __init__(self, norm_id, text, valid=True, complexity=1):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.history = []  # Track changes to the norm
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        self.valid = False
        self.history.append(('invalidated', self.complexity))
        self.log_event("Invalidated")

    def update_complexity(self, adjustment):
        old_complexity = self.complexity
        self.complexity = max(COMPLEXITY_MIN, min(COMPLEXITY_MAX, self.complexity + adjustment))
        self.history.append(('complexity_update', old_complexity, self.complexity))
        self.log_event(f"Complexity updated from {old_complexity} to {self.complexity}")

    def log_event(self, message):
        log_message = f"Norm {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

class Case:
    def __init__(self, case_id, text, norm):
        self.id = case_id
        self.text = text
        self.norm = norm
        self.constitutional = norm.valid
        self.log_event("A new case is brought to the Courts")

    def influence_norm(self):
        if self.constitutional:
            adjustment = random.randint(-2, 2)
            self.norm.update_complexity(adjustment)
            self.log_event(f"Influenced the associated norm's complexity by {adjustment}")

    def log_event(self, message):
        log_message = f"Case {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0
        self.valid_norms_history = []
        self.invalid_norms_history = []

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            log_message = f"\n\n{'='*20} START OF DAY {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)

            # Political system creates a norm
            norm = self.parliament.create_norm()
            log_message = f"Political System produced: {norm.text}"
            logging.info(log_message)
            print(log_message)

            # Judicial system checks constitutionality
            self.judicial_system.check_constitutionality(norm)

            # Judicial system creates a case
            case = self.judicial_system.create_case(norm)
            if case:
                log_message = f"Judicial System produced: {case.text}"
                logging.info(log_message)
                print(log_message)

                # Cases influence norms (dynamic reconfiguration)
                case.influence_norm()

            # Track valid and invalid norms
            self.valid_norms_history.append(len([n for n in self.parliament.norms if n.valid]))
            self.invalid_norms_history.append(len([n for n in self.parliament.norms if not n.valid]))

            log_message = f"\n{'='*20} END OF DAY {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)
            
            await asyncio.sleep(0.1)  # Simulate the passage of time

        logging.info("Simulation completed.")
        self.plot_results()

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.valid_norms_history, label='Valid Norms')
        plt.plot(self.invalid_norms_history, label='Invalid Norms')
        plt.xlabel('Days')
        plt.ylabel('Number of Norms')
        plt.title('Simulation of Norm Validation Over Time')
        plt.legend()
        plt.show()

class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0
        self.norms = []

    def create_norm(self):
        self.norm_counter += 1
        norm = Norm(
            norm_id=self.norm_counter,
            text=f'Law {self.norm_counter}',
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.norms.append(norm)
        return norm

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.cases = []

    def check_constitutionality(self, norm):
        log_message = f"Judicial System: Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)
        print(log_message)
        
        if norm.complexity > 5:
            norm.invalidate()
        
        log_message = f"Judicial System: Norm {norm.id} has been checked for constitutionality. Valid status: {norm.valid}"
        logging.info(log_message)
        print(log_message)

    def create_case(self, norm):
        if not norm.valid:
            log_message = f"Judicial System: Cannot create case based on invalid norm {norm.id}"
            logging.info(log_message)
            print(log_message)
            return None

        self.case_counter += 1
        case = Case(
            case_id=self.case_counter,
            text=f'Case {self.case_counter} referencing {norm.text}',
            norm=norm
        )
        self.cases.append(case)
        return case

# Main function to run the simulation
async def main():
    society = Society()
    await society.simulate()

# Run the simulation
asyncio.run(main())