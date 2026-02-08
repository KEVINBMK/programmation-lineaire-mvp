"""
Module Model pour la résolution de problèmes de programmation linéaire.
Utilise scipy.optimize.linprog pour résoudre les problèmes d'optimisation.
"""

from scipy.optimize import linprog
import numpy as np


class LinearProgramModel:
    """
    Classe pour résoudre des problèmes de programmation linéaire.
    
    Cette classe encapsule la logique backend pour résoudre des problèmes
    d'optimisation linéaire en utilisant la bibliothèque scipy.
    """
    
    def __init__(self):
        """
        Initialise le modèle de programmation linéaire.
        """
        self.résultat = None
        self.succès = False
    
    def résoudre_problème(self, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, 
                         bounds=None, method='highs'):
        """
        Résout un problème de programmation linéaire.
        
        Minimise : c^T * x
        Sous contraintes :
            A_ub @ x <= b_ub  (contraintes d'inégalité)
            A_eq @ x == b_eq  (contraintes d'égalité)
            bounds            (bornes sur les variables)
        
        Args:
            c (list ou array): Coefficients de la fonction objectif à minimiser
            A_ub (array, optionnel): Matrice des contraintes d'inégalité
            b_ub (array, optionnel): Vecteur des contraintes d'inégalité
            A_eq (array, optionnel): Matrice des contraintes d'égalité
            b_eq (array, optionnel): Vecteur des contraintes d'égalité
            bounds (list de tuples, optionnel): Bornes pour chaque variable [(min, max), ...]
            method (str): Méthode de résolution ('highs', 'simplex', etc.)
        
        Returns:
            dict: Dictionnaire contenant les résultats:
                - 'succès': Boolean indiquant si la résolution a réussi
                - 'x': Solution optimale (si succès)
                - 'valeur_optimale': Valeur de la fonction objectif (si succès)
                - 'message': Message décrivant le résultat
                - 'statut': Code de statut de la résolution
        """
        try:
            # Convertir les entrées en arrays numpy
            c = np.array(c)
            
            if A_ub is not None:
                A_ub = np.array(A_ub)
            if b_ub is not None:
                b_ub = np.array(b_ub)
            if A_eq is not None:
                A_eq = np.array(A_eq)
            if b_eq is not None:
                b_eq = np.array(b_eq)
            
            # Résoudre le problème
            résultat = linprog(c=c, A_ub=A_ub, b_ub=b_ub, 
                             A_eq=A_eq, b_eq=b_eq, 
                             bounds=bounds, method=method)
            
            self.résultat = résultat
            self.succès = résultat.success
            
            # Formatter les résultats
            résultat_dict = {
                'succès': résultat.success,
                'message': résultat.message,
                'statut': résultat.status
            }
            
            if résultat.success:
                résultat_dict['x'] = résultat.x.tolist()
                résultat_dict['valeur_optimale'] = float(résultat.fun)
            
            return résultat_dict
            
        except Exception as e:
            # Gérer les erreurs
            return {
                'succès': False,
                'message': f'Erreur lors de la résolution: {str(e)}',
                'statut': -1
            }
    
    def obtenir_dernier_résultat(self):
        """
        Retourne le dernier résultat de résolution.
        
        Returns:
            object: Objet résultat de scipy ou None
        """
        return self.résultat
