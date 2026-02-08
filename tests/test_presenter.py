"""
Tests unitaires pour le module Presenter.
Teste la classe LinearProgramPresenter et ses méthodes.
"""

import unittest
from unittest.mock import Mock
from src.model import LinearProgramModel
from src.presenter import LinearProgramPresenter


class TestLinearProgramPresenter(unittest.TestCase):
    """
    Classe de tests pour LinearProgramPresenter.
    """
    
    def setUp(self):
        """
        Initialise un nouveau presenter avant chaque test.
        """
        self.model = LinearProgramModel()
        self.presenter = LinearProgramPresenter(self.model)
    
    def test_initialisation(self):
        """
        Test de l'initialisation du presenter.
        """
        self.assertIsNotNone(self.presenter.model)
        self.assertEqual(self.presenter.model, self.model)
    
    def test_valider_entrée_valide(self):
        """
        Test de validation avec des entrées valides.
        """
        c = [1, 2, 3]
        A_ub = [[1, 2, 3], [4, 5, 6]]
        b_ub = [10, 20]
        
        est_valide, message = self.presenter.valider_entrée(c, A_ub, b_ub)
        
        self.assertTrue(est_valide)
        self.assertIsNone(message)
    
    def test_valider_entrée_c_vide(self):
        """
        Test avec fonction objectif vide.
        """
        c = []
        
        est_valide, message = self.presenter.valider_entrée(c)
        
        self.assertFalse(est_valide)
        self.assertIn("vide", message.lower())
    
    def test_valider_entrée_c_non_numérique(self):
        """
        Test avec fonction objectif non numérique.
        """
        c = [1, "deux", 3]
        
        est_valide, message = self.presenter.valider_entrée(c)
        
        self.assertFalse(est_valide)
        self.assertIn("nombres", message.lower())
    
    def test_valider_entrée_dimensions_incompatibles(self):
        """
        Test avec dimensions incompatibles entre A_ub et c.
        """
        c = [1, 2]
        A_ub = [[1, 2, 3]]  # 3 colonnes au lieu de 2
        b_ub = [10]
        
        est_valide, message = self.presenter.valider_entrée(c, A_ub, b_ub)
        
        self.assertFalse(est_valide)
        self.assertIn("colonnes", message.lower())
    
    def test_valider_entrée_A_ub_sans_b_ub(self):
        """
        Test avec A_ub fourni mais pas b_ub.
        """
        c = [1, 2]
        A_ub = [[1, 2]]
        
        est_valide, message = self.presenter.valider_entrée(c, A_ub, None)
        
        self.assertFalse(est_valide)
        self.assertIn("b_ub", message)
    
    def test_valider_entrée_bornes_invalides(self):
        """
        Test avec bornes invalides.
        """
        c = [1, 2]
        bounds = [(5, 1), (0, 10)]  # min > max pour la première borne
        
        est_valide, message = self.presenter.valider_entrée(c, bounds=bounds)
        
        self.assertFalse(est_valide)
        self.assertIn("min", message.lower())
    
    def test_valider_entrée_nombre_bornes_incorrect(self):
        """
        Test avec nombre de bornes incorrect.
        """
        c = [1, 2, 3]
        bounds = [(0, 10), (0, 10)]  # Seulement 2 bornes pour 3 variables
        
        est_valide, message = self.presenter.valider_entrée(c, bounds=bounds)
        
        self.assertFalse(est_valide)
        self.assertIn("bornes", message.lower())
    
    def test_formater_résultat_succès(self):
        """
        Test du formatage d'un résultat réussi.
        """
        résultat = {
            'succès': True,
            'x': [1.0, 2.0, 3.0],
            'valeur_optimale': 10.5,
            'message': 'Optimization terminated successfully.'
        }
        
        formaté = self.presenter.formater_résultat(résultat)
        
        self.assertIn("Résolution réussie", formaté)
        self.assertIn("Solution optimale", formaté)
        self.assertIn("1.000000", formaté)
        self.assertIn("10.500000", formaté)
    
    def test_formater_résultat_échec(self):
        """
        Test du formatage d'un résultat échoué.
        """
        résultat = {
            'succès': False,
            'message': 'Le problème est infaisable'
        }
        
        formaté = self.presenter.formater_résultat(résultat)
        
        self.assertIn("Échec", formaté)
        self.assertIn("infaisable", formaté)
    
    def test_formater_résultat_none(self):
        """
        Test du formatage avec résultat None.
        """
        formaté = self.presenter.formater_résultat(None)
        
        self.assertIn("Aucun résultat", formaté)
    
    def test_résoudre_avec_validation(self):
        """
        Test de la méthode résoudre qui inclut la validation.
        """
        c = [1, 2]
        A_ub = [[1, 1]]
        b_ub = [10]
        bounds = [(0, None), (0, None)]
        
        résultat = self.presenter.résoudre(c, A_ub, b_ub, bounds=bounds)
        
        # Le résultat devrait être valide
        self.assertIsNotNone(résultat)
        self.assertIn('succès', résultat)
    
    def test_résoudre_avec_entrée_invalide(self):
        """
        Test de résoudre avec entrée invalide.
        """
        c = []  # Vide, donc invalide
        
        résultat = self.presenter.résoudre(c)
        
        self.assertFalse(résultat['succès'])
        self.assertIn("validation", résultat['message'].lower())


if __name__ == '__main__':
    unittest.main()
