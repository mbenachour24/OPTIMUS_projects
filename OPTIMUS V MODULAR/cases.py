# cases.py
import logging
import time
import random
from logging_config import configure_logger

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
        self.complexity = max(1, min(10, self.complexity + adjustment))
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
        if self.status["cassation"] < 3:
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