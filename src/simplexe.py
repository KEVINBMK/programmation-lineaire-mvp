"""
simplexe.py
-----------
Implémentation de l'algorithme du Simplexe avec affichage des tableaux
comme enseigné dans le cours de Recherche Opérationnelle.

La méthode suit les étapes :
1. Construire le tableau initial (forme standard)
2. Identifier la variable entrante (plus grand coefficient positif dans Δ)
3. Identifier la variable sortante (plus petit ratio positif R = C/colonne entrante)
4. Appliquer le pivot (règle du rectangle)
5. Répéter jusqu'à ce que tous les Δ soient négatifs ou nuls
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TableauSimplexe:
    """
    Représente un tableau du simplexe à une itération donnée.
    
    Structure du tableau :
    HB (Hors Base) : Variables sur la première ligne
    B (Base) : Variables dans la première colonne
    """
    # Matrice des coefficients (sans la ligne Δ)
    matrice: np.ndarray
    
    # Ligne Δ (dernière ligne)
    delta: np.ndarray
    
    # Colonne C (termes constants / solution actuelle)
    colonne_c: np.ndarray
    
    # Valeur de -Z (coin inférieur droit)
    valeur_z: float
    
    # Noms des variables hors base (HB)
    vars_hb: List[str]
    
    # Noms des variables dans la base (B)
    vars_base: List[str]
    
    # Indice de la variable entrante (-1 si aucune)
    var_entrante_idx: int = -1
    
    # Indice de la variable sortante (-1 si aucune)
    var_sortante_idx: int = -1
    
    # Colonne des ratios R (pour affichage)
    colonne_r: Optional[np.ndarray] = None
    
    # Numéro de l'itération
    iteration: int = 0
    
    # Message d'état
    message: str = ""


class SimplexeSolveur:
    """
    Solveur utilisant l'algorithme du Simplexe avec affichage des tableaux.
    Implémente la méthode vue en cours.
    """
    
    def __init__(self):
        """Initialise le solveur."""
        self.tableaux: List[TableauSimplexe] = []
        self.solution_trouvee = False
        self.solution_infinie = False
        self.valeur_optimale = None
        self.variables_solution = {}
    
    def resoudre(self, c: List[float], A: List[List[float]], b: List[float],
                 noms_vars: Optional[List[str]] = None, maximiser: bool = True) -> List[TableauSimplexe]:
        """
        Résout un problème de programmation linéaire sous forme standard.
        
        Args:
            c: Coefficients de la fonction objectif (à maximiser)
            A: Matrice des contraintes (Ax <= b)
            b: Termes constants des contraintes
            noms_vars: Noms des variables principales (optionnel)
            maximiser: True pour maximiser, False pour minimiser
        
        Returns:
            Liste des tableaux du simplexe (un par itération)
        
        Exemple du cours :
            Max Z = 1200x1 + 1000x2
            3x1 + 4x2 <= 160
            6x1 + 3x2 <= 180
            
            c = [1200, 1000]
            A = [[3, 4], [6, 3]]
            b = [160, 180]
        """
        self.tableaux = []
        self.solution_trouvee = False
        self.solution_infinie = False
        
        n_vars = len(c)  # Nombre de variables principales
        n_contraintes = len(b)  # Nombre de contraintes
        
        # Noms des variables
        if noms_vars is None:
            noms_vars = [f"x{i+1}" for i in range(n_vars)]
        
        # Noms des variables d'écart
        noms_ecart = [f"t{i+1}" for i in range(n_contraintes)]
        
        # Si minimisation, on inverse les coefficients
        if not maximiser:
            c = [-ci for ci in c]
        
        # ============================================================
        # CONSTRUCTION DU TABLEAU INITIAL
        # ============================================================
        
        # Variables Hors Base (HB) : les variables principales
        vars_hb = noms_vars.copy()
        
        # Variables dans la Base (B) : les variables d'écart
        vars_base = noms_ecart.copy()
        
        # Matrice du tableau (coefficients des contraintes)
        # Chaque ligne correspond à une contrainte
        matrice = np.array(A, dtype=float)
        
        # Colonne C : termes constants
        colonne_c = np.array(b, dtype=float)
        
        # Ligne Δ : coefficients de la fonction objectif
        # Au départ, ce sont les coefficients de Z
        delta = np.array(c, dtype=float)
        
        # Valeur initiale de -Z
        valeur_z = 0.0
        
        # Créer le tableau initial
        tableau_initial = TableauSimplexe(
            matrice=matrice.copy(),
            delta=delta.copy(),
            colonne_c=colonne_c.copy(),
            valeur_z=valeur_z,
            vars_hb=vars_hb.copy(),
            vars_base=vars_base.copy(),
            iteration=0,
            message="Tableau initial - Solution de départ : variables principales = 0"
        )
        self.tableaux.append(tableau_initial)
        
        # ============================================================
        # ITERATIONS DU SIMPLEXE
        # ============================================================
        
        iteration = 0
        max_iterations = 100  # Sécurité contre les boucles infinies
        
        while iteration < max_iterations:
            iteration += 1
            
            # ---------------------------------------------------------
            # CRITÈRE D'ARRÊT : tous les Δ sont négatifs ou nuls
            # ---------------------------------------------------------
            if np.all(delta <= 0):
                self.solution_trouvee = True
                self.valeur_optimale = -valeur_z if maximiser else valeur_z
                
                # Récupérer les valeurs des variables
                for i, var in enumerate(vars_base):
                    self.variables_solution[var] = colonne_c[i]
                for var in vars_hb:
                    self.variables_solution[var] = 0.0
                
                # Mettre à jour le message du dernier tableau
                self.tableaux[-1].message = (
                    f"SOLUTION OPTIMALE TROUVÉE !\n"
                    f"Tous les coefficients Δ sont ≤ 0.\n"
                    f"Valeur optimale Z = {self.valeur_optimale:.4f}"
                )
                break
            
            # ---------------------------------------------------------
            # CRITÈRE DE SÉLECTION DE LA VARIABLE ENTRANTE
            # On choisit la variable HB avec le plus grand Δ positif
            # ---------------------------------------------------------
            var_entrante_idx = np.argmax(delta)
            var_entrante = vars_hb[var_entrante_idx]
            
            # Colonne de la variable entrante
            colonne_entrante = matrice[:, var_entrante_idx]
            
            # ---------------------------------------------------------
            # VÉRIFICATION : solution infinie ?
            # Si tous les coefficients de la colonne entrante sont <= 0
            # ---------------------------------------------------------
            if np.all(colonne_entrante <= 0):
                self.solution_infinie = True
                self.tableaux[-1].message = (
                    f"SOLUTION INFINIE !\n"
                    f"La variable {var_entrante} a tous ses coefficients ≤ 0."
                )
                break
            
            # ---------------------------------------------------------
            # CRITÈRE DE SÉLECTION DE LA VARIABLE SORTANTE
            # On calcule les ratios R = C / colonne_entrante
            # On prend le plus petit ratio positif
            # ---------------------------------------------------------
            ratios = np.full(len(colonne_c), np.inf)
            for i in range(len(colonne_c)):
                if colonne_entrante[i] > 0:
                    ratios[i] = colonne_c[i] / colonne_entrante[i]
            
            var_sortante_idx = np.argmin(ratios)
            var_sortante = vars_base[var_sortante_idx]
            
            # Valeur du pivot
            pivot = matrice[var_sortante_idx, var_entrante_idx]
            
            # Créer un tableau avec les infos de cette itération
            tableau_pivot = TableauSimplexe(
                matrice=matrice.copy(),
                delta=delta.copy(),
                colonne_c=colonne_c.copy(),
                valeur_z=valeur_z,
                vars_hb=vars_hb.copy(),
                vars_base=vars_base.copy(),
                var_entrante_idx=var_entrante_idx,
                var_sortante_idx=var_sortante_idx,
                colonne_r=ratios.copy(),
                iteration=iteration,
                message=(
                    f"Itération {iteration}\n"
                    f"• Variable entrante : {var_entrante} (Δ = {delta[var_entrante_idx]:.2f})\n"
                    f"• Variable sortante : {var_sortante} (R = {ratios[var_sortante_idx]:.2f})\n"
                    f"• Pivot = {pivot:.2f}"
                )
            )
            self.tableaux.append(tableau_pivot)
            
            # ---------------------------------------------------------
            # APPLICATION DU PIVOT (Règle du rectangle)
            # ---------------------------------------------------------
            
            # 1. Diviser la ligne du pivot par le pivot
            matrice[var_sortante_idx, :] /= pivot
            colonne_c[var_sortante_idx] /= pivot
            
            # 2. Mettre à zéro les autres éléments de la colonne du pivot
            for i in range(len(vars_base)):
                if i != var_sortante_idx:
                    facteur = matrice[i, var_entrante_idx]
                    matrice[i, :] -= facteur * matrice[var_sortante_idx, :]
                    colonne_c[i] -= facteur * colonne_c[var_sortante_idx]
            
            # 3. Mettre à jour la ligne Δ
            facteur_delta = delta[var_entrante_idx]
            delta -= facteur_delta * matrice[var_sortante_idx, :]
            valeur_z -= facteur_delta * colonne_c[var_sortante_idx]
            
            # 4. Échanger les variables (entrante <-> sortante)
            vars_base[var_sortante_idx] = var_entrante
            vars_hb[var_entrante_idx] = var_sortante
        
        return self.tableaux
    
    def afficher_tableau(self, tableau: TableauSimplexe) -> str:
        """
        Génère une représentation textuelle d'un tableau du simplexe.
        
        Args:
            tableau: Le tableau à afficher
        
        Returns:
            Chaîne de caractères formatée
        """
        lignes = []
        
        # Titre
        if tableau.iteration == 0:
            lignes.append(f"{'='*60}")
            lignes.append("TABLEAU INITIAL")
            lignes.append(f"{'='*60}")
        else:
            lignes.append(f"{'='*60}")
            lignes.append(f"TABLEAU {tableau.iteration}")
            lignes.append(f"{'='*60}")
        
        # En-tête
        header = ["HB/B"] + tableau.vars_hb + ["C"]
        if tableau.colonne_r is not None:
            header.append("R")
        
        # Largeur des colonnes
        col_width = 12
        
        # Ligne d'en-tête
        lignes.append(" | ".join(f"{h:>{col_width}}" for h in header))
        lignes.append("-" * (len(header) * (col_width + 3)))
        
        # Lignes des variables de base
        for i, var_base in enumerate(tableau.vars_base):
            row = [var_base]
            for j in range(len(tableau.vars_hb)):
                val = tableau.matrice[i, j]
                # Marquer le pivot
                if i == tableau.var_sortante_idx and j == tableau.var_entrante_idx:
                    row.append(f"[{val:.2f}]")
                else:
                    row.append(f"{val:.2f}")
            row.append(f"{tableau.colonne_c[i]:.2f}")
            
            if tableau.colonne_r is not None:
                if tableau.colonne_r[i] == np.inf:
                    row.append("-")
                else:
                    row.append(f"{tableau.colonne_r[i]:.2f}")
            
            lignes.append(" | ".join(f"{r:>{col_width}}" for r in row))
        
        # Ligne Δ
        lignes.append("-" * (len(header) * (col_width + 3)))
        row_delta = ["Δ"]
        for j in range(len(tableau.vars_hb)):
            val = tableau.delta[j]
            if j == tableau.var_entrante_idx and tableau.iteration > 0:
                row_delta.append(f"[{val:.2f}]")
            else:
                row_delta.append(f"{val:.2f}")
        row_delta.append(f"{tableau.valeur_z:.2f}")
        if tableau.colonne_r is not None:
            row_delta.append("")
        
        lignes.append(" | ".join(f"{r:>{col_width}}" for r in row_delta))
        
        # Message
        if tableau.message:
            lignes.append("")
            lignes.append(tableau.message)
        
        return "\n".join(lignes)
    
    def afficher_solution(self) -> str:
        """
        Affiche la solution finale.
        
        Returns:
            Chaîne de caractères avec la solution
        """
        lignes = []
        lignes.append(f"\n{'='*60}")
        lignes.append("RÉSULTAT FINAL")
        lignes.append(f"{'='*60}\n")
        
        if self.solution_trouvee:
            lignes.append("✓ Solution optimale trouvée !")
            lignes.append(f"\nValeur optimale : Z = {self.valeur_optimale:.4f}")
            lignes.append("\nValeurs des variables :")
            
            # Trier les variables pour un affichage cohérent
            for var, val in sorted(self.variables_solution.items()):
                if var.startswith('x') or var.startswith('y'):
                    lignes.append(f"  • {var} = {val:.4f}")
            
            lignes.append("\nVariables d'écart :")
            for var, val in sorted(self.variables_solution.items()):
                if var.startswith('t') or var.startswith('s'):
                    lignes.append(f"  • {var} = {val:.4f}")
        
        elif self.solution_infinie:
            lignes.append("✗ Le problème a une solution infinie.")
        
        else:
            lignes.append("✗ Aucune solution trouvée.")
        
        return "\n".join(lignes)


def exemple_cours():
    """
    Exemple du cours :
    Max Z = 1200x1 + 1000x2
    3x1 + 4x2 <= 160
    6x1 + 3x2 <= 180
    x1, x2 >= 0
    """
    print("\n" + "#"*60)
    print("# EXEMPLE DU COURS")
    print("#"*60)
    
    # Coefficients de la fonction objectif
    c = [1200, 1000]
    
    # Matrice des contraintes
    A = [
        [3, 4],  # 3x1 + 4x2 <= 160
        [6, 3]   # 6x1 + 3x2 <= 180
    ]
    
    # Termes constants
    b = [160, 180]
    
    # Résoudre
    solveur = SimplexeSolveur()
    tableaux = solveur.resoudre(c, A, b)
    
    # Afficher tous les tableaux
    for tableau in tableaux:
        print("\n")
        print(solveur.afficher_tableau(tableau))
    
    # Afficher la solution
    print(solveur.afficher_solution())


def resoudre_rapide(probleme, verbose: bool = True):
    """
    Fonction utilitaire pour résoudre rapidement un problème avec le Simplexe.
    
    Args:
        probleme: Le problème à résoudre (ProblemePL)
        verbose: Afficher les détails ou non
    
    Returns:
        La solution du problème (Solution)
    """
    from .models import Solution
    import numpy as np
    
    # Extraire les données du problème
    c = probleme.c.tolist()
    A = probleme.A_ub.tolist() if probleme.A_ub is not None else []
    b = probleme.b_ub.tolist() if probleme.b_ub is not None else []
    noms_vars = probleme.noms_variables
    maximiser = (probleme.type_optimisation == 'max')
    
    if verbose:
        print("\n🔍 Résolution en cours avec la méthode du Simplexe...")
        print(f"   Variables : {len(c)}")
        print(f"   Contraintes : {len(b)}")
    
    # Résoudre
    solveur = SimplexeSolveur()
    tableaux = solveur.resoudre(c, A, b, noms_vars, maximiser)
    
    # Créer l'objet Solution
    solution = Solution()
    solution.noms_variables = noms_vars
    
    if solveur.solution_trouvee:
        valeurs_vars = [solveur.variables_solution.get(nom, 0.0) for nom in noms_vars]
        solution.succes = True
        solution.valeurs_variables = np.array(valeurs_vars)
        solution.valeur_objectif = solveur.valeur_optimale
        solution.message = "Solution optimale trouvée"
        
        if verbose:
            print("✓ Solution trouvée avec succès!")
    else:
        solution.succes = False
        solution.valeurs_variables = None
        solution.valeur_objectif = None
        solution.message = "Aucune solution trouvée" if not solveur.solution_infinie else "Solution infinie"
        
        if verbose:
            print(f"✗ {solution.message}")
    
    return solution


if __name__ == "__main__":
    exemple_cours()
