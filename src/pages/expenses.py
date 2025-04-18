import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
from datetime import datetime

from src.models.expenses import (
    Expense, get_expense_categories, get_expense_frequencies,
    get_distribution_methods, get_sample_expenses
)
from src.utils.data_manager import save_expenses
from src.utils.calculations import (
    calculate_total_expenses, calculate_expense_distribution,
    format_currency
)

def show():
    """
    Affiche la page de gestion des charges fixes
    """
    st.markdown("<h1 class='main-header'>Gestion des Charges Fixes</h1>", unsafe_allow_html=True)
    
    # Initialisation des charges s'ils n'existent pas dans la session
    if 'expenses' not in st.session_state:
        st.session_state.expenses = get_sample_expenses()
    
    # Initialisation des associés s'ils n'existent pas dans la session
    if 'associates' not in st.session_state:
        st.session_state.associates = []
    
    # Récupération des charges et des associés
    expenses = st.session_state.expenses
    associates = st.session_state.associates
    
    # Onglets pour les différentes fonctionnalités
    tab1, tab2, tab3 = st.tabs(["Liste des charges", "Ajouter/Modifier une charge", "Répartition des charges"])
    
    with tab1:
        display_expenses_list(expenses)
    
    with tab2:
        add_edit_expense(expenses)
    
    with tab3:
        display_expense_distribution(expenses, associates)
    
    # Bouton pour sauvegarder les modifications
    if st.button("Sauvegarder les modifications"):
        save_expenses(expenses)
        st.success("Les modifications ont été sauvegardées avec succès.")

