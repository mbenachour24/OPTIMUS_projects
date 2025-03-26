# This file is part of the OPTMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

import asyncio
import random
import logging
from datetime import datetime
import os

# Setup enhanced logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Constants
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
SIMULATION_DAYS = 100

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.websocket = None
        # Clear old notifications file at startup
        try:
            os.makedirs('data', exist_ok=True)
            os.remove('data/notifications.json')
            logging.info("Cleared old notifications file")
        except FileNotFoundError:
            logging.info("No old notifications file to clear")

    async def broadcast_update(self, data):
        if self.websocket:
            try:
                await self.websocket.broadcast(data)
                logging.info(f"Broadcasted update: {data}")
            except Exception as e:
                logging.error(f"Failed to broadcast update: {e}")
        else:
            logging.warning("No active WebSocket to broadcast the update.")

# Instantiate the notification manager globally
notification_manager = NotificationManager()

class Norm:
    def __init__(self, norm_id, text, valid=True, complexity=1):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        self.valid = False
        self.log_event("Invalidated")
        # Use asyncio.run to ensure the coroutine runs in a new event loop
        asyncio.run(notification_manager.broadcast_update({
            'type': 'norm_update',
            'norm_id': self.id,
            'valid': self.valid
        }))

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
        self.resolved_at = None  # New field for resolution timestamp
        self.log_event("A new case is brought to the Courts")

    def log_event(self, message):
        log_message = f"Case {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

class CitizenPressure:
    def __init__(self, judicial_system, parliament):
        self.judicial_system = judicial_system
        self.parliament = parliament
        self.daily_case_count = 5
        self.case_types = [
            "Environmental Concern",
            "Civil Rights Issue",
            "Labor Dispute",
            "Consumer Protection",
            "Luhmann's theory Public Safety Concern",
            "Mohamed got funds and it's not fair",
            "Alien invasion",
            "Zombie outbreak",
        ]

    def generate_daily_cases(self):
        generated_cases = []
        valid_norms = [norm for norm in self.parliament.norms if norm.valid]
        
        if not valid_norms:
            print("No valid norm to generate case.")
            return "No valid norm to generate case."

        for _ in range(self.daily_case_count):
            # Select a valid norm
            norm = random.choice(valid_norms)
            
            # Create a case
            case_type = random.choice(self.case_types)
            case = self.judicial_system.create_case_from_pressure(
                norm=norm,
                pressure_text=f"Citizen Petition: {case_type} regarding {norm.text}"
            )
            if case:
                generated_cases.append(case)
                
        return generated_cases

class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0
        self.norms = []

    def create_norm(self):
        self.norm_counter += 1
        norm = Norm(
            norm_id=self.norm_counter,  # Correctly incremented norm ID
            text=f'Law {self.norm_counter}',
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.norms.append(norm)
        logging.info(f"Debug: Created Norm #{self.norm_counter} with ID {norm.id}")  # Add debug log
        return norm

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.pending_cases = []  # New pool for pending cases
        self.solved_cases = []   # New pool for solved cases

    def check_constitutionality(self, norm):
        log_message = f"Judicial System: Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)
        print(log_message)

        log_message = f"Judicial System: Norm {norm.id} has been checked for constitutionality. Valid status: {norm.valid}"
        logging.info(log_message)
        print(log_message)

    def create_case(self, norm):
        if norm.valid:
            self.case_counter += 1
            case = Case(
                case_id=self.case_counter,
                text=f'Case {self.case_counter} referencing {norm.text}',
                norm=norm
            )
            self.pending_cases.append(case)
            case.log_event("Case created and added to pending cases.")
            return case
        else:
            log_message = f"Cannot create a case for an invalid norm (Norm #{norm.id})"
            logging.info(log_message)
            print(log_message)
            return None

    def create_case_from_pressure(self, norm, pressure_text):
        """Create a case from citizen pressure, only if norm is valid"""
        if not norm.valid:
            log_message = f"Cannot create a case for an invalid norm (Norm #{norm.id})"
            logging.info(log_message)
            print(log_message)
            return None
            
        self.case_counter += 1
        case = Case(
            case_id=self.case_counter,
            text=pressure_text,
            norm=norm
        )
        self.pending_cases.append(case)
        case.log_event("Case created from citizen pressure and added to pending cases.")
        return case

    def solve_case(self, case_id):
        """Solve a pending case and move it to solved cases"""
        # Find the case in pending cases
        case = next((case for case in self.pending_cases if case.id == case_id), None)
        if not case:
            raise ValueError(f"No pending case found with ID {case_id}")

        # Remove from pending and add to solved
        self.pending_cases.remove(case)
        self.solved_cases.append(case)
        
        # Add resolution timestamp and log
        case.resolved_at = datetime.now().isoformat()
        case.log_event("Case has been resolved by the Judicial System")
        
        return case

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.citizen_pressure = CitizenPressure(self.judicial_system, self.parliament)
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            print(f"Debug: Starting Day {self.iteration}")

            # Political system creates a norm
            norm = self.parliament.create_norm()
            print(f"Debug: Created Norm: {norm.text}, Valid: {norm.valid}")

            # Judicial system checks constitutionality
            self.judicial_system.check_constitutionality(norm)

            # Generate citizen pressure cases
            generated_cases = self.citizen_pressure.generate_daily_cases()
            print(f"Debug: Generated {len(generated_cases)} citizen pressure cases")

            print(f"Debug: Ending Day {self.iteration}")
            await asyncio.sleep(1)

async def main():
    society = Society()
    await society.simulate()

if __name__ == "__main__":
    asyncio.run(main())