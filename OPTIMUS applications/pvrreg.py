import time
import random

# Functional Units
class President:
    def __init__(self):
        self.regulations_signed = 0
    
    def enact_decree(self, council_approval):
        if council_approval:
            self.regulations_signed += 1
            return "Decree enacted by President"
        else:
            return "Decree blocked by Council"

class PrimeMinister:
    def __init__(self):
        self.regulations_issued = 0
        self.delegations = 0
    
    def issue_regulation(self, law_executive_scope):
        if law_executive_scope:
            self.regulations_issued += 1
            return "Regulation issued by Prime Minister"
        else:
            return "Regulation outside executive scope"
    
    def delegate_power(self):
        self.delegations += 1
        return f"Delegated power {self.delegations} times"

class JudicialOversight:
    def __init__(self):
        self.regulations_reviewed = 0
    
    def review_regulation(self, regulation_valid):
        self.regulations_reviewed += 1
        if regulation_valid:
            return "Regulation upheld by Judiciary"
        else:
            return "Regulation invalidated by Judiciary"

# Simulation Orchestration
class RegulatorySimulation:
    def __init__(self):
        self.president = President()
        self.prime_minister = PrimeMinister()
        self.judiciary = JudicialOversight()
        self.iterations = 0
    
    def simulate_cycle(self):
        # Simulating President's decree enactment
        council_approval = random.choice([True, False])
        print(self.president.enact_decree(council_approval))
        
        # Simulating Prime Minister's regulation issuance
        law_executive_scope = random.choice([True, False])
        print(self.prime_minister.issue_regulation(law_executive_scope))
        
        # Simulating power delegation
        if random.random() > 0.7:  # 30% chance of delegation
            print(self.prime_minister.delegate_power())
        
        # Simulating Judiciary review
        regulation_valid = random.choice([True, False])
        print(self.judiciary.review_regulation(regulation_valid))
        
        self.iterations += 1
    
    def run_simulation(self, cycles):
        print(f"Starting simulation for {cycles} cycles...\n")
        for _ in range(cycles):
            print(f"Cycle {_ + 1}")
            self.simulate_cycle()
            print("-" * 30)
            time.sleep(1)  # Simulating time progression
        self.display_stats()
    
    def display_stats(self):
        print("\nSimulation Completed!")
        print(f"Total Cycles: {self.iterations}")
        print(f"Presidential Decrees Signed: {self.president.regulations_signed}")
        print(f"Prime Minister Regulations Issued: {self.prime_minister.regulations_issued}")
        print(f"Powers Delegated by Prime Minister: {self.prime_minister.delegations}")
        print(f"Judicial Reviews Conducted: {self.judiciary.regulations_reviewed}")

# Run the simulation
if __name__ == "__main__":
    society = RegulatorySimulation()
    society.run_simulation(cycles=10)