# Guide de Présentation du Projet
## Solveur de Programmation Linéaire - Méthode du Simplexe

---

## 1. Introduction du Projet

### Objectif
Développer un solveur de programmation linéaire qui implémente l'algorithme du Simplexe avec affichage détaillé des tableaux, conforme au cours de Recherche Opérationnelle.

### Problématique
Comment résoudre des problèmes d'optimisation linéaire et visualiser les étapes de résolution de manière pédagogique ?

### Solution apportée
- Implémentation de la méthode du Simplexe avec tableaux
- Interface web interactive (Streamlit)
- Visualisation graphique pour problèmes à 2 variables
- Exemples prédéfinis du cours

---

## 2. Architecture du Projet

```
Programmation_lineair/
├── src/                    # Code source principal
│   ├── models.py           # Modélisation des problèmes
│   └── simplexe.py         # Méthode du Simplexe
├── examples/               # Exemples et démos
│   ├── examples.py         # Exemples CLI
│   └── main.py             # Menu interactif
├── app.py                  # Interface Streamlit
└── requirements.txt        # Dépendances
```

### Choix d'architecture MVP
- **Séparation claire** : Code source (src/) vs Exemples (examples/)
- **Modularité** : Chaque fichier a une responsabilité unique
- **Réutilisabilité** : Package src/ importable
- **Interface moderne** : Streamlit pour l'accessibilité web

---

## 3. Détail des Composants

### 3.1 - models.py (Modélisation)

**Rôle** : Définir les structures de données pour représenter un problème de PL

**Classes principales :**

#### `ProblemePL`
```python
class ProblemePL:
    # Représente un problème de programmation linéaire
    - c : coefficients fonction objectif
    - A_ub : matrice contraintes d'inégalité
    - b_ub : termes constants des inégalités
    - bounds : bornes sur les variables
```

**Méthodes clés :**
- `definir_fonction_objectif()` : Configure la fonction à optimiser
- `ajouter_contrainte_inegalite()` : Ajoute une contrainte (≤)
- `ajouter_contrainte_equalite()` : Ajoute une contrainte (=)
- `afficher_probleme()` : Affichage formaté

**Pourquoi cette classe ?**
- Encapsulation : Toutes les données du problème sont regroupées
- Validation : Les méthodes vérifient la cohérence des données
- Simplicité : Interface claire pour construire un problème

#### `Solution`
```python
class Solution:
    # Stocke le résultat d'une résolution
    - succes : booléen (solution trouvée ?)
    - valeurs_variables : valeurs optimales
    - valeur_objectif : Z optimal
```

**Points forts :**
- Séparation problème/solution
- Réutilisable

---

### 3.2 - simplexe.py (Cœur algorithme)

**Rôle** : Implémenter l'algorithme du Simplexe avec affichage des tableaux (comme dans le cours)

**Classe principale :**

#### `SimplexeSolveur`

**Algorithme implémenté :**

```
1. Construction du tableau initial
   - Variables d'écart pour contraintes ≤
   - Variables HB (Hors Base) = variables principales
   - Variables B (Base) = variables d'écart

2. TANT QUE (il existe un Δ > 0) :
   
   a) Sélection variable ENTRANTE
      → Plus grand coefficient positif dans ligne Δ
   
   b) Calcul colonne R (ratios)
      → R[i] = C[i] / colonne_entrante[i]
   
   c) Sélection variable SORTANTE
      → Plus petit ratio positif dans R
   
   d) Application du PIVOT (règle du rectangle)
      - Ligne pivot / pivot
      - Autres lignes : règle du rectangle
      - Mise à jour ligne Δ
   
   e) Échange variables (entrante ↔ sortante)

3. FIN : Tous les Δ ≤ 0 → Solution optimale
```

**Classe TableauSimplexe :**
```python
@dataclass
class TableauSimplexe:
    matrice: np.ndarray        # Coefficients
    delta: np.ndarray          # Ligne Δ
    colonne_c: np.ndarray      # Termes constants
    vars_hb: List[str]         # Variables hors base
    vars_base: List[str]       # Variables dans la base
    var_entrante_idx: int      # Index var entrante
    var_sortante_idx: int      # Index var sortante
```

