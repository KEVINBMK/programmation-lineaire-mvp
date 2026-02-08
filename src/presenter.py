"""
Module Presenter pour la gestion de la logique de présentation.
Agit comme intermédiaire entre le Model et la View.
"""

import numpy as np


class LinearProgramPresenter:
    """
    Classe Presenter qui gère la logique de présentation.
    
    Cette classe valide les entrées de l'utilisateur et formate
    les résultats du modèle pour la vue.
    """
    
    def __init__(self, model):
        """
        Initialise le Presenter avec un modèle.
        
        Args:
            model: Instance de LinearProgramModel
        """
        self.model = model
    
    def valider_entrée(self, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
        """
        Valide les entrées du problème de programmation linéaire.
        
        Args:
            c: Coefficients de la fonction objectif
            A_ub: Matrice des contraintes d'inégalité
            b_ub: Vecteur des contraintes d'inégalité
            A_eq: Matrice des contraintes d'égalité
            b_eq: Vecteur des contraintes d'égalité
            bounds: Bornes des variables
        
        Returns:
            tuple: (est_valide (bool), message_erreur (str ou None))
        """
        try:
            # Vérifier que c n'est pas vide
            if c is None or len(c) == 0:
                return False, "La fonction objectif ne peut pas être vide"
            
            # Vérifier que c contient uniquement des nombres
            try:
                c_array = np.array(c, dtype=float)
                n_variables = len(c_array)
            except (ValueError, TypeError):
                return False, "La fonction objectif doit contenir uniquement des nombres"
            
            # Valider les contraintes d'inégalité
            if A_ub is not None:
                if b_ub is None:
                    return False, "Si A_ub est fourni, b_ub doit aussi être fourni"
                
                try:
                    A_ub_array = np.array(A_ub, dtype=float)
                    b_ub_array = np.array(b_ub, dtype=float)
                except (ValueError, TypeError):
                    return False, "Les contraintes d'inégalité doivent contenir uniquement des nombres"
                
                # Vérifier les dimensions
                if A_ub_array.ndim != 2:
                    return False, "A_ub doit être une matrice 2D"
                
                if A_ub_array.shape[1] != n_variables:
                    return False, f"A_ub doit avoir {n_variables} colonnes (une par variable)"
                
                if len(b_ub_array) != A_ub_array.shape[0]:
                    return False, "Le nombre de lignes de A_ub doit correspondre à la taille de b_ub"
            
            # Valider les contraintes d'égalité
            if A_eq is not None:
                if b_eq is None:
                    return False, "Si A_eq est fourni, b_eq doit aussi être fourni"
                
                try:
                    A_eq_array = np.array(A_eq, dtype=float)
                    b_eq_array = np.array(b_eq, dtype=float)
                except (ValueError, TypeError):
                    return False, "Les contraintes d'égalité doivent contenir uniquement des nombres"
                
                # Vérifier les dimensions
                if A_eq_array.ndim != 2:
                    return False, "A_eq doit être une matrice 2D"
                
                if A_eq_array.shape[1] != n_variables:
                    return False, f"A_eq doit avoir {n_variables} colonnes (une par variable)"
                
                if len(b_eq_array) != A_eq_array.shape[0]:
                    return False, "Le nombre de lignes de A_eq doit correspondre à la taille de b_eq"
            
            # Valider les bornes
            if bounds is not None:
                if len(bounds) != n_variables:
                    return False, f"Le nombre de bornes doit correspondre au nombre de variables ({n_variables})"
                
                for i, bound in enumerate(bounds):
                    if bound is not None:
                        if not isinstance(bound, (tuple, list)) or len(bound) != 2:
                            return False, f"La borne {i} doit être un tuple (min, max) ou None"
                        
                        min_val, max_val = bound
                        if min_val is not None and max_val is not None:
                            if min_val > max_val:
                                return False, f"Pour la borne {i}, min ({min_val}) ne peut pas être > max ({max_val})"
            
            return True, None
            
        except Exception as e:
            return False, f"Erreur de validation: {str(e)}"
    
    def formater_résultat(self, résultat):
        """
        Formate les résultats pour l'affichage.
        
        Args:
            résultat (dict): Résultat retourné par le modèle
        
        Returns:
            str: Résultat formaté pour l'affichage
        """
        if résultat is None:
            return "Aucun résultat disponible"
        
        lignes = []
        lignes.append("=" * 60)
        lignes.append("RÉSULTATS DE LA PROGRAMMATION LINÉAIRE")
        lignes.append("=" * 60)
        lignes.append("")
        
        if résultat.get('succès', False):
            lignes.append("✓ Résolution réussie !")
            lignes.append("")
            
            # Afficher la solution optimale
            if 'x' in résultat:
                lignes.append("Solution optimale :")
                x = résultat['x']
                for i, val in enumerate(x):
                    lignes.append(f"  x{i+1} = {val:.6f}")
                lignes.append("")
            
            # Afficher la valeur optimale
            if 'valeur_optimale' in résultat:
                lignes.append(f"Valeur optimale de la fonction objectif : {résultat['valeur_optimale']:.6f}")
                lignes.append("")
        else:
            lignes.append("✗ Échec de la résolution")
            lignes.append("")
        
        # Afficher le message
        if 'message' in résultat:
            lignes.append(f"Message : {résultat['message']}")
            lignes.append("")
        
        lignes.append("=" * 60)
        
        return "\n".join(lignes)
    
    def résoudre(self, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
        """
        Valide les entrées et résout le problème.
        
        Args:
            c: Coefficients de la fonction objectif
            A_ub: Matrice des contraintes d'inégalité
            b_ub: Vecteur des contraintes d'inégalité
            A_eq: Matrice des contraintes d'égalité
            b_eq: Vecteur des contraintes d'égalité
            bounds: Bornes des variables
        
        Returns:
            dict: Résultat de la résolution
        """
        # Valider les entrées
        est_valide, message_erreur = self.valider_entrée(c, A_ub, b_ub, A_eq, b_eq, bounds)
        
        if not est_valide:
            return {
                'succès': False,
                'message': f'Erreur de validation: {message_erreur}',
                'statut': -1
            }
        
        # Résoudre le problème
        return self.model.résoudre_problème(c, A_ub, b_ub, A_eq, b_eq, bounds)
