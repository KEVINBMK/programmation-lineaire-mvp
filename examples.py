"""
examples.py
-----------
Ce fichier contient des exemples de problèmes de programmation linéaire classiques.
Ces exemples illustrent différents types de problèmes qu'on peut résoudre.
"""

from models import ProblemePL
from solver import resoudre_rapide


def exemple_production():
    """
    Problème classique de production optimale.
    
    Une entreprise fabrique deux produits A et B.
    - Produit A rapporte 40€ de profit, Produit B rapporte 30€
    - Chaque produit A nécessite 2h de machine et 1h de main d'œuvre
    - Chaque produit B nécessite 1h de machine et 1h de main d'œuvre
    - On a 100h de machine et 80h de main d'œuvre disponibles
    
    Combien de chaque produit fabriquer pour maximiser le profit?
    """
    print("\n" + "="*60)
    print("EXEMPLE 1 : Problème de production optimale")
    print("="*60)
    
    # Créer le problème
    probleme = ProblemePL("Production de produits A et B")
    
    # Définir les noms des variables
    probleme.definir_noms_variables(['A', 'B'])
    
    # Fonction objectif: Maximiser 40*A + 30*B (profit)
    probleme.definir_fonction_objectif([40, 30], maximiser=True)
    
    # Contraintes:
    # Temps machine: 2*A + 1*B <= 100
    probleme.ajouter_contrainte_inegalite([2, 1], 100)
    
    # Main d'œuvre: 1*A + 1*B <= 80
    probleme.ajouter_contrainte_inegalite([1, 1], 80)
    
    # Les variables doivent être positives (défini par défaut)
    probleme.definir_bornes([(0, None), (0, None)])
    
    # Afficher le problème
    probleme.afficher_probleme()
    
    # Résoudre
    solution = resoudre_rapide(probleme)
    
    # Afficher la solution
    solution.afficher_solution()
    
    return probleme, solution


def exemple_melange():
    """
    Problème de mélange optimal (blend problem).
    
    Une raffinerie mélange deux types de pétrole brut pour produire de l'essence.
    - Brut 1 coûte 100€/tonne et contient 50% d'octane
    - Brut 2 coûte 80€/tonne et contient 30% d'octane
    - On veut produire au moins 100 tonnes d'essence
    - L'essence doit avoir au moins 40% d'octane
    
    Quelle quantité de chaque brut acheter pour minimiser le coût?
    """
    print("\n" + "="*60)
    print("EXEMPLE 2 : Problème de mélange optimal")
    print("="*60)
    
    # Créer le problème
    probleme = ProblemePL("Mélange de pétrole brut")
    
    # Variables: x1 = tonnes de brut 1, x2 = tonnes de brut 2
    probleme.definir_noms_variables(['Brut1', 'Brut2'])
    
    # Fonction objectif: Minimiser 100*x1 + 80*x2 (coût)
    probleme.definir_fonction_objectif([100, 80], maximiser=False)
    
    # Contrainte 1: Production minimale x1 + x2 >= 100
    # On transforme en: -x1 - x2 <= -100
    probleme.ajouter_contrainte_inegalite([-1, -1], -100)
    
    # Contrainte 2: Taux d'octane 0.5*x1 + 0.3*x2 >= 0.4*(x1 + x2)
    # Simplifié: 0.1*x1 - 0.1*x2 >= 0
    # Transformé en: -0.1*x1 + 0.1*x2 <= 0
    probleme.ajouter_contrainte_inegalite([-0.1, 0.1], 0)
    
    # Les variables doivent être positives
    probleme.definir_bornes([(0, None), (0, None)])
    
    # Afficher et résoudre
    probleme.afficher_probleme()
    solution = resoudre_rapide(probleme)
    solution.afficher_solution()
    
    return probleme, solution


