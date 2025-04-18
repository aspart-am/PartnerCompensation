"""
Modèle de données pour les associés de la SISA
"""

class Associate:
    def __init__(self, id, first_name, last_name, profession, speciality=None, 
                 entry_date=None, roles=None, patients_mt=0, presence_time=1.0, 
                 distribution_key=None, email=None, phone=None, rpps=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.profession = profession  # Médecin, Infirmier, Kinésithérapeute, etc.
        self.speciality = speciality  # Spécialité pour les médecins
        self.entry_date = entry_date  # Date d'entrée dans la SISA
        self.roles = roles or []  # Rôles dans la structure (coordinateur, référent qualité, etc.)
        self.patients_mt = patients_mt  # Nombre de patients médecin traitant (pour les médecins)
        self.presence_time = presence_time  # Temps de présence (ETP)
        self.distribution_key = distribution_key or 1.0  # Clé de répartition pour la rémunération
        self.email = email
        self.phone = phone
        self.rpps = rpps  # Numéro RPPS pour les professionnels de santé

    def is_doctor(self):
        """
        Vérifie si l'associé est un médecin
        """
        return self.profession.lower() == "médecin"
    
    def is_medical_profession(self):
        """
        Vérifie si l'associé exerce une profession médicale
        """
        medical_professions = ["médecin", "sage-femme", "chirurgien-dentiste", "pharmacien", "biologiste"]
        return self.profession.lower() in medical_professions
    
    def is_paramedical_profession(self):
        """
        Vérifie si l'associé exerce une profession paramédicale
        """
        paramedical_professions = [
            "infirmier", "masseur-kinésithérapeute", "pédicure-podologue", "ergothérapeute", 
            "psychomotricien", "orthophoniste", "orthoptiste", "manipulateur d'électroradiologie", 
            "audioprothésiste", "opticien-lunetier", "prothésiste", "orthésiste", "diététicien", 
            "aide-soignant", "auxiliaire de puériculture", "ambulancier", "assistant dentaire"
        ]
        return self.profession.lower() in paramedical_professions
    
    def has_role(self, role):
        """
        Vérifie si l'associé a un rôle spécifique
        """
        return role in self.roles
    
    def get_full_name(self):
        """
        Retourne le nom complet de l'associé
        """
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profession": self.profession,
            "speciality": self.speciality,
            "entry_date": self.entry_date,
            "roles": self.roles,
            "patients_mt": self.patients_mt,
            "presence_time": self.presence_time,
            "distribution_key": self.distribution_key,
            "email": self.email,
            "phone": self.phone,
            "rpps": self.rpps
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Associate à partir d'un dictionnaire
        """
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            profession=data.get("profession"),
            speciality=data.get("speciality"),
            entry_date=data.get("entry_date"),
            roles=data.get("roles"),
            patients_mt=data.get("patients_mt", 0),
            presence_time=data.get("presence_time", 1.0),
            distribution_key=data.get("distribution_key"),
            email=data.get("email"),
            phone=data.get("phone"),
            rpps=data.get("rpps")
        )


# Liste des professions médicales et paramédicales
def get_professions():
    """
    Retourne la liste des professions médicales et paramédicales
    """
    medical_professions = [
        "Médecin généraliste",
        "Médecin spécialiste",
        "Sage-femme",
        "Chirurgien-dentiste",
        "Pharmacien",
        "Biologiste"
    ]
    
    paramedical_professions = [
        "Infirmier",
        "Infirmier en pratique avancée (IPA)",
        "Masseur-kinésithérapeute",
        "Pédicure-podologue",
        "Ergothérapeute",
        "Psychomotricien",
        "Orthophoniste",
        "Orthoptiste",
        "Manipulateur d'électroradiologie",
        "Audioprothésiste",
        "Opticien-lunetier",
        "Prothésiste",
        "Orthésiste",
        "Diététicien",
        "Aide-soignant",
        "Auxiliaire de puériculture",
        "Ambulancier",
        "Assistant dentaire"
    ]
    
    return {
        "medical": medical_professions,
        "paramedical": paramedical_professions,
        "all": medical_professions + paramedical_professions
    }


# Liste des spécialités médicales
def get_medical_specialities():
    """
    Retourne la liste des spécialités médicales
    """
    return [
        "Allergologie",
        "Anatomie et cytologie pathologiques",
        "Anesthésie-réanimation",
        "Biologie médicale",
        "Cardiologie et maladies vasculaires",
        "Chirurgie générale",
        "Chirurgie maxillo-faciale",
        "Chirurgie orale",
        "Chirurgie orthopédique et traumatologique",
        "Chirurgie pédiatrique",
        "Chirurgie plastique, reconstructrice et esthétique",
        "Chirurgie thoracique et cardiovasculaire",
        "Chirurgie vasculaire",
        "Chirurgie viscérale et digestive",
        "Dermatologie et vénéréologie",
        "Endocrinologie-diabétologie-nutrition",
        "Gastro-entérologie et hépatologie",
        "Génétique médicale",
        "Gériatrie",
        "Gynécologie médicale",
        "Gynécologie obstétrique",
        "Hématologie",
        "Hépato-gastro-entérologie",
        "Médecine d'urgence",
        "Médecine du travail",
        "Médecine générale",
        "Médecine intensive-réanimation",
        "Médecine interne",
        "Médecine légale et expertises médicales",
        "Médecine nucléaire",
        "Médecine physique et de réadaptation",
        "Médecine vasculaire",
        "Néphrologie",
        "Neurochirurgie",
        "Neurologie",
        "Oncologie",
        "Ophtalmologie",
        "Oto-rhino-laryngologie - chirurgie cervico-faciale",
        "Pédiatrie",
        "Pneumologie",
        "Psychiatrie",
        "Radiologie et imagerie médicale",
        "Rhumatologie",
        "Santé publique",
        "Urologie"
    ]


# Liste des rôles possibles dans la structure
def get_roles():
    """
    Retourne la liste des rôles possibles dans la structure
    """
    return [
        "Coordinateur",
        "Référent qualité",
        "Référent système d'information",
        "Référent formation",
        "Référent protocoles",
        "Référent missions de santé publique",
        "Référent relations externes",
        "Membre du conseil de gestion",
        "Gérant"
    ]


# Exemples d'associés pour initialiser l'application
def get_sample_associates():
    """
    Retourne une liste d'exemples d'associés
    """
    associates = []
    
    # 5 médecins
    associates.append(Associate(
        id="1",
        first_name="Jean",
        last_name="Dupont",
        profession="Médecin généraliste",
        speciality="Médecine générale",
        entry_date="2020-01-01",
        roles=["Coordinateur", "Référent protocoles"],
        patients_mt=800,
        presence_time=1.0,
        distribution_key=1.0,
        email="jean.dupont@example.com",
        phone="0123456789",
        rpps="10123456789"
    ))
    
    associates.append(Associate(
        id="2",
        first_name="Marie",
        last_name="Martin",
        profession="Médecin généraliste",
        speciality="Médecine générale",
        entry_date="2020-01-01",
        roles=["Référent qualité"],
        patients_mt=750,
        presence_time=1.0,
        distribution_key=1.0,
        email="marie.martin@example.com",
        phone="0123456790",
        rpps="10123456790"
    ))
    
    associates.append(Associate(
        id="3",
        first_name="Pierre",
        last_name="Durand",
        profession="Médecin généraliste",
        speciality="Médecine générale",
        entry_date="2020-01-01",
        roles=["Référent formation"],
        patients_mt=700,
        presence_time=1.0,
        distribution_key=1.0,
        email="pierre.durand@example.com",
        phone="0123456791",
        rpps="10123456791"
    ))
    
    associates.append(Associate(
        id="4",
        first_name="Sophie",
        last_name="Petit",
        profession="Médecin généraliste",
        speciality="Médecine générale",
        entry_date="2020-01-01",
        roles=["Référent missions de santé publique"],
        patients_mt=650,
        presence_time=1.0,
        distribution_key=1.0,
        email="sophie.petit@example.com",
        phone="0123456792",
        rpps="10123456792"
    ))
    
    associates.append(Associate(
        id="5",
        first_name="Thomas",
        last_name="Bernard",
        profession="Médecin spécialiste",
        speciality="Cardiologie et maladies vasculaires",
        entry_date="2020-01-01",
        roles=["Référent relations externes"],
        patients_mt=500,
        presence_time=0.8,
        distribution_key=0.8,
        email="thomas.bernard@example.com",
        phone="0123456793",
        rpps="10123456793"
    ))
    
    # Autres professionnels de santé
    associates.append(Associate(
        id="6",
        first_name="Claire",
        last_name="Robert",
        profession="Infirmier",
        entry_date="2020-01-01",
        roles=[],
        presence_time=1.0,
        distribution_key=0.7,
        email="claire.robert@example.com",
        phone="0123456794",
        rpps="10123456794"
    ))
    
    associates.append(Associate(
        id="7",
        first_name="Michel",
        last_name="Richard",
        profession="Masseur-kinésithérapeute",
        entry_date="2020-01-01",
        roles=[],
        presence_time=1.0,
        distribution_key=0.7,
        email="michel.richard@example.com",
        phone="0123456795",
        rpps="10123456795"
    ))
    
    associates.append(Associate(
        id="8",
        first_name="Isabelle",
        last_name="Moreau",
        profession="Orthophoniste",
        entry_date="2020-01-01",
        roles=[],
        presence_time=0.8,
        distribution_key=0.6,
        email="isabelle.moreau@example.com",
        phone="0123456796",
        rpps="10123456796"
    ))
    
    associates.append(Associate(
        id="9",
        first_name="Philippe",
        last_name="Simon",
        profession="Pédicure-podologue",
        entry_date="2020-01-01",
        roles=[],
        presence_time=0.5,
        distribution_key=0.5,
        email="philippe.simon@example.com",
        phone="0123456797",
        rpps="10123456797"
    ))
    
    associates.append(Associate(
        id="10",
        first_name="Nathalie",
        last_name="Laurent",
        profession="Diététicien",
        entry_date="2020-01-01",
        roles=[],
        presence_time=0.5,
        distribution_key=0.5,
        email="nathalie.laurent@example.com",
        phone="0123456798",
        rpps="10123456798"
    ))
    
    # Ajout d'autres associés pour atteindre 24
    professions = ["Infirmier", "Masseur-kinésithérapeute", "Orthophoniste", "Psychomotricien", 
                  "Ergothérapeute", "Sage-femme", "Chirurgien-dentiste", "Pharmacien", 
                  "Infirmier en pratique avancée (IPA)", "Orthoptiste", "Diététicien", 
                  "Pédicure-podologue", "Aide-soignant", "Assistant dentaire"]
    
    for i in range(11, 25):
        profession_index = (i - 11) % len(professions)
        associates.append(Associate(
            id=str(i),
            first_name=f"Prénom{i}",
            last_name=f"Nom{i}",
            profession=professions[profession_index],
            entry_date="2020-01-01",
            roles=[],
            presence_time=0.8,
            distribution_key=0.5,
            email=f"prenom{i}.nom{i}@example.com",
            phone=f"01234567{i if i > 9 else '0' + str(i)}",
            rpps=f"101234567{i if i > 9 else '0' + str(i)}"
        ))
    
    return associates
