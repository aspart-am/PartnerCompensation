"""
Modèle de données pour les indicateurs ACI
"""

class Indicator:
    def __init__(self, id, name, description, axis, type_indicator, is_prerequisite, 
                 points_fixed, points_variable, reference_patients=4000, max_level=1):
        self.id = id
        self.name = name
        self.description = description
        self.axis = axis  # 1: Accès aux soins, 2: Travail en équipe, 3: Système d'information
        self.type_indicator = type_indicator  # "socle" ou "optionnel"
        self.is_prerequisite = is_prerequisite
        self.points_fixed = points_fixed
        self.points_variable = points_variable
        self.reference_patients = reference_patients
        self.max_level = max_level  # Certains indicateurs ont plusieurs niveaux
        self.completion_status = 0  # 0: Non complété, 1: Niveau 1 complété, 2: Niveau 2 complété, etc.
        self.completion_percentage = 0  # Pour les indicateurs avec pourcentage de complétion

    def calculate_points(self, nb_patients, nb_associates=None):
        """
        Calcule les points obtenus pour cet indicateur
        """
        if self.completion_status == 0:
            return 0
        
        points = self.points_fixed
        
        # Si l'indicateur a des points variables, on les calcule en fonction du nombre de patients
        if self.points_variable > 0:
            ratio = min(nb_patients / self.reference_patients, 1) if self.reference_patients > 0 else 1
            
            # Pour les indicateurs avec pourcentage de complétion
            if self.completion_percentage > 0:
                ratio = ratio * (self.completion_percentage / 100)
                
            points += self.points_variable * ratio
        
        return points
    
    def calculate_amount(self, nb_patients, nb_associates=None, point_value=7):
        """
        Calcule le montant en euros pour cet indicateur
        """
        return self.calculate_points(nb_patients, nb_associates) * point_value


