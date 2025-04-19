import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.calculations import (
    calculate_total_points, calculate_total_amount, calculate_points_by_axis,
    calculate_points_by_type, format_currency, has_ipa
)
from src.utils.data_manager import save_indicators
from src.models.indicators import get_indicators
from src.data.indicator_details import indicator_details

def show():
    """
    Affiche la page de gestion des indicateurs ACI
    """
    st.markdown("<h1 class='main-header'>Gestion des Indicateurs ACI</h1>", unsafe_allow_html=True)
    
    # Initialisation des indicateurs s'ils n'existent pas dans la session
    if 'indicators' not in st.session_state:
        st.session_state.indicators = get_indicators()
    
    # Initialisation des associés s'ils n'existent pas dans la session
    if 'associates' not in st.session_state:
        st.session_state.associates = []
    
    # Récupération des indicateurs et des associés
    indicators = st.session_state.indicators
    associates = st.session_state.associates
    
    # Calcul du nombre total de patients médecin traitant
    nb_patients = sum(associate.patients_mt for associate in associates if associate.profession.lower().startswith("médecin"))
    
    # Vérification de la présence d'un IPA
    has_ipa_in_structure = has_ipa(associates)
    
    # Affichage du nombre de patients et de la présence d'un IPA
    col1, col2 = st.columns(2)
    with col1:
        nb_patients = st.number_input("Nombre total de patients médecin traitant", min_value=0, value=nb_patients, step=100)
    
    with col2:
        has_ipa_in_structure = st.checkbox("Présence d'un Infirmier en Pratique Avancée (IPA)", value=has_ipa_in_structure)
    
    # Onglets pour les différents axes
    tab1, tab2, tab3, tab4 = st.tabs(["Tous les indicateurs", "Axe 1 - Accès aux soins", "Axe 2 - Travail en équipe", "Axe 3 - Système d'information"])
    
    with tab1:
        display_all_indicators(indicators, nb_patients, has_ipa_in_structure)
    
    with tab2:
        display_axis_indicators(indicators, 1, nb_patients, has_ipa_in_structure)
    
    with tab3:
        display_axis_indicators(indicators, 2, nb_patients, has_ipa_in_structure)
    
    with tab4:
        display_axis_indicators(indicators, 3, nb_patients, has_ipa_in_structure)
    
    # Affichage des résultats
    st.markdown("---")
    st.markdown("<h2 class='sub-header'>Résultats</h2>", unsafe_allow_html=True)
    
    # Calcul des points et du montant total
    total_points = calculate_total_points(indicators, nb_patients, len(associates))
    total_amount = calculate_total_amount(indicators, nb_patients, len(associates))
    
    # Calcul des points par axe et par type
    points_by_axis = calculate_points_by_axis(indicators, nb_patients, len(associates))
    points_by_type = calculate_points_by_type(indicators, nb_patients, len(associates))
    
    # Affichage des résultats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>Points et rémunération</h3>
            <p>Total des points : <strong>{}</strong></p>
            <p>Montant total : <strong>{}</strong></p>
        </div>
        """.format(int(total_points), format_currency(total_amount)), unsafe_allow_html=True)
        
        # Graphique de répartition des points par axe
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
        
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>Répartition des points</h3>
            <p>Axe 1 - Accès aux soins : <strong>{} points</strong></p>
            <p>Axe 2 - Travail en équipe : <strong>{} points</strong></p>
            <p>Axe 3 - Système d'information : <strong>{} points</strong></p>
            <p>Indicateurs socles : <strong>{} points</strong></p>
            <p>Indicateurs optionnels : <strong>{} points</strong></p>
        </div>
        """.format(
            int(points_by_axis[1]), 
            int(points_by_axis[2]), 
            int(points_by_axis[3]),
            int(points_by_type["socle"]),
            int(points_by_type["optionnel"])
        ), unsafe_allow_html=True)
        
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
    
    # Bouton pour sauvegarder les modifications
    if st.button("Sauvegarder les modifications"):
        save_indicators(indicators)
        st.success("Les modifications ont été sauvegardées avec succès.")

def display_all_indicators(indicators, nb_patients, has_ipa_in_structure):
    """
    Affiche tous les indicateurs
    """
    st.markdown("<h2 class='sub-header'>Tous les indicateurs</h2>", unsafe_allow_html=True)
    
    # Affichage des indicateurs socles et prérequis
    st.markdown("<h3 class='blue-text'>Indicateurs socles et prérequis</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs socles et prérequis
    socle_indicators = [indicator for indicator in indicators if indicator.type_indicator == "socle" and indicator.is_prerequisite]
    
    # Affichage des indicateurs socles et prérequis
    for indicator in socle_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab="all")
    
    # Affichage des indicateurs socles non prérequis
    st.markdown("<h3 class='blue-text'>Indicateurs socles</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs socles non prérequis
    socle_non_prerequisite_indicators = [indicator for indicator in indicators if indicator.type_indicator == "socle" and not indicator.is_prerequisite]
    
    # Affichage des indicateurs socles non prérequis
    for indicator in socle_non_prerequisite_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab="all")
    
    # Affichage des indicateurs optionnels
    st.markdown("<h3 class='blue-text'>Indicateurs optionnels</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs optionnels
    optional_indicators = [indicator for indicator in indicators if indicator.type_indicator == "optionnel"]
    
    # Affichage des indicateurs optionnels
    for indicator in optional_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab="all")

