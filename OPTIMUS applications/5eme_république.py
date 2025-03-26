import asyncio
import random
import logging
import time

# Configuration du logging pour le fichier et le terminal
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Supprimer tous les handlers existants pour éviter la duplication
if logger.hasHandlers():
    logger.handlers.clear()

# Handler pour le fichier
file_handler = logging.FileHandler('journalofficiel2.log', 'a')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Handler pour le terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Constantes
COMPLEXITÉ_MIN = 1
COMPLEXITÉ_MAX = 10
JOURS_DE_SIMULATION = 100
NOMBRE_MAX_CASSATIONS = 3

class Norme:
    """Classe de base pour toutes les normes."""
    def __init__(self, identifiant_norme, texte, valide=True, complexité=1):
        self.id = identifiant_norme
        self.texte = texte
        self.valide = valide
        self.complexité = complexité
        self.historique = []
        self.enregistrer_événement(f"Initialisée avec une complexité de {complexité} et validité {valide}")

    def mettre_à_jour_complexité(self, ajustement):
        ancienne_complexité = self.complexité
        self.complexité = max(COMPLEXITÉ_MIN, min(COMPLEXITÉ_MAX, self.complexité + ajustement))
        self.enregistrer_événement(f"Complexité mise à jour de {ancienne_complexité} à {self.complexité}")
        self.historique.append(('complexité', self.complexité, time.time()))

    def invalider(self):
        self.valide = False
        self.enregistrer_événement("Invalidée")
        self.historique.append(('valide', self.valide, time.time()))

    def valider(self):
        self.valide = True
        self.enregistrer_événement("Validée")
        self.historique.append(('valide', self.valide, time.time()))

    def obtenir_historique(self):
        self.enregistrer_événement("Obtention de l'historique")
        return self.historique

    def enregistrer_événement(self, message):
        logging.info(f"Norme {self.id} : {message}")

    def __str__(self):
        return f"Norme(id={self.id}, texte={self.texte}, valide={self.valide}, complexité={self.complexité})"

class Loi(Norme):
    """Représente une loi créée par le Parlement."""
    def enregistrer_événement(self, message):
        logging.info(f"Loi {self.id} : {message}")

class Règlement(Norme):
    """Représente un règlement créé par le Gouvernement."""
    def enregistrer_événement(self, message):
        logging.info(f"Règlement {self.id} : {message}")

class Affaire:
    """Représente une affaire judiciaire."""
    def __init__(self, identifiant_affaire, texte, id_norme, constitutionnelle, complexité):
        self.id = identifiant_affaire
        self.texte = texte
        self.id_norme = id_norme
        self.constitutionnelle = constitutionnelle
        self.complexité = complexité
        self.historique = []
        self.nombre_cassations = 0
        self.statuts = {
            "première_instance": False,
            "appel": False,
            "cassation": 0  # Suivi du nombre de cassations
        }
        self.décision_finale = None
        self.enregistrer_événement("Une nouvelle affaire est portée devant les tribunaux")

    def mettre_à_jour_complexité(self, ajustement):
        ancienne_complexité = self.complexité
        self.complexité = max(COMPLEXITÉ_MIN, min(COMPLEXITÉ_MAX, self.complexité + ajustement))
        self.enregistrer_événement(f"Complexité mise à jour de {ancienne_complexité} à {self.complexité}")
        self.historique.append(('complexité', self.complexité, time.time()))

    def traiter_en_première_instance(self):
        if not self.statuts["première_instance"]:
            self.statuts["première_instance"] = True
            self.enregistrer_événement("Traitée en Première Instance")
            self.décision_finale = self.simuler_audience()
            return self.décision_finale
        return None

    def traiter_en_appel(self):
        if not self.statuts["appel"]:
            self.statuts["appel"] = True
            self.enregistrer_événement("Traitée en Cour d'Appel")
            self.décision_finale = self.simuler_audience()
            return self.décision_finale
        return None

    def traiter_en_cassation(self):
        if self.statuts["cassation"] < NOMBRE_MAX_CASSATIONS:
            self.statuts["cassation"] += 1
            self.enregistrer_événement(f"Traitée en Cour de Cassation, nombre de cassations : {self.statuts['cassation']}")
            décision_cassation = self.simuler_audience()
            if décision_cassation == "acceptée":
                self.décision_finale = "casse et annule"
                return "casse et annule"
            elif décision_cassation == "rejetée":
                self.statuts["appel"] = False  # Réinitialiser le statut de l'appel
                return "rejette"
        return None

    def simuler_audience(self):
        return random.choice(["acceptée", "rejetée"])

    def obtenir_historique(self):
        self.enregistrer_événement("Obtention de l'historique")
        return self.historique

    def enregistrer_événement(self, message):
        logging.info(f"Affaire {self.id} : {message}")

    def __str__(self):
        return f"Affaire(id={self.id}, texte={self.texte}, id_norme={self.id_norme}, constitutionnelle={self.constitutionnelle}, complexité={self.complexité})"