# Définition des indicateurs ACI basés sur le guide
def get_indicators():
    """
    Retourne la liste des indicateurs ACI
    """
    indicators = []
    
    # Axe 1 - Accès aux soins - Indicateurs Socles et Prérequis
    indicators.append(Indicator(
        id="A1S1",
        name="Horaires d'ouverture et soins non programmés",
        description="Amplitude horaire et accès à des soins non programmés chaque jour ouvré",
        axis=1,
        type_indicator="socle",
        is_prerequisite=True,
        points_fixed=800,
        points_variable=0
    ))
    
    indicators.append(Indicator(
        id="A1S2",
        name="Réponse aux crises sanitaires graves",
        description="Rédaction d'un plan de préparation et mise en œuvre d'actions pouvant répondre aux besoins en soins de patients",
        axis=1,
        type_indicator="socle",
        is_prerequisite=True,
        points_fixed=100,
        points_variable=350
    ))
    
    # Axe 1 - Accès aux soins - Indicateurs Optionnels
    indicators.append(Indicator(
        id="A1O1",
        name="Offre d'une diversité de services de soins médicaux spécialisés",
        description="Présence de professionnels associés de la structure",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=300,
        points_variable=0,
        max_level=2
    ))
    
    indicators.append(Indicator(
        id="A1O2",
        name="Consultations de spécialistes de second recours extérieurs à la structure",
        description="Présence de spécialistes, sages-femmes, chirurgiens-dentistes ou pharmaciens vacataires",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=300,
        points_variable=0,
        max_level=2
    ))
    
    indicators.append(Indicator(
        id="A1O3",
        name="Accueil de médecins intervenant dans la structure dans le cadre d'un CSTM",
        description="Valoriser l'intervention au sein de la structure d'au moins un médecin signataire d'un contrat de solidarité territoriale médecin (CSTM)",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=200,
        points_variable=0
    ))
    
    indicators.append(Indicator(
        id="A1O4",
        name="Missions de santé publique",
        description="Réalisation de missions de santé publique (maximum 2 missions valorisées)",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=200,  # +200 si présence d'un IPA
        points_variable=700
    ))
    
    indicators.append(Indicator(
        id="A1O5",
        name="Implication des usagers",
        description="Mise en place d'outils ou actions visant à impliquer les usagers",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=200,
        points_variable=300,
        max_level=2
    ))
    
    indicators.append(Indicator(
        id="A1O6",
        name="Soins non programmés en lien avec le dispositif de Service d'accès aux soins",
        description="Participation des médecins au dispositif SAS",
        axis=1,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=200,  # 100 pour 50% des médecins, 200 pour 100% ou toutes les sollicitations
        points_variable=0
    ))
    
    # Axe 2 - Travail en équipe et coordination - Indicateurs Socles et Prérequis
    indicators.append(Indicator(
        id="A2S1",
        name="Fonction de coordination",
        description="Animation de la coordination, coordination des parcours et des patients, suivi de l'utilisation du système d'information, relation avec les institutions",
        axis=2,
        type_indicator="socle",
        is_prerequisite=True,
        points_fixed=1000,
        points_variable=1700  # +1100 au-delà de 8000 patients
    ))
    
    # Axe 2 - Travail en équipe et coordination - Indicateurs Socles
    indicators.append(Indicator(
        id="A2S2",
        name="Protocoles pluri-professionnels",
        description="Élaboration de protocoles pluri-professionnels (8 protocoles maximum valorisés)",
        axis=2,
        type_indicator="socle",
        is_prerequisite=False,
        points_fixed=100,  # par protocole, +40 par protocole si présence d'un IPA
        points_variable=0
    ))
    
    indicators.append(Indicator(
        id="A2S3",
        name="Concertation pluri-professionnelle",
        description="Organisation de réunions de concertation pluri-professionnelle",
        axis=2,
        type_indicator="socle",
        is_prerequisite=False,
        points_fixed=0,
        points_variable=1000  # +200 si présence d'un IPA
    ))
    
    # Axe 2 - Travail en équipe et coordination - Indicateurs Optionnels
    indicators.append(Indicator(
        id="A2O1",
        name="Formation de professionnels de santé",
        description="Accueil de stagiaires (4 stages maximum valorisés)",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=450,  # 450 pour 2 stages, +225 pour le 3ème et 4ème stage
        points_variable=0
    ))
    
    indicators.append(Indicator(
        id="A2O2",
        name="Coordination externe",
        description="Mise en place d'une coordination avec les acteurs externes",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=0,
        points_variable=200
    ))
    
    indicators.append(Indicator(
        id="A2O3",
        name="Démarche qualité",
        description="Mise en place d'une démarche d'auto-évaluation",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=100,  # Niveau 1
        points_variable=500,  # 200 pour niveau 2, 300 pour niveau 3
        max_level=3
    ))
    
    indicators.append(Indicator(
        id="A2O4",
        name="Protocoles nationaux de coopération des soins non programmés",
        description="Mise en œuvre de protocoles nationaux de coopération (6 protocoles maximum valorisés)",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=100,  # par protocole
        points_variable=0
    ))
    
    indicators.append(Indicator(
        id="A2O5",
        name="Parcours Insuffisance Cardiaque",
        description="Participation au parcours de soins des patients ayant une insuffisance cardiaque",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=0,
        points_variable=100
    ))
    
    indicators.append(Indicator(
        id="A2O6",
        name="Coordination d'un parcours 'surpoids ou obésité de l'enfant'",
        description="Participation à un parcours visant à accompagner les enfants en situation de surpoids ou d'obésité",
        axis=2,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=100,
        points_variable=0
    ))
    
    # Axe 3 - Système d'information - Indicateur Socle et Prérequis
    indicators.append(Indicator(
        id="A3S1",
        name="Système d'information de niveau standard",
        description="Mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'standard'",
        axis=3,
        type_indicator="socle",
        is_prerequisite=True,
        points_fixed=500,
        points_variable=200  # par PS associé jusqu'à 16, puis 150 par PS au-delà
    ))
    
    # Axe 3 - Système d'information - Indicateur Optionnel
    indicators.append(Indicator(
        id="A3O1",
        name="Système d'information de niveau avancé",
        description="Mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'avancé'",
        axis=3,
        type_indicator="optionnel",
        is_prerequisite=False,
        points_fixed=100,
        points_variable=0
    ))
    
    return indicators
