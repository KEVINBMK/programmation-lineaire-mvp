# Documentation du Projet

## Vue d'ensemble

Ce projet implémente un solveur de programmation linéaire utilisant l'architecture MVP (Model-View-Presenter). Il permet de résoudre des problèmes d'optimisation linéaire de la forme :

```
Minimiser : c₁*x₁ + c₂*x₂ + ... + cₙ*xₙ

Sous contraintes :
  A_ub * x ≤ b_ub  (contraintes d'inégalité)
  A_eq * x = b_eq  (contraintes d'égalité)
  bounds           (bornes sur les variables)
```

## Architecture

### 1. Model (src/model.py)

Le module Model contient la logique backend de résolution :

- **Classe** : `LinearProgramModel`
- **Méthode principale** : `résoudre_problème(c, A_ub, b_ub, A_eq, b_eq, bounds, method)`
  - Utilise `scipy.optimize.linprog` pour résoudre le problème
  - Retourne un dictionnaire avec les résultats
- **Méthode auxiliaire** : `obtenir_dernier_résultat()`
  - Retourne le dernier résultat de résolution

### 2. Presenter (src/presenter.py)

Le module Presenter agit comme intermédiaire entre Model et View :

- **Classe** : `LinearProgramPresenter`
- **Méthodes principales** :
  - `valider_entrée(c, A_ub, b_ub, A_eq, b_eq, bounds)` : Valide les données saisies
  - `formater_résultat(résultat)` : Formate les résultats pour affichage
  - `résoudre(c, A_ub, b_ub, A_eq, b_eq, bounds)` : Orchestre validation et résolution

### 3. View (src/view.py)

Le module View gère l'interface utilisateur CLI :

- **Classe** : `ConsoleView`
- **Méthodes principales** :
  - `afficher_menu()` : Affiche le menu principal
  - `demander_données()` : Collecte les données du problème
  - `obtenir_exemple_simple()` : Fournit un exemple prédéfini
  - `montrer_résultat(résultat_formaté)` : Affiche les résultats
  - `afficher_message(message)` : Affiche un message
  - `afficher_erreur(erreur)` : Affiche une erreur
  - `demander_continuer()` : Demande si l'utilisateur veut continuer

### 4. Main (src/main.py)

Le point d'entrée coordonne les trois modules MVP :

- Crée les instances Model, View et Presenter
- Gère la boucle principale de l'application
- Traite les choix de l'utilisateur

## Tests

Le projet inclut des tests unitaires complets pour chaque module :

### test_model.py
- Test d'initialisation
- Test de résolution simple
- Test sans contraintes
- Test de problème infaisable
- Test avec contraintes d'égalité
- Test avec erreurs de dimension

### test_presenter.py
- Test de validation d'entrées valides
- Test de validation d'entrées invalides
- Test de formatage de résultats
- Test de résolution avec validation

### test_view.py
- Test d'affichage du menu
- Test de demande de données
- Test d'obtention d'exemple
- Test d'affichage de résultats et messages

**Total : 32 tests unitaires**

## Exemples d'utilisation

### Exemple 1 : Problème simple

Résoudre :
```
Minimiser : -1*x₁ + 4*x₂
Sous contraintes :
  -3*x₁ + x₂ ≤ 6
  x₁ + 2*x₂ ≤ 4
  x₁, x₂ ≥ 0
```

**Résultat attendu** : x₁ = 4, x₂ = 0, valeur optimale = -4

### Exemple 2 : Problème personnalisé

Résoudre :
```
Minimiser : 3*x₁ + 2*x₂ + x₃
Sous contraintes :
  2*x₁ + x₂ + x₃ ≤ 20
  x₁ + x₂ + x₃ ≤ 15
  0 ≤ x₁, x₂, x₃ ≤ 10
```

## Dépendances

- **scipy** : Bibliothèque pour calculs scientifiques et optimisation
- **numpy** : Bibliothèque pour calculs matriciels

## Commandes utiles

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancer l'application
python src/main.py

# Exécuter tous les tests
python -m unittest discover tests

# Exécuter un test spécifique
python -m unittest tests.test_model

# Exécuter avec verbose
python -m unittest discover tests -v
```

## Structure des fichiers

```
programmation-lineaire-mvp/
├── .gitignore              # Exclusions Git
├── README.md               # Documentation principale
├── requirements.txt        # Dépendances Python
├── docs/
│   └── documentation.md    # Documentation détaillée
├── src/
│   ├── __init__.py         # Module Python
│   ├── model.py            # Module Model
│   ├── presenter.py        # Module Presenter  
│   ├── view.py             # Module View
│   └── main.py             # Point d'entrée
└── tests/
    ├── __init__.py         # Module de tests
    ├── test_model.py       # Tests pour Model
    ├── test_presenter.py   # Tests pour Presenter
    └── test_view.py        # Tests pour View
```

## Validation

✅ 32 tests unitaires passent avec succès  
✅ Application CLI fonctionne correctement  
✅ Validation des entrées implémentée  
✅ Gestion d'erreurs robuste  
✅ Code documenté en français  
✅ Architecture MVP respectée
