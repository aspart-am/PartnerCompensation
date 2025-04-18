import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def show():
    """
    Affiche la page d'accueil de l'application
    """
    st.markdown("<h1 class='main-header'>Gestion des Rémunérations SISA</h1>", unsafe_allow_html=True)
    
    # En-tête avec date
    current_date = datetime.now().strftime("%d/%m/%Y")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 class='sub-header'>Bienvenue dans l'application de gestion des rémunérations SISA</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='text-align: right; padding-top: 1rem;'>Date: {current_date}</p>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class='card'>
        <p>Cette application vous permet de gérer les rémunérations des associés d'une SISA (Société Interprofessionnelle de Soins Ambulatoires) 
        en fonction de la validation des Indicateurs ACI de la CPAM.</p>
        <p>Utilisez le menu de navigation à gauche pour accéder aux différentes fonctionnalités.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Présentation des fonctionnalités
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-square" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <polyline points="9 11 12 14 22 4"></polyline>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                </svg>
                Indicateurs ACI
            </h3>
            <p>Gérez les indicateurs ACI de la CPAM :</p>
            <ul>
                <li>Indicateurs socles (obligatoires)</li>
                <li>Indicateurs optionnels</li>
                <li>Suivi de l'état de complétion</li>
                <li>Calcul automatique des points et rémunérations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                Gestion des Associés
            </h3>
            <p>Gérez les informations des associés :</p>
            <ul>
                <li>Ajout, modification et suppression d'associés</li>
                <li>Définition des rôles et fonctions</li>
                <li>Suivi du nombre de patients médecins traitants</li>
                <li>Paramètres de répartition des rémunérations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-euro" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <path d="M4 10h12"></path>
                    <path d="M4 14h9"></path>
                    <path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12c0 4.4 3.5 8 7.8 8 2 0 3.8-.8 5.2-2"></path>
                </svg>
                Charges Fixes
            </h3>
            <p>Gérez les charges fixes de la SISA :</p>
            <ul>
                <li>Logiciel de santé</li>
                <li>Rémunération du coordinateur</li>
                <li>Location de salle</li>
                <li>Autres dépenses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3 class='blue-text'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bar-chart-3" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <path d="M3 3v18h18"></path>
                    <path d="M18 17V9"></path>
                    <path d="M13 17V5"></path>
                    <path d="M8 17v-3"></path>
                </svg>
                Tableau de Bord
            </h3>
            <p>Visualisez les données financières :</p>
            <ul>
                <li>Synthèse des rémunérations</li>
                <li>Répartition par associé</li>
                <li>Simulation interactive</li>
                <li>Exportation des rapports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Pied de page avec statistiques
    st.markdown("---")
    
    # Statistiques fictives pour la démo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Indicateurs validés", value="12/18", delta="67%")
    with col2:
        st.metric(label="Associés", value="24", delta="2 nouveaux")
    with col3:
        st.metric(label="Rémunération ACI", value="42 500 €", delta="8 500 €")
    with col4:
        st.metric(label="Charges annuelles", value="15 200 €", delta="-2%")
    
    st.markdown("""
    <p style='text-align: center; margin-top: 2rem;'>
        Pour commencer, utilisez le menu de navigation à gauche pour accéder aux différentes fonctionnalités.
    </p>
    """, unsafe_allow_html=True)
