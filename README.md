# Programmation Linéaire MVP

Solveur de programmation linéaire basé sur le modèle MVP (Model-View-Presenter) utilisant Python et scipy.

## Description

Ce projet implémente un solveur de programmation linéaire avec une architecture MVP claire :

- **Model** : Gère la logique backend avec `scipy.optimize.linprog`
- **View** : Interface utilisateur en ligne de commande (CLI)
- **Presenter** : Coordonne la validation des entrées et le formatage des résultats

## Structure du Projet

```
programmation-lineaire-mvp/
├── src/
│   ├── __init__.py
│   ├── model.py          # Module Model (LinearProgramModel)
│   ├── presenter.py      # Module Presenter (LinearProgramPresenter)
│   ├── view.py           # Module View (ConsoleView)
│   └── main.py           # Point d'entrée principal
├── tests/
│   ├── __init__.py
│   ├── test_model.py     # Tests unitaires pour Model
│   ├── test_presenter.py # Tests unitaires pour Presenter
│   └── test_view.py      # Tests unitaires pour View
├── docs/
├── requirements.txt
└── README.md
```

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le repository :
```bash
git clone https://github.com/KEVINBMK/programmation-lineaire-mvp.git
cd programmation-lineaire-mvp
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer l'application

Pour démarrer le solveur en mode interactif :

```bash
python -m src.main
```

ou

```bash
python src/main.py
```

### Menu principal

L'application propose trois options :

1. **Résoudre un problème simple (exemple)** : Utilise un exemple prédéfini
2. **Résoudre un problème personnalisé** : Permet de saisir vos propres données
3. **Quitter** : Ferme l'application

### Exemple d'utilisation

#### Problème d'exemple

Le problème d'exemple résout :

```
Minimiser : -1*x₁ + 4*x₂

Sous contraintes :
  -3*x₁ + 1*x₂ ≤ 6
   1*x₁ + 2*x₂ ≤ 4
   x₁, x₂ ≥ 0
```

Sélectionnez l'option `1` dans le menu pour voir la solution.

#### Problème personnalisé

Pour résoudre votre propre problème :

1. Sélectionnez l'option `2`
2. Entrez les coefficients de la fonction objectif (ex: `1 2 3`)
3. Indiquez le nombre de contraintes d'inégalité
4. Pour chaque contrainte, entrez :
   - Les coefficients de la contrainte
   - La valeur limite
5. Spécifiez les bornes des variables (optionnel)

**Exemple de saisie :**

```
Fonction objectif : 1 2
Nombre de contraintes : 1
Contrainte 1 coefficients : 1 1
Contrainte 1 limite : 10
Bornes : n
```

Cela résout :
```
Minimiser : 1*x₁ + 2*x₂
Sous contrainte : x₁ + x₂ ≤ 10
```

## Exécuter les tests

Pour exécuter tous les tests unitaires :

```bash
python -m unittest discover tests
```

Pour exécuter un fichier de test spécifique :

```bash
python -m unittest tests.test_model
python -m unittest tests.test_presenter
python -m unittest tests.test_view
```

Pour exécuter un test spécifique :

```bash
python -m unittest tests.test_model.TestLinearProgramModel.test_résoudre_problème_simple
```

## Architecture MVP

### Model (src/model.py)

**Classe : `LinearProgramModel`**

- `résoudre_problème(c, A_ub, b_ub, A_eq, b_eq, bounds, method)` : Résout le problème de programmation linéaire
- `obtenir_dernier_résultat()` : Retourne le dernier résultat de résolution

### Presenter (src/presenter.py)

**Classe : `LinearProgramPresenter`**

- `valider_entrée(c, A_ub, b_ub, A_eq, b_eq, bounds)` : Valide les données d'entrée
- `formater_résultat(résultat)` : Formate les résultats pour l'affichage
- `résoudre(c, A_ub, b_ub, A_eq, b_eq, bounds)` : Valide et résout le problème

### View (src/view.py)

**Classe : `ConsoleView`**

- `afficher_menu()` : Affiche le menu principal
- `demander_données()` : Collecte les données du problème
- `obtenir_exemple_simple()` : Retourne un exemple prédéfini
- `montrer_résultat(résultat_formaté)` : Affiche les résultats
- `afficher_message(message)` : Affiche un message
- `afficher_erreur(erreur)` : Affiche une erreur
- `demander_continuer()` : Demande si l'utilisateur veut continuer

## Dépendances

- `scipy` : Pour la résolution de problèmes de programmation linéaire
- `numpy` : Pour les opérations matricielles

Voir `requirements.txt` pour les versions spécifiques.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est un MVP (Minimum Viable Product) développé à des fins éducatives.

## Auteur

KEVINBMK