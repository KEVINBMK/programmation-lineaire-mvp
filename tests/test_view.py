"""
Tests unitaires pour le module View.
Teste la classe ConsoleView et ses méthodes.
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.view import ConsoleView


class TestConsoleView(unittest.TestCase):
    """
    Classe de tests pour ConsoleView.
    """
    
    def setUp(self):
        """
        Initialise une nouvelle vue avant chaque test.
        """
        self.view = ConsoleView()
    
    def test_initialisation(self):
        """
        Test de l'initialisation de la vue.
        """
        self.assertIsNotNone(self.view)
    
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_afficher_menu(self, mock_stdout, mock_input):
        """
        Test de l'affichage du menu.
        """
        choix = self.view.afficher_menu()
        
        self.assertEqual(choix, '1')
        output = mock_stdout.getvalue()
        self.assertIn("Menu principal", output)
        self.assertIn("Quitter", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_obtenir_exemple_simple(self, mock_stdout):
        """
        Test de l'obtention d'un exemple simple.
        """
        exemple = self.view.obtenir_exemple_simple()
        
        self.assertIsNotNone(exemple)
        self.assertIn('c', exemple)
        self.assertIn('A_ub', exemple)
        self.assertIn('b_ub', exemple)
        self.assertIn('bounds', exemple)
        
        # Vérifier le contenu
        self.assertEqual(exemple['c'], [-1, 4])
        self.assertEqual(len(exemple['A_ub']), 2)
        self.assertEqual(len(exemple['b_ub']), 2)
        
        output = mock_stdout.getvalue()
        self.assertIn("EXEMPLE", output)
    
    @patch('builtins.input', side_effect=['1 2 3', '2', '1 1 1', '10', '2 2 2', '20', 'n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_données_avec_contraintes(self, mock_stdout, mock_input):
        """
        Test de la demande de données avec contraintes.
        """
        données = self.view.demander_données()
        
        self.assertIsNotNone(données)
        self.assertEqual(données['c'], [1.0, 2.0, 3.0])
        self.assertEqual(len(données['A_ub']), 2)
        self.assertEqual(len(données['b_ub']), 2)
        self.assertIsNone(données['bounds'])
    
    @patch('builtins.input', side_effect=['1 2', '0', 'n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_données_sans_contraintes(self, mock_stdout, mock_input):
        """
        Test de la demande de données sans contraintes.
        """
        données = self.view.demander_données()
        
        self.assertIsNotNone(données)
        self.assertEqual(données['c'], [1.0, 2.0])
        self.assertIsNone(données['A_ub'])
        self.assertIsNone(données['b_ub'])
        self.assertIsNone(données['bounds'])
    
    @patch('builtins.input', side_effect=['1 2', '0', 'o', '0', '10', '', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_données_avec_bornes(self, mock_stdout, mock_input):
        """
        Test de la demande de données avec bornes.
        """
        données = self.view.demander_données()
        
        self.assertIsNotNone(données)
        self.assertEqual(données['c'], [1.0, 2.0])
        self.assertIsNotNone(données['bounds'])
        self.assertEqual(len(données['bounds']), 2)
        self.assertEqual(données['bounds'][0], (0.0, 10.0))
        self.assertEqual(données['bounds'][1], (None, 5.0))
    
    @patch('builtins.input', return_value='abc')
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_données_erreur_coefficients(self, mock_stdout, mock_input):
        """
        Test avec coefficients invalides.
        """
        données = self.view.demander_données()
        
        self.assertIsNone(données)
        output = mock_stdout.getvalue()
        self.assertIn("Erreur", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_montrer_résultat(self, mock_stdout):
        """
        Test de l'affichage d'un résultat.
        """
        résultat = "Résultat du test"
        
        self.view.montrer_résultat(résultat)
        
        output = mock_stdout.getvalue()
        self.assertIn(résultat, output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_afficher_message(self, mock_stdout):
        """
        Test de l'affichage d'un message.
        """
        message = "Ceci est un message de test"
        
        self.view.afficher_message(message)
        
        output = mock_stdout.getvalue()
        self.assertIn(message, output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_afficher_erreur(self, mock_stdout):
        """
        Test de l'affichage d'une erreur.
        """
        erreur = "Ceci est une erreur de test"
        
        self.view.afficher_erreur(erreur)
        
        output = mock_stdout.getvalue()
        self.assertIn(erreur, output)
        self.assertIn("Erreur", output)
    
    @patch('builtins.input', return_value='o')
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_continuer_oui(self, mock_stdout, mock_input):
        """
        Test de demander_continuer avec réponse oui.
        """
        résultat = self.view.demander_continuer()
        
        self.assertTrue(résultat)
    
    @patch('builtins.input', return_value='n')
    @patch('sys.stdout', new_callable=StringIO)
    def test_demander_continuer_non(self, mock_stdout, mock_input):
        """
        Test de demander_continuer avec réponse non.
        """
        résultat = self.view.demander_continuer()
        
        self.assertFalse(résultat)


if __name__ == '__main__':
    unittest.main()
