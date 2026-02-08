"""
Module View pour gérer l'interface utilisateur en ligne de commande.
Gère les interactions avec l'utilisateur via la console.
"""


class ConsoleView:
    """
    Classe pour gérer l'interface utilisateur en ligne de commande.
    
    Cette classe gère l'affichage du menu, la collecte des données
    de l'utilisateur et l'affichage des résultats.
    """
    
    def __init__(self):
        """
        Initialise la vue console.
        """
        pass
    
    def afficher_menu(self):
        """
        Affiche le menu principal de l'application.
        
        Returns:
            str: Choix de l'utilisateur
        """
        print("\n" + "=" * 60)
        print("PROGRAMMATION LINÉAIRE - SOLVEUR MVP")
        print("=" * 60)
        print("\nMenu principal:")
        print("  1. Résoudre un problème simple (exemple)")
        print("  2. Résoudre un problème personnalisé")
        print("  3. Quitter")
        print("\n" + "-" * 60)
        
        choix = input("Votre choix (1-3): ").strip()
        return choix
    
    def demander_données(self):
        """
        Demande les données du problème à l'utilisateur.
        
        Returns:
            dict: Dictionnaire contenant les paramètres du problème:
                - 'c': coefficients de la fonction objectif
                - 'A_ub': matrice des contraintes d'inégalité (optionnel)
                - 'b_ub': vecteur des contraintes d'inégalité (optionnel)
                - 'bounds': bornes des variables (optionnel)
        """
        print("\n" + "=" * 60)
        print("SAISIE DES DONNÉES DU PROBLÈME")
        print("=" * 60)
        print("\nNous allons minimiser la fonction: c₁*x₁ + c₂*x₂ + ... + cₙ*xₙ")
        print("Sous contraintes: A*x <= b")
        print()
        
        # Demander la fonction objectif
        print("Fonction objectif (à minimiser):")
        c_input = input("  Entrez les coefficients c séparés par des espaces (ex: 1 2 3): ").strip()
        
        try:
            c = [float(x) for x in c_input.split()]
        except ValueError:
            print("Erreur: Les coefficients doivent être des nombres")
            return None
        
        if len(c) == 0:
            print("Erreur: Au moins un coefficient est requis")
            return None
        
        n_variables = len(c)
        print(f"\n✓ {n_variables} variable(s) détectée(s)")
        
        # Demander les contraintes d'inégalité
        print("\nContraintes d'inégalité (A*x <= b):")
        n_contraintes = input(f"  Nombre de contraintes (0 pour aucune): ").strip()
        
        try:
            n_contraintes = int(n_contraintes)
        except ValueError:
            print("Erreur: Nombre invalide")
            return None
        
        A_ub = None
        b_ub = None
        
        if n_contraintes > 0:
            A_ub = []
            b_ub = []
            
            for i in range(n_contraintes):
                print(f"\n  Contrainte {i+1}:")
                ligne = input(f"    Coefficients (A[{i+1}]) - {n_variables} valeurs séparées par espaces: ").strip()
                
                try:
                    coeffs = [float(x) for x in ligne.split()]
                    if len(coeffs) != n_variables:
                        print(f"Erreur: {n_variables} coefficients requis, {len(coeffs)} fournis")
                        return None
                    A_ub.append(coeffs)
                except ValueError:
                    print("Erreur: Les coefficients doivent être des nombres")
                    return None
                
                b_val = input(f"    Valeur limite (b[{i+1}]): ").strip()
                try:
                    b_ub.append(float(b_val))
                except ValueError:
                    print("Erreur: La valeur limite doit être un nombre")
                    return None
        
        # Demander les bornes
        print("\nBornes des variables:")
        bornes_option = input("  Voulez-vous spécifier des bornes? (o/n): ").strip().lower()
        
        bounds = None
        if bornes_option == 'o':
            bounds = []
            for i in range(n_variables):
                print(f"\n  Variable x{i+1}:")
                min_val = input(f"    Minimum (appuyez sur Entrée pour aucune limite): ").strip()
                max_val = input(f"    Maximum (appuyez sur Entrée pour aucune limite): ").strip()
                
                try:
                    min_bound = float(min_val) if min_val else None
                    max_bound = float(max_val) if max_val else None
                    bounds.append((min_bound, max_bound))
                except ValueError:
                    print("Erreur: Les bornes doivent être des nombres")
                    return None
        
        return {
            'c': c,
            'A_ub': A_ub,
            'b_ub': b_ub,
            'bounds': bounds
        }
    
    def obtenir_exemple_simple(self):
        """
        Retourne un exemple simple de problème de programmation linéaire.
        
        Returns:
            dict: Paramètres d'un exemple simple
        """
        print("\n" + "=" * 60)
        print("EXEMPLE SIMPLE DE PROBLÈME")
        print("=" * 60)
        print("\nProblème:")
        print("  Minimiser: -1*x₁ + 4*x₂")
        print("  Sous contraintes:")
        print("    -3*x₁ + 1*x₂ <= 6")
        print("    1*x₁ + 2*x₂ <= 4")
        print("    x₂ >= -3")
        print("  Bornes:")
        print("    x₁, x₂ >= 0")
        print()
        
        return {
            'c': [-1, 4],
            'A_ub': [[-3, 1], [1, 2]],
            'b_ub': [6, 4],
            'bounds': [(0, None), (0, None)]
        }
    
    def montrer_résultat(self, résultat_formaté):
        """
        Affiche le résultat formaté à l'utilisateur.
        
        Args:
            résultat_formaté (str): Résultat formaté par le Presenter
        """
        print("\n" + résultat_formaté)
    
    def afficher_message(self, message):
        """
        Affiche un message simple à l'utilisateur.
        
        Args:
            message (str): Message à afficher
        """
        print(f"\n{message}")
    
    def afficher_erreur(self, erreur):
        """
        Affiche un message d'erreur à l'utilisateur.
        
        Args:
            erreur (str): Message d'erreur
        """
        print(f"\n✗ Erreur: {erreur}")
    
    def demander_continuer(self):
        """
        Demande à l'utilisateur s'il veut continuer.
        
        Returns:
            bool: True si l'utilisateur veut continuer, False sinon
        """
        print()
        réponse = input("Voulez-vous résoudre un autre problème? (o/n): ").strip().lower()
        return réponse == 'o'
