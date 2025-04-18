"""
Descriptions détaillées des indicateurs ACI basées sur les textes de la CPAM
"""

# Dictionnaire contenant les descriptions détaillées des indicateurs ACI
indicator_details = {
    # Axe 1 - Accès aux soins - Indicateurs Socles et Prérequis
    "A1S1": {
        "title": "Horaires d'ouverture et soins non programmés",
        "description": """
### Objectif
Assurer une amplitude horaire d'ouverture importante et un accès à des soins non programmés chaque jour ouvré.

### Critères de validation
- **Amplitude horaire** : La structure doit être ouverte au minimum 8h par jour en semaine et le samedi matin, avec une possibilité d'adaptation selon les besoins du territoire.
- **Soins non programmés** : La structure doit organiser une réponse aux demandes de soins non programmés chaque jour ouvré.

### Points attribués
- **Points fixes** : 800 points
- **Points variables** : 0 point
        """
    },
    "A1S2": {
        "title": "Réponse aux crises sanitaires graves",
        "description": """
### Objectif
Permettre à la structure de s'organiser pour répondre aux besoins en soins des patients en cas de crise sanitaire grave.

### Critères de validation
- **Plan de préparation** : Rédaction d'un plan de préparation aux crises sanitaires graves.
- **Actions mises en œuvre** : Mise en œuvre d'actions pouvant répondre aux besoins en soins des patients en cas de crise sanitaire grave.

### Points attribués
- **Points fixes** : 100 points
- **Points variables** : 350 points (selon le nombre de patients)
        """
    },

    # Axe 1 - Accès aux soins - Indicateurs Optionnels
    "A1O1": {
        "title": "Offre d'une diversité de services de soins médicaux spécialisés",
        "description": """
### Objectif
Valoriser la présence de professionnels associés de la structure offrant une diversité de services de soins médicaux spécialisés.

### Critères de validation
- **Niveau 1** : Présence d'au moins un médecin spécialiste associé de la structure.
- **Niveau 2** : Présence d'au moins deux médecins spécialistes associés de la structure.

### Points attribués
- **Points fixes** : 300 points
- **Points variables** : 0 point
        """
    },
    "A1O2": {
        "title": "Consultations de spécialistes de second recours extérieurs à la structure",
        "description": """
### Objectif
Valoriser la présence de spécialistes, sages-femmes, chirurgiens-dentistes ou pharmaciens vacataires.

### Critères de validation
- **Niveau 1** : Présence d'au moins un spécialiste, sage-femme, chirurgien-dentiste ou pharmacien vacataire.
- **Niveau 2** : Présence d'au moins deux spécialistes, sages-femmes, chirurgiens-dentistes ou pharmaciens vacataires.

### Points attribués
- **Points fixes** : 300 points
- **Points variables** : 0 point
        """
    },
    "A1O3": {
        "title": "Accueil de médecins intervenant dans la structure dans le cadre d'un CSTM",
        "description": """
### Objectif
Valoriser l'intervention au sein de la structure d'au moins un médecin signataire d'un contrat de solidarité territoriale médecin (CSTM).

### Critères de validation
- Présence d'au moins un médecin signataire d'un CSTM intervenant dans la structure.

### Points attribués
- **Points fixes** : 200 points
- **Points variables** : 0 point
        """
    },
    "A1O4": {
        "title": "Missions de santé publique",
        "description": """
### Objectif
Valoriser la réalisation de missions de santé publique par la structure.

### Critères de validation
- Réalisation d'au moins une mission de santé publique parmi celles définies par l'ARS.
- Maximum 2 missions valorisées.

### Points attribués
- **Points fixes** : 200 points par mission (maximum 2 missions)
- **Points variables** : 700 points (selon le nombre de patients)
- **Bonus IPA** : +200 points fixes si présence d'un IPA et réalisation de 2 missions
        """
    },
    "A1O5": {
        "title": "Implication des usagers",
        "description": """
### Objectif
Valoriser la mise en place d'outils ou actions visant à impliquer les usagers.

### Critères de validation
- **Niveau 1** : Mise en place d'au moins un outil ou action visant à impliquer les usagers.
- **Niveau 2** : Mise en place d'au moins deux outils ou actions visant à impliquer les usagers.

### Points attribués
- **Points fixes** : 200 points
- **Points variables** : 300 points (selon le nombre de patients)
        """
    },
    "A1O6": {
        "title": "Soins non programmés en lien avec le dispositif de Service d'accès aux soins",
        "description": """
### Objectif
Valoriser la participation des médecins au dispositif SAS (Service d'accès aux soins).

### Critères de validation
- Participation d'au moins 50% des médecins de la structure au dispositif SAS.
- Ou prise en charge de toutes les sollicitations du SAS.

### Points attribués
- **Points fixes** : 100 points si 50% des médecins participent, 200 points si 100% des médecins participent ou si toutes les sollicitations sont prises en charge.
- **Points variables** : 0 point
        """
    },

    # Axe 2 - Travail en équipe et coordination - Indicateurs Socles et Prérequis
    "A2S1": {
        "title": "Fonction de coordination",
        "description": """
### Objectif
Valoriser la mise en place d'une fonction de coordination au sein de la structure.

### Critères de validation
- Animation de la coordination.
- Coordination des parcours et des patients.
- Suivi de l'utilisation du système d'information.
- Relation avec les institutions.

### Points attribués
- **Points fixes** : 1000 points
- **Points variables** : 1700 points (selon le nombre de patients)
- **Bonus** : +1100 points au-delà de 8000 patients
        """
    },

    # Axe 2 - Travail en équipe et coordination - Indicateurs Socles
    "A2S2": {
        "title": "Protocoles pluri-professionnels",
        "description": """
### Objectif
Valoriser l'élaboration de protocoles pluri-professionnels au sein de la structure.

### Critères de validation
- Élaboration d'au moins un protocole pluri-professionnel.
- Maximum 8 protocoles valorisés.

### Points attribués
- **Points fixes** : 100 points par protocole (maximum 8 protocoles)
- **Bonus IPA** : +40 points fixes par protocole si présence d'un IPA
        """
    },
    "A2S3": {
        "title": "Concertation pluri-professionnelle",
        "description": """
### Objectif
Valoriser l'organisation de réunions de concertation pluri-professionnelle au sein de la structure.

### Critères de validation
- Organisation régulière de réunions de concertation pluri-professionnelle.
- Formalisation des réunions (ordre du jour, compte-rendu, etc.).

### Points attribués
- **Points fixes** : 0 point
- **Points variables** : 1000 points (selon le nombre de patients)
- **Bonus IPA** : +200 points variables si présence d'un IPA
        """
    },

    # Axe 2 - Travail en équipe et coordination - Indicateurs Optionnels
    "A2O1": {
        "title": "Formation de professionnels de santé",
        "description": """
### Objectif
Valoriser l'accueil de stagiaires au sein de la structure.

### Critères de validation
- Accueil d'au moins un stagiaire.
- Maximum 4 stages valorisés.

### Points attribués
- **Points fixes** : 450 points pour 2 stages, +225 points pour le 3ème et 4ème stage
- **Points variables** : 0 point
        """
    },
    "A2O2": {
        "title": "Coordination externe",
        "description": """
### Objectif
Valoriser la mise en place d'une coordination avec les acteurs externes.

### Critères de validation
- Mise en place d'une coordination avec les acteurs externes (hôpitaux, EHPAD, etc.).
- Formalisation de cette coordination.

### Points attribués
- **Points fixes** : 0 point
- **Points variables** : 200 points (selon le nombre de patients)
        """
    },
    "A2O3": {
        "title": "Démarche qualité",
        "description": """
### Objectif
Valoriser la mise en place d'une démarche d'auto-évaluation au sein de la structure.

### Critères de validation
- **Niveau 1** : Mise en place d'une démarche d'auto-évaluation.
- **Niveau 2** : Mise en place d'une démarche d'auto-évaluation et d'un plan d'amélioration.
- **Niveau 3** : Mise en place d'une démarche d'auto-évaluation, d'un plan d'amélioration et d'un suivi des actions.

### Points attribués
- **Points fixes** : 100 points (Niveau 1)
- **Points variables** : 200 points pour le niveau 2, 300 points pour le niveau 3
        """
    },
    "A2O4": {
        "title": "Protocoles nationaux de coopération des soins non programmés",
        "description": """
### Objectif
Valoriser la mise en œuvre de protocoles nationaux de coopération pour les soins non programmés.

### Critères de validation
- Mise en œuvre d'au moins un protocole national de coopération.
- Maximum 6 protocoles valorisés.

### Points attribués
- **Points fixes** : 100 points par protocole (maximum 6 protocoles)
- **Points variables** : 0 point
        """
    },
    "A2O5": {
        "title": "Parcours Insuffisance Cardiaque",
        "description": """
### Objectif
Valoriser la participation au parcours de soins des patients ayant une insuffisance cardiaque.

### Critères de validation
- Participation au parcours de soins des patients ayant une insuffisance cardiaque.
- Mise en place d'actions spécifiques pour ces patients.

### Points attribués
- **Points fixes** : 0 point
- **Points variables** : 100 points (selon le nombre de patients)
        """
    },
    "A2O6": {
        "title": "Coordination d'un parcours 'surpoids ou obésité de l'enfant'",
        "description": """
### Objectif
Valoriser la participation à un parcours visant à accompagner les enfants en situation de surpoids ou d'obésité.

### Critères de validation
- Participation à un parcours visant à accompagner les enfants en situation de surpoids ou d'obésité.
- Mise en place d'actions spécifiques pour ces enfants.

### Points attribués
- **Points fixes** : 100 points
- **Points variables** : 0 point
        """
    },

    # Axe 3 - Système d'information - Indicateur Socle et Prérequis
    "A3S1": {
        "title": "Système d'information de niveau standard",
        "description": """
### Objectif
Valoriser la mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'standard'.

### Critères de validation
- Mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'standard'.
- Utilisation effective par les professionnels de la structure.

### Points attribués
- **Points fixes** : 500 points
- **Points variables** : 200 points par PS associé jusqu'à 16, puis 150 points par PS au-delà
        """
    },

    # Axe 3 - Système d'information - Indicateur Optionnel
    "A3O1": {
        "title": "Système d'information de niveau avancé",
        "description": """
### Objectif
Valoriser la mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'avancé'.

### Critères de validation
- Mise en place d'un système d'information labellisé e-santé par l'ANS de niveau 'avancé'.
- Utilisation effective par les professionnels de la structure.

### Points attribués
- **Points fixes** : 100 points
- **Points variables** : 0 point
        """
    }
}