class Tribunal:
    """Classe de base pour tous les tribunaux."""
    def __init__(self, nom_tribunal):
        self.nom_tribunal = nom_tribunal
        self.enregistrer_événement(f"Tribunal {nom_tribunal} initialisé")

    def enregistrer_affaire(self, affaire):
        self.enregistrer_événement(f"Affaire {affaire.id} enregistrée dans le tribunal {self.nom_tribunal}")
        affaire.enregistrer_événement(f"Enregistrée dans le tribunal {self.nom_tribunal}")

    def conduire_audience(self, affaire):
        self.enregistrer_événement(f"Audience conduite pour l'affaire {affaire.id} dans le tribunal {self.nom_tribunal}")
        affaire.enregistrer_événement(f"Audience conduite dans le tribunal {self.nom_tribunal}")

    def rendre_jugement(self, affaire):
        jugement = random.choice(["acceptée", "rejetée"])
        self.enregistrer_événement(f"Jugement rendu pour l'affaire {affaire.id} dans le tribunal {self.nom_tribunal} : {jugement}")
        affaire.enregistrer_événement(f"Jugement rendu dans le tribunal {self.nom_tribunal} : {jugement}")
        return jugement

    def enregistrer_événement(self, message):
        logging.info(f"Tribunal {self.nom_tribunal} : {message}")

class SystèmePolitique:
    """Classe de base pour tous les systèmes politiques."""
    def __init__(self):
        self.compteur_normes = 0
        self.normes = []

    def créer_norme(self):
        """Méthode abstraite à surcharger dans les sous-classes."""
        raise NotImplementedError("Cette méthode doit être surchargée dans les sous-classes.")
        
class Sénat(SystèmePolitique):
    """Représente le Sénat qui participe au vote des lois."""
    def __init__(self):
        super().__init__()

    def voter_loi(self, loi):
        """Voter une loi au Sénat."""
        loi.enregistrer_événement("Votée par le Sénat")
        return loi

class Parlement(SystèmePolitique):
    """Représente le Parlement législatif qui crée les lois."""
    def __init__(self):
        super().__init__()
        self.sénat = Sénat()

    def créer_norme(self):
        """Créer une loi avec une complexité aléatoire."""
        self.compteur_normes += 1
        loi = Loi(
            identifiant_norme=self.compteur_normes,
            texte=f'Loi {self.compteur_normes}',
            complexité=random.randint(COMPLEXITÉ_MIN, COMPLEXITÉ_MAX)
        )
        self.normes.append(loi)
        return loi

    def voter_loi(self, loi):
        """Voter une loi à l'Assemblée nationale."""
        loi.enregistrer_événement("Votée par l'Assemblée nationale")
        self.sénat.voter_loi(loi)  # Vote au Sénat
        return loi

    def navette_parlementaire(self, loi):
        """Simuler la navette parlementaire."""
        loi.enregistrer_événement("Navette parlementaire initiée")
        # Simuler les allers-retours entre les deux chambres
        if random.choice([True, False]):  # Simuler un accord ou désaccord
            loi.enregistrer_événement("Accord trouvé entre les deux chambres")
        else:
            loi.enregistrer_événement("Désaccord, commission mixte paritaire convoquée")
        return loi

    def proposer_révision_constitution(self, texte_révision):
        """Proposer une révision de la Constitution."""
        self.compteur_normes += 1
        révision = Norme(
            identifiant_norme=self.compteur_normes,
            texte=f'Révision Constitutionnelle {self.compteur_normes}: {texte_révision}',
            complexité=random.randint(COMPLEXITÉ_MIN, COMPLEXITÉ_MAX)
        )
        self.normes.append(révision)
        révision.enregistrer_événement("Proposition de révision constitutionnelle déposée au Parlement")
        return révision

    def voter_révision(self, révision):
        """Voter une révision constitutionnelle."""
        révision.enregistrer_événement("Votée par le Parlement")
        return révision

