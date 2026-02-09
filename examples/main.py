"""
main.py
-------
Point d'entrée principal du programme de programmation linéaire.
Ce fichier fournit un menu interactif pour utiliser le solveur.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import ProblemePL
from src.simplexe import resoudre_rapide
from examples import (
    exemple_simple, 
    exemple_production, 
    exemple_melange, 
    exemple_transport,
    executer_tous_les_exemples
)


def afficher_menu_principal():
    """Affiche le menu principal du programme."""
    print("\n" + "="*60)
    print(" "*15 + "SOLVEUR DE PROGRAMMATION LINÉAIRE")
    print("="*60)
    print("\n Que voulez-vous faire?\n")
    print("  1. Voir un exemple simple")
    print("  2. Problème de production")
    print("  3. Problème de mélange")
    print("  4. Problème de transport")
    print("  5. Voir tous les exemples")
    print("  6. Créer un problème personnalisé")
    print("  7. Aide - Comment utiliser ce programme")
    print("  0. Quitter")
    print("\n" + "="*60)


def creer_probleme_personnalise():
    """
    Guide l'utilisateur pour créer son propre problème de programmation linéaire.
    """
    print("\n" + "="*60)
    print("CRÉATION D'UN PROBLÈME PERSONNALISÉ")
    print("="*60)
    
    # Nom du problème
    nom = input("\nNom du problème (optionnel): ").strip()
    if not nom:
        nom = "Problème personnalisé"
    
    probleme = ProblemePL(nom)
    
    # Nombre de variables
    try:
        nb_vars = int(input("\nNombre de variables: "))
        if nb_vars <= 0:
            print("Le nombre de variables doit être positif!")
            return
    except ValueError:
        print("Entrée invalide!")
        return
    
    # Noms des variables
    noms = []
    print(f"\nNoms des variables (appuyez sur Entrée pour utiliser x1, x2, ...):")
    for i in range(nb_vars):
        nom_var = input(f"  Variable {i+1}: ").strip()
        if not nom_var:
            nom_var = f"x{i+1}"
        noms.append(nom_var)
    
    probleme.definir_noms_variables(noms)
    
    # Fonction objectif
    print(f"\nCoefficients de la fonction objectif:")
    coeffs = []
    for nom in noms:
        try:
            coeff = float(input(f"  Coefficient de {nom}: "))
            coeffs.append(coeff)
        except ValueError:
            print("Entrée invalide! Utilisation de 1.0")
            coeffs.append(1.0)
    
    type_opt = input("\nMaximiser ou Minimiser? (max/min): ").strip().lower()
    maximiser = type_opt != 'min'
    
    probleme.definir_fonction_objectif(coeffs, maximiser=maximiser)
    
    # Contraintes d'inégalité
    print(f"\nContraintes d'inégalité (<=)")
    try:
        nb_contraintes = int(input("Nombre de contraintes d'inégalité: "))
        
        for i in range(nb_contraintes):
            print(f"\n  Contrainte {i+1}:")
            coeffs_contrainte = []
            for nom in noms:
                try:
                    c = float(input(f"    Coefficient de {nom}: "))
                    coeffs_contrainte.append(c)
                except ValueError:
                    coeffs_contrainte.append(0.0)
            
            try:
                borne = float(input(f"    Borne (côté droit): "))
            except ValueError:
                borne = 0.0
            
            probleme.ajouter_contrainte_inegalite(coeffs_contrainte, borne)
    except ValueError:
        print("Aucune contrainte d'inégalité ajoutée.")
    
    # Bornes sur les variables
    print(f"\nBornes sur les variables (Entrée pour défaut: >= 0):")
    bornes = []
    for nom in noms:
        reponse = input(f"  {nom} >= 0 ? (o/n, défaut: o): ").strip().lower()
        if reponse == 'n':
            try:
                min_val = input("    Minimum (Entrée pour -∞): ").strip()
                max_val = input("    Maximum (Entrée pour +∞): ").strip()
                
                min_val = float(min_val) if min_val else None
                max_val = float(max_val) if max_val else None
                
                bornes.append((min_val, max_val))
            except ValueError:
                bornes.append((0, None))
        else:
            bornes.append((0, None))
    
    probleme.definir_bornes(bornes)
    
    # Afficher et résoudre
    probleme.afficher_probleme()
    
    print("\n" + "-"*60)
    continuer = input("Résoudre ce problème? (o/n): ").strip().lower()
    
    if continuer == 'o':
        solution = resoudre_rapide(probleme)
        solution.afficher_solution()
    else:
        print("Résolution annulée.")


def afficher_aide():
    """Affiche l'aide sur l'utilisation du programme."""
    print("\n" + "="*60)
    print(" "*20 + "AIDE")
    print("="*60)
    print("""
Ce programme permet de résoudre des problèmes de programmation linéaire.

Un problème de programmation linéaire consiste à:
  - Optimiser (maximiser ou minimiser) une fonction objectif linéaire
  - Tout en respectant des contraintes linéaires

Structure d'un problème:
  1. Variables de décision (ex: x1, x2, ...)
  2. Fonction objectif (ex: Maximiser 3x1 + 2x2)
  3. Contraintes (ex: x1 + x2 <= 10)
  4. Bornes sur les variables (ex: x1 >= 0)

Utilisation:
  - Options 1-4: Voir des exemples prédéfinis
  - Option 5: Voir tous les exemples en séquence
  - Option 6: Créer votre propre problème interactivement
  - Option 7: Afficher cette aide

Exemples d'applications:
  - Optimisation de production
  - Allocation de ressources
  - Problèmes de transport et logistique
  - Mélange optimal (blend problems)
  - Planification financière

Pour plus d'informations, consultez le fichier README.md
    """)
    print("="*60)


def main():
    """Fonction principale du programme."""
    while True:
        afficher_menu_principal()
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == '0':
            print("\n" + "="*60)
            print(" "*15 + "Au revoir! À bientôt!")
            print("="*60 + "\n")
            break
        
        elif choix == '1':
            exemple_simple()
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choix == '2':
            exemple_production()
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choix == '3':
            exemple_melange()
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choix == '4':
            exemple_transport()
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choix == '5':
            executer_tous_les_exemples()
        
        elif choix == '6':
            creer_probleme_personnalise()
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choix == '7':
            afficher_aide()
            input("\nAppuyez sur Entrée pour continuer...")
        
        else:
            print("\n❌ Choix invalide! Veuillez choisir une option du menu.")
            input("Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + " "*15 + "BIENVENUE DANS LE SOLVEUR PL" + " "*15 + "#")
    print("#" + " "*58 + "#")
    print("#"*60)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print(" "*15 + "Programme interrompu par l'utilisateur")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("Le programme va se terminer.\n")
