"""
app.py
------
Interface Streamlit moderne pour le solveur de programmation linéaire.
Design moderne avec couleurs attrayantes et animations.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.models import ProblemePL, Solution
from src.simplexe import SimplexeSolveur, TableauSimplexe


# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Solveur PL | Programmation Linéaire",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLES CSS PERSONNALISÉS - DESIGN MODERNE
# ============================================================

st.markdown("""
<style>
    /* Import de la police Google */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Style global */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal avec dégradé */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Cards modernes */
    .card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid rgba(200,200,200,0.8);
        color: #333333;
    }
    
    .card h4 {
        color: #333333;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .card p {
        color: #666666;
        margin: 0;
    }
    
    .card-success {
        background: linear-gradient(145deg, #d4edda, #c3e6cb);
        border-left: 5px solid #28a745;
        color: #155724;
    }
    
    .card-success h3 {
        color: #155724;
    }
    
    .card-error {
        background: linear-gradient(145deg, #f8d7da, #f5c6cb);
        border-left: 5px solid #dc3545;
        color: #721c24;
    }
    
    .card-error h3 {
        color: #721c24;
    }
    
    .card-info {
        background: linear-gradient(145deg, #e7f3ff, #cce5ff);
        border-left: 5px solid #007bff;
        color: #004085;
    }
    
    .card-info h3 {
        color: #004085;
    }
    
    /* Résultat principal */
    .result-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(17, 153, 142, 0.3);
        margin: 1rem 0;
    }
    
    .result-box h2 {
        color: white;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .result-box .value {
        color: white;
        font-size: 3rem;
        font-weight: 700;
    }
    
    /* Variables résultat */
    .variable-card {
        background: linear-gradient(145deg, #667eea, #764ba2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .variable-card .var-name {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
    }
    
    .variable-card .var-value {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Sidebar style */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Boutons stylisés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Metrics améliorés */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Section titre */
    .section-title {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Exemple cards */
    .example-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .example-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateY(-3px);
    }
    
    /* Animation fade-in */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def creer_graphique_2d(probleme: ProblemePL, solution: Solution):
    """
    Crée un graphique 2D pour visualiser le problème et la solution.
    Fonctionne uniquement pour les problèmes à 2 variables.
    """
    if len(probleme.c) != 2:
        return None
    
    fig = go.Figure()
    
    # Couleurs modernes
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    # Tracer les contraintes
    x_range = np.linspace(0, 50, 500)
    
    if probleme.A_ub is not None:
        for i, (row, b) in enumerate(zip(probleme.A_ub, probleme.b_ub)):
            if row[1] != 0:
                y = (b - row[0] * x_range) / row[1]
                fig.add_trace(go.Scatter(
                    x=x_range, y=y,
                    mode='lines',
                    name=f'Contrainte {i+1}',
                    line=dict(color=colors[i % len(colors)], width=3)
                ))
    
    # Marquer la solution optimale
    if solution.succes:
        fig.add_trace(go.Scatter(
            x=[solution.valeurs_variables[0]],
            y=[solution.valeurs_variables[1]],
            mode='markers+text',
            name='Solution optimale',
            marker=dict(size=20, color='#11998e', symbol='star'),
            text=[f'({solution.valeurs_variables[0]:.2f}, {solution.valeurs_variables[1]:.2f})'],
            textposition='top center',
            textfont=dict(size=14, color='#11998e')
        ))
    
    fig.update_layout(
        title=dict(
            text='<b>Visualisation du Problème</b>',
            font=dict(size=20, color='#333')
        ),
        xaxis_title=probleme.noms_variables[0],
        yaxis_title=probleme.noms_variables[1],
        xaxis=dict(range=[0, 50], gridcolor='#eee'),
        yaxis=dict(range=[0, 50], gridcolor='#eee'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ddd',
            borderwidth=1
        ),
        height=500
    )
    
    return fig


def afficher_formulation_mathematique(probleme: ProblemePL):
    """Affiche la formulation mathématique du problème de manière élégante."""
    
    st.markdown("### Formulation Mathématique")
    
    # Fonction objectif
    objectif = "Maximiser" if probleme.type_optimisation == 'max' else "Minimiser"
    termes = [f"{probleme.c[i]:.2g}·{probleme.noms_variables[i]}" 
             for i in range(len(probleme.c))]
    
    st.latex(f"\\text{{{objectif}}} \\quad Z = {' + '.join(termes)}")
    
    # Contraintes
    st.markdown("**Sous contraintes :**")
    
    if probleme.A_ub is not None:
        for i, (ligne, b) in enumerate(zip(probleme.A_ub, probleme.b_ub)):
            termes = [f"{ligne[j]:.2g}·{probleme.noms_variables[j]}" 
                     for j in range(len(ligne)) if ligne[j] != 0]
            st.latex(f"{' + '.join(termes)} \\leq {b:.2g}")
    
    if probleme.A_eq is not None:
        for i, (ligne, b) in enumerate(zip(probleme.A_eq, probleme.b_eq)):
            termes = [f"{ligne[j]:.2g}·{probleme.noms_variables[j]}" 
                     for j in range(len(ligne)) if ligne[j] != 0]
            st.latex(f"{' + '.join(termes)} = {b:.2g}")


def afficher_tableaux_simplexe(probleme: ProblemePL):
    """
    Affiche les tableaux du simplexe étape par étape.
    Uniquement pour les problèmes avec contraintes d'inégalité (<= seulement).
    """
    # Vérifier que le problème est compatible (seulement des contraintes <=)
    if probleme.A_eq is not None and len(probleme.b_eq) > 0:
        st.warning("L'affichage des tableaux du simplexe n'est disponible que pour les contraintes ≤")
        return
    
    if probleme.A_ub is None:
        st.warning("Aucune contrainte définie")
        return
    
    st.markdown("### Tableaux du Simplexe (Méthode du cours)")
    
    # Préparer les données pour le solveur simplexe
    c = probleme.c.tolist()
    A = probleme.A_ub.tolist()
    b = probleme.b_ub.tolist()
    noms_vars = probleme.noms_variables
    maximiser = (probleme.type_optimisation == 'max')
    
    # Résoudre avec notre solveur simplexe
    solveur = SimplexeSolveur()
    tableaux = solveur.resoudre(c, A, b, noms_vars, maximiser)
    
    # Afficher chaque tableau
    for i, tableau in enumerate(tableaux):
        # Titre du tableau
        if tableau.iteration == 0:
            st.markdown(f"**Tableau Initial**")
        else:
            st.markdown(f"**Tableau {tableau.iteration}**")
        
        # Construire le DataFrame pour l'affichage
        n_vars_hb = len(tableau.vars_hb)
        n_lignes = len(tableau.vars_base)
        
        # Colonnes du tableau
        colonnes = tableau.vars_hb + ['C']
        if tableau.colonne_r is not None:
            colonnes.append('R')
        
        # Données du tableau
        data = []
        for j in range(n_lignes):
            ligne = []
            for k in range(n_vars_hb):
                val = tableau.matrice[j, k]
                # Mettre en évidence le pivot
                if j == tableau.var_sortante_idx and k == tableau.var_entrante_idx:
                    ligne.append(f"[{val:.2f}]")
                else:
                    ligne.append(f"{val:.2f}")
            ligne.append(f"{tableau.colonne_c[j]:.2f}")
            if tableau.colonne_r is not None:
                if tableau.colonne_r[j] == np.inf:
                    ligne.append("-")
                else:
                    ligne.append(f"{tableau.colonne_r[j]:.2f}")
            data.append(ligne)
        
        # Ligne Delta
        ligne_delta = []
        for k in range(n_vars_hb):
            val = tableau.delta[k]
            if k == tableau.var_entrante_idx and tableau.iteration > 0:
                ligne_delta.append(f"[{val:.2f}]")
            else:
                ligne_delta.append(f"{val:.2f}")
        ligne_delta.append(f"{tableau.valeur_z:.2f}")
        if tableau.colonne_r is not None:
            ligne_delta.append("")
        data.append(ligne_delta)
        
        # Index (variables de base + Δ)
        index = tableau.vars_base + ['Δ']
        
        # Créer le DataFrame
        df = pd.DataFrame(data, columns=colonnes, index=index)
        
        # Afficher le tableau avec style
        st.dataframe(df, use_container_width=True)
        
        # Afficher le message explicatif
        if tableau.message:
            if "SOLUTION OPTIMALE" in tableau.message:
                st.success(tableau.message)
            elif "entrante" in tableau.message:
                st.info(tableau.message)
            else:
                st.caption(tableau.message)
        
        st.markdown("---")
    
    # Résumé final
    if solveur.solution_trouvee:
        st.markdown("### Interprétation des résultats")
        st.markdown(f"""
        - **Valeur optimale** : Z = {solveur.valeur_optimale:.4f}
        - Les variables **Hors Base (HB)** sont nulles
        - Les valeurs des variables **dans la Base** se lisent dans la colonne **C**
        - La valeur **-Z** se lit à l'intersection de C et Δ
        """)


# ============================================================
# EXEMPLES PRÉDÉFINIS
# ============================================================

def get_exemple_simple():
    """
    Retourne l'exemple du cours (Exemple 1 du syllabus).
    Max Z = 1200x1 + 1000x2
    3x1 + 4x2 <= 160
    6x1 + 3x2 <= 180
    """
    probleme = ProblemePL("Exemple du Cours")
    probleme.definir_noms_variables(['x1', 'x2'])
    probleme.definir_fonction_objectif([1200, 1000], maximiser=True)
    probleme.ajouter_contrainte_inegalite([3, 4], 160)
    probleme.ajouter_contrainte_inegalite([6, 3], 180)
    probleme.definir_bornes([(0, None), (0, None)])
    return probleme

def get_exemple_production():
    """Retourne l'exemple de production."""
    probleme = ProblemePL("Production Optimale")
    probleme.definir_noms_variables(['Produit_A', 'Produit_B'])
    probleme.definir_fonction_objectif([40, 30], maximiser=True)
    probleme.ajouter_contrainte_inegalite([2, 1], 100)
    probleme.ajouter_contrainte_inegalite([1, 1], 80)
    probleme.definir_bornes([(0, None), (0, None)])
    return probleme

def get_exemple_melange():
    """Retourne l'exemple de mélange."""
    probleme = ProblemePL("Mélange Optimal")
    probleme.definir_noms_variables(['Brut_1', 'Brut_2'])
    probleme.definir_fonction_objectif([100, 80], maximiser=False)
    probleme.ajouter_contrainte_inegalite([-1, -1], -100)
    probleme.ajouter_contrainte_inegalite([-0.1, 0.1], 0)
    probleme.definir_bornes([(0, None), (0, None)])
    return probleme

def get_exemple_transport():
    """Retourne l'exemple de transport."""
    probleme = ProblemePL("Transport Optimal")
    probleme.definir_noms_variables(['U1→A', 'U1→B', 'U2→A', 'U2→B'])
    probleme.definir_fonction_objectif([8, 6, 5, 7], maximiser=False)
    probleme.ajouter_contrainte_inegalite([1, 1, 0, 0], 50)
    probleme.ajouter_contrainte_inegalite([0, 0, 1, 1], 40)
    probleme.ajouter_contrainte_equalite([1, 0, 1, 0], 30)
    probleme.ajouter_contrainte_equalite([0, 1, 0, 1], 60)
    probleme.definir_bornes([(0, None)] * 4)
    return probleme


# ============================================================
# INTERFACE PRINCIPALE
# ============================================================

def main():
    """Fonction principale de l'application Streamlit."""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>Solveur de Programmation Linéaire</h1>
        <p>Résolvez vos problèmes d'optimisation avec élégance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Menu de navigation
    with st.sidebar:
        st.markdown("## Navigation")
        
        mode = st.radio(
            "Choisir un mode :",
            ["Exemples Prédéfinis", "Problème Personnalisé"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("### À propos")
        st.markdown("""
        Ce solveur utilise la **Méthode du Simplexe** 
        enseignée dans le cours de Recherche Opérationnelle.
        
        **Fonctionnalités :**
        - Maximisation / Minimisation
        - Contraintes ≤
        - Affichage des tableaux étape par étape
        - Visualisation graphique
        """)
        
        st.markdown("---")
        st.markdown("### Méthode de Résolution")
        st.info("Méthode du Simplexe (Algorithme du cours)")
    
    # Contenu principal selon le mode
    if mode == "Exemples Prédéfinis":
        afficher_mode_exemples()
    else:
        afficher_mode_personnalise()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Solveur de Programmation Linéaire | Projet L4 | 2026</p>
    </div>
    """, unsafe_allow_html=True)


def afficher_mode_exemples():
    """Affiche le mode exemples prédéfinis."""
    
    st.markdown('<p class="section-title">Choisissez un Exemple</p>', unsafe_allow_html=True)
    
    # Grille d'exemples avec colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
                <h4>Exemple du Cours</h4>
                <p>Max Z = 1200x1 + 1000x2 (syllabus p.46)</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Charger Exemple du Cours", key="btn1", use_container_width=True):
                st.session_state.exemple = "simple"
        
        with st.container():
            st.markdown("""
            <div class="card">
                <h4>Mélange Optimal</h4>
                <p>Minimiser le coût de mélange</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Charger Exemple Mélange", key="btn3", use_container_width=True):
                st.session_state.exemple = "melange"
    
    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
                <h4>Production Optimale</h4>
                <p>Maximiser le profit de production</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Charger Exemple Production", key="btn2", use_container_width=True):
                st.session_state.exemple = "production"
        
        with st.container():
            st.markdown("""
            <div class="card">
                <h4>Transport</h4>
                <p>Optimiser les coûts logistiques</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Charger Exemple Transport", key="btn4", use_container_width=True):
                st.session_state.exemple = "transport"
    
    # Afficher l'exemple sélectionné
    if 'exemple' in st.session_state:
        st.markdown("---")
        
        # Charger le problème correspondant
        if st.session_state.exemple == "simple":
            probleme = get_exemple_simple()
        elif st.session_state.exemple == "production":
            probleme = get_exemple_production()
        elif st.session_state.exemple == "melange":
            probleme = get_exemple_melange()
        else:
            probleme = get_exemple_transport()
        
        # Afficher et résoudre
        afficher_probleme_et_solution(probleme)


def afficher_mode_personnalise():
    """Affiche le mode de création personnalisée."""
    
    st.markdown('<p class="section-title">Créer Votre Problème</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Configuration")
        
        nb_vars = st.number_input("Nombre de variables", min_value=2, max_value=10, value=2)
        type_opt = st.radio("Type d'optimisation", ["Maximiser", "Minimiser"], horizontal=True)
        
        st.markdown("### Noms des variables")
        noms_vars = []
        cols = st.columns(min(nb_vars, 4))
        for i in range(nb_vars):
            with cols[i % 4]:
                nom = st.text_input(f"Variable {i+1}", value=f"x{i+1}", key=f"var_{i}")
                noms_vars.append(nom)
        
        st.markdown("### Fonction Objectif")
        coeffs_obj = []
        cols = st.columns(min(nb_vars, 4))
        for i in range(nb_vars):
            with cols[i % 4]:
                coeff = st.number_input(f"Coeff. {noms_vars[i]}", value=1.0, key=f"coeff_{i}")
                coeffs_obj.append(coeff)
    
    with col2:
        st.markdown("### Contraintes d'Inégalité (≤)")
        
        nb_contraintes = st.number_input("Nombre de contraintes", min_value=1, max_value=10, value=2)
        
        contraintes = []
        for i in range(nb_contraintes):
            st.markdown(f"**Contrainte {i+1}:**")
            cols = st.columns(nb_vars + 1)
            coeffs = []
            for j in range(nb_vars):
                with cols[j]:
                    c = st.number_input(f"{noms_vars[j]}", value=1.0, key=f"c_{i}_{j}")
                    coeffs.append(c)
            with cols[-1]:
                borne = st.number_input("≤", value=10.0, key=f"b_{i}")
            contraintes.append((coeffs, borne))
    
    # Bouton de résolution
    st.markdown("---")
    
    if st.button("Résoudre le Problème", use_container_width=True):
        # Créer le problème
        probleme = ProblemePL("Problème Personnalisé")
        probleme.definir_noms_variables(noms_vars)
        probleme.definir_fonction_objectif(coeffs_obj, maximiser=(type_opt == "Maximiser"))
        
        for coeffs, borne in contraintes:
            probleme.ajouter_contrainte_inegalite(coeffs, borne)
        
        probleme.definir_bornes([(0, None)] * nb_vars)
        
        # Afficher et résoudre
        afficher_probleme_et_solution(probleme)


def afficher_probleme_et_solution(probleme: ProblemePL):
    """Affiche le problème et sa solution."""
    
    # Créer deux colonnes pour le problème et la solution
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="card card-info fade-in">
            <h3>Problème : {probleme.nom}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        afficher_formulation_mathematique(probleme)
    
    with col2:
        # Résoudre le problème avec la méthode du Simplexe
        solveur = SimplexeSolveur()
        
        # Extraire les données du problème
        c = probleme.c.tolist()
        A = probleme.A_ub.tolist() if probleme.A_ub is not None else []
        b = probleme.b_ub.tolist() if probleme.b_ub is not None else []
        noms_vars = probleme.noms_variables
        maximiser = (probleme.type_optimisation == 'max')
        
        with st.spinner("Résolution en cours avec la méthode du Simplexe..."):
            tableaux = solveur.resoudre(c, A, b, noms_vars, maximiser)
        
        # Créer l'objet Solution à partir des résultats du Simplexe
        solution = Solution()
        if solveur.solution_trouvee:
            valeurs_vars = [solveur.variables_solution.get(nom, 0.0) for nom in noms_vars]
            solution.succes = True
            solution.valeurs_variables = np.array(valeurs_vars)
            solution.valeur_objectif = solveur.valeur_optimale
            solution.noms_variables = noms_vars
            solution.message = "Solution optimale trouvée"
        else:
            solution.succes = False
            solution.valeurs_variables = None
            solution.valeur_objectif = None
            solution.message = "Aucune solution trouvée" if not solveur.solution_infinie else "Solution infinie"
        
        if solution.succes:
            # Affichage du résultat principal
            st.markdown(f"""
            <div class="result-box fade-in">
                <h2>Solution Optimale Trouvée</h2>
                <div class="value">{solution.valeur_objectif:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Valeurs des variables
            st.markdown("### Valeurs des Variables")
            
            cols = st.columns(len(solution.noms_variables))
            for i, (nom, val) in enumerate(zip(solution.noms_variables, solution.valeurs_variables)):
                with cols[i]:
                    st.metric(label=nom, value=f"{val:.4f}")
        else:
            st.markdown(f"""
            <div class="card card-error fade-in">
                <h3>Pas de Solution</h3>
                <p>{solution.message}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Graphique 2D si applicable
    if len(probleme.c) == 2 and solution.succes:
        st.markdown("---")
        st.markdown('<p class="section-title">Visualisation Graphique</p>', unsafe_allow_html=True)
        
        fig = creer_graphique_2d(probleme, solution)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques supplémentaires
    if solution.succes:
        st.markdown("---")
        st.markdown('<p class="section-title">Statistiques</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Variables", len(probleme.c))
        
        with col2:
            nb_ineq = len(probleme.b_ub) if probleme.b_ub is not None else 0
            st.metric("Contraintes ≤", nb_ineq)
        
        with col3:
            nb_eq = len(probleme.b_eq) if probleme.b_eq is not None else 0
            st.metric("Contraintes =", nb_eq)
        
        with col4:
            st.metric("Méthode", "SIMPLEXE")
    
    # Afficher les tableaux du simplexe (uniquement pour contraintes <=)
    if probleme.A_ub is not None and (probleme.A_eq is None or len(probleme.b_eq) == 0):
        st.markdown("---")
        st.markdown('<p class="section-title">Détail de la Résolution par le Simplexe</p>', unsafe_allow_html=True)
        
        with st.expander("Voir les tableaux du Simplexe étape par étape", expanded=False):
            afficher_tableaux_simplexe(probleme)


# Point d'entrée
if __name__ == "__main__":
    main()