class Gouvernement(SystèmePolitique):
    """Représente le Gouvernement exécutif qui crée les règlements."""
    def __init__(self):
        super().__init__()
        self.compteur_règlements = 0  # Compteur distinct pour les règlements

    def créer_norme(self):
        """Créer un règlement avec une complexité aléatoire."""
        self.compteur_règlements += 1
        règlement = Règlement(
            identifiant_norme=self.compteur_règlements,
            texte=f'Règlement {self.compteur_règlements}',
            complexité=random.randint(COMPLEXITÉ_MIN, COMPLEXITÉ_MAX)
        )
        self.normes.append(règlement)
        return règlement

    def engager_responsabilité(self, loi):
        """Engager la responsabilité du Gouvernement sur un texte (article 49.3)."""
        loi.enregistrer_événement("Responsabilité du Gouvernement engagée sur la loi")
        if random.choice([True, False]):  # Simuler une motion de censure
            loi.enregistrer_événement("Motion de censure adoptée, Gouvernement censuré")
            return False
        else:
            loi.enregistrer_événement("Motion de censure rejetée, Gouvernement maintenu")
            return True

class ConseilConstitutionnel:
    """Représente le Conseil Constitutionnel pour le contrôle des lois."""
    def __init__(self):
        self.nom = "Conseil Constitutionnel"
        self.enregistrer_événement("Conseil Constitutionnel initialisé")

    def contrôler_constitutionnalité(self, loi):
        """Contrôle la constitutionnalité d'une loi avant promulgation."""
        est_constitutionnelle = random.choice([True, False])  # Simuler le processus de contrôle
        loi.valide = est_constitutionnelle  # Mettre à jour l'état de validité
        loi.enregistrer_événement(f"Contrôle de constitutionnalité : {'constitutionnelle' if est_constitutionnelle else 'inconstitutionnelle'}")
        return est_constitutionnelle

    def traiter_qpc(self, loi):
        """Traitement d'une question prioritaire de constitutionnalité."""
        loi.enregistrer_événement("QPC traitée par le Conseil Constitutionnel")
        if random.choice([True, False]):  # Simuler le résultat de la QPC
            loi.enregistrer_événement("QPC validée, loi conforme à la Constitution")
            return True
        else:
            loi.enregistrer_événement("QPC invalidée, loi non conforme à la Constitution")
            return False

    def contrôler_élection(self, élection):
        """Contrôle de la régularité d'une élection."""
        self.enregistrer_événement(f"Contrôle de la régularité de l'élection : {élection}")
        if random.choice([True, False]):  # Simuler le résultat du contrôle
            self.enregistrer_événement("Élection validée")
            return True
        else:
            self.enregistrer_événement("Élection invalidée")
            return False

    def contrôler_traité(self, traité):
        """Contrôle de la conformité d'un traité avec la Constitution."""
        self.enregistrer_événement(f"Contrôle de la conformité du traité : {traité}")
        if random.choice([True, False]):  # Simuler le résultat du contrôle
            self.enregistrer_événement("Traitée conforme à la Constitution")
            return True
        else:
            self.enregistrer_événement("Traitée non conforme à la Constitution")
            return False

    def protéger_droits_fondamentaux(self, droit):
        """Simuler la protection des droits fondamentaux."""
        self.enregistrer_événement(f"Protection du droit fondamental : {droit}")

    def enregistrer_événement(self, message):
        logging.info(f"Conseil Constitutionnel : {message}")

class ConseilÉtat:
    """Représente le Conseil d'État pour le contrôle des règlements."""
    def __init__(self):
        self.nom = "Conseil d'État"
        self.enregistrer_événement("Conseil d'État initialisé")

    def examiner_règlement(self, règlement):
        """Examine la légalité d'un règlement."""
        est_legal = random.choice([True, False])  # Simuler le processus d'examen
        règlement.valide = est_legal  # Mettre à jour l'état de validité
        règlement.enregistrer_événement(f"Examen de légalité : {'légal' if est_legal else 'illégal'}")
        return est_legal

    def enregistrer_événement(self, message):
        logging.info(f"Conseil d'État : {message}")

