"""
Utilitaires pour la gestion des données (sauvegarde et chargement)
"""

import json
import os
import pandas as pd
import streamlit as st
from datetime import datetime

from src.models.indicators import Indicator, get_indicators
from src.models.associates import Associate, get_sample_associates
from src.models.expenses import Expense, get_sample_expenses

# Dossier de sauvegarde des données
DATA_DIR = "data"

def ensure_data_dir():
    """
    S'assure que le dossier de données existe
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_indicators(indicators):
    """
    Sauvegarde les indicateurs dans un fichier JSON
    
    Args:
        indicators (list): Liste des indicateurs
    """
    ensure_data_dir()
    
    # Conversion des indicateurs en dictionnaires
    indicators_data = []
    for indicator in indicators:
        indicator_dict = {
            "id": indicator.id,
            "name": indicator.name,
            "description": indicator.description,
            "axis": indicator.axis,
            "type_indicator": indicator.type_indicator,
            "is_prerequisite": indicator.is_prerequisite,
            "points_fixed": indicator.points_fixed,
            "points_variable": indicator.points_variable,
            "reference_patients": indicator.reference_patients,
            "max_level": indicator.max_level,
            "completion_status": indicator.completion_status,
            "completion_percentage": indicator.completion_percentage
        }
        indicators_data.append(indicator_dict)
    
    # Sauvegarde dans un fichier JSON
    with open(os.path.join(DATA_DIR, "indicators.json"), "w", encoding="utf-8") as f:
        json.dump(indicators_data, f, ensure_ascii=False, indent=4)

def load_indicators():
    """
    Charge les indicateurs depuis un fichier JSON
    
    Returns:
        list: Liste des indicateurs
    """
    ensure_data_dir()
    
    # Vérification de l'existence du fichier
    if not os.path.exists(os.path.join(DATA_DIR, "indicators.json")):
        # Si le fichier n'existe pas, on retourne les indicateurs par défaut
        return get_indicators()
    
    # Chargement depuis le fichier JSON
    with open(os.path.join(DATA_DIR, "indicators.json"), "r", encoding="utf-8") as f:
        indicators_data = json.load(f)
    
    # Conversion des dictionnaires en objets Indicator
    indicators = []
    for indicator_dict in indicators_data:
        indicator = Indicator(
            id=indicator_dict["id"],
            name=indicator_dict["name"],
            description=indicator_dict["description"],
            axis=indicator_dict["axis"],
            type_indicator=indicator_dict["type_indicator"],
            is_prerequisite=indicator_dict["is_prerequisite"],
            points_fixed=indicator_dict["points_fixed"],
            points_variable=indicator_dict["points_variable"],
            reference_patients=indicator_dict["reference_patients"],
            max_level=indicator_dict["max_level"]
        )
        indicator.completion_status = indicator_dict["completion_status"]
        indicator.completion_percentage = indicator_dict["completion_percentage"]
        indicators.append(indicator)
    
    return indicators

def save_associates(associates):
    """
    Sauvegarde les associés dans un fichier JSON
    
    Args:
        associates (list): Liste des associés
    """
    ensure_data_dir()
    
    # Conversion des associés en dictionnaires
    associates_data = [associate.to_dict() for associate in associates]
    
    # Sauvegarde dans un fichier JSON
    with open(os.path.join(DATA_DIR, "associates.json"), "w", encoding="utf-8") as f:
        json.dump(associates_data, f, ensure_ascii=False, indent=4)

def load_associates():
    """
    Charge les associés depuis un fichier JSON
    
    Returns:
        list: Liste des associés
    """
    ensure_data_dir()
    
    # Vérification de l'existence du fichier
    if not os.path.exists(os.path.join(DATA_DIR, "associates.json")):
        # Si le fichier n'existe pas, on retourne les associés par défaut
        return get_sample_associates()
    
    # Chargement depuis le fichier JSON
    with open(os.path.join(DATA_DIR, "associates.json"), "r", encoding="utf-8") as f:
        associates_data = json.load(f)
    
    # Conversion des dictionnaires en objets Associate
    associates = [Associate.from_dict(associate_dict) for associate_dict in associates_data]
    
    return associates

def save_expenses(expenses):
    """
    Sauvegarde les charges dans un fichier JSON
    
    Args:
        expenses (list): Liste des charges
    """
    ensure_data_dir()
    
    # Conversion des charges en dictionnaires
    expenses_data = [expense.to_dict() for expense in expenses]
    
    # Sauvegarde dans un fichier JSON
    with open(os.path.join(DATA_DIR, "expenses.json"), "w", encoding="utf-8") as f:
        json.dump(expenses_data, f, ensure_ascii=False, indent=4)

def load_expenses():
    """
    Charge les charges depuis un fichier JSON
    
    Returns:
        list: Liste des charges
    """
    ensure_data_dir()
    
    # Vérification de l'existence du fichier
    if not os.path.exists(os.path.join(DATA_DIR, "expenses.json")):
        # Si le fichier n'existe pas, on retourne les charges par défaut
        return get_sample_expenses()
    
    # Chargement depuis le fichier JSON
    with open(os.path.join(DATA_DIR, "expenses.json"), "r", encoding="utf-8") as f:
        expenses_data = json.load(f)
    
    # Conversion des dictionnaires en objets Expense
    expenses = [Expense.from_dict(expense_dict) for expense_dict in expenses_data]
    
    return expenses

def export_to_excel(indicators, associates, expenses, filename=None):
    """
    Exporte les données dans un fichier Excel
    
    Args:
        indicators (list): Liste des indicateurs
        associates (list): Liste des associés
        expenses (list): Liste des charges
        filename (str, optional): Nom du fichier. Defaults to None.
        
    Returns:
        str: Chemin du fichier Excel
    """
    ensure_data_dir()
    
    # Génération du nom de fichier s'il n'est pas spécifié
    if filename is None:
        now = datetime.now()
        filename = f"export_sisa_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Chemin complet du fichier
    filepath = os.path.join(DATA_DIR, filename)
    
    # Création d'un writer Excel
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Feuille des indicateurs
        indicators_data = []
        for indicator in indicators:
            indicator_dict = {
                "ID": indicator.id,
                "Nom": indicator.name,
                "Description": indicator.description,
                "Axe": indicator.axis,
                "Type": indicator.type_indicator,
                "Prérequis": "Oui" if indicator.is_prerequisite else "Non",
                "Points fixes": indicator.points_fixed,
                "Points variables": indicator.points_variable,
                "Statut de complétion": indicator.completion_status,
                "Pourcentage de complétion": indicator.completion_percentage
            }
            indicators_data.append(indicator_dict)
        
        pd.DataFrame(indicators_data).to_excel(writer, sheet_name="Indicateurs", index=False)
        
        # Feuille des associés
        associates_data = []
        for associate in associates:
            associate_dict = {
                "ID": associate.id,
                "Prénom": associate.first_name,
                "Nom": associate.last_name,
                "Profession": associate.profession,
                "Spécialité": associate.speciality,
                "Date d'entrée": associate.entry_date,
                "Rôles": ", ".join(associate.roles),
                "Patients MT": associate.patients_mt,
                "Temps de présence": associate.presence_time,
                "Clé de répartition": associate.distribution_key,
                "Email": associate.email,
                "Téléphone": associate.phone,
                "RPPS": associate.rpps
            }
            associates_data.append(associate_dict)
        
        pd.DataFrame(associates_data).to_excel(writer, sheet_name="Associés", index=False)
        
        # Feuille des charges
        expenses_data = []
        for expense in expenses:
            expense_dict = {
                "ID": expense.id,
                "Nom": expense.name,
                "Description": expense.description,
                "Catégorie": expense.category,
                "Montant": expense.amount,
                "Fréquence": expense.frequency,
                "Date de début": expense.start_date,
                "Date de fin": expense.end_date,
                "Méthode de répartition": expense.distribution_method,
                "Montant annuel": expense.get_annual_amount(),
                "Montant mensuel": expense.get_monthly_amount()
            }
            expenses_data.append(expense_dict)
        
        pd.DataFrame(expenses_data).to_excel(writer, sheet_name="Charges", index=False)
    
    return filepath

def import_from_excel(filepath):
    """
    Importe les données depuis un fichier Excel
    
    Args:
        filepath (str): Chemin du fichier Excel
        
    Returns:
        tuple: Tuple contenant les listes d'indicateurs, d'associés et de charges
    """
    # Vérification de l'existence du fichier
    if not os.path.exists(filepath):
        st.error(f"Le fichier {filepath} n'existe pas.")
        return None, None, None
    
    try:
        # Lecture du fichier Excel
        indicators_df = pd.read_excel(filepath, sheet_name="Indicateurs")
        associates_df = pd.read_excel(filepath, sheet_name="Associés")
        expenses_df = pd.read_excel(filepath, sheet_name="Charges")
        
        # Conversion des DataFrames en objets
        indicators = []
        for _, row in indicators_df.iterrows():
            indicator = Indicator(
                id=row["ID"],
                name=row["Nom"],
                description=row["Description"],
                axis=row["Axe"],
                type_indicator=row["Type"],
                is_prerequisite=row["Prérequis"] == "Oui",
                points_fixed=row["Points fixes"],
                points_variable=row["Points variables"],
                reference_patients=4000,  # Valeur par défaut
                max_level=1  # Valeur par défaut
            )
            indicator.completion_status = row["Statut de complétion"]
            indicator.completion_percentage = row["Pourcentage de complétion"]
            indicators.append(indicator)
        
        associates = []
        for _, row in associates_df.iterrows():
            roles = row["Rôles"].split(", ") if isinstance(row["Rôles"], str) else []
            associate = Associate(
                id=row["ID"],
                first_name=row["Prénom"],
                last_name=row["Nom"],
                profession=row["Profession"],
                speciality=row["Spécialité"],
                entry_date=row["Date d'entrée"],
                roles=roles,
                patients_mt=row["Patients MT"],
                presence_time=row["Temps de présence"],
                distribution_key=row["Clé de répartition"],
                email=row["Email"],
                phone=row["Téléphone"],
                rpps=row["RPPS"]
            )
            associates.append(associate)
        
        expenses = []
        for _, row in expenses_df.iterrows():
            expense = Expense(
                id=row["ID"],
                name=row["Nom"],
                description=row["Description"],
                category=row["Catégorie"],
                amount=row["Montant"],
                frequency=row["Fréquence"],
                start_date=row["Date de début"],
                end_date=row["Date de fin"],
                distribution_method=row["Méthode de répartition"]
            )
            expenses.append(expense)
        
        return indicators, associates, expenses
    
    except Exception as e:
        st.error(f"Erreur lors de l'importation du fichier Excel : {str(e)}")
        return None, None, None

def initialize_session_state():
    """
    Initialise les données de session si elles n'existent pas
    """
    if 'indicators' not in st.session_state:
        st.session_state.indicators = load_indicators()
    
    if 'associates' not in st.session_state:
        st.session_state.associates = load_associates()
    
    if 'expenses' not in st.session_state:
        st.session_state.expenses = load_expenses()
