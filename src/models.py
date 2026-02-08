"""
models.py
---------
Ce fichier contient les classes pour modéliser un problème de programmation linéaire.

Un problème de programmation linéaire standard a la forme :
    Minimiser (ou Maximiser) : c^T * x
    Sous contraintes :
        A_ub * x <= b_ub  (contraintes d'inégalité)
        A_eq * x == b_eq  (contraintes d'égalité)
        bounds : limites sur les variables
"""

import numpy as np
from typing import List, Tuple, Optional


class ProblemePL:
    """
    Classe représentant un problème de programmation linéaire.
    """
    
    def __init__(self, nom: str = "Problème PL"):
        """
        Initialise un nouveau problème de programmation linéaire.
        
        Args:
            nom: Le nom du problème pour l'identifier
        """
        self.nom = nom
        
        # Fonction objectif (coefficients)
        self.c = None  # Vecteur des coefficients de la fonction objectif
        
        # Contraintes d'inégalité (A_ub * x <= b_ub)
        self.A_ub = None  # Matrice des contraintes d'inégalité
        self.b_ub = None  # Vecteur du côté droit des inégalités
        
        # Contraintes d'égalité (A_eq * x == b_eq)
        self.A_eq = None  # Matrice des contraintes d'égalité
        self.b_eq = None  # Vecteur du côté droit des égalités
        
        # Bornes sur les variables (par défaut >= 0)
        self.bounds = None
        
        # Type de problème : 'min' ou 'max'
        self.type_optimisation = 'max'
        
        # Noms des variables pour un affichage plus clair
        self.noms_variables = []
    
    def definir_fonction_objectif(self, coefficients: List[float], maximiser: bool = True):
        """
        Définit la fonction objectif à optimiser.
        
        Args:
            coefficients: Liste des coefficients de la fonction objectif
            maximiser: True pour maximiser, False pour minimiser
        """
        self.c = np.array(coefficients, dtype=float)
        self.type_optimisation = 'max' if maximiser else 'min'
        
        # Créer des noms de variables par défaut si non définis
        if not self.noms_variables:
            self.noms_variables = [f'x{i+1}' for i in range(len(coefficients))]
    
    def ajouter_contrainte_inegalite(self, coefficients: List[float], borne: float):
        """
        Ajoute une contrainte d'inégalité (somme <= borne).
        
        Args:
            coefficients: Coefficients de la contrainte
            borne: Valeur maximum (côté droit de l'inégalité)
        """
        contrainte = np.array(coefficients, dtype=float)
        
        if self.A_ub is None:
            self.A_ub = contrainte.reshape(1, -1)
            self.b_ub = np.array([borne])
        else:
            self.A_ub = np.vstack([self.A_ub, contrainte])
            self.b_ub = np.append(self.b_ub, borne)
    
    def ajouter_contrainte_equalite(self, coefficients: List[float], borne: float):
        """
        Ajoute une contrainte d'égalité (somme == borne).
        
        Args:
            coefficients: Coefficients de la contrainte
            borne: Valeur exacte (côté droit de l'égalité)
        """
        contrainte = np.array(coefficients, dtype=float)
        
        if self.A_eq is None:
            self.A_eq = contrainte.reshape(1, -1)
            self.b_eq = np.array([borne])
        else:
            self.A_eq = np.vstack([self.A_eq, contrainte])
            self.b_eq = np.append(self.b_eq, borne)
    
    def definir_bornes(self, bornes: List[Tuple[Optional[float], Optional[float]]]):
        """
        Définit les bornes pour chaque variable.
        
        Args:
            bornes: Liste de tuples (min, max) pour chaque variable
                   None signifie pas de borne
                   Ex: [(0, None), (0, 10)] pour x1 >= 0, 0 <= x2 <= 10
        """
        self.bounds = bornes
    
    def definir_noms_variables(self, noms: List[str]):
        """
        Définit des noms personnalisés pour les variables.
        
        Args:
            noms: Liste des noms des variables
        """
        self.noms_variables = noms
    
    def afficher_probleme(self):
        """
        Affiche une représentation textuelle du problème.
        """
        print(f"\n{'='*60}")
        print(f"Problème : {self.nom}")
        print(f"{'='*60}\n")
        
        # Fonction objectif
        objectif = "Maximiser" if self.type_optimisation == 'max' else "Minimiser"
        print(f"{objectif} :")
        if self.c is not None:
            termes = [f"{self.c[i]:.2f}*{self.noms_variables[i]}" 
                     for i in range(len(self.c))]
            print(f"  Z = {' + '.join(termes)}")
        
        # Contraintes d'inégalité
        if self.A_ub is not None:
            print("\nSous contraintes d'inégalité (<=):")
            for i, (ligne, b) in enumerate(zip(self.A_ub, self.b_ub)):
                termes = [f"{ligne[j]:.2f}*{self.noms_variables[j]}" 
                         for j in range(len(ligne)) if ligne[j] != 0]
                print(f"  {' + '.join(termes)} <= {b:.2f}")
        
        # Contraintes d'égalité
        if self.A_eq is not None:
            print("\nSous contraintes d'égalité (==):")
            for i, (ligne, b) in enumerate(zip(self.A_eq, self.b_eq)):
                termes = [f"{ligne[j]:.2f}*{self.noms_variables[j]}" 
                         for j in range(len(ligne)) if ligne[j] != 0]
                print(f"  {' + '.join(termes)} == {b:.2f}")
        
        # Bornes
        if self.bounds:
            print("\nBornes sur les variables:")
            for i, (min_val, max_val) in enumerate(self.bounds):
                min_str = f"{min_val:.2f}" if min_val is not None else "-∞"
                max_str = f"{max_val:.2f}" if max_val is not None else "+∞"
                print(f"  {min_str} <= {self.noms_variables[i]} <= {max_str}")
        
        print(f"\n{'='*60}\n")


class Solution:
    """
    Classe représentant la solution d'un problème de programmation linéaire.
    """
    
    def __init__(self):
        """Initialise une solution vide."""
        self.succes = False
        self.valeurs_variables = None
        self.valeur_objectif = None
        self.message = ""
        self.noms_variables = []
    
    def afficher_solution(self):
        """Affiche la solution de manière formatée."""
        print(f"\n{'='*60}")
        print("SOLUTION")
        print(f"{'='*60}\n")
        
        if self.succes:
            print("✓ Solution optimale trouvée!\n")
            
            # Valeur de la fonction objectif
            print(f"Valeur optimale : Z = {self.valeur_objectif:.4f}\n")
            
            # Valeurs des variables
            print("Valeurs des variables :")
            for nom, valeur in zip(self.noms_variables, self.valeurs_variables):
                print(f"  {nom} = {valeur:.4f}")
        else:
            print("✗ Pas de solution trouvée")
            print(f"Raison : {self.message}")
        
        print(f"\n{'='*60}\n")
