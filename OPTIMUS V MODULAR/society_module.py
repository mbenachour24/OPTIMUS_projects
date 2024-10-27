# society.py
import logging
import random
import asyncio
import numpy as np
from political_system import Parliament, Government, President, PrimeMinister
from judicial_system import JudicialSystem
from logging_config import configure_logger
from analysis import calculate_correlations, plot_results, perform_granger_test

# Constants
SIMULATION_DAYS = 365
CITIZEN_PRESSURE_MIN = 1
CITIZEN_PRESSURE_MAX = 10

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

        # Link judicial system to parliament and government
        self.parliament.judicial_system = self.judicial_system
        self.government.judicial_system = self.judicial_system
        self.iteration = 0

        # Historical data for analysis
        self.caseload_history = []
        self.normative_inflation_history = []
        self.temporal_gap_history = []
        self.history = []

    def check_constitutionality(self, norm, current_iteration):
        if norm.id not in Society.norms or Society.norms[norm.id]['last_checked_iteration'] != current_iteration:
            is_constitutional = self.judicial_system.control_norm_constitutionality(norm)
            Society.norms[norm.id] = {'constitutional': is_constitutional, 'last_checked_iteration': current_iteration}
        else:
            logging.info(f"Norm {norm.id}: Already checked in this iteration")

    async def simulate(self):
        for day in range(SIMULATION_DAYS):
            self.iteration = day + 1
            logging.info(f"\n--- DAY {self.iteration} ---\n")

            citizen_pressure = random.randint(CITIZEN_PRESSURE_MIN, CITIZEN_PRESSURE_MAX)
            event = self.parliament.random_event()
            citizen_pressure = self.adjust_citizen_pressure(event, citizen_pressure)

            # Generate norms and regulations
            self.parliament.generate_norms()
            self.government.generate_norms()

            # Veto attempt by president
            vetoed_law = self.president.attempt_veto(self.parliament.norm_pool)
            if vetoed_law:
                self.judicial_system.inspect_veto_legality(vetoed_law)

            # Process cases
            self.judicial_system.generate_case()
            self.judicial_system.process_cases()

            # Track historical data
            self.track_histories()
            await asyncio.sleep(0.1)

        await self.finalize_simulation()

    def adjust_citizen_pressure(self, event, citizen_pressure):
        adjustments = {
            "Economic Boom": random.randint(1, 5),
            "Economic Crisis": -random.randint(1, 5),
            "Social Movement": random.randint(2, 7),
            "Natural Disaster": random.randint(1, 3)
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

    async def finalize_simulation(self):
        await asyncio.sleep(0.1)
        calculate_correlations(self.caseload_history, self.normative_inflation_history, self.temporal_gap_history)
        plot_results(self.caseload_history, self.normative_inflation_history, self.temporal_gap_history)
        perform_granger_test(self.normative_inflation_history, self.caseload_history)