**Points à présenter :**

1. **Règle du rectangle** (formule clé) :
   ```
   nouveau_coefficient = ancien_coefficient - (facteur_ligne * facteur_colonne) / pivot
   ```

2. **Détection de cas particuliers** :
   - Solution infinie : colonne entrante ≤ 0
   - Pas de solution : contradictions

3. **Traçabilité** : Chaque tableau est sauvegardé avec ses métadonnées

---

### 3.4 - app.py (Interface Streamlit)

**Rôle** : Interface web moderne et accessible

**Fonctionnalités implémentées :**

1. **Navigation intuitive**
   - Sidebar : Exemples vs Problème personnalisé
   - Cards cliquables pour les exemples

2. **Affichage de la solution**
   - Résultat principal (Z optimal)
   - Valeurs des variables (métriques)
   - Statistiques du problème

3. **Tableaux du Simplexe (innovation)**
   ```python
   def afficher_tableaux_simplexe(probleme: ProblemePL):
       # Affiche chaque tableau étape par étape
       # Avec mise en évidence du pivot
       # Explication de chaque itération
   ```
   - Tableau formaté en DataFrame
   - Pivot marqué entre crochets [...]
   - Messages explicatifs à chaque étape

4. **Visualisation 2D**
   - Graphique Plotly interactif
   - Contraintes affichées comme droites
   - Solution optimale marquée par une étoile

**Points forts techniques :**
- CSS personnalisé pour le design
- Responsive (fonctionne sur téléphone)
- Performance : mise en cache des calculs

---

## 4. Exemple de Démonstration

### Problème du cours (page 46 du syllabus)

**Énoncé :**
```
Maximiser Z = 1200x₁ + 1000x₂

Sous contraintes :
  3x₁ + 4x₂ ≤ 160
  6x₁ + 3x₂ ≤ 180
  x₁, x₂ ≥ 0
```

**Résolution :**

1. **Tableau initial**
   - Variables HB : x1, x2
   - Variables Base : t1, t2 (écart)
   - Solution départ : x1=0, x2=0, t1=160, t2=180

2. **Itération 1**
   - Entrante : x1 (Δ = 1200, le plus grand)
   - Sortante : t2 (R = 30, le plus petit)
   - Pivot = 6

3. **Itération 2**
   - Entrante : x2 (Δ = 400)
   - Sortante : t1 (R = 28)
   - Pivot = 2.5

4. **Solution optimale**
   - x₁ = 16, x₂ = 28
   - Z = 47 200
   - Tous les Δ ≤ 0 → STOP

**Interprétation :**
- t1 = 0 → Contrainte 1 saturée (utilisée à 100%)
- t2 = 0 → Contrainte 2 saturée

---

## 5. Points Forts à Mettre en Avant

### 5.1 Aspects Techniques

✓ **Algorithmique**
- Implémentation fidèle à l'algorithme du cours
- Gestion des cas particuliers (solution infinie, etc.)
- Complexité optimale

✓ **Architecture**
- Structure MVP claire et modulaire
- Séparation des responsabilités
- Code réutilisable (package src/)

✓ **Qualité du code**
- Commentaires en français (comme demandé)
- Type hints (ProblemePL, Solution, etc.)
- Docstrings détaillées

### 5.2 Aspects Fonctionnels

✓ **Pédagogie**
- Affichage des tableaux étape par étape
- Messages explicatifs à chaque itération
- Visualisation graphique

