import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from src.utils.calculations import (
    calculate_total_points, calculate_total_amount, calculate_points_by_axis,
    calculate_points_by_type, calculate_total_expenses, calculate_net_amount,
    calculate_associate_distribution, calculate_expense_distribution,
    calculate_associate_net_amount, format_currency, format_percentage,
    get_total_patients_mt, has_ipa
)
from src.utils.data_manager import export_to_excel, initialize_session_state

def show():
    """
    Affiche le tableau de bord
    """
    st.markdown("<h1 class='main-header'>Tableau de Bord</h1>", unsafe_allow_html=True)
    
    # Initialisation des données de session
    initialize_session_state()
    
    # Récupération des données
    indicators = st.session_state.indicators
    associates = st.session_state.associates
    expenses = st.session_state.expenses
    
    # Onglets pour les différentes fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["Synthèse", "Rémunération par associé", "Simulation", "Export"])
    
    with tab1:
        display_summary(indicators, associates, expenses)
    
    with tab2:
        display_associate_distribution(indicators, associates, expenses)
    
    with tab3:
        display_simulation(indicators, associates, expenses)
    
    with tab4:
        display_export(indicators, associates, expenses)

def display_summary(indicators, associates, expenses):
    """
    Affiche une synthèse des rémunérations et des charges
    """
    st.markdown("<h2 class='sub-header'>Synthèse</h2>", unsafe_allow_html=True)
    
    # Calcul du nombre total de patients médecin traitant
    nb_patients = get_total_patients_mt(associates)
    
    # Vérification de la présence d'un IPA
    has_ipa_in_structure = has_ipa(associates)
    
    # Calcul des points et du montant total
    total_points = calculate_total_points(indicators, nb_patients, len(associates))
    total_amount = calculate_total_amount(indicators, nb_patients, len(associates))
    
    # Calcul des points par axe et par type
    points_by_axis = calculate_points_by_axis(indicators, nb_patients, len(associates))
    points_by_type = calculate_points_by_type(indicators, nb_patients, len(associates))
    
    # Calcul du montant total des charges
    total_expenses_amount = calculate_total_expenses(expenses)
    
    # Calcul du montant net
    net_amount = calculate_net_amount(total_amount, total_expenses_amount)
    
    # Affichage des informations générales
    st.markdown("<h3 class='blue-text'>Informations générales</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nombre d'associés", len(associates))
    
    with col2:
        st.metric("Patients médecin traitant", nb_patients)
    
    with col3:
        st.metric("Présence d'un IPA", "Oui" if has_ipa_in_structure else "Non")
    
    # Affichage des résultats financiers
    st.markdown("<h3 class='blue-text'>Résultats financiers</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rémunération ACI", format_currency(total_amount))
    
    with col2:
        st.metric("Charges totales", format_currency(total_expenses_amount))
    
    with col3:
        st.metric("Montant net", format_currency(net_amount))
    
    # Graphique de répartition des points par axe
    st.markdown("<h3 class='blue-text'>Répartition des points par axe</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        axes = ["Axe 1 - Accès aux soins", "Axe 2 - Travail en équipe", "Axe 3 - Système d'information"]
        values = [points_by_axis[1], points_by_axis[2], points_by_axis[3]]
        colors = ["#1E88E5", "#42A5F5", "#90CAF9"]
        
        ax.bar(axes, values, color=colors)
        ax.set_title("Répartition des points par axe")
        ax.set_ylabel("Points")
        
        # Ajout des valeurs sur les barres
        for i, v in enumerate(values):
            ax.text(i, v + 5, str(int(v)), ha='center')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Graphique de répartition des points par type
        fig, ax = plt.subplots(figsize=(6, 4))
        types = ["Indicateurs socles", "Indicateurs optionnels"]
        values = [points_by_type["socle"], points_by_type["optionnel"]]
        colors = ["#1E88E5", "#42A5F5"]
        
        # Vérification que les valeurs ne sont pas NaN
        if not np.isnan(values).any() and sum(values) > 0:
            ax.pie(values, labels=types, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title("Répartition des points par type d'indicateur")
        else:
            ax.text(0.5, 0.5, "Données insuffisantes pour afficher le graphique", 
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.axis('off')
        
        st.pyplot(fig)
    
    # Graphique de répartition des charges par catégorie
    st.markdown("<h3 class='blue-text'>Répartition des charges par catégorie</h3>", unsafe_allow_html=True)
    
    if expenses:
        # Calcul de la répartition des charges par catégorie
        expenses_by_category = {}
        for expense in expenses:
            if expense.category not in expenses_by_category:
                expenses_by_category[expense.category] = 0
            expenses_by_category[expense.category] += expense.get_annual_amount()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
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
    else:
        st.info("Aucune charge n'a été ajoutée.")

def display_associate_distribution(indicators, associates, expenses):
    """
    Affiche la répartition des rémunérations par associé
    """
    st.markdown("<h2 class='sub-header'>Rémunération par associé</h2>", unsafe_allow_html=True)
    
    if not associates:
        st.info("Aucun associé n'a été ajouté.")
        return
    
    # Calcul du nombre total de patients médecin traitant
    nb_patients = get_total_patients_mt(associates)
    
    # Calcul des points et du montant total
    total_points = calculate_total_points(indicators, nb_patients, len(associates))
    total_amount = calculate_total_amount(indicators, nb_patients, len(associates))
    
    # Calcul du montant total des charges
    total_expenses_amount = calculate_total_expenses(expenses)
    
    # Calcul de la répartition des rémunérations par associé
    distribution_method = st.selectbox(
        "Méthode de répartition des rémunérations",
        options=["equal", "presence_time", "distribution_key"],
        format_func=lambda x: {
            "equal": "Répartition égale entre tous les associés",
            "presence_time": "Répartition au prorata du temps de présence",
            "distribution_key": "Répartition selon la clé de répartition définie pour chaque associé"
        }[x]
    )
    
    associate_distribution = calculate_associate_distribution(total_amount, associates, distribution_method)
    
    # Calcul de la répartition des charges par associé
    expense_distributions = []
    for expense in expenses:
        expense_distributions.append(calculate_expense_distribution(expense, associates))
    
    # Calcul du montant net par associé
    associate_net_amounts = {}
    for associate in associates:
        associate_net_amounts[associate.id] = calculate_associate_net_amount(
            associate.id, associate_distribution, expense_distributions
        )
    
    # Création d'un DataFrame pour l'affichage
    associates_data = []
    for associate in associates:
        associates_data.append({
            "Nom": associate.last_name,
            "Prénom": associate.first_name,
            "Profession": associate.profession,
            "Rémunération brute": associate_distribution[associate.id],
            "Charges": associate_distribution[associate.id] - associate_net_amounts[associate.id],
            "Rémunération nette": associate_net_amounts[associate.id],
            "Pourcentage": associate_distribution[associate.id] / total_amount * 100 if total_amount > 0 else 0
        })
    
    df = pd.DataFrame(associates_data)
    
    # Tri du DataFrame par rémunération brute
    df = df.sort_values(by="Rémunération brute", ascending=False)
    
    # Formatage des colonnes
    df["Rémunération brute"] = df["Rémunération brute"].apply(format_currency)
    df["Charges"] = df["Charges"].apply(format_currency)
    df["Rémunération nette"] = df["Rémunération nette"].apply(format_currency)
    df["Pourcentage"] = df["Pourcentage"].apply(lambda x: f"{x:.2f}%")
    
    # Affichage du DataFrame
    st.dataframe(df, use_container_width=True)
    
    # Graphique de répartition des rémunérations par associé
    st.markdown("<h3 class='blue-text'>Répartition des rémunérations par associé</h3>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Création du graphique
    associate_names = [f"{a['Prénom']} {a['Nom']}" for _, a in df.iterrows()]
    amounts = [float(a["Rémunération brute"].replace(" €", "").replace(",", ".")) for _, a in df.iterrows()]
    
    bars = ax.bar(associate_names, amounts, color="#1E88E5")
    
    # Rotation des étiquettes pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, format_currency(height), ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Graphique de répartition des rémunérations nettes par associé
    st.markdown("<h3 class='blue-text'>Répartition des rémunérations nettes par associé</h3>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Création du graphique
    associate_names = [f"{a['Prénom']} {a['Nom']}" for _, a in df.iterrows()]
    amounts = [float(a["Rémunération nette"].replace(" €", "").replace(",", ".")) for _, a in df.iterrows()]
    
    bars = ax.bar(associate_names, amounts, color="#42A5F5")
    
    # Rotation des étiquettes pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, format_currency(height), ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)

def display_simulation(indicators, associates, expenses):
    """
    Affiche une simulation interactive
    """
    st.markdown("<h2 class='sub-header'>Simulation</h2>", unsafe_allow_html=True)
    
    if not associates:
        st.info("Aucun associé n'a été ajouté.")
        return
    
    # Calcul du nombre total de patients médecin traitant
    nb_patients = get_total_patients_mt(associates)
    
    # Vérification de la présence d'un IPA
    has_ipa_in_structure = has_ipa(associates)
    
    # Paramètres de simulation
    st.markdown("<h3 class='blue-text'>Paramètres de simulation</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sim_nb_patients = st.number_input("Nombre de patients médecin traitant", min_value=0, value=nb_patients, step=100)
    
    with col2:
        sim_has_ipa = st.checkbox("Présence d'un IPA", value=has_ipa_in_structure)
    
    # Simulation des indicateurs
    st.markdown("<h3 class='blue-text'>Simulation des indicateurs</h3>", unsafe_allow_html=True)
    
    # Création d'une copie des indicateurs pour la simulation
    sim_indicators = []
    for indicator in indicators:
        sim_indicator = type('', (), {})()
        for attr in dir(indicator):
            if not attr.startswith('__') and not callable(getattr(indicator, attr)):
                setattr(sim_indicator, attr, getattr(indicator, attr))
        sim_indicators.append(sim_indicator)
    
    # Affichage des indicateurs pour simulation
    for i, indicator in enumerate(sim_indicators):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{indicator.id} - {indicator.name}**")
        
        with col2:
            if indicator.max_level > 1:
                # Indicateur avec plusieurs niveaux
                indicator.completion_status = st.selectbox(
                    f"Niveau de complétion",
                    options=list(range(indicator.max_level + 1)),
                    index=indicator.completion_status,
                    key=f"sim_completion_status_{i}",
                    format_func=lambda x: f"Niveau {x}" if x > 0 else "Non complété"
                )
            else:
                # Indicateur avec un seul niveau
                indicator.completion_status = 1 if st.checkbox(
                    f"Complété",
                    value=indicator.completion_status == 1,
                    key=f"sim_completion_status_{i}"
                ) else 0
            
            # Pour les indicateurs avec pourcentage de complétion
            if indicator.points_variable > 0 and indicator.completion_status > 0:
                indicator.completion_percentage = st.slider(
                    f"Pourcentage",
                    min_value=0,
                    max_value=100,
                    value=indicator.completion_percentage,
                    key=f"sim_completion_percentage_{i}"
                )
    
    # Calcul des résultats de la simulation
    sim_total_points = calculate_total_points(sim_indicators, sim_nb_patients, len(associates))
    sim_total_amount = calculate_total_amount(sim_indicators, sim_nb_patients, len(associates))
    
    # Calcul des points par axe et par type
    sim_points_by_axis = calculate_points_by_axis(sim_indicators, sim_nb_patients, len(associates))
    sim_points_by_type = calculate_points_by_type(sim_indicators, sim_nb_patients, len(associates))
    
    # Calcul du montant total des charges
    total_expenses_amount = calculate_total_expenses(expenses)
    
    # Calcul du montant net
    sim_net_amount = calculate_net_amount(sim_total_amount, total_expenses_amount)
    
    # Affichage des résultats de la simulation
    st.markdown("<h3 class='blue-text'>Résultats de la simulation</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Points totaux", int(sim_total_points))
    
    with col2:
        st.metric("Rémunération totale", format_currency(sim_total_amount))
    
    with col3:
        st.metric("Montant net", format_currency(sim_net_amount))
    
    # Graphique de répartition des points par axe
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        axes = ["Axe 1 - Accès aux soins", "Axe 2 - Travail en équipe", "Axe 3 - Système d'information"]
        values = [sim_points_by_axis[1], sim_points_by_axis[2], sim_points_by_axis[3]]
        colors = ["#1E88E5", "#42A5F5", "#90CAF9"]
        
        ax.bar(axes, values, color=colors)
        ax.set_title("Répartition des points par axe")
        ax.set_ylabel("Points")
        
        # Ajout des valeurs sur les barres
        for i, v in enumerate(values):
            ax.text(i, v + 5, str(int(v)), ha='center')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Graphique de répartition des points par type
        fig, ax = plt.subplots(figsize=(6, 4))
        types = ["Indicateurs socles", "Indicateurs optionnels"]
        values = [sim_points_by_type["socle"], sim_points_by_type["optionnel"]]
        colors = ["#1E88E5", "#42A5F5"]
        
        # Vérification que les valeurs ne sont pas NaN
        if not np.isnan(values).any() and sum(values) > 0:
            ax.pie(values, labels=types, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title("Répartition des points par type d'indicateur")
        else:
            ax.text(0.5, 0.5, "Données insuffisantes pour afficher le graphique", 
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.axis('off')
        
        st.pyplot(fig)

def display_export(indicators, associates, expenses):
    """
    Affiche les options d'export
    """
    st.markdown("<h2 class='sub-header'>Export des données</h2>", unsafe_allow_html=True)
    
    # Export au format Excel
    st.markdown("<h3 class='blue-text'>Export au format Excel</h3>", unsafe_allow_html=True)
    
    if st.button("Exporter les données au format Excel"):
        try:
            # Export des données
            filename = f"export_sisa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = export_to_excel(indicators, associates, expenses, filename)
            
            # Affichage du message de succès
            st.success(f"Les données ont été exportées avec succès dans le fichier {filepath}.")
            
            # Bouton de téléchargement
            with open(filepath, "rb") as file:
                st.download_button(
                    label="Télécharger le fichier Excel",
                    data=file,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Une erreur s'est produite lors de l'export des données : {str(e)}")
    
    # Génération de rapports
    st.markdown("<h3 class='blue-text'>Génération de rapports</h3>", unsafe_allow_html=True)
    
    report_type = st.selectbox(
        "Type de rapport",
        options=["Synthèse globale", "Répartition par associé", "Détail des indicateurs", "Détail des charges"]
    )
    
    if st.button("Générer le rapport"):
        st.info("Fonctionnalité en cours de développement.")
