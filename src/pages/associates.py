import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
from datetime import datetime

from src.models.associates import (
    Associate, get_professions, get_medical_specialities, 
    get_roles, get_sample_associates
)
from src.utils.data_manager import save_associates
from src.utils.calculations import (
    get_total_patients_mt, get_total_medical_professions,
    get_total_paramedical_professions, get_unique_professions,
    format_currency
)

def show():
    """
    Affiche la page de gestion des associés
    """
    st.markdown("<h1 class='main-header'>Gestion des Associés</h1>", unsafe_allow_html=True)
    
    # Initialisation des associés s'ils n'existent pas dans la session
    if 'associates' not in st.session_state:
        st.session_state.associates = get_sample_associates()
    
    # Récupération des associés
    associates = st.session_state.associates
    
    # Onglets pour les différentes fonctionnalités
    tab1, tab2, tab3 = st.tabs(["Liste des associés", "Ajouter/Modifier un associé", "Statistiques"])
    
    with tab1:
        display_associates_list(associates)
    
    with tab2:
        add_edit_associate(associates)
    
    with tab3:
        display_statistics(associates)
    
    # Bouton pour sauvegarder les modifications
    if st.button("Sauvegarder les modifications"):
        save_associates(associates)
        st.success("Les modifications ont été sauvegardées avec succès.")

