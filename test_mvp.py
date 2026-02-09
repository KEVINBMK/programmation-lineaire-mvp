from src.simplexe import SimplexeSolveur

# Test de l'exemple du cours
c = [1200, 1000]
A = [[3, 4], [6, 3]]
b = [160, 180]

solveur = SimplexeSolveur()
tableaux = solveur.resoudre(c, A, b)

if solveur.solution_trouvee:
    print(f"✓ Test réussi!")
    print(f"  x1 = {solveur.variables_solution['x1']:.0f}")
    print(f"  x2 = {solveur.variables_solution['x2']:.0f}")
    print(f"  Z = {solveur.valeur_optimale:.0f}")
    print(f"  Nombre de tableaux: {len(tableaux)}")
else:
    print("✗ Erreur dans le test")
