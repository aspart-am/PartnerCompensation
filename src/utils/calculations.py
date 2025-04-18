"""
Utilitaires pour les calculs de rémunération et la gestion des données
"""

import pandas as pd
import numpy as np
from src.models.indicators import Indicator
from src.models.associates import Associate
from src.models.expenses import Expense

# Valeur d'un point ACI en euros
POINT_VALUE = 7

def calculate_total_points(indicators, nb_patients, nb_associates=None):
    """
    Calcule le nombre total de points obtenus pour l'ensemble des indicateurs
    
    Args:
        indicators (list): Liste des indicateurs
        nb_patients (int): Nombre de patients médecin traitant
        nb_associates (int, optional): Nombre d'associés. Defaults to None.
        
    Returns:
        float: Nombre total de points
    """
    total_points = 0
    
    # Vérifier si tous les indicateurs socles et prérequis sont complétés
    prerequisites_completed = True
    for indicator in indicators:
        if indicator.is_prerequisite and indicator.completion_status == 0:
            prerequisites_completed = False
            break
    
    # Si tous les prérequis sont complétés, on calcule les points
    if prerequisites_completed:
        for indicator in indicators:
            total_points += indicator.calculate_points(nb_patients, nb_associates)
    
    return total_points

def calculate_total_amount(indicators, nb_patients, nb_associates=None, point_value=POINT_VALUE):
    """
    Calcule le montant total en euros pour l'ensemble des indicateurs
    
    Args:
        indicators (list): Liste des indicateurs
        nb_patients (int): Nombre de patients médecin traitant
        nb_associates (int, optional): Nombre d'associés. Defaults to None.
        point_value (float, optional): Valeur d'un point en euros. Defaults to POINT_VALUE.
        
    Returns:
        float: Montant total en euros
    """
    total_points = calculate_total_points(indicators, nb_patients, nb_associates)
    return total_points * point_value

def calculate_points_by_axis(indicators, nb_patients, nb_associates=None):
    """
    Calcule le nombre de points obtenus par axe
    
    Args:
        indicators (list): Liste des indicateurs
        nb_patients (int): Nombre de patients médecin traitant
        nb_associates (int, optional): Nombre d'associés. Defaults to None.
        
    Returns:
        dict: Dictionnaire avec les points par axe
    """
    points_by_axis = {1: 0, 2: 0, 3: 0}
    
    # Vérifier si tous les indicateurs socles et prérequis sont complétés
    prerequisites_completed = True
    for indicator in indicators:
        if indicator.is_prerequisite and indicator.completion_status == 0:
            prerequisites_completed = False
            break
    
    # Si tous les prérequis sont complétés, on calcule les points par axe
    if prerequisites_completed:
        for indicator in indicators:
            axis = indicator.axis
            points = indicator.calculate_points(nb_patients, nb_associates)
            points_by_axis[axis] += points
    
    return points_by_axis

def calculate_points_by_type(indicators, nb_patients, nb_associates=None):
    """
    Calcule le nombre de points obtenus par type d'indicateur (socle ou optionnel)
    
    Args:
        indicators (list): Liste des indicateurs
        nb_patients (int): Nombre de patients médecin traitant
        nb_associates (int, optional): Nombre d'associés. Defaults to None.
        
    Returns:
        dict: Dictionnaire avec les points par type
    """
    points_by_type = {"socle": 0, "optionnel": 0}
    
    # Vérifier si tous les indicateurs socles et prérequis sont complétés
    prerequisites_completed = True
    for indicator in indicators:
        if indicator.is_prerequisite and indicator.completion_status == 0:
            prerequisites_completed = False
            break
    
    # Si tous les prérequis sont complétés, on calcule les points par type
    if prerequisites_completed:
        for indicator in indicators:
            type_indicator = indicator.type_indicator
            points = indicator.calculate_points(nb_patients, nb_associates)
            points_by_type[type_indicator] += points
    
    return points_by_type

def calculate_associate_distribution(total_amount, associates, distribution_method="equal"):
    """
    Calcule la répartition du montant total entre les associés
    
    Args:
        total_amount (float): Montant total à répartir
        associates (list): Liste des associés
        distribution_method (str, optional): Méthode de répartition. Defaults to "equal".
        
    Returns:
        dict: Dictionnaire avec les montants par associé
    """
    distribution = {}
    
    if distribution_method == "equal":
        # Répartition égale entre tous les associés
        amount_per_associate = total_amount / len(associates)
        for associate in associates:
            distribution[associate.id] = amount_per_associate
    
    elif distribution_method == "presence_time":
        # Répartition au prorata du temps de présence
        total_presence_time = sum(associate.presence_time for associate in associates)
        for associate in associates:
            distribution[associate.id] = total_amount * (associate.presence_time / total_presence_time)
    
    elif distribution_method == "distribution_key":
        # Répartition selon la clé de répartition définie pour chaque associé
        total_distribution_key = sum(associate.distribution_key for associate in associates)
        for associate in associates:
            distribution[associate.id] = total_amount * (associate.distribution_key / total_distribution_key)
    
    elif distribution_method == "medical_only":
        # Répartition uniquement entre les professions médicales
        medical_associates = [a for a in associates if a.is_medical_profession()]
        if medical_associates:
            amount_per_associate = total_amount / len(medical_associates)
            for associate in associates:
                if associate.is_medical_profession():
                    distribution[associate.id] = amount_per_associate
                else:
                    distribution[associate.id] = 0
        else:
            # Si aucun associé médical, répartition égale
            amount_per_associate = total_amount / len(associates)
            for associate in associates:
                distribution[associate.id] = amount_per_associate
    
    elif distribution_method == "paramedical_only":
        # Répartition uniquement entre les professions paramédicales
        paramedical_associates = [a for a in associates if a.is_paramedical_profession()]
        if paramedical_associates:
            amount_per_associate = total_amount / len(paramedical_associates)
            for associate in associates:
                if associate.is_paramedical_profession():
                    distribution[associate.id] = amount_per_associate
                else:
                    distribution[associate.id] = 0
        else:
            # Si aucun associé paramédical, répartition égale
            amount_per_associate = total_amount / len(associates)
            for associate in associates:
                distribution[associate.id] = amount_per_associate
    
    else:
        # Méthode de répartition non reconnue, répartition égale
        amount_per_associate = total_amount / len(associates)
        for associate in associates:
            distribution[associate.id] = amount_per_associate
    
    return distribution

