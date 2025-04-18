import streamlit as st
import pandas as pd
import numpy as np
from src.pages import home, indicators, associates, expenses, dashboard

# Configuration de la page
st.set_page_config(
    page_title="Gestion Rémunération SISA - ACI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement du CSS personnalisé
with open('src/static/css/style.css', 'r') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialisation des données de session si elles n'existent pas
if 'indicators' not in st.session_state:
    st.session_state.indicators = {}
if 'associates' not in st.session_state:
    st.session_state.associates = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Barre latérale pour la navigation
st.sidebar.markdown("<h1 class='blue-text'>Gestion SISA</h1>", unsafe_allow_html=True)
pages = {
    "Accueil": home,
    "Indicateurs ACI": indicators,
    "Gestion des Associés": associates,
    "Charges Fixes": expenses,
    "Tableau de Bord": dashboard
}

# Sélection de la page
selection = st.sidebar.radio("Navigation", list(pages.keys()))

# Affichage de la page sélectionnée
pages[selection].show()

# Pied de page
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 - Application de Gestion SISA")
