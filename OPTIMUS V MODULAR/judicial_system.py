# judicial_system.py
import logging
import random
from cases import Case
from norms import Law, Regulation

class JudicialSystem:
    def __init__(self, parliament, government, president):
        self.case_pool = []
        self.case_counter = 0
        self.case_ids = set()
        self.parliament = parliament
        self.government = government
        self.president = president
        self.precedents = {}
        self.valid_rules = []
        self.caseload = 0
        self.judicial_decisions = 0
        self.norms_constitutionality = {}

        # Initialize subsystems here
        self.first_instance = FirstInstance("First Instance")
        self.appeal_court = Appeal("Appeal")
        self.cassation_court = Cassation("Court of Cassation")
        self.constitutional_council = Court("Constitutional Council")

    def control_norm_constitutionality(self, norm, check_type="CONTRÔLE DE CONSTITUTIONNALITÉ"):
        if norm.id in self.norms_constitutionality:
            is_constitutional = self.norms_constitutionality[norm.id]
        else:
            is_constitutional = random.choice([True, False]) if norm.norm_type == "ordinaire" else norm.valid
            self.norms_constitutionality[norm.id] = is_constitutional

        logging.info(f"JudicialSystem: {check_type} for norm {norm.id}: {'constitutional' if is_constitutional else 'unconstitutional'}")
        if not is_constitutional:
            self.remove_norm(norm)
            logging.info(f"Norm {norm.id}: Abrogated and canceled due to unconstitutionality")
        return is_constitutional

    def remove_norm(self, norm):
        if isinstance(norm, Law):
            self.parliament.norm_pool.remove(norm)
        elif isinstance(norm, Regulation):
            self.government.norm_pool.remove(norm)

    def generate_case(self):
        if self.parliament.norm_pool or self.government.norm_pool:
            norm = random.choice(self.parliament.norm_pool + self.government.norm_pool)
            new_case = Case(
                case_id=self.case_counter,
                text=f'Case {self.case_counter} referencing {norm.text}',
                norm_id=norm.id,
                constitutional=self.control_norm_constitutionality(norm),
                complexity=norm.complexity
            )
            self.case_pool.append(new_case)
            self.case_ids.add(self.case_counter)
            self.case_counter += 1
            logging.info(f"JudicialSystem: Generated new case: {new_case}")

    def process_cases(self):
        for case in self.case_pool[:]:
            self.first_instance.file_case(case)
            self.first_instance.conduct_hearing(case)
            judgment = self.first_instance.render_judgment(case)
            case.final_outcome = judgment

            if case.final_outcome == "rejected":
                self.appeal_court.file_case(case)
                self.appeal_court.conduct_hearing(case)
                judgment = self.appeal_court.render_judgment(case)
                case.final_outcome = judgment

                if case.final_outcome == "rejected":
                    while case.cassation_count < 3:
                        case.cassation_count += 1
                        self.cassation_court.file_case(case)
                        self.cassation_court.conduct_hearing(case)
                        judgment = self.cassation_court.render_judgment(case)
                        case.final_outcome = judgment

                        if case.final_outcome == "accepted":
                            break

            self.set_precedent(case)
            logging.info(f"Case {case.id}: Processed with outcome: {case.final_outcome}")
            self.case_pool.remove(case)

    def set_precedent(self, case):
        self.precedents[case.norm_id] = case.final_outcome
        logging.info(f"JudicialSystem: Set precedent for norm {case.norm_id}: {case.final_outcome}")

    def inspect_veto_legality(self, law):
        """Check the legality of a presidential veto on a law."""
        is_legal = random.choice([True, False])  # Randomly determine legality
        logging.info(f"JudicialSystem: Veto legality check for law {law.id}: {'legal' if is_legal else 'illegal'}")
        
        if not is_legal:
            # If the veto is deemed illegal, the law remains in effect
            self.remove_norm(law)
            logging.info(f"Law {law.id}: Veto deemed illegal, law remains valid")
        else:
            # If the veto is legal, control the constitutionality of the law
            self.control_norm_constitutionality(law, "CONTRÔLE DE CONSTITUTIONNALITÉ POST-VETO")
            
# Court and its subclasses
class Court:
    def __init__(self, court_name):
        self.court_name = court_name
        logging.info(f"{self.court_name} Court: Initialized")

    def file_case(self, case):
        logging.info(f"{self.court_name} Court: Case {case.id} filed")

    def conduct_hearing(self, case):
        logging.info(f"{self.court_name} Court: Conducted hearing for case {case.id}")

    def render_judgment(self, case):
        judgment = random.choice(["accepted", "rejected"])
        logging.info(f"{self.court_name} Court: Rendered judgment for case {case.id}: {judgment}")
        return judgment

class FirstInstance(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"FirstInstance Court: Initialized {court_name} court")

class Appeal(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"Appeal Court: Initialized {court_name} court")

class Cassation(Court):
    def __init__(self, court_name):
        super().__init__(court_name)
        logging.info(f"Cassation Court: Initialized {court_name} court")