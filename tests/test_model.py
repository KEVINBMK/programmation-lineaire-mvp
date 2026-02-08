"""
Tests unitaires pour le module Model.
Teste la classe LinearProgramModel et ses méthodes.
"""

import unittest
import numpy as np
from src.model import LinearProgramModel


class TestLinearProgramModel(unittest.TestCase):
    """
    Classe de tests pour LinearProgramModel.
    """
    
    def setUp(self):
        """
        Initialise un nouveau modèle avant chaque test.
        """
        self.model = LinearProgramModel()
    
    def test_initialisation(self):
        """
        Test de l'initialisation du modèle.
        """
        self.assertIsNone(self.model.résultat)
        self.assertFalse(self.model.succès)
    
    def test_résoudre_problème_simple(self):
        """
        Test de résolution d'un problème simple.
        Minimiser: -1*x1 + 4*x2
        Sous contraintes:
            -3*x1 + 1*x2 <= 6
            1*x1 + 2*x2 <= 4
            x1, x2 >= 0
        """
        c = [-1, 4]
        A_ub = [[-3, 1], [1, 2]]
        b_ub = [6, 4]
        bounds = [(0, None), (0, None)]
        
        résultat = self.model.résoudre_problème(c, A_ub, b_ub, bounds=bounds)
        
        self.assertTrue(résultat['succès'])
        self.assertIn('x', résultat)
        self.assertIn('valeur_optimale', résultat)
        self.assertEqual(len(résultat['x']), 2)
    
    def test_résoudre_problème_sans_contraintes(self):
        """
        Test avec fonction objectif uniquement (problème non borné).
        """
        c = [-1, -1]
        bounds = [(0, 10), (0, 10)]
        
        résultat = self.model.résoudre_problème(c, bounds=bounds)
        
        # Le problème devrait être résolu avec les bornes
        self.assertTrue(résultat['succès'])
    
    def test_résoudre_problème_infaisable(self):
        """
        Test d'un problème infaisable.
        x1 >= 10 et x1 <= 5 (impossible)
        """
        c = [1, 1]
        A_ub = [[1, 0], [-1, 0]]
        b_ub = [5, -10]
        bounds = [(0, None), (0, None)]
        
        résultat = self.model.résoudre_problème(c, A_ub, b_ub, bounds=bounds)
        
        # Le problème est infaisable
        self.assertFalse(résultat['succès'])
    
    def test_résoudre_avec_contraintes_égalité(self):
        """
        Test avec contraintes d'égalité.
        """
        c = [1, 2]
        A_eq = [[1, 1]]
        b_eq = [5]
        bounds = [(0, None), (0, None)]
        
        résultat = self.model.résoudre_problème(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        
        self.assertTrue(résultat['succès'])
        self.assertIn('x', résultat)
    
    def test_résoudre_avec_erreur_dimension(self):
        """
        Test avec des dimensions incompatibles.
        """
        c = [1, 2]
        A_ub = [[1, 2, 3]]  # 3 colonnes au lieu de 2
        b_ub = [5]
        
        résultat = self.model.résoudre_problème(c, A_ub, b_ub)
        
        # Devrait retourner une erreur
        self.assertFalse(résultat['succès'])
        self.assertIn('Erreur', résultat['message'])
    
    def test_obtenir_dernier_résultat(self):
        """
        Test de la méthode obtenir_dernier_résultat.
        """
        c = [1, 2]
        bounds = [(0, 10), (0, 10)]
        
        self.model.résoudre_problème(c, bounds=bounds)
        
        dernier_résultat = self.model.obtenir_dernier_résultat()
        self.assertIsNotNone(dernier_résultat)


if __name__ == '__main__':
    unittest.main()
