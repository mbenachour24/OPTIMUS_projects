import time
import random

# President class with executive powers including referenda, dissolving parliament, and exceptional powers (Article 16)
class President:
    def __init__(self):
        self.term_limit = 5  # Five-year term
        self.term_count = 0  # Two-term limit
        self.popularity = random.uniform(0.4, 0.8)
        self.exceptional_powers = False  # Article 16 powers
        self.can_dissolve_assembly = True
    
    def propose_referendum(self):
        if random.random() > 0.85:  # Rarely propose referenda
            return "Referendum Proposal"
        return None

    def dissolve_assembly(self, prime_minister, assembly_president):
        if self.can_dissolve_assembly and prime_minister and assembly_president:
            print("President dissolves the National Assembly.")
            self.can_dissolve_assembly = False
            return True
        return False

    def invoke_exceptional_powers(self, crisis):
        if crisis:  # Exceptional powers only during crises
            self.exceptional_powers = True
            print("President invokes Article 16: exceptional powers due to crisis.")

    def election(self):
        self.term_count += 1
        if self.term_count <= 2 and self.popularity > 0.5:
            print("President re-elected.")
        else:
            print("New president elected.")
            self.popularity = random.uniform(0.4, 0.8)
            self.term_count = 1  # New president's first term
        self.can_dissolve_assembly = True  # Reset dissolution power


# Prime Minister class - Manages laws, government survival, and coalition building
class PrimeMinister:
    def __init__(self):
        self.policies = []
        self.coalition_support = random.uniform(0.4, 0.8)  # Simulating coalition support
    
    def propose_law(self):
        law = f"Government Law {len(self.policies) + 1}"
        self.policies.append(law)
        return law

    def confidence_vote(self):
        # Confidence vote based on coalition support
        return random.random() < self.coalition_support

    def propose_amended_law(self, original_law):
        return f"Amended {original_law}"

    def negotiate_coalition(self):
        # Randomly adjust coalition support each cycle to reflect political dynamics
        self.coalition_support = random.uniform(0.5, 0.9)


# Parliament class - National Assembly and Senate pass laws, initiate confidence votes
class Parliament:
    def __init__(self):
        self.assembly_support = random.uniform(0.4, 0.8)  # National Assembly support
        self.senate_support = random.uniform(0.4, 0.8)  # Senate support
        self.laws = []
    
    def pass_law_in_assembly(self, law):
        if random.random() < self.assembly_support:
            return f"Law {law} passed by National Assembly."
        return f"Law {law} rejected by National Assembly."
    
    def pass_law_in_senate(self, law):
        if random.random() < self.senate_support:
            return f"Law {law} passed by Senate."
        return f"Law {law} rejected by Senate."
    
    def vote_of_no_confidence(self):
        # No-confidence vote occurs when the coalition is unstable
        if random.random() > 0.7:
            return True
        return False


# Constitutional Council - Reviews laws for constitutionality
class ConstitutionalCouncil:
    def __init__(self):
        self.reviewed_laws = []

    def review_law(self, law):
        if random.random() > 0.2:  # 80% chance of passing constitutional review
            self.reviewed_laws.append((law, "Valid"))
            return f"Law {law} is constitutional."
        else:
            self.reviewed_laws.append((law, "Invalid"))
            return f"Law {law} is unconstitutional."


# Central System - Coordinates all institutions, tracks crises and government stability
class FifthRepublic:
    def __init__(self):
        self.president = President()
        self.prime_minister = PrimeMinister()
        self.parliament = Parliament()
        self.constitutional_council = ConstitutionalCouncil()
        self.cycles = 0
        self.crisis_active = False  # Crisis state
    
    def simulate_crisis(self):
        # Simulate random crises affecting the Republic
        if random.random() > 0.8:
            self.crisis_active = True
            print("Crisis detected: Economic downturn or national emergency.")
        else:
            self.crisis_active = False

    def simulate_cycle(self):
        print(f"\n--- Cycle {self.cycles + 1} ---")
        self.cycles += 1

        # Simulate crisis before every cycle
        self.simulate_crisis()

        # Presidential actions: Referendum, Article 16 invocation
        referendum = self.president.propose_referendum()
        if referendum:
            print(f"President proposes: {referendum}")

        self.president.invoke_exceptional_powers(self.crisis_active)

        # Prime Minister coalition negotiations
        self.prime_minister.negotiate_coalition()

        # Prime Minister proposes laws
        gov_law = self.prime_minister.propose_law()
        print(f"Prime Minister proposed: {gov_law}")
        passed_law_assembly = self.parliament.pass_law_in_assembly(gov_law)

        if "passed" in passed_law_assembly:
            passed_law_senate = self.parliament.pass_law_in_senate(gov_law)
            print(passed_law_senate)

            if "passed" in passed_law_senate:
                # Constitutional review after both chambers approve
                print(self.constitutional_council.review_law(gov_law))
            else:
                # Law rejected in Senate can be amended and re-proposed
                amended_law = self.prime_minister.propose_amended_law(gov_law)
                print(f"Prime Minister proposes amendment: {amended_law}")
                print(self.parliament.pass_law_in_assembly(amended_law))

        else:
            print(passed_law_assembly)

        # Vote of no confidence in Parliament
        if self.parliament.vote_of_no_confidence():
            print("Vote of no confidence initiated!")
            if not self.prime_minister.confidence_vote():
                print("Government collapses. Prime Minister resigns.")
                self.prime_minister = PrimeMinister()  # New Prime Minister appointed
            else:
                print("Government survives confidence vote.")

        # Presidential election every 5 cycles
        if self.cycles % 5 == 0:
            self.president.election()

        # Time delay to simulate temporal evolution
        time.sleep(1)

# Simulate the Fifth Republic government system
fifth_republic = FifthRepublic()
for _ in range(15):  # Simulate 15 cycles of government
    fifth_republic.simulate_cycle()