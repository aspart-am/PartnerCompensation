"""
Modèle de données pour les charges fixes de la SISA
"""

class Expense:
    def __init__(self, id, name, description, category, amount, frequency="mensuel", 
                 start_date=None, end_date=None, distribution_method="equal"):
        self.id = id
        self.name = name
        self.description = description
        self.category = category  # Logiciel de santé, Rémunération coordinateur, Location salle, Autre
        self.amount = amount  # Montant en euros
        self.frequency = frequency  # Mensuel, Trimestriel, Annuel, Ponctuel
        self.start_date = start_date  # Date de début (pour les charges récurrentes)
        self.end_date = end_date  # Date de fin (pour les charges récurrentes)
        self.distribution_method = distribution_method  # Méthode de répartition (égale, au prorata du temps de présence, etc.)

    def get_annual_amount(self):
        """
        Calcule le montant annuel de la charge
        """
        if self.frequency == "mensuel":
            return self.amount * 12
        elif self.frequency == "trimestriel":
            return self.amount * 4
        elif self.frequency == "annuel":
            return self.amount
        elif self.frequency == "ponctuel":
            return self.amount
        else:
            return self.amount
    
    def get_monthly_amount(self):
        """
        Calcule le montant mensuel de la charge
        """
        if self.frequency == "mensuel":
            return self.amount
        elif self.frequency == "trimestriel":
            return self.amount / 3
        elif self.frequency == "annuel":
            return self.amount / 12
        elif self.frequency == "ponctuel":
            return self.amount / 12  # On répartit sur un an
        else:
            return self.amount
    
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "amount": self.amount,
            "frequency": self.frequency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "distribution_method": self.distribution_method
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Expense à partir d'un dictionnaire
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            amount=data.get("amount", 0),
            frequency=data.get("frequency", "mensuel"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            distribution_method=data.get("distribution_method", "equal")
        )


# Liste des catégories de charges
def get_expense_categories():
    """
    Retourne la liste des catégories de charges
    """
    return [
        "Logiciel de santé",
        "Rémunération coordinateur",
        "Location salle",
        "Matériel médical",
        "Fournitures administratives",
        "Assurances",
        "Frais bancaires",
        "Télécommunications",
        "Entretien et réparations",
        "Honoraires comptables",
        "Honoraires juridiques",
        "Formation",
        "Cotisations professionnelles",
        "Impôts et taxes",
        "Autre"
    ]


# Liste des fréquences de charges
def get_expense_frequencies():
    """
    Retourne la liste des fréquences de charges
    """
    return [
        "mensuel",
        "trimestriel",
        "annuel",
        "ponctuel"
    ]


# Liste des méthodes de répartition des charges
def get_distribution_methods():
    """
    Retourne la liste des méthodes de répartition des charges
    """
    return [
        "equal",  # Répartition égale entre tous les associés
        "presence_time",  # Répartition au prorata du temps de présence
        "distribution_key",  # Répartition selon la clé de répartition définie pour chaque associé
        "medical_only",  # Répartition uniquement entre les professions médicales
        "paramedical_only",  # Répartition uniquement entre les professions paramédicales
        "custom"  # Répartition personnalisée
    ]


# Exemples de charges pour initialiser l'application
def get_sample_expenses():
    """
    Retourne une liste d'exemples de charges
    """
    expenses = []
    
    expenses.append(Expense(
        id="1",
        name="Logiciel médical",
        description="Abonnement au logiciel de gestion médicale",
        category="Logiciel de santé",
        amount=500,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="2",
        name="Rémunération du coordinateur",
        description="Rémunération mensuelle du coordinateur de la SISA",
        category="Rémunération coordinateur",
        amount=1500,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="3",
        name="Location des locaux",
        description="Loyer mensuel des locaux de la SISA",
        category="Location salle",
        amount=2000,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="presence_time"
    ))
    
    expenses.append(Expense(
        id="4",
        name="Assurance professionnelle",
        description="Assurance responsabilité civile professionnelle",
        category="Assurances",
        amount=1200,
        frequency="annuel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="5",
        name="Comptabilité",
        description="Honoraires du cabinet comptable",
        category="Honoraires comptables",
        amount=800,
        frequency="trimestriel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="6",
        name="Matériel informatique",
        description="Achat de nouveaux ordinateurs",
        category="Matériel médical",
        amount=5000,
        frequency="ponctuel",
        start_date="2023-06-01",
        distribution_method="distribution_key"
    ))
    
    expenses.append(Expense(
        id="7",
        name="Fournitures de bureau",
        description="Papier, stylos, etc.",
        category="Fournitures administratives",
        amount=200,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="8",
        name="Internet et téléphonie",
        description="Abonnement internet et téléphonie fixe",
        category="Télécommunications",
        amount=150,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="equal"
    ))
    
    expenses.append(Expense(
        id="9",
        name="Entretien des locaux",
        description="Service de nettoyage hebdomadaire",
        category="Entretien et réparations",
        amount=400,
        frequency="mensuel",
        start_date="2020-01-01",
        distribution_method="presence_time"
    ))
    
    expenses.append(Expense(
        id="10",
        name="Formation collective",
        description="Formation sur les nouveaux protocoles de soins",
        category="Formation",
        amount=3000,
        frequency="ponctuel",
        start_date="2023-09-01",
        distribution_method="medical_only"
    ))
    
    return expenses