class Président:
    """Représente le Président de la République."""
    def __init__(self):
        self.nom = "Président"
        self.enregistrer_événement("Président de la République en fonction")

    def promulguer_loi(self, loi):
        """Promulgue une loi après son adoption par le Parlement."""
        if loi.valide:
            loi.enregistrer_événement("Promulguée par le Président")
        else:
            loi.enregistrer_événement("Non promulguée en raison d'inconstitutionnalité")

    def dissoudre_assemblée(self):
        """Dissoudre l'Assemblée Nationale."""
        self.enregistrer_événement("Assemblée Nationale dissoute par le Président")

    def nommer_premier_ministre(self, premier_ministre):
        """Nomme le Premier ministre."""
        self.enregistrer_événement(f"{premier_ministre} nommé Premier ministre par le Président")

    def nommer_gouvernement(self, membres_gouvernement):
        """Nomme les membres du Gouvernement sur proposition du Premier ministre."""
        for membre in membres_gouvernement:
            self.enregistrer_événement(f"{membre} nommé membre du Gouvernement par le Président")

    def négocier_traité(self, traité):
        """Négocie et ratifie les traités internationaux."""
        self.enregistrer_événement(f"Traitement du traité {traité} par le Président")

    def activer_pouvoirs_exceptionnels(self):
        """Activer les pouvoirs exceptionnels selon l'article 16."""
        self.enregistrer_événement("Pouvoirs exceptionnels activés par le Président en vertu de l'article 16")

    def réunion_conseil_ministres(self, ordre_du_jour):
        """Simuler une réunion du Conseil des ministres."""
        self.enregistrer_événement(f"Réunion du Conseil des ministres avec l'ordre du jour : {ordre_du_jour}")

    def soumettre_référendum(self, loi):
        """Soumettre un projet de loi à référendum."""
        loi.enregistrer_événement("Soumis à référendum par le Président")
        if random.choice([True, False]):  # Simuler le résultat du référendum
            loi.enregistrer_événement("Référendum adopté")
            return True
        else:
            loi.enregistrer_événement("Référendum rejeté")
            return False

    def enregistrer_événement(self, message):
        logging.info(f"Président : {message}")

class SystèmeJudiciaire:
    """Représente le système judiciaire et ses processus."""
    def __init__(self):
        self.compteur_affaires = 0
        self.affaires = []
        self.normes_constitutionnalité = {}

        # Initialisation des tribunaux
        self.première_instance = Tribunal("Première Instance")
        self.cour_appel = Tribunal("Appel")
        self.cour_cassation = Tribunal("Cour de Cassation")

    def contrôle_constitutionnalité_norme(self, norme, type_controle="CONTRÔLE DE CONSTITUTIONNALITÉ"):
        """Contrôle la constitutionnalité d'une norme."""
        est_constitutionnelle = norme.valide
        norme.enregistrer_événement(f"{type_controle} : {'constitutionnelle' if est_constitutionnelle else 'inconstitutionnelle'}")
        if not est_constitutionnelle:
            self.abroger_norme(norme)
        return est_constitutionnelle

    def abroger_norme(self, norme):
        """Supprime une norme du système."""
        norme.enregistrer_événement("Abrogée et annulée en raison de l'inconstitutionnalité")

    def créer_affaire(self, norme):
        """Crée une nouvelle affaire à partir d'une norme."""
        if self.compteur_affaires not in [affaire.id for affaire in self.affaires]:
            nouvelle_affaire = Affaire(
                identifiant_affaire=self.compteur_affaires,
                texte=f'Affaire {self.compteur_affaires} référant à {norme.texte}',
                id_norme=norme.id,
                constitutionnelle=self.contrôle_constitutionnalité_norme(norme),
                complexité=norme.complexité
            )
            self.affaires.append(nouvelle_affaire)
            self.compteur_affaires += 1
            logging.info(f"Nouvelle affaire générée : {nouvelle_affaire}")
            return nouvelle_affaire
        return None

    def traiter_affaires(self):
        """Traite toutes les affaires en attente dans le système judiciaire."""
        for affaire in self.affaires[:]:
            # Première instance
            self.première_instance.enregistrer_affaire(affaire)
            self.première_instance.conduire_audience(affaire)
            jugement = self.première_instance.rendre_jugement(affaire)
            affaire.décision_finale = jugement

            # Si rejetée en première instance, aller en appel
            if affaire.décision_finale == "rejetée":
                self.cour_appel.enregistrer_affaire(affaire)
                self.cour_appel.conduire_audience(affaire)
                jugement = self.cour_appel.rendre_jugement(affaire)
                affaire.décision_finale = jugement

                # Si rejetée en appel, aller en cassation
                while affaire.décision_finale == "rejetée" and affaire.nombre_cassations < NOMBRE_MAX_CASSATIONS:
                    self.cour_cassation.enregistrer_affaire(affaire)
                    self.cour_cassation.conduire_audience(affaire)
                    jugement = self.cour_cassation.rendre_jugement(affaire)
                    affaire.décision_finale = jugement
                    affaire.nombre_cassations += 1

                    # Si acceptée en cassation, retourner en appel
                    if jugement == "acceptée":
                        affaire.statuts["appel"] = False  # Réinitialiser le statut de l'appel
                        self.cour_appel.enregistrer_affaire(affaire)
                        self.cour_appel.conduire_audience(affaire)
                        jugement = self.cour_appel.rendre_jugement(affaire)
                        affaire.décision_finale = jugement

            affaire.enregistrer_événement(f"Traitée avec le résultat : {affaire.décision_finale}")
            self.affaires.remove(affaire)

    def enregistrer_événement(self, message):
        logging.info(f"Système Judiciaire : {message}")

