import time
import random
import matplotlib.pyplot as plt
import numpy as np
import logging

# Set up logging
logging.basicConfig(filename='autopoiesis3.log', 
                    filemode='w',  # 'w' to overwrite the file each time; use 'a' to append
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # INFO level to capture standard logs

# Example of logging different levels of information
logging.info("Simulation started.")
logging.error("An error occurred.")  # For any error logging
logging.warning("This is a warning.")
logging.debug("Debug information.")

# Autopoietic System with sub-coalition dynamics, leadership changes, and crisis adaptation
class AutopoieticSystem:
    def __init__(self, name, hierarchy_level, dependency_matrix):
        self.name = name
        self.hierarchy_level = hierarchy_level  # Dynamic hierarchy level
        self.internal_operations = []
        self.memory = []
        self.rejection_streak = 0
        self.fatigue = 0
        self.trust = 1.0
        self.power = 1.0
        self.resources = 1.0  # Resource level (e.g., economic resources)
        self.dependency_matrix = dependency_matrix  # Dependencies on other systems
        self.failure_mode = False
        self.failure_duration = 0
        self.coalition = None  # Coalition the system is part of
        self.sub_coalitions = []  # Sub-coalitions the system may form
        self.coalition_leader = False  # Whether the system is leading the coalition
        self.q_table = {}  # Q-table for reinforcement learning
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.2

    def generate_operation(self, external_shock, shock_type):
        if self.failure_mode:
            logging.info(f"{self.name}: Catastrophic failure! Unable to generate valid operations.")
            self.failure_duration += 1
            return {
                'id': f"{self.name}-Fail-{random.randint(1, 100)}",
                'valid': False, 'power': self.power, 'trust': self.trust,
                'resources': self.resources, 'hierarchy_level': self.hierarchy_level
            }

        # Handle external shocks and resource depletion
        if external_shock > 0:
            logging.info(f"{self.name}: External {shock_type} shock of magnitude {external_shock}! Increasing fatigue.")
            if shock_type == 'economic':
                self.power -= external_shock * 0.1
                self.resources -= external_shock * 0.2  # Economic shocks affect resources more
            elif shock_type == 'political':
                self.trust -= external_shock * 0.1
            self.fatigue += external_shock

        # Adjust behavior based on coalition membership
        if self.coalition:
            logging.info(f"{self.name} is part of coalition {self.coalition}. Sharing resources.")
            self.resources = min(self.resources + 0.1, 1.5)  # Coalition helps share resources

        # Power and resource competition
        validity = False if self.fatigue > 3 or self.resources < 0.3 else random.choice([True, False])
        if self.power >= 1.5 and self.resources > 0.5:
            validity = True
            logging.info(f"{self.name}: Exerting dominance with high power and resources.")

        # Adjust resource usage and accumulation
        self.resources += random.uniform(-0.1, 0.2)  # Resource accumulation/depletion
        self.resources = max(0, min(self.resources, 1.5))  # Cap resources at 1.5

        self.power += random.uniform(-0.1, 0.1)
        self.trust += random.uniform(-0.05, 0.05)
        self.trust = max(0, min(self.trust, 1))
        operation_id = f"{self.name}-Op{random.randint(1, 100)}"
        operation = {
            'id': operation_id, 'valid': validity, 'power': self.power, 'trust': self.trust,
            'resources': self.resources, 'hierarchy_level': self.hierarchy_level
        }
        self.internal_operations.append(operation)
        logging.info(f"{self.name}: Generated {operation_id}, Valid: {validity}, Power: {self.power}, Trust: {self.trust}, Resources: {self.resources}, Hierarchy: {self.hierarchy_level}")
        return operation

    def process_input(self, external_operation):
        if self.failure_mode:
            return

        # Influence from external system based on power, trust, resources, and hierarchy
        influence_factor = (external_operation['trust'] + external_operation['power'] + external_operation['resources']) / 3
        if external_operation['valid'] and influence_factor > 0.5:
            reaction = True
            self.rejection_streak = 0
            self.trust += 0.05
        else:
            reaction = random.choice([True, False])
            if not reaction:
                self.rejection_streak += 1
                self.fatigue += 1
                self.trust -= 0.05

        # Reinforcement learning and coalition management
        self.memory.append({'external_id': external_operation['id'], 'accepted': reaction, 'trust': external_operation['trust']})
        if len(self.memory) > 10:
            self.memory.pop(0)

        state = (self.trust, self.power, external_operation['valid'])
        reward = 1 if reaction else -1
        new_state = (self.trust, self.power, external_operation['valid'])
        self.update_q_table(state, 'accept' if reaction else 'reject', reward, new_state)

        # Dynamic hierarchy adjustment based on power, trust, and resources
        if self.power > 1.5 and self.trust > 0.8 and self.resources > 0.5:
            self.hierarchy_level = max(1, self.hierarchy_level - 1)  # Move up in hierarchy
            logging.info(f"{self.name}: Moving UP in the hierarchy due to high power/trust/resources!")
        elif self.power < 0.5 or self.trust < 0.4 or self.resources < 0.3:
            self.hierarchy_level += 1  # Move down in hierarchy
            logging.info(f"{self.name}: Moving DOWN in the hierarchy due to low power/trust/resources!")

        # Check for system collapse
        if self.power < 0.2 and self.trust < 0.2 and self.resources < 0.2:
            self.failure_mode = True
            logging.info(f"{self.name}: COLLAPSE! System is no longer operational.")

        # Dissolve coalition if trust drops below threshold
        if self.coalition and self.trust < 0.5:
            logging.info(f"{self.name}: Dissolving coalition with {self.coalition} due to low trust.")
            self.dissolve_coalition()

        logging.info(f"{self.name}: Processed {external_operation['id']} with influence factor {influence_factor}, Trust: {self.trust}, Resources: {self.resources}, Hierarchy Level: {self.hierarchy_level}")
        return reaction

    def update_q_table(self, state, action, reward, new_state):
        if state not in self.q_table:
            self.q_table[state] = {'accept': 0, 'reject': 0}
        best_next_action = self.get_best_action(new_state)
        td_target = reward + self.discount_factor * self.q_table[new_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def get_best_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {'accept': 0, 'reject': 0}
        return max(self.q_table[state], key=self.q_table[state].get)

    def reset_if_needed(self):
        if self.failure_duration >= 5:
            logging.info(f"{self.name}: Resetting after catastrophic failure.")
            self.failure_mode = False
            self.failure_duration = 0
            self.fatigue = 5
            self.resources = 1.0  # Reset resources upon recovery

    def form_coalition(self, other_system):
        if self.trust > 0.7 and other_system.trust > 0.7:
            self.coalition = f"Coalition with {other_system.name}"
            other_system.coalition = f"Coalition with {self.name}"
            logging.info(f"{self.name} formed a coalition with {other_system.name}!")
            # Sub-coalitions may form if trust is high enough within a coalition
            if random.random() < 0.5:
                self.form_sub_coalition(other_system)

    def dissolve_coalition(self):
        logging.info(f"{self.name} has dissolved its coalition.")
        self.coalition = None

    def form_sub_coalition(self, other_system):
        """Form a sub-coalition within a larger coalition."""
        sub_coalition_name = f"Sub-coalition with {other_system.name}"
        self.sub_coalitions.append(sub_coalition_name)
        other_system.sub_coalitions.append(sub_coalition_name)
        logging.info(f"{self.name} formed a sub-coalition with {other_system.name}!")

    def challenge_leadership(self, coalition_leader):
        """Challenge the current leader of the coalition if power is greater."""
        if self.power > coalition_leader.power:
            logging.info(f"{self.name} challenges {coalition_leader.name} for leadership!")
            success = random.choice([True, False])
            if success:
                logging.info(f"{self.name} has overtaken {coalition_leader.name} as coalition leader!")
                self.coalition_leader = True
                coalition_leader.coalition_leader = False
            else:
                logging.info(f"{self.name}'s leadership challenge failed. Trust in the coalition falls.")
                self.trust -= 0.2
                if self.trust < 0.5:
                    self.dissolve_coalition()

    def adjust_for_dependency(self, dependent_systems):
        """Adjust resource levels based on dependencies."""
        if dependent_systems:
            total_dependency = sum(self.dependency_matrix.get(sys.name, 0) for sys in dependent_systems)
            self.resources -= total_dependency * 0.1  # Resources are drained based on dependency levels
            logging.info(f"{self.name}: Resources adjusted for dependencies, new level: {self.resources}")

# External regulator class to stabilize systems and manage resource redistribution
class ExternalRegulator:
    def __init__(self):
        pass

    def intervene(self, system):
        if system.power < 0.3 or system.resources < 0.3 or system.trust < 0.3:
            logging.info(f"Regulator intervenes to stabilize {system.name}. Injecting resources.")
            system.resources = min(system.resources + 0.5, 1.5)  # Inject resources to stabilize system
            system.trust = min(system.trust + 0.2, 1)  # Boost trust
            system.power = min(system.power + 0.2, 1.5)  # Boost power

    def redistribute_resources(self, systems):
        """Redistribute resources from the most powerful systems to weaker ones."""
        rich_systems = sorted(systems, key=lambda sys: sys.resources, reverse=True)[:2]  # Top 2 richest systems
        poor_systems = sorted(systems, key=lambda sys: sys.resources)[:2]  # Bottom 2 weakest systems
        for rich in rich_systems:
            for poor in poor_systems:
                transfer = min(rich.resources * 0.1, 0.2)  # Transfer 10% of rich system's resources
                logging.info(f"Regulator redistributes {transfer} resources from {rich.name} to {poor.name}.")
                rich.resources -= transfer
                poor.resources = min(poor.resources + transfer, 1.5)

# Society class with resource redistribution, coalitions, sub-coalitions, and dependency management
# Updated Society class to handle 20 systems
# Heterogeneous initialization of systems for fine-tuning

class Society:
    def __init__(self):
        # Adjust dependency matrices and initial values for more diversity among systems
        self.systems = []
        for i in range(1, 21):
            name = f"System {i}"
            hierarchy_level = random.randint(1, 10)  # Random hierarchy level from 1 to 10
            initial_resources = random.uniform(0.5, 1.5)  # Different initial resources for each system
            initial_power = random.uniform(0.5, 1.5)  # Different initial power for each system
            initial_trust = random.uniform(0.3, 1.0)  # Different initial trust for each system
            dependency_matrix = {f"System {j}": random.uniform(0.1, 0.5) for j in range(1, 21) if j != i}
            
            system = AutopoieticSystem(
                name=name, 
                hierarchy_level=hierarchy_level, 
                dependency_matrix=dependency_matrix
            )
            system.resources = initial_resources
            system.power = initial_power
            system.trust = initial_trust
            
            self.systems.append(system)
        
        self.regulator = ExternalRegulator()
        self.fatigue_levels = {f"System {i+1}": [] for i in range(20)}
        self.trust_levels = {f"System {i+1}": [] for i in range(20)}
        self.power_levels = {f"System {i+1}": [] for i in range(20)}
        self.resource_levels = {f"System {i+1}": [] for i in range(20)}
        self.hierarchy_levels = {f"System {i+1}": [] for i in range(20)}

    def simulate(self, iterations=20):
        for i in range(iterations):
            logging.info(f"\n--- Iteration {i + 1} ---")
            external_shock = random.uniform(0, 3) if (i % 3 == 0) else 0
            shock_type = random.choice(['economic', 'political', 'social']) if external_shock > 0 else None

            for system in self.systems:
                # Each system generates an operation
                operation = system.generate_operation(external_shock, shock_type)

                # All other systems process the generated operation
                for other_system in self.systems:
                    if other_system != system:
                        other_system.process_input(operation)
                
                # Regulator intervention for system-specific crises
                self.regulator.intervene(system)

                # Resource redistribution based on wealth disparities
            self.regulator.redistribute_resources(self.systems)

            # Track system data (fatigue, trust, power, resources, hierarchy) over iterations
            for system in self.systems:
                self.fatigue_levels[system.name].append(system.fatigue)
                self.trust_levels[system.name].append(system.trust)
                self.power_levels[system.name].append(system.power)
                self.resource_levels[system.name].append(system.resources)
                self.hierarchy_levels[system.name].append(system.hierarchy_level)

            # Allow systems to recover from failure
            for system in self.systems:
                system.reset_if_needed()

            time.sleep(0.5)  # To avoid flooding the output, reduce the sleep time

    def plot_results(self):
        plt.figure(figsize=(14, 12))

        # Plot fatigue levels
        plt.subplot(5, 1, 1)
        for system in self.fatigue_levels:
            plt.plot(self.fatigue_levels[system], label=f"{system} Fatigue")
        plt.ylabel("Fatigue Level")
        plt.legend()

        # Plot trust levels
        plt.subplot(5, 1, 2)
        for system in self.trust_levels:
            plt.plot(self.trust_levels[system], label=f"{system} Trust")
        plt.ylabel("Trust Level")
        plt.legend()

        # Plot power levels
        plt.subplot(5, 1, 3)
        for system in self.power_levels:
            plt.plot(self.power_levels[system], label=f"{system} Power")
        plt.ylabel("Power Level")
        plt.legend()

        # Plot resource levels
        plt.subplot(5, 1, 4)
        for system in self.resource_levels:
            plt.plot(self.resource_levels[system], label=f"{system} Resources")
        plt.ylabel("Resource Level")
        plt.legend()

        # Plot hierarchy levels
        plt.subplot(5, 1, 5)
        for system in self.hierarchy_levels:
            plt.plot(self.hierarchy_levels[system], label=f"{system} Hierarchy")
        plt.xlabel("Iterations")
        plt.ylabel("Hierarchy Level")
        plt.legend()

        plt.tight_layout()
        plt.show()

# Initialize and run the fine-tuned simulation
society = Society()
society.simulate()

# Plot the results
society.plot_results()