def exemple_transport():
    """
    Problème de transport simplifié.
    
    Une entreprise a 2 usines et 2 entrepôts.
    - Usine 1 peut produire 50 unités
    - Usine 2 peut produire 40 unités
    - Entrepôt A demande 30 unités
    - Entrepôt B demande 60 unités
    
    Coûts de transport:
    - Usine1 → Entrepôt A: 8€, Usine1 → Entrepôt B: 6€
    - Usine2 → Entrepôt A: 5€, Usine2 → Entrepôt B: 7€
    """
    print("\n" + "="*60)
    print("EXEMPLE 3 : Problème de transport")
    print("="*60)
    
    # Créer le problème
    probleme = ProblemePL("Transport optimal")
    
    # Variables: x11, x12, x21, x22 (de usine i vers entrepôt j)
    probleme.definir_noms_variables(['U1→A', 'U1→B', 'U2→A', 'U2→B'])
    
    # Fonction objectif: Minimiser le coût total
    probleme.definir_fonction_objectif([8, 6, 5, 7], maximiser=False)
    
    # Contraintes de capacité des usines:
    # Usine 1: x11 + x12 <= 50
    probleme.ajouter_contrainte_inegalite([1, 1, 0, 0], 50)
    
    # Usine 2: x21 + x22 <= 40
    probleme.ajouter_contrainte_inegalite([0, 0, 1, 1], 40)
    
    # Contraintes de demande des entrepôts (égalité):
    # Entrepôt A: x11 + x21 == 30
    probleme.ajouter_contrainte_equalite([1, 0, 1, 0], 30)
    
    # Entrepôt B: x12 + x22 == 60
    probleme.ajouter_contrainte_equalite([0, 1, 0, 1], 60)
    
    # Variables positives
    probleme.definir_bornes([(0, None)] * 4)
    
    # Afficher et résoudre
    probleme.afficher_probleme()
    solution = resoudre_rapide(probleme)
    solution.afficher_solution()
    
    return probleme, solution


def exemple_simple():
    """
    Exemple très simple pour comprendre les bases.
    
    Maximiser: z = 3*x1 + 2*x2
    Sous contraintes:
        2*x1 + x2 <= 18
        2*x1 + 3*x2 <= 42
        3*x1 + x2 <= 24
        x1, x2 >= 0
    """
    print("\n" + "="*60)
    print("EXEMPLE 0 : Problème simple (introduction)")
    print("="*60)
    
    probleme = ProblemePL("Exemple simple")
    probleme.definir_noms_variables(['x1', 'x2'])
    
    # Maximiser z = 3*x1 + 2*x2
    probleme.definir_fonction_objectif([3, 2], maximiser=True)
    
    # Contraintes
    probleme.ajouter_contrainte_inegalite([2, 1], 18)
    probleme.ajouter_contrainte_inegalite([2, 3], 42)
    probleme.ajouter_contrainte_inegalite([3, 1], 24)
    
    # Variables positives
    probleme.definir_bornes([(0, None), (0, None)])
    
    probleme.afficher_probleme()
    solution = resoudre_rapide(probleme)
    solution.afficher_solution()
    
    return probleme, solution


def executer_tous_les_exemples():
    """
    Exécute tous les exemples disponibles.
    """
    print("\n" + "#"*60)
    print("# EXEMPLES DE PROGRAMMATION LINÉAIRE")
    print("#"*60)
    
    exemples = [
        exemple_simple,
        exemple_production,
        exemple_melange,
        exemple_transport
    ]
    
    for exemple in exemples:
        try:
            exemple()
            input("\nAppuyez sur Entrée pour continuer...")
        except Exception as e:
            print(f"Erreur dans l'exemple: {e}")
            continue
    
    print("\n" + "#"*60)
    print("# TOUS LES EXEMPLES TERMINÉS")
    print("#"*60)


if __name__ == "__main__":
    # Si on exécute ce fichier directement, lancer tous les exemples
    executer_tous_les_exemples()