def calculate_expense_distribution(expense, associates):
    """
    Calcule la répartition d'une charge entre les associés
    
    Args:
        expense (Expense): Charge à répartir
        associates (list): Liste des associés
        
    Returns:
        dict: Dictionnaire avec les montants par associé
    """
    annual_amount = expense.get_annual_amount()
    return calculate_associate_distribution(annual_amount, associates, expense.distribution_method)

def calculate_total_expenses(expenses):
    """
    Calcule le montant total des charges
    
    Args:
        expenses (list): Liste des charges
        
    Returns:
        float: Montant total des charges
    """
    return sum(expense.get_annual_amount() for expense in expenses)

def calculate_net_amount(total_amount, total_expenses):
    """
    Calcule le montant net après déduction des charges
    
    Args:
        total_amount (float): Montant total des rémunérations
        total_expenses (float): Montant total des charges
        
    Returns:
        float: Montant net
    """
    return total_amount - total_expenses

def calculate_associate_net_amount(associate_id, associate_distribution, expense_distributions):
    """
    Calcule le montant net pour un associé après déduction des charges
    
    Args:
        associate_id (str): Identifiant de l'associé
        associate_distribution (dict): Répartition des rémunérations
        expense_distributions (list): Liste des répartitions des charges
        
    Returns:
        float: Montant net pour l'associé
    """
    # Montant brut pour l'associé
    gross_amount = associate_distribution.get(associate_id, 0)
    
    # Somme des charges pour l'associé
    total_expenses = 0
    for expense_distribution in expense_distributions:
        total_expenses += expense_distribution.get(associate_id, 0)
    
    # Montant net
    return gross_amount - total_expenses

def get_total_patients_mt(associates):
    """
    Calcule le nombre total de patients médecin traitant
    
    Args:
        associates (list): Liste des associés
        
    Returns:
        int: Nombre total de patients médecin traitant
    """
    return sum(associate.patients_mt for associate in associates if associate.is_doctor())

def get_total_medical_professions(associates):
    """
    Calcule le nombre total de professions médicales
    
    Args:
        associates (list): Liste des associés
        
    Returns:
        int: Nombre total de professions médicales
    """
    return sum(1 for associate in associates if associate.is_medical_profession())

def get_total_paramedical_professions(associates):
    """
    Calcule le nombre total de professions paramédicales
    
    Args:
        associates (list): Liste des associés
        
    Returns:
        int: Nombre total de professions paramédicales
    """
    return sum(1 for associate in associates if associate.is_paramedical_profession())

def get_unique_professions(associates):
    """
    Retourne la liste des professions uniques représentées par les associés
    
    Args:
        associates (list): Liste des associés
        
    Returns:
        list: Liste des professions uniques
    """
    return list(set(associate.profession for associate in associates))

def get_associates_by_profession(associates, profession):
    """
    Retourne la liste des associés exerçant une profession donnée
    
    Args:
        associates (list): Liste des associés
        profession (str): Profession recherchée
        
    Returns:
        list: Liste des associés exerçant la profession
    """
    return [associate for associate in associates if associate.profession == profession]

def get_associates_with_role(associates, role):
    """
    Retourne la liste des associés ayant un rôle donné
    
    Args:
        associates (list): Liste des associés
        role (str): Rôle recherché
        
    Returns:
        list: Liste des associés ayant le rôle
    """
    return [associate for associate in associates if role in associate.roles]

def has_ipa(associates):
    """
    Vérifie si au moins un associé est un infirmier en pratique avancée (IPA)
    
    Args:
        associates (list): Liste des associés
        
    Returns:
        bool: True si au moins un associé est un IPA, False sinon
    """
    return any(associate.profession == "Infirmier en pratique avancée (IPA)" for associate in associates)

def format_currency(amount):
    """
    Formate un montant en euros
    
    Args:
        amount (float): Montant à formater
        
    Returns:
        str: Montant formaté
    """
    return f"{amount:.2f} €"

def format_percentage(value):
    """
    Formate une valeur en pourcentage
    
    Args:
        value (float): Valeur à formater
        
    Returns:
        str: Valeur formatée
    """
    return f"{value * 100:.2f}%"