def display_associates_list(associates):
    """
    Affiche la liste des associés
    """
    st.markdown("<h2 class='sub-header'>Liste des associés</h2>", unsafe_allow_html=True)
    
    # Filtres
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtre par profession
        professions = ["Toutes"] + list(set(associate.profession for associate in associates))
        selected_profession = st.selectbox("Filtrer par profession", professions)
    
    with col2:
        # Filtre par rôle
        all_roles = set()
        for associate in associates:
            all_roles.update(associate.roles)
        
        roles = ["Tous"] + list(all_roles)
        selected_role = st.selectbox("Filtrer par rôle", roles)
    
    # Filtrage des associés
    filtered_associates = associates
    
    if selected_profession != "Toutes":
        filtered_associates = [a for a in filtered_associates if a.profession == selected_profession]
    
    if selected_role != "Tous":
        filtered_associates = [a for a in filtered_associates if selected_role in a.roles]
    
    # Affichage des associés
    if not filtered_associates:
        st.info("Aucun associé ne correspond aux critères de filtrage.")
    else:
        # Création d'un DataFrame pour l'affichage
        associates_data = []
        for associate in filtered_associates:
            associates_data.append({
                "ID": associate.id,
                "Nom": associate.last_name,
                "Prénom": associate.first_name,
                "Profession": associate.profession,
                "Spécialité": associate.speciality or "",
                "Patients MT": associate.patients_mt,
                "Temps de présence": associate.presence_time,
                "Rôles": ", ".join(associate.roles) if associate.roles else ""
            })
        
        df = pd.DataFrame(associates_data)
        
        # Affichage du DataFrame
        st.dataframe(df, use_container_width=True)
        
        # Sélection d'un associé pour modification ou suppression
        selected_associate_id = st.selectbox(
            "Sélectionner un associé pour modification ou suppression",
            options=[a.id for a in filtered_associates],
            format_func=lambda x: next((a.get_full_name() + " - " + a.profession) for a in filtered_associates if a.id == x)
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Modifier l'associé sélectionné"):
                st.session_state.edit_associate_id = selected_associate_id
                st.session_state.active_tab = "Ajouter/Modifier un associé"
                st.rerun()
        
        with col2:
            if st.button("Supprimer l'associé sélectionné"):
                # Confirmation de suppression
                if st.checkbox("Confirmer la suppression"):
                    # Suppression de l'associé
                    st.session_state.associates = [a for a in st.session_state.associates if a.id != selected_associate_id]
                    st.success("L'associé a été supprimé avec succès.")
                    st.rerun()

def add_edit_associate(associates):
    """
    Ajoute ou modifie un associé
    """
    st.markdown("<h2 class='sub-header'>Ajouter/Modifier un associé</h2>", unsafe_allow_html=True)
    
    # Vérification si on est en mode édition
    edit_mode = 'edit_associate_id' in st.session_state
    
    # Récupération de l'associé à éditer si on est en mode édition
    associate_to_edit = None
    if edit_mode:
        associate_to_edit = next((a for a in associates if a.id == st.session_state.edit_associate_id), None)
        
        if associate_to_edit:
            st.markdown(f"<h3 class='blue-text'>Modification de l'associé : {associate_to_edit.get_full_name()}</h3>", unsafe_allow_html=True)
        else:
            st.error("L'associé à modifier n'a pas été trouvé.")
            edit_mode = False
    else:
        st.markdown("<h3 class='blue-text'>Ajout d'un nouvel associé</h3>", unsafe_allow_html=True)
    
    # Formulaire d'ajout/modification
    with st.form("associate_form"):
        # Informations personnelles
        st.markdown("<h4>Informations personnelles</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "Prénom",
                value=associate_to_edit.first_name if edit_mode else ""
            )
        
        with col2:
            last_name = st.text_input(
                "Nom",
                value=associate_to_edit.last_name if edit_mode else ""
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input(
                "Email",
                value=associate_to_edit.email if edit_mode else ""
            )
        
        with col2:
            phone = st.text_input(
                "Téléphone",
                value=associate_to_edit.phone if edit_mode else ""
            )
        
        # Informations professionnelles
        st.markdown("<h4>Informations professionnelles</h4>", unsafe_allow_html=True)
        
        # Récupération des listes de professions et spécialités
        professions_dict = get_professions()
        all_professions = professions_dict["all"]
        specialities = get_medical_specialities()
        
        col1, col2 = st.columns(2)
        
        with col1:
            profession = st.selectbox(
                "Profession",
                options=all_professions,
                index=all_professions.index(associate_to_edit.profession) if edit_mode and associate_to_edit.profession in all_professions else 0
            )
        
        with col2:
            # Affichage du champ de spécialité uniquement pour les médecins spécialistes
            if profession == "Médecin spécialiste":
                speciality = st.selectbox(
                    "Spécialité",
                    options=specialities,
                    index=specialities.index(associate_to_edit.speciality) if edit_mode and associate_to_edit.speciality in specialities else 0
                )
            else:
                speciality = None
        
        col1, col2 = st.columns(2)
        
        with col1:
            rpps = st.text_input(
                "Numéro RPPS",
                value=associate_to_edit.rpps if edit_mode else ""
            )
        
        with col2:
            entry_date = st.date_input(
                "Date d'entrée dans la SISA",
                value=datetime.strptime(associate_to_edit.entry_date, "%Y-%m-%d").date() if edit_mode and associate_to_edit.entry_date else datetime.now().date()
            )
        
        # Paramètres spécifiques
        st.markdown("<h4>Paramètres spécifiques</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Affichage du champ de patients médecin traitant uniquement pour les médecins
            if profession.startswith("Médecin"):
                patients_mt = st.number_input(
                    "Nombre de patients médecin traitant",
                    min_value=0,
                    value=associate_to_edit.patients_mt if edit_mode else 0
                )
            else:
                patients_mt = 0
        
        with col2:
            presence_time = st.slider(
                "Temps de présence (ETP)",
                min_value=0.1,
                max_value=1.0,
                value=associate_to_edit.presence_time if edit_mode else 1.0,
                step=0.1
            )
        
        distribution_key = st.slider(
            "Clé de répartition pour la rémunération",
            min_value=0.1,
            max_value=1.0,
            value=associate_to_edit.distribution_key if edit_mode else 1.0,
            step=0.1
        )
        
        # Rôles dans la structure
        st.markdown("<h4>Rôles dans la structure</h4>", unsafe_allow_html=True)
        
        # Récupération de la liste des rôles
        all_roles = get_roles()
        
        # Sélection des rôles
        selected_roles = []
        for role in all_roles:
            if st.checkbox(
                role,
                value=role in associate_to_edit.roles if edit_mode else False,
                key=f"role_{role}"
            ):
                selected_roles.append(role)
        
        # Boutons de soumission
        submit_button = st.form_submit_button("Enregistrer")
        
        if submit_button:
            # Validation des champs obligatoires
            if not first_name or not last_name or not profession:
                st.error("Les champs Prénom, Nom et Profession sont obligatoires.")
            else:
                # Création ou mise à jour de l'associé
                if edit_mode:
                    # Mise à jour de l'associé existant
                    associate_to_edit.first_name = first_name
                    associate_to_edit.last_name = last_name
                    associate_to_edit.profession = profession
                    associate_to_edit.speciality = speciality
                    associate_to_edit.entry_date = entry_date.strftime("%Y-%m-%d")
                    associate_to_edit.roles = selected_roles
                    associate_to_edit.patients_mt = patients_mt
                    associate_to_edit.presence_time = presence_time
                    associate_to_edit.distribution_key = distribution_key
                    associate_to_edit.email = email
                    associate_to_edit.phone = phone
                    associate_to_edit.rpps = rpps
                    
                    st.success("L'associé a été modifié avec succès.")
                    
                    # Réinitialisation du mode édition
                    if 'edit_associate_id' in st.session_state:
                        del st.session_state.edit_associate_id
                else:
                    # Création d'un nouvel associé
                    new_associate = Associate(
                        id=str(uuid.uuid4()),
                        first_name=first_name,
                        last_name=last_name,
                        profession=profession,
                        speciality=speciality,
                        entry_date=entry_date.strftime("%Y-%m-%d"),
                        roles=selected_roles,
                        patients_mt=patients_mt,
                        presence_time=presence_time,
                        distribution_key=distribution_key,
                        email=email,
                        phone=phone,
                        rpps=rpps
                    )
                    
                    # Ajout de l'associé à la liste
                    st.session_state.associates.append(new_associate)
                    
                    st.success("L'associé a été ajouté avec succès.")
                
                # Rechargement de la page
                st.rerun()
    
    # Bouton pour annuler l'édition
    if edit_mode:
        if st.button("Annuler la modification"):
            # Réinitialisation du mode édition
            if 'edit_associate_id' in st.session_state:
                del st.session_state.edit_associate_id
            
            st.rerun()

def display_statistics(associates):
    """
    Affiche des statistiques sur les associés
    """
    st.markdown("<h2 class='sub-header'>Statistiques</h2>", unsafe_allow_html=True)
    
    if not associates:
        st.info("Aucun associé n'a été ajouté.")
        return
    
    # Calcul des statistiques
    total_associates = len(associates)
    total_patients = get_total_patients_mt(associates)
    total_medical = get_total_medical_professions(associates)
    total_paramedical = get_total_paramedical_professions(associates)
    unique_professions = get_unique_professions(associates)
    
    # Affichage des statistiques générales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nombre d'associés", total_associates)
    
    with col2:
        st.metric("Patients médecin traitant", total_patients)
    
    with col3:
        st.metric("Professions médicales", total_medical)
    
    with col4:
        st.metric("Professions paramédicales", total_paramedical)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique de répartition des professions
        st.markdown("<h3 class='blue-text'>Répartition des professions</h3>", unsafe_allow_html=True)
        
        profession_counts = {}
        for profession in unique_professions:
            profession_counts[profession] = len([a for a in associates if a.profession == profession])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tri des professions par nombre d'associés
        sorted_professions = sorted(profession_counts.items(), key=lambda x: x[1], reverse=True)
        professions = [p[0] for p in sorted_professions]
        counts = [p[1] for p in sorted_professions]
        
        # Création du graphique
        bars = ax.bar(professions, counts, color="#1E88E5")
        
        # Rotation des étiquettes pour une meilleure lisibilité
        plt.xticks(rotation=45, ha='right')
        
        # Ajout des valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(int(height)), ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Graphique de répartition des patients médecin traitant
        st.markdown("<h3 class='blue-text'>Patients médecin traitant par médecin</h3>", unsafe_allow_html=True)
        
        # Filtrage des médecins
        doctors = [a for a in associates if a.profession.startswith("Médecin")]
        
        if doctors:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Création du graphique
            doctor_names = [f"{d.first_name} {d.last_name}" for d in doctors]
            patient_counts = [d.patients_mt for d in doctors]
            
            # Tri des médecins par nombre de patients
            sorted_indices = sorted(range(len(patient_counts)), key=lambda i: patient_counts[i], reverse=True)
            doctor_names = [doctor_names[i] for i in sorted_indices]
            patient_counts = [patient_counts[i] for i in sorted_indices]
            
            bars = ax.bar(doctor_names, patient_counts, color="#42A5F5")
            
            # Rotation des étiquettes pour une meilleure lisibilité
            plt.xticks(rotation=45, ha='right')
            
            # Ajout des valeurs sur les barres
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, str(int(height)), ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Aucun médecin n'a été ajouté.")
    
    # Tableau récapitulatif
    st.markdown("<h3 class='blue-text'>Tableau récapitulatif</h3>", unsafe_allow_html=True)
    
    # Création d'un DataFrame pour l'affichage
    associates_data = []
    for associate in associates:
        associates_data.append({
            "Nom": associate.last_name,
            "Prénom": associate.first_name,
            "Profession": associate.profession,
            "Spécialité": associate.speciality or "",
            "Patients MT": associate.patients_mt,
            "Temps de présence": associate.presence_time,
            "Clé de répartition": associate.distribution_key,
            "Rôles": ", ".join(associate.roles) if associate.roles else ""
        })
    
    df = pd.DataFrame(associates_data)
    
    # Affichage du DataFrame
    st.dataframe(df, use_container_width=True)