✓ **Utilisabilité**
- Interface web (pas besoin d'installer Python)
- Exemples prédéfinis du cours
- Création de problèmes personnalisés

✓ **Accessibilité**
- Déployé sur Streamlit Cloud → URL publique
- Accessible sur téléphone/tablette
- Pas de configuration nécessaire

### 5.3 Valeur Ajoutée

1. **Conformité au cours**
   - Tableaux identiques au syllabus
   - Méthode enseignée (pas une boîte noire)

2. **Outil pédagogique**
   - Permet de vérifier ses exercices
   - Comprendre les étapes du Simplexe

3. **Production quality**
   - Tests validés
   - Déployé en ligne
   - Documentation complète

---

## 6. Défis Rencontrés et Solutions

### Défi 1 : Affichage des tableaux
**Problème** : Formater les tableaux de manière lisible
**Solution** : Dataclass + pandas DataFrame + CSS personnalisé

### Défi 2 : Règle du rectangle
**Problème** : Appliquer correctement les transformations
**Solution** : Implémentation par étapes avec validation

### Défi 3 : Interface utilisateur
**Problème** : Rendre l'app accessible aux non-programmeurs
**Solution** : Streamlit + Design épuré + Exemples clairs

---

## 7. Démonstration Live

### Scénario de présentation

1. **Accès à l'application**
   ```
   https://kevinbmk-programmation-lineaire-mvp.streamlit.app
   ```

2. **Charger l'exemple du cours**
   - Cliquer sur "Exemple du Cours"
   - Montrer la formulation mathématique

3. **Montrer la solution**
   - Valeur optimale : Z = 47200
   - Variables : x1=16, x2=28

4. **Déplier les tableaux du Simplexe**
   - Tableau initial
   - Itération 1 (pivot sur x1)
   - Itération 2 (pivot sur x2)
   - Solution finale

5. **Visualisation graphique**
   - Contraintes (droites)
   - Zone réalisable
   - Point optimal (étoile)

6. **Créer un problème personnalisé**
   - Montrer la flexibilité
   - Résoudre en temps réel

---

## 8. Technologies Utilisées

| Technologie | Usage | Justification |
|-------------|-------|---------------|
| Python 3.12 | Langage | Standard en data science |
| NumPy | Calculs matriciels | Performance |
| Streamlit | Interface web | Rapidité de développement |
| Plotly | Visualisation | Graphiques interactifs |
| Pandas | Affichage tableaux | Formatage élégant |
| Git/GitHub | Versioning | Bonnes pratiques |
| Streamlit Cloud | Déploiement | Gratuit et simple |

---

## 9. Perspectives d'Amélioration

### Court terme
- [ ] Export des résultats en PDF
- [ ] Plus d'exemples du cours
- [ ] Mode pas-à-pas interactif

### Moyen terme
- [ ] Programmation linéaire en nombres entiers
- [ ] Analyse de sensibilité
- [ ] Problèmes de dualité

### Long terme
- [ ] API REST
- [ ] Dashboard d'analyse
- [ ] Base de données de problèmes

---

## 10. Conclusion

### Résumé des réalisations
✓ Solveur fonctionnel conforme au cours
✓ Interface web moderne et accessible
✓ Code propre et documenté
✓ Déployé en production

### Compétences démontrées
- Algorithmique (Simplexe)
- Programmation orientée objet
- Développement web (Streamlit)
- DevOps (Git, déploiement)
- Documentation technique

### Impact
Outil pédagogique utilisable par tous les étudiants pour :
- Vérifier leurs exercices
- Comprendre la méthode du Simplexe
- Visualiser les solutions

---

## Annexes

### A. Commandes utiles

```bash
# Lancer localement
streamlit run app.py

# Tester le solveur
python test_mvp.py

# Menu console
python examples/main.py
```

### B. Exemple de code d'utilisation

```python
from src.models import ProblemePL
from src.simplexe import SimplexeSolveur

# Créer un problème
probleme = ProblemePL("Mon problème")
probleme.definir_fonction_objectif([1200, 1000], maximiser=True)
probleme.ajouter_contrainte_inegalite([3, 4], 160)
probleme.ajouter_contrainte_inegalite([6, 3], 180)

# Résoudre
solveur = SimplexeSolveur()
tableaux = solveur.resoudre([1200, 1000], [[3, 4], [6, 3]], [160, 180])

# Afficher les tableaux
for tableau in tableaux:
    print(solveur.afficher_tableau(tableau))
```

### C. Ressources

- Repo GitHub : https://github.com/KEVINBMK/programmation-lineaire-mvp
- Application : https://kevinbmk-programmation-lineaire-mvp.streamlit.app
- Documentation Streamlit : https://docs.streamlit.io
- Documentation NumPy : https://numpy.org/doc/

---

**Projet réalisé par : KEVIN**
**Date : Février 2026**
**Université : UPC - L4**
**Cours : Recherche Opérationnelle**
