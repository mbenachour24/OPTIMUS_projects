# norms.py
import logging
import time
from logging_config import configure_logger

class Norm:
    def __init__(self, norm_id, text, valid, complexity, norm_type="ordinaire"):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.norm_type = norm_type
        self.history = []
        logging.info(f"Norm {self.id}: Initialized with complexity {complexity} and validity {valid}")

    def update_complexity(self, adjustment):
        old_complexity = self.complexity
        self.complexity = max(1, min(10, self.complexity + adjustment))
        logging.info(f"Norm {self.id}: Updated complexity from {old_complexity} to {self.complexity}")
        self.history.append(('complexity', self.complexity, time.time()))

    def invalidate(self):
        self.valid = False
        logging.info(f"Norm {self.id}: Invalidated")
        self.history.append(('valid', self.valid, time.time()))

    def validate(self):
        self.valid = True
        logging.info(f"Norm {self.id}: Validated")
        self.history.append(('valid', self.valid, time.time()))

    def get_history(self):
        logging.info(f"Norm {self.id}: Getting history")
        return self.history

    def __str__(self):
        return f"Norm(id={self.id}, text={self.text}, valid={self.valid}, complexity={self.complexity})"

class Law(Norm):
    pass

class Regulation(Norm):
    pass