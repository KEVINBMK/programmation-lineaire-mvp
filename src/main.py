"""
Point d'entrée principal de l'application de programmation linéaire MVP.
Coordonne les modules Model, View et Presenter.
"""

from src.model import LinearProgramModel
from src.view import ConsoleView
from src.presenter import LinearProgramPresenter


def main():
    """
    Fonction principale de l'application.
    
    Crée les instances du Model, View et Presenter et gère
    la boucle principale de l'application.
    """
    # Initialiser les composants MVP
    model = LinearProgramModel()
    view = ConsoleView()
    presenter = LinearProgramPresenter(model)
    
    # Message de bienvenue
    print("\n" + "=" * 60)
    print("BIENVENUE DANS LE SOLVEUR DE PROGRAMMATION LINÉAIRE")
    print("=" * 60)
    print("\nCe programme résout des problèmes de programmation linéaire")
    print("en utilisant la méthode du simplexe (via scipy).")
    
    continuer = True
    
    while continuer:
        try:
            # Afficher le menu
            choix = view.afficher_menu()
            
            if choix == '1':
                # Exemple simple
                données = view.obtenir_exemple_simple()
                
                # Résoudre le problème
                résultat = presenter.résoudre(
                    c=données['c'],
                    A_ub=données['A_ub'],
                    b_ub=données['b_ub'],
                    bounds=données['bounds']
                )
                
                # Formater et afficher le résultat
                résultat_formaté = presenter.formater_résultat(résultat)
                view.montrer_résultat(résultat_formaté)
                
                # Demander si l'utilisateur veut continuer
                continuer = view.demander_continuer()
                
            elif choix == '2':
                # Problème personnalisé
                données = view.demander_données()
                
                if données is None:
                    view.afficher_erreur("Données invalides, veuillez réessayer")
                    continue
                
                # Résoudre le problème
                résultat = presenter.résoudre(
                    c=données['c'],
                    A_ub=données['A_ub'],
                    b_ub=données['b_ub'],
                    bounds=données['bounds']
                )
                
                # Formater et afficher le résultat
                résultat_formaté = presenter.formater_résultat(résultat)
                view.montrer_résultat(résultat_formaté)
                
                # Demander si l'utilisateur veut continuer
                continuer = view.demander_continuer()
                
            elif choix == '3':
                # Quitter
                view.afficher_message("Merci d'avoir utilisé le solveur. Au revoir!")
                continuer = False
                
            else:
                view.afficher_erreur("Choix invalide. Veuillez choisir 1, 2 ou 3")
        
        except KeyboardInterrupt:
            view.afficher_message("\n\nInterruption détectée. Au revoir!")
            continuer = False
        
        except Exception as e:
            view.afficher_erreur(f"Erreur inattendue: {str(e)}")
            continuer = view.demander_continuer()


if __name__ == "__main__":
    main()
