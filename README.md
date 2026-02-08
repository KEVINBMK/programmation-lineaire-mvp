# Solveur de Programmation Linéaire 📊

Un programme Python complet pour résoudre des problèmes de programmation linéaire avec une interface interactive et des exemples pédagogiques.

## 📋 Description

Ce projet permet de résoudre des problèmes de **programmation linéaire** (PL), c'est-à-dire des problèmes d'optimisation où :
- La fonction objectif est **linéaire** (ex: maximiser 3x₁ + 2x₂)
- Les contraintes sont **linéaires** (ex: x₁ + x₂ ≤ 10)

## 🎯 Fonctionnalités

- ✅ Résolution de problèmes de maximisation et minimisation
- ✅ Support des contraintes d'inégalité (≤) et d'égalité (=)
- ✅ Gestion des bornes sur les variables
- ✅ Interface interactive avec menu
- ✅ Exemples prédéfinis (production, mélange, transport)
- ✅ Création de problèmes personnalisés
- ✅ Affichage clair des résultats

## 📁 Structure du projet

```
Programmation_lineair/
│
├── main.py              # Point d'entrée - Menu interactif
├── models.py            # Classes ProblemePL et Solution
├── solver.py            # Algorithme de résolution (SolveurPL)
├── examples.py          # Exemples de problèmes classiques
├── requirements.txt     # Dépendances Python
└── README.md           # Ce fichier
```

### Organisation du code

#### 1. **models.py** - Structures de données
- `ProblemePL`: Classe pour modéliser un problème
- `Solution`: Classe pour stocker les résultats

#### 2. **solver.py** - Résolution
- `SolveurPL`: Classe qui utilise scipy pour résoudre
- Méthode du simplexe (algorithme HiGHS par défaut)

#### 3. **examples.py** - Exemples pédagogiques
- Exemple simple (introduction)
- Problème de production
- Problème de mélange
- Problème de transport

#### 4. **main.py** - Interface utilisateur
- Menu interactif
- Création de problèmes personnalisés
- Aide intégrée

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd Programmation_lineair
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

   Cela installera :
   - `scipy` : Pour l'algorithme de résolution
   - `numpy` : Pour les opérations matricielles

## 💻 Utilisation

### Lancer le programme principal

```bash
python main.py
```

Vous verrez un menu interactif avec plusieurs options.

### Lancer les exemples directement

```bash
python examples.py
```

### Utiliser le solveur dans votre code

```python
from models import ProblemePL
from solver import resoudre_rapide

# Créer un problème
probleme = ProblemePL("Mon problème")

# Définir les variables
probleme.definir_noms_variables(['x1', 'x2'])

# Fonction objectif: Maximiser 3x1 + 2x2
probleme.definir_fonction_objectif([3, 2], maximiser=True)

# Ajouter des contraintes
probleme.ajouter_contrainte_inegalite([2, 1], 18)  # 2x1 + x2 <= 18
probleme.ajouter_contrainte_inegalite([2, 3], 42)  # 2x1 + 3x2 <= 42

# Définir les bornes (x1, x2 >= 0)
probleme.definir_bornes([(0, None), (0, None)])

# Résoudre
solution = resoudre_rapide(probleme)

# Afficher la solution
solution.afficher_solution()
```

## 📚 Exemples inclus

### Exemple 1: Problème simple
```
Maximiser: z = 3x₁ + 2x₂
Sous contraintes:
    2x₁ + x₂ ≤ 18
    2x₁ + 3x₂ ≤ 42
    3x₁ + x₂ ≤ 24
    x₁, x₂ ≥ 0
```

### Exemple 2: Production optimale
Une entreprise fabrique deux produits avec des ressources limitées.
Objectif: Maximiser le profit.

### Exemple 3: Problème de mélange
Mélanger différents bruts de pétrole pour obtenir un produit final.
Objectif: Minimiser le coût tout en respectant les spécifications.

### Exemple 4: Transport
Optimiser le transport entre usines et entrepôts.
Objectif: Minimiser les coûts de transport.

## 🧮 Concepts mathématiques

### Forme standard d'un problème de PL

**Maximiser (ou Minimiser):**
```
z = c₁x₁ + c₂x₂ + ... + cₙxₙ
```

**Sous contraintes:**
```
a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤ b₁
a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤ b₂
...
x₁, x₂, ..., xₙ ≥ 0
```

### Algorithme utilisé

Le programme utilise la bibliothèque **scipy** qui implémente:
- **HiGHS**: Solveur moderne très performant (défaut)
- **Simplexe révisé**: Algorithme classique
- **Point intérieur**: Pour les grands problèmes

## 🎓 Cas d'usage

La programmation linéaire peut résoudre de nombreux problèmes réels:

1. **Optimisation de production**
   - Planification de fabrication
   - Allocation de ressources
   - Maximisation du profit

2. **Logistique et transport**
   - Routage optimal
   - Allocation d'entrepôts
   - Minimisation des coûts

3. **Finance**
   - Optimisation de portefeuille
   - Allocation d'actifs
   - Gestion de budget

4. **Industrie**
   - Mélange optimal (raffinage, alimentation)
   - Découpe de matériaux
   - Planification d'équipes

## 🔧 Personnalisation

### Changer la méthode de résolution

```python
from solver import SolveurPL

solveur = SolveurPL()
solveur.changer_methode('interior-point')
solution = solveur.resoudre(probleme)
```

Méthodes disponibles:
- `'highs'` (défaut, recommandé)
- `'highs-ds'`
- `'highs-ipm'`
- `'interior-point'`
- `'revised simplex'`
- `'simplex'`

## 📊 Interprétation des résultats

Après résolution, vous obtenez:
- **Statut**: Solution trouvée ou non
- **Valeur optimale**: Valeur de la fonction objectif
- **Valeurs des variables**: Solution optimale pour chaque variable

## ⚠️ Limites et contraintes

- Le problème doit être **linéaire** (pas de x², xy, etc.)
- Les algorithmes trouvent un **optimum global** (avantage de la PL)
- Pour les problèmes très grands (>10000 variables), considérer des méthodes spécialisées

## 🐛 Dépannage

### Problème: "Pas de solution trouvée"
- Vérifiez que les contraintes ne sont pas contradictoires
- Assurez-vous qu'une solution est possible

### Problème: ImportError
```bash
pip install --upgrade scipy numpy
```

### Problème: Solution non bornée
- Ajoutez des contraintes pour borner les variables
- Vérifiez la formulation du problème

## 📝 TODO / Améliorations futures

- [ ] Support des variables entières (programmation linéaire en nombres entiers)
- [ ] Export des résultats en fichier
- [ ] Visualisation graphique (2D pour 2 variables)
- [ ] Interface graphique (GUI)
- [ ] Import de problèmes depuis fichier

## 👥 Contribution

Ce projet est à but pédagogique. N'hésitez pas à:
- Ajouter de nouveaux exemples
- Améliorer la documentation
- Optimiser le code

## 📄 Licence

Projet éducatif - Libre d'utilisation pour l'apprentissage

## 📞 Support

Pour toute question sur le projet ou la programmation linéaire, consultez:
- La documentation scipy: https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html
- Les exemples dans `examples.py`
- L'aide intégrée (option 7 du menu)

---

**Bon apprentissage de la programmation linéaire! 🎓📊**