def display_expenses_list(expenses):
    """
    Affiche la liste des charges
    """
    st.markdown("<h2 class='sub-header'>Liste des charges</h2>", unsafe_allow_html=True)
    
    # Filtres
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtre par catégorie
        categories = ["Toutes"] + get_expense_categories()
        selected_category = st.selectbox("Filtrer par catégorie", categories)
    
    with col2:
        # Filtre par fréquence
        frequencies = ["Toutes"] + get_expense_frequencies()
        selected_frequency = st.selectbox("Filtrer par fréquence", frequencies)
    
    # Filtrage des charges
    filtered_expenses = expenses
    
    if selected_category != "Toutes":
        filtered_expenses = [e for e in filtered_expenses if e.category == selected_category]
    
    if selected_frequency != "Toutes":
        filtered_expenses = [e for e in filtered_expenses if e.frequency == selected_frequency]
    
    # Affichage des charges
    if not filtered_expenses:
        st.info("Aucune charge ne correspond aux critères de filtrage.")
    else:
        # Création d'un DataFrame pour l'affichage
        expenses_data = []
        for expense in filtered_expenses:
            expenses_data.append({
                "ID": expense.id,
                "Nom": expense.name,
                "Catégorie": expense.category,
                "Montant": expense.amount,
                "Fréquence": expense.frequency,
                "Montant annuel": expense.get_annual_amount(),
                "Montant mensuel": expense.get_monthly_amount(),
                "Méthode de répartition": expense.distribution_method
            })
        
        df = pd.DataFrame(expenses_data)
        
        # Formatage des colonnes monétaires
        df["Montant"] = df["Montant"].apply(format_currency)
        df["Montant annuel"] = df["Montant annuel"].apply(format_currency)
        df["Montant mensuel"] = df["Montant mensuel"].apply(format_currency)
        
        # Affichage du DataFrame
        st.dataframe(df, use_container_width=True)
        
        # Sélection d'une charge pour modification ou suppression
        selected_expense_id = st.selectbox(
            "Sélectionner une charge pour modification ou suppression",
            options=[e.id for e in filtered_expenses],
            format_func=lambda x: next((e.name + " - " + e.category) for e in filtered_expenses if e.id == x)
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Modifier la charge sélectionnée"):
                st.session_state.edit_expense_id = selected_expense_id
                st.session_state.active_tab = "Ajouter/Modifier une charge"
                st.rerun()
        
        with col2:
            if st.button("Supprimer la charge sélectionnée"):
                # Confirmation de suppression
                if st.checkbox("Confirmer la suppression"):
                    # Suppression de la charge
                    st.session_state.expenses = [e for e in st.session_state.expenses if e.id != selected_expense_id]
                    st.success("La charge a été supprimée avec succès.")
                    st.rerun()

def add_edit_expense(expenses):
    """
    Ajoute ou modifie une charge
    """
    st.markdown("<h2 class='sub-header'>Ajouter/Modifier une charge</h2>", unsafe_allow_html=True)
    
    # Vérification si on est en mode édition
    edit_mode = 'edit_expense_id' in st.session_state
    
    # Récupération de la charge à éditer si on est en mode édition
    expense_to_edit = None
    if edit_mode:
        expense_to_edit = next((e for e in expenses if e.id == st.session_state.edit_expense_id), None)
        
        if expense_to_edit:
            st.markdown(f"<h3 class='blue-text'>Modification de la charge : {expense_to_edit.name}</h3>", unsafe_allow_html=True)
        else:
            st.error("La charge à modifier n'a pas été trouvée.")
            edit_mode = False
    else:
        st.markdown("<h3 class='blue-text'>Ajout d'une nouvelle charge</h3>", unsafe_allow_html=True)
    
    # Formulaire d'ajout/modification
    with st.form("expense_form"):
        # Informations générales
        st.markdown("<h4>Informations générales</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Nom",
                value=expense_to_edit.name if edit_mode else ""
            )
        
        with col2:
            category = st.selectbox(
                "Catégorie",
                options=get_expense_categories(),
                index=get_expense_categories().index(expense_to_edit.category) if edit_mode and expense_to_edit.category in get_expense_categories() else 0
            )
        
        description = st.text_area(
            "Description",
            value=expense_to_edit.description if edit_mode else ""
        )
        
        # Informations financières
        st.markdown("<h4>Informations financières</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input(
                "Montant (€)",
                min_value=0.0,
                value=expense_to_edit.amount if edit_mode else 0.0,
                step=100.0
            )
        
        with col2:
            frequency = st.selectbox(
                "Fréquence",
                options=get_expense_frequencies(),
                index=get_expense_frequencies().index(expense_to_edit.frequency) if edit_mode and expense_to_edit.frequency in get_expense_frequencies() else 0
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Date de début",
                value=datetime.strptime(expense_to_edit.start_date, "%Y-%m-%d").date() if edit_mode and expense_to_edit.start_date else datetime.now().date()
            )
        
        with col2:
            end_date = st.date_input(
                "Date de fin (optionnelle)",
                value=datetime.strptime(expense_to_edit.end_date, "%Y-%m-%d").date() if edit_mode and expense_to_edit.end_date else None
            )
        
        # Méthode de répartition
        st.markdown("<h4>Méthode de répartition</h4>", unsafe_allow_html=True)
        
        distribution_methods_dict = {
            "equal": "Répartition égale entre tous les associés",
            "presence_time": "Répartition au prorata du temps de présence",
            "distribution_key": "Répartition selon la clé de répartition définie pour chaque associé",
            "medical_only": "Répartition uniquement entre les professions médicales",
            "paramedical_only": "Répartition uniquement entre les professions paramédicales",
            "custom": "Répartition personnalisée"
        }
        
        distribution_method = st.selectbox(
            "Méthode de répartition",
            options=list(distribution_methods_dict.keys()),
            format_func=lambda x: distribution_methods_dict[x],
            index=list(distribution_methods_dict.keys()).index(expense_to_edit.distribution_method) if edit_mode and expense_to_edit.distribution_method in distribution_methods_dict else 0
        )
        
        # Boutons de soumission
        submit_button = st.form_submit_button("Enregistrer")
        
        if submit_button:
            # Validation des champs obligatoires
            if not name or amount <= 0:
                st.error("Les champs Nom et Montant sont obligatoires et le montant doit être supérieur à 0.")
            else:
                # Création ou mise à jour de la charge
                if edit_mode:
                    # Mise à jour de la charge existante
                    expense_to_edit.name = name
                    expense_to_edit.description = description
                    expense_to_edit.category = category
                    expense_to_edit.amount = amount
                    expense_to_edit.frequency = frequency
                    expense_to_edit.start_date = start_date.strftime("%Y-%m-%d")
                    expense_to_edit.end_date = end_date.strftime("%Y-%m-%d") if end_date else None
                    expense_to_edit.distribution_method = distribution_method
                    
                    st.success("La charge a été modifiée avec succès.")
                    
                    # Réinitialisation du mode édition
                    if 'edit_expense_id' in st.session_state:
                        del st.session_state.edit_expense_id
                else:
                    # Création d'une nouvelle charge
                    new_expense = Expense(
                        id=str(uuid.uuid4()),
                        name=name,
                        description=description,
                        category=category,
                        amount=amount,
                        frequency=frequency,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d") if end_date else None,
                        distribution_method=distribution_method
                    )
                    
                    # Ajout de la charge à la liste
                    st.session_state.expenses.append(new_expense)
                    
                    st.success("La charge a été ajoutée avec succès.")
                
                # Rechargement de la page
                st.rerun()
    
    # Bouton pour annuler l'édition
    if edit_mode:
        if st.button("Annuler la modification"):
            # Réinitialisation du mode édition
            if 'edit_expense_id' in st.session_state:
                del st.session_state.edit_expense_id
            
            st.rerun()

def display_expense_distribution(expenses, associates):
    """
    Affiche la répartition des charges entre les associés
    """
    st.markdown("<h2 class='sub-header'>Répartition des charges</h2>", unsafe_allow_html=True)
    
    if not expenses:
        st.info("Aucune charge n'a été ajoutée.")
        return
    
    if not associates:
        st.info("Aucun associé n'a été ajouté. Veuillez ajouter des associés pour visualiser la répartition des charges.")
        return
    
    # Calcul du montant total des charges
    total_expenses_amount = calculate_total_expenses(expenses)
    
    # Affichage du montant total des charges
    st.markdown(f"<h3 class='blue-text'>Montant total des charges : {format_currency(total_expenses_amount)}</h3>", unsafe_allow_html=True)
    
    # Calcul de la répartition des charges par catégorie
    expenses_by_category = {}
    for expense in expenses:
        if expense.category not in expenses_by_category:
            expenses_by_category[expense.category] = 0
        expenses_by_category[expense.category] += expense.get_annual_amount()
    
    # Graphique de répartition des charges par catégorie
    st.markdown("<h3 class='blue-text'>Répartition des charges par catégorie</h3>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tri des catégories par montant
    sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
    categories = [c[0] for c in sorted_categories]
    amounts = [c[1] for c in sorted_categories]
    
    # Création du graphique
    bars = ax.bar(categories, amounts, color="#1E88E5")
    
    # Rotation des étiquettes pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, format_currency(height), ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Graphique de répartition des charges par fréquence
    st.markdown("<h3 class='blue-text'>Répartition des charges par fréquence</h3>", unsafe_allow_html=True)
    
    # Calcul de la répartition des charges par fréquence
    expenses_by_frequency = {}
    for expense in expenses:
        if expense.frequency not in expenses_by_frequency:
            expenses_by_frequency[expense.frequency] = 0
        expenses_by_frequency[expense.frequency] += expense.get_annual_amount()
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Tri des fréquences par montant
    sorted_frequencies = sorted(expenses_by_frequency.items(), key=lambda x: x[1], reverse=True)
    frequencies = [f[0] for f in sorted_frequencies]
    amounts = [f[1] for f in sorted_frequencies]
    
    # Création du graphique
    ax.pie(amounts, labels=frequencies, autopct='%1.1f%%', startangle=90, colors=["#1E88E5", "#42A5F5", "#90CAF9", "#BBDEFB"])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Répartition des charges par fréquence")
    
    st.pyplot(fig)
    
    # Répartition des charges par associé
    st.markdown("<h3 class='blue-text'>Répartition des charges par associé</h3>", unsafe_allow_html=True)
    
    # Calcul de la répartition des charges par associé
    expense_distributions = []
    for expense in expenses:
        expense_distributions.append(calculate_expense_distribution(expense, associates))
    
    # Calcul du montant total par associé
    total_by_associate = {}
    for associate in associates:
        total_by_associate[associate.id] = 0
        for distribution in expense_distributions:
            total_by_associate[associate.id] += distribution.get(associate.id, 0)
    
    # Création d'un DataFrame pour l'affichage
    associates_data = []
    for associate in associates:
        associates_data.append({
            "Nom": associate.last_name,
            "Prénom": associate.first_name,
            "Profession": associate.profession,
            "Montant des charges": total_by_associate[associate.id],
            "Pourcentage": total_by_associate[associate.id] / total_expenses_amount * 100 if total_expenses_amount > 0 else 0
        })
    
    df = pd.DataFrame(associates_data)
    
    # Tri du DataFrame par montant des charges
    df = df.sort_values(by="Montant des charges", ascending=False)
    
    # Formatage des colonnes
    df["Montant des charges"] = df["Montant des charges"].apply(format_currency)
    df["Pourcentage"] = df["Pourcentage"].apply(lambda x: f"{x:.2f}%")
    
    # Affichage du DataFrame
    st.dataframe(df, use_container_width=True)
    
    # Graphique de répartition des charges par associé
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Création du graphique
    associate_names = [f"{a['Prénom']} {a['Nom']}" for _, a in df.iterrows()]
    amounts = [float(a["Montant des charges"].replace(" €", "").replace(",", ".")) for _, a in df.iterrows()]
    
    bars = ax.bar(associate_names, amounts, color="#1E88E5")
    
    # Rotation des étiquettes pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, format_currency(height), ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
