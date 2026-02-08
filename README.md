# Solveur de Programmation Linéaire

Projet Python pour résoudre des problèmes de programmation linéaire avec la méthode du Simplexe.

## Description

Ce projet implémente un solveur de programmation linéaire (PL) permettant de :
- Maximiser ou minimiser une fonction objectif linéaire
- Gérer des contraintes d'inégalité et d'égalité
- Afficher les tableaux du Simplexe étape par étape (comme dans le cours)

## Fonctionnalités

- Résolution par la méthode du Simplexe
- Affichage des tableaux avec variable entrante, sortante et pivot
- Interface web Streamlit
- Visualisation graphique pour les problèmes à 2 variables
- Exemples prédéfinis du cours

## Structure du projet

```
Programmation_lineair/
├── app.py              # Interface Streamlit
├── simplexe.py         # Algorithme du Simplexe avec tableaux
├── solver.py           # Solveur rapide (scipy)
├── models.py           # Classes ProblemePL et Solution
├── examples.py         # Exemples en ligne de commande
├── main.py             # Menu interactif console
└── requirements.txt    # Dépendances
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Interface web (Streamlit)

```bash
streamlit run app.py
```

### Ligne de commande

```bash
python main.py
```

### Exemple du cours

```python
from simplexe import SimplexeSolveur

# Max Z = 1200x1 + 1000x2
# 3x1 + 4x2 <= 160
# 6x1 + 3x2 <= 180

c = [1200, 1000]
A = [[3, 4], [6, 3]]
b = [160, 180]

solveur = SimplexeSolveur()
tableaux = solveur.resoudre(c, A, b)

# Affiche tous les tableaux
for t in tableaux:
    print(solveur.afficher_tableau(t))
```

Résultat : x1 = 16, x2 = 28, Z = 47200

## Méthode du Simplexe

Le programme implémente l'algorithme du tableau du Simplexe :

1. Construire le tableau initial (forme standard avec variables d'écart)
2. Sélectionner la variable entrante (plus grand coefficient positif dans la ligne Delta)
3. Sélectionner la variable sortante (plus petit ratio positif dans la colonne R)
4. Appliquer le pivot (règle du rectangle)
5. Répéter jusqu'à ce que tous les coefficients Delta soient négatifs ou nuls

## Auteurs

Projet L4 - UPC 2024-2025
