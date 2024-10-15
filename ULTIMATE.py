import random
import time

class PoliticalSystem:
    def __init__(self):
        self.norm_pool = []
        self.norm_counter = 0
        self.action = "decision"

    def generate_norms(self):
        new_norm = {
            'id': self.norm_counter,
            'text': f'Norm {self.norm_counter}',
            'valid': random.choice([True, False]),
            'complexity': random.randint(1, 10)  # Quantitative complexity
        }
        self.norm_pool.append(new_norm)
        self.norm_counter += 1
        print(f"Generated new norm: {new_norm}")

    def reform_norm(self, revised_norm):
        for index, norm in enumerate(self.norm_pool):
            if norm['id'] == revised_norm['id']:
                self.norm_pool[index] = revised_norm
                print(f"Revised norm: {revised_norm}")

    def has_decision(self):
        return self.action == "decision"

    def produce_norms_decision(self):
        if self.has_decision():
            new_rules = ["Rule 1", "Rule 2"]
            return new_rules
        else:
            return []

    def send_expectations(self, citizen_pressure):
        expectations = ["Apply Norm X", "Clarify Rule Y", "Citizen concern Z"]
        if citizen_pressure > 3:
            expectations.append("Prioritize Norm Enforcement")
        return expectations

    def receive_stabilization(self, stabilized_norms):
        for norm in stabilized_norms:
            print(f"Acknowledged stabilization of {norm}.")

    def make_decisions(self, citizen_pressure):
        decisions = []
        if citizen_pressure > 3:
            decisions.append("Decision A")
            decisions.append("Decision B")
            print("Political system made decisions based on citizen pressure.")
        return decisions

    def perform_actions(self):
        actions = ["Act 1", "Unconstitutional Act", "Act 3"]
        print("Political system performed actions.")
        return actions

    def random_event(self):
        events = ["Economic Boom", "Economic Crisis", "Social Movement", "Natural Disaster"]
        event = random.choice(events)
        print(f"Random event occurred: {event}")
        return event


class JudicialSystem:
    def __init__(self, political_system):
        self.case_pool = []
        self.case_counter = 0
        self.political_system = political_system
        self.precedents = {}
        self.valid_rules = []
        self.caseload = 0
        self.judicial_decisions = 0

    def generate_case(self):
        if self.political_system.norm_pool:
            norm = random.choice(self.political_system.norm_pool)
            new_case = {
                'id': self.case_counter,
                'text': f'Case {self.case_counter} referencing {norm["text"]}',
                'norm_id': norm['id'],
                'constitutional': random.choice([True, False]),
                'complexity': norm['complexity']
            }
            self.case_pool.append(new_case)
            self.case_counter += 1
            print(f"Generated new case: {new_case}")

    def set_precedent(self, case):
        norm_id = case['norm_id']
        self.precedents[norm_id] = case['constitutional']
        print(f"Set precedent for norm {norm_id}: {case['constitutional']}")

    def apply_precedent(self, case):
        norm_id = case['norm_id']
        if norm_id in self.precedents:
            case['constitutional'] = self.precedents[norm_id]
            print(f"Applied precedent to case {case['id']}: {case['constitutional']}")

    def process_cases(self):
        for case in self.case_pool[:]:
            self.apply_precedent(case)
            self.set_precedent(case)
            print(f"Processed case {case['id']} with outcome: {case['constitutional']}")
            self.case_pool.remove(case)

    def periodic_rule_evaluation(self):
        for norm in self.political_system.norm_pool:
            related_cases = [case for case in self.case_pool if case['norm_id'] == norm['id']]
            if len(related_cases) > 5:
                norm['complexity'] = min(10, norm['complexity'] + 1)
            else:
                norm['complexity'] = max(1, norm['complexity'] - 1)
            print(f"Adjusted complexity for norm {norm['id']}: {norm['complexity']}")

    def address_expectations(self, expectations, citizen_pressure):
        self.caseload += citizen_pressure
        for expectation in expectations:
            if expectation.startswith("Apply Norm"):
                if citizen_pressure > 5:
                    print(f"Applying {expectation} with increased scrutiny due to public demand.")
                else:
                    print(f"Applying {expectation} to relevant cases.")
            else:
                print(f"Addressing {expectation} within legal framework.")

    def stabilize_norms(self, norms):
        for norm in norms:
            print(f"Reinforcing the validity of {norm} through consistent application.")

    def produce_judicial_decisions(self):
        if self.caseload > 0 and self.valid_rules:
            decisions_made = min(self.caseload, 5)
            self.judicial_decisions += decisions_made
            self.caseload -= decisions_made
            print(f"Produced {decisions_made} judicial decisions. Remaining caseload: {self.caseload}")
        else:
            print("No decisions made due to lack of cases or valid rules.")

    def apply_decisions(self, decisions):
        for decision in decisions:
            print(f"Applying political decision '{decision}' to relevant cases.")

    def control_political_actions(self, political_actions):
        for action in political_actions:
            if self.is_legal() and action == "Unconstitutional Act":
                print(f"Annulled political act '{action}' due to unconstitutionality.")
            else:
                print(f"Political act '{action}' deemed constitutional.")

    def is_legal(self):
        return bool(self.valid_rules)

    def receive_rules(self, rules):
        self.valid_rules.extend(rules)

class Society:
    def __init__(self):
        self.political_system = PoliticalSystem()
        self.judicial_system = JudicialSystem(self.political_system)
        self.iteration = 0

    def simulate(self):
        while True:
            self.iteration += 1
            print(f"\n--- Iteration {self.iteration} ---")

            # Political system generates new norms
            self.political_system.generate_norms()

            # Judicial system generates new cases
            self.judicial_system.generate_case()

            # Judicial system processes cases
            self.judicial_system.process_cases()

            # High citizen pressure scenario
            citizen_pressure = random.randint(1, 10)
            expectations = self.political_system.send_expectations(citizen_pressure)
            self.judicial_system.address_expectations(expectations, citizen_pressure)
            political_decisions = self.political_system.make_decisions(citizen_pressure)
            self.judicial_system.apply_decisions(political_decisions)

            # Ensure the judicial system receives new rules periodically
            new_rules = self.political_system.perform_actions()  # Consider actions as norms
            self.judicial_system.receive_rules(new_rules)

            # Judicial system produces judicial decisions
            self.judicial_system.produce_judicial_decisions()

            # Control political actions
            political_actions = self.political_system.perform_actions()
            self.judicial_system.control_political_actions(political_actions)

            # Periodic rule evaluation every 5 iterations
            if self.iteration % 5 == 0:
                self.judicial_system.periodic_rule_evaluation()

            # Introduce random events to add more contingency
            event = self.political_system.random_event()
            if event == "Economic Boom":
                citizen_pressure += random.randint(1, 5)
            elif event == "Economic Crisis":
                citizen_pressure -= random.randint(1, 5)
            elif event == "Social Movement":
                citizen_pressure += random.randint(2, 7)
            elif event == "Natural Disaster":
                citizen_pressure += random.randint(1, 3)

            # Add a small delay to simulate real-time processing and prevent infinite fast loop
            time.sleep(1)


	# Create an instance of Society to run the simulation
society = Society()
society.simulate()