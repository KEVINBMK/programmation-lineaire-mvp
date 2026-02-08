"""
solver.py
---------
Ce fichier contient le solveur pour résoudre les problèmes de programmation linéaire.
On utilise scipy.optimize.linprog qui implémente l'algorithme du simplexe.
"""

import numpy as np
from scipy.optimize import linprog
from .models import ProblemePL, Solution


class SolveurPL:
    """
    Classe qui résout un problème de programmation linéaire.
    """
    
    def __init__(self):
        """Initialise le solveur."""
        self.methode = 'highs'  # Méthode HiGHS (la plus rapide et robuste)
    
    def resoudre(self, probleme: ProblemePL, verbose: bool = False) -> Solution:
        """
        Résout le problème de programmation linéaire.
        
        Args:
            probleme: Instance de ProblemePL à résoudre
            verbose: Si True, affiche des informations détaillées
        
        Returns:
            Une instance de Solution contenant le résultat
        """
        # Vérifier que le problème est bien défini
        if probleme.c is None:
            raise ValueError("La fonction objectif n'est pas définie!")
        
        # Préparer les coefficients de la fonction objectif
        # scipy.optimize.linprog minimise par défaut, donc si on veut maximiser,
        # on multiplie par -1
        c = probleme.c.copy()
        if probleme.type_optimisation == 'max':
            c = -c  # Transformer max en min
        
        # Préparer les bornes (par défaut: variables >= 0)
        bounds = probleme.bounds
        if bounds is None:
            bounds = [(0, None) for _ in range(len(c))]
        
        if verbose:
            print("🔍 Résolution en cours...")
            print(f"   Méthode : {self.methode}")
            print(f"   Variables : {len(c)}")
            print(f"   Contraintes inégalité : {len(probleme.b_ub) if probleme.b_ub is not None else 0}")
            print(f"   Contraintes égalité : {len(probleme.b_eq) if probleme.b_eq is not None else 0}")
        
        # Résoudre avec scipy
        try:
            resultat = linprog(
                c=c,
                A_ub=probleme.A_ub,
                b_ub=probleme.b_ub,
                A_eq=probleme.A_eq,
                b_eq=probleme.b_eq,
                bounds=bounds,
                method=self.methode
            )
            
            # Créer l'objet Solution
            solution = Solution()
            solution.noms_variables = probleme.noms_variables
            
            if resultat.success:
                solution.succes = True
                solution.valeurs_variables = resultat.x
                
                # Si on avait transformé en minimisation, retransformer la valeur
                if probleme.type_optimisation == 'max':
                    solution.valeur_objectif = -resultat.fun
                else:
                    solution.valeur_objectif = resultat.fun
                
                solution.message = "Solution optimale trouvée"
                
                if verbose:
                    print("✓ Solution trouvée avec succès!")
            else:
                solution.succes = False
                solution.message = resultat.message
                
                if verbose:
                    print(f"✗ Échec: {resultat.message}")
            
            return solution
            
        except Exception as e:
            # En cas d'erreur
            solution = Solution()
            solution.succes = False
            solution.message = f"Erreur lors de la résolution: {str(e)}"
            solution.noms_variables = probleme.noms_variables
            
            if verbose:
                print(f"✗ Erreur: {str(e)}")
            
            return solution
    
    def changer_methode(self, methode: str):
        """
        Change la méthode de résolution.
        
        Args:
            methode: 'highs', 'highs-ds', 'highs-ipm', 'interior-point', 
                    'revised simplex', ou 'simplex'
        """
        methodes_valides = [
            'highs', 'highs-ds', 'highs-ipm', 
            'interior-point', 'revised simplex', 'simplex'
        ]
        
        if methode in methodes_valides:
            self.methode = methode
            print(f"Méthode changée en: {methode}")
        else:
            print(f"Méthode invalide. Méthodes disponibles: {methodes_valides}")


def resoudre_rapide(probleme: ProblemePL, verbose: bool = True) -> Solution:
    """
    Fonction utilitaire pour résoudre rapidement un problème.
    
    Args:
        probleme: Le problème à résoudre
        verbose: Afficher les détails ou non
    
    Returns:
        La solution du problème
    """
    solveur = SolveurPL()
    return solveur.resoudre(probleme, verbose=verbose)