def display_axis_indicators(indicators, axis, nb_patients, has_ipa_in_structure):
    """
    Affiche les indicateurs d'un axe spécifique
    """
    axis_names = {
        1: "Axe 1 - Accès aux soins",
        2: "Axe 2 - Travail en équipe",
        3: "Axe 3 - Système d'information"
    }
    
    st.markdown(f"<h2 class='sub-header'>{axis_names[axis]}</h2>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs de l'axe
    axis_indicators = [indicator for indicator in indicators if indicator.axis == axis]
    
    # Affichage des indicateurs socles et prérequis
    st.markdown("<h3 class='blue-text'>Indicateurs socles et prérequis</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs socles et prérequis de l'axe
    socle_indicators = [indicator for indicator in axis_indicators if indicator.type_indicator == "socle" and indicator.is_prerequisite]
    
    # Affichage des indicateurs socles et prérequis
    for indicator in socle_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab=f"axe{axis}")
    
    # Affichage des indicateurs socles non prérequis
    st.markdown("<h3 class='blue-text'>Indicateurs socles</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs socles non prérequis de l'axe
    socle_non_prerequisite_indicators = [indicator for indicator in axis_indicators if indicator.type_indicator == "socle" and not indicator.is_prerequisite]
    
    # Affichage des indicateurs socles non prérequis
    for indicator in socle_non_prerequisite_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab=f"axe{axis}")
    
    # Affichage des indicateurs optionnels
    st.markdown("<h3 class='blue-text'>Indicateurs optionnels</h3>", unsafe_allow_html=True)
    
    # Filtrage des indicateurs optionnels de l'axe
    optional_indicators = [indicator for indicator in axis_indicators if indicator.type_indicator == "optionnel"]
    
    # Affichage des indicateurs optionnels
    for indicator in optional_indicators:
        display_indicator(indicator, nb_patients, has_ipa_in_structure, tab=f"axe{axis}")

def display_indicator(indicator, nb_patients, has_ipa_in_structure, tab="all"):
    """
    Affiche un indicateur avec ses contrôles
    
    Args:
        indicator: L'indicateur à afficher
        nb_patients: Le nombre de patients médecin traitant
        has_ipa_in_structure: Indique si la structure a un IPA
        tab: L'onglet dans lequel l'indicateur est affiché (pour éviter les doublons de clés)
    """
    # Création d'un expander pour l'indicateur
    with st.expander(f"{indicator.id} - {indicator.name}"):
        # Récupération des détails de l'indicateur
        if indicator.id in indicator_details:
            details = indicator_details[indicator.id]
            st.markdown(f"## {details['title']}")
            st.markdown(details['description'])
        else:
            st.markdown(f"**Description :** {indicator.description}")
        
        # Affichage des informations de l'indicateur
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Type :** {indicator.type_indicator.capitalize()}")
            st.markdown(f"**Prérequis :** {'Oui' if indicator.is_prerequisite else 'Non'}")
            st.markdown(f"**Points fixes :** {indicator.points_fixed}")
            st.markdown(f"**Points variables :** {indicator.points_variable}")
        
        with col2:
            # Contrôles pour l'état de complétion
            if indicator.max_level > 1:
                # Indicateur avec plusieurs niveaux
                indicator.completion_status = st.radio(
                    "Niveau de complétion",
                    options=list(range(indicator.max_level + 1)),
                    index=indicator.completion_status,
                    key=f"completion_status_{indicator.id}_{tab}",
                    horizontal=True,
                    format_func=lambda x: f"Niveau {x}" if x > 0 else "Non complété"
                )
            else:
                # Indicateur avec un seul niveau
                indicator.completion_status = 1 if st.checkbox(
                    "Indicateur complété",
                    value=indicator.completion_status == 1,
                    key=f"completion_status_{indicator.id}_{tab}"
                ) else 0
            
            # Pour les indicateurs avec pourcentage de complétion
            if indicator.points_variable > 0 and indicator.completion_status > 0:
                indicator.completion_percentage = st.slider(
                    "Pourcentage de complétion",
                    min_value=0,
                    max_value=100,
                    value=indicator.completion_percentage,
                    key=f"completion_percentage_{indicator.id}_{tab}"
                )
            
            # Cas spécifiques pour certains indicateurs
            if indicator.id == "A1O4":  # Missions de santé publique
                st.markdown("**Nombre de missions de santé publique :** 2 maximum valorisées")
                
                # Bonus si présence d'un IPA
                if has_ipa_in_structure:
                    st.markdown("**Bonus IPA :** +200 points fixes si présence d'un IPA et réalisation de 2 missions")
            
            elif indicator.id == "A2S2":  # Protocoles pluri-professionnels
                st.markdown("**Nombre de protocoles :** 8 maximum valorisés")
                
                # Bonus si présence d'un IPA
                if has_ipa_in_structure:
                    st.markdown("**Bonus IPA :** +40 points fixes par protocole si présence d'un IPA")
            
            elif indicator.id == "A2S3":  # Concertation pluri-professionnelle
                # Bonus si présence d'un IPA
                if has_ipa_in_structure:
                    st.markdown("**Bonus IPA :** +200 points variables si présence d'un IPA")
        
        # Calcul et affichage des points et du montant
        points = indicator.calculate_points(nb_patients)
        amount = indicator.calculate_amount(nb_patients)
        
        st.markdown(f"**Points obtenus :** {int(points)}")
        st.markdown(f"**Montant :** {format_currency(amount)}")
