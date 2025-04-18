# PartnerCompensation - Gestion des Rémunérations SISA

Application de gestion des rémunérations des associés d'une SISA (Société Interprofessionnelle de Soins Ambulatoires) basée sur les indicateurs ACI de la CPAM.

## Fonctionnalités

- **Gestion des indicateurs ACI** : Suivi et modification de l'état de complétion des indicateurs socles et optionnels
- **Gestion des associés** : Ajout, modification et suppression des associés, avec leurs rôles et paramètres
- **Gestion des charges fixes** : Suivi des charges (logiciel de santé, rémunération coordinateur, location salle, etc.)
- **Tableau de bord** : Visualisation des rémunérations et des charges, avec des simulations interactives

## Installation

1. Clonez ce dépôt :
   ```
   git clone https://github.com/votre-utilisateur/PartnerCompensation.git
   cd PartnerCompensation
   ```

2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```
   streamlit run app.py
   ```

## Structure du projet

```
PartnerCompensation/
├── app.py                  # Point d'entrée de l'application
├── requirements.txt        # Dépendances
├── data/                   # Dossier pour les données sauvegardées
├── src/                    # Code source
│   ├── components/         # Composants réutilisables
│   ├── data/               # Données statiques
│   ├── models/             # Modèles de données
│   │   ├── indicators.py   # Modèle pour les indicateurs ACI
│   │   ├── associates.py   # Modèle pour les associés
│   │   └── expenses.py     # Modèle pour les charges
│   ├── pages/              # Pages de l'application
│   │   ├── home.py         # Page d'accueil
│   │   ├── indicators.py   # Page de gestion des indicateurs
│   │   ├── associates.py   # Page de gestion des associés
│   │   ├── expenses.py     # Page de gestion des charges
│   │   └── dashboard.py    # Tableau de bord
│   └── utils/              # Utilitaires
│       ├── calculations.py # Fonctions de calcul
│       └── data_manager.py # Gestion des données
```

## Utilisation

### Gestion des indicateurs ACI

La page "Indicateurs ACI" permet de visualiser et modifier l'état de complétion des indicateurs socles et optionnels. Les indicateurs sont regroupés par axe :
- Axe 1 - Accès aux soins
- Axe 2 - Travail en équipe
- Axe 3 - Système d'information

Pour chaque indicateur, vous pouvez définir son état de complétion et, le cas échéant, le pourcentage de complétion pour les indicateurs avec points variables.

### Gestion des associés

La page "Gestion des Associés" permet d'ajouter, modifier et supprimer des associés. Pour chaque associé, vous pouvez définir :
- Informations personnelles (nom, prénom, email, téléphone)
- Informations professionnelles (profession, spécialité, RPPS, date d'entrée)
- Paramètres spécifiques (patients médecin traitant, temps de présence, clé de répartition)
- Rôles dans la structure (coordinateur, référent qualité, etc.)

### Gestion des charges fixes

La page "Charges Fixes" permet de gérer les charges de la SISA :
- Logiciel de santé
- Rémunération du coordinateur
- Location de salle
- Autres dépenses

Pour chaque charge, vous pouvez définir le montant, la fréquence et la méthode de répartition entre les associés.

### Tableau de bord

Le tableau de bord offre une vue synthétique des rémunérations et des charges, avec des graphiques et des tableaux. Il permet également de simuler différents scénarios en modifiant l'état de complétion des indicateurs.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
