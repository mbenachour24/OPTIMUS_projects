import asyncio
import random
import logging

# I3dad es-sejellat b etfasil
logging.basicConfig(level=logging.DEBUG, filename='mini_optimu2.log', filemode='a', format='%(message)s')

# ethawabet
COMPLEXITY_MIN = 1  # A9all daraja s3ouba lel qanoun
COMPLEXITY_MAX = 10  # A9sa daraja s3ouba lel qanoun
SIMULATION_DAYS = 100  # 3add el ayam fi el mo7akaa

# Ta3rif class qanoun (bdel 9anoun)
class qanoun:
    def __init__(self, qanoun_id, text, valid=True, complexity=1):
        self.id = qanoun_id
        self.text = text
        self.valid = valid  # Besh nchoufou idha el qanoun sa7i7 welle batel
        self.complexity = complexity  # Daraja s3ouba lel qanoun
        self.log_event(f"El qanoun ra9em {self.id} t3amal, 3ando s3ouba {complexity} w si7a {valid}")

    def invalidate(self):
        self.valid = False  # Idha el qanoun mouch dustouri, yebtal
        self.log_event("El qanoun hedha batel")

    def log_event(self, message):
        log_message = f"qanoun {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

# Ta3rif class qadheya (bdel 9adheya)
class qadheya:
    def __init__(self, qadheya_id, text, qanoun):
        self.id = qadheya_id
        self.text = text
        self.qanoun = qanoun
        self.constitutional = qanoun.valid  # Besh nchoufou idha el qanoun hedha dustouri welle la
        self.log_event("9adheya jdida twesslet lel ma7kama")

    def log_event(self, message):
        log_message = f"El qadheya {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

# Ta3rif class netham s-siyasi
class PoliticalSystem:
    def __init__(self):
        self.qanoun_counter = 0
        self.qanouns = []

    def create_qanoun(self):
        self.qanoun_counter += 1
        new_qanoun = qanoun(
            qanoun_id=self.qanoun_counter,
            text=f'qanoun {self.qanoun_counter}',
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.qanouns.append(new_qanoun)
        return new_qanoun

# Ta3rif class netham el 9ada2i
class JudicialSystem:
    def __init__(self):
        self.qadheya_counter = 0
        self.qadheyas = []

    def check_constitutionality(self, qanoun):
        log_message = f"netham el 9ada2i: 9a3din nchoufou idha el qanoun {qanoun.id} dustouri, s3oubetou {qanoun.complexity}"
        logging.info(log_message)
        print(log_message)
        
        if qanoun.complexity > 5:
            qanoun.invalidate()
        
        # Risala ba3d el ta7a99o9 min dustouriyet el qanoun
        log_message = f"netham el 9ada2i: el qanoun {qanoun.id} t3amellou check, w dustouriytou: {qanoun.valid}"
        logging.info(log_message)
        print(log_message)

    def create_qadheya(self, qanoun):
        if not qanoun.valid:
            log_message = f"netham el 9ada2i: ma najamnash na3mlo qadheya 3ala qanoun batel {qanoun.id}"
            logging.info(log_message)
            print(log_message)
            return None

        self.qadheya_counter += 1
        new_qadheya = qadheya(
            qadheya_id=self.qadheya_counter,
            text=f'qadheya {self.qadheya_counter} li fiha qanoun {qanoun.text}',
            qanoun=qanoun
        )
        self.qadheyas.append(new_qadheya)
        return new_qadheya

# Ta3rif class el mojteme3
class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            log_message = f"\n\n{'='*20} Bidayet nhar {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)

            # netham el siyasi ya3mel qanoun jdida
            new_qanoun = self.parliament.create_qanoun()
            log_message = f"netham el siyasi 3amel qanoun: {new_qanoun.text}"
            logging.info(log_message)
            print(log_message)

            # netham el 9ada2i ychouf dustouriyet el qanoun
            self.judicial_system.check_constitutionality(new_qanoun)

            # netham el 9ada2i ya3mel qadheya
            new_qadheya = self.judicial_system.create_qadheya(new_qanoun)
            if new_qadheya:
                log_message = f"netham el 9ada2i 3amel qadheya: {new_qadheya.text}"
                logging.info(log_message)
                print(log_message)

            log_message = f"\n{'='*20} Nehaya nhar {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)
            
            await asyncio.sleep(1)  # Besh ymethl el wa9et ili yemchi

        logging.info("el mo7akaa kemlet.")

# Tachghil el mo7akaa
async def main():
    society = Society()
    await society.simulate()

asyncio.run(main())