class AutoritéAdministrativeIndépendante:
    def __init__(self, nom):
        self.nom = nom
        self.enregistrer_événement(f"{nom} initialisée")

    def réguler(self, domaine):
        """Simuler la régulation d'un domaine spécifique."""
        self.enregistrer_événement(f"Régulation du domaine : {domaine}")

    def enregistrer_événement(self, message):
        logging.info(f"{self.nom} : {message}")

class Société:
    """Classe représentant la société avec ses composantes politiques et judiciaires."""
    def __init__(self):
        self.parlement = Parlement()
        self.gouvernement = Gouvernement()
        self.système_judiciaire = SystèmeJudiciaire()
        self.président = Président()
        self.conseil_constitutionnel = ConseilConstitutionnel()
        self.conseil_etat = ConseilÉtat()
        self.itération = 0
        self.aae = AutoritéAdministrativeIndépendante("Autorité Administrative Indépendante")

    async def simuler(self):
        while self.itération < JOURS_DE_SIMULATION:
            self.itération += 1
            logging.info(f"\n\n{'='*20} DÉBUT DU JOUR {self.itération} {'='*20}\n")

            # Le Parlement crée une loi
            loi = self.parlement.créer_norme()
            logging.info(f"Parlement a produit : {loi.texte}")

            # Navette parlementaire
            self.parlement.navette_parlementaire(loi)

            # Le Gouvernement crée un règlement
            règlement = self.gouvernement.créer_norme()
            logging.info(f"Gouvernement a produit : {règlement.texte}")

            # Le Conseil Constitutionnel contrôle la constitutionnalité des lois
            if self.conseil_constitutionnel.contrôler_constitutionnalité(loi):
                self.président.promulguer_loi(loi)

            # Le Conseil d'État contrôle la légalité des règlements
            if self.conseil_etat.examiner_règlement(règlement):
                logging.info(f"Règlement {règlement.texte} validé par le Conseil d'État")

            # Le système judiciaire crée des affaires pour les normes valides
            if loi.valide:
                affaire_loi = self.système_judiciaire.créer_affaire(loi)
                if affaire_loi:
                    logging.info(f"Système Judiciaire a produit : {affaire_loi.texte}")

            if règlement.valide:
                affaire_règlement = self.système_judiciaire.créer_affaire(règlement)
                if affaire_règlement:
                    logging.info(f"Système Judiciaire a produit : {affaire_règlement.texte}")

            # Traiter les affaires
            self.système_judiciaire.traiter_affaires()

            logging.info(f"\n{'='*20} FIN DU JOUR {self.itération} {'='*20}\n")
            await asyncio.sleep(1)  # Simule le passage du temps

        logging.info("Simulation terminée.")

async def main():
    société = Société()
    await société.simuler()

asyncio.run(main())
