#!/usr/bin/env python3
"""
Service API Externe - Service Contenu Culturel
Projet DEVNET - L3 RI ISI Keur Massar
Service spécialisé pour la fourniture de contenu éducatif et culturel
"""

from flask import Flask, jsonify, request
import requests
import random
from datetime import datetime
import json

app = Flask(__name__)

# Base de données de contenu éducatif
CONTENT_DB = {
    'mathematiques': {
        'college': {
            'title': 'Mathématiques - Niveau Collège',
            'chapters': [
                {
                    'id': 1,
                    'title': 'Les Nombres et Calculs',
                    'content': '''
                    <h3>Les différents types de nombres</h3>
                    <p><strong>Les entiers naturels</strong> : 0, 1, 2, 3, ...</p>
                    <p><strong>Les entiers relatifs</strong> : ..., -3, -2, -1, 0, 1, 2, 3, ...</p>
                    <p><strong>Les décimaux</strong> : nombres avec une virgule et un nombre fini de chiffres après</p>
                    <p><strong>Les fractions</strong> : quotient de deux nombres</p>
                    
                    <h3>Opérations de base</h3>
                    <ul>
                        <li><strong>Addition</strong> : a + b</li>
                        <li><strong>Soustraction</strong> : a - b</li>
                        <li><strong>Multiplication</strong> : a × b</li>
                        <li><strong>Division</strong> : a ÷ b</li>
                    </ul>
                    
                    <h3>Propriétés importantes</h3>
                    <p>La multiplication est distributive par rapport à l'addition :</p>
                    <p>a × (b + c) = a × b + a × c</p>
                    ''',
                    'examples': [
                        '2 + 3 = 5',
                        '10 - 4 = 6',
                        '3 × 4 = 12',
                        '15 ÷ 3 = 5'
                    ]
                },
                {
                    'id': 2,
                    'title': 'Géométrie Plane',
                    'content': '''
                    <h3>Les figures géométriques fondamentales</h3>
                    <p><strong>Triangle</strong> : 3 côtés, 3 angles</p>
                    <p><strong>Carré</strong> : 4 côtés égaux, 4 angles droits</p>
                    <p><strong>Rectangle</strong> : 4 côtés, 4 angles droits</p>
                    <p><strong>Cercle</strong> : ensemble des points à égale distance du centre</p>
                    
                    <h3>Périmètres et Aires</h3>
                    <ul>
                        <li>Carré : P = 4c, A = c²</li>
                        <li>Rectangle : P = 2(L + l), A = L × l</li>
                        <li>Cercle : P = 2πr, A = πr²</li>
                    </ul>
                    ''',
                    'examples': [
                        'Un carré de 5cm a un périmètre de 20cm',
                        'Un cercle de rayon 3cm a une aire de 28.27cm²'
                    ]
                },
                {
                    'id': 3,
                    'title': 'Fractions et Nombres Rationnels',
                    'content': '''
                    <h3>Définition des fractions</h3>
                    <p>Une fraction a/b représente le quotient de a par b</p>
                    
                    <h3>Opérations sur les fractions</h3>
                    <ul>
                        <li><strong>Addition</strong> : a/b + c/d = (ad + bc)/(bd)</li>
                        <li><strong>Soustraction</strong> : a/b - c/d = (ad - bc)/(bd)</li>
                        <li><strong>Multiplication</strong> : a/b × c/d = ac/(bd)</li>
                        <li><strong>Division</strong> : a/b ÷ c/d = ad/(bc)</li>
                    </ul>
                    
                    <h3>Simplification</h3>
                    <p>Pour simplifier une fraction, on divise numérateur et dénominateur par leur PGCD</p>
                    ''',
                    'examples': [
                        '1/2 + 1/3 = 5/6',
                        '2/3 × 3/4 = 1/2',
                        '3/4 ÷ 1/2 = 3/2',
                        '4/6 = 2/3 (simplifié)'
                    ]
                },
                {
                    'id': 4,
                    'title': 'Proportionnalité et Pourcentages',
                    'content': '''
                    <h3>Grandeurs proportionnelles</h3>
                    <p>Deux grandeurs sont proportionnelles si leur rapport est constant</p>
                    
                    <h3>Tableau de proportionnalité</h3>
                    <p>Si a/b = c/d, alors a × d = b × c (produit en croix)</p>
                    
                    <h3>Pourcentages</h3>
                    <ul>
                        <li>Calculer p% d'un nombre : nombre × p/100</li>
                        <li>Augmentation de p% : nombre × (1 + p/100)</li>
                        <li>Réduction de p% : nombre × (1 - p/100)</li>
                    </ul>
                    ''',
                    'examples': [
                        '25% de 200 = 50',
                        'Augmenter 100 de 20% = 120',
                        'Réduire 150 de 10% = 135',
                        '3/5 = 60%'
                    ]
                }
            ]
        },
        'lycee': {
            'title': 'Mathématiques - Niveau Lycée',
            'chapters': [
                {
                    'id': 5,
                    'title': 'Fonctions et Dérivées',
                    'content': '''
                    <h3>Notion de fonction</h3>
                    <p>Une fonction f associe à chaque réel x un unique réel f(x)</p>
                    
                    <h3>Dérivée d'une fonction</h3>
                    <p>La dérivée f'(x) représente le coefficient directeur de la tangente</p>
                    
                    <h3>Règles de dérivation</h3>
                    <ul>
                        <li>(x^n)' = nx^(n-1)</li>
                        <li>(ax + b)' = a</li>
                        <li>(uv)' = u'v + uv'</li>
                        <li>(u/v)' = (u'v - uv')/v²</li>
                    </ul>
                    
                    <h3>Tableau de dérivées usuelles</h3>
                    <table border="1">
                        <tr><th>Fonction</th><th>Dérivée</th></tr>
                        <tr><td>x²</td><td>2x</td></tr>
                        <tr><td>x³</td><td>3x²</td></tr>
                        <tr><td>1/x</td><td>-1/x²</td></tr>
                        <tr><td>√x</td><td>1/(2√x)</td></tr>
                    </table>
                    ''',
                    'examples': [
                        'f(x) = x² → f\'(x) = 2x',
                        'f(x) = 3x + 2 → f\'(x) = 3',
                        'f(x) = 1/x → f\'(x) = -1/x²'
                    ]
                },
                {
                    'id': 6,
                    'title': 'Trigonométrie',
                    'content': '''
                    <h3>Fonctions trigonométriques</h3>
                    <p><strong>sin(x)</strong> : sinus de l'angle x</p>
                    <p><strong>cos(x)</strong> : cosinus de l'angle x</p>
                    <p><strong>tan(x)</strong> : tangente de l'angle x = sin(x)/cos(x)</p>
                    
                    <h3>Valeurs remarquables</h3>
                    <table border="1">
                        <tr><th>Angle</th><th>sin</th><th>cos</th><th>tan</th></tr>
                        <tr><td>0°</td><td>0</td><td>1</td><td>0</td></tr>
                        <tr><td>30°</td><td>1/2</td><td>√3/2</td><td>1/√3</td></tr>
                        <tr><td>45°</td><td>√2/2</td><td>√2/2</td><td>1</td></tr>
                        <tr><td>60°</td><td>√3/2</td><td>1/2</td><td>√3</td></tr>
                        <tr><td>90°</td><td>1</td><td>0</td><td>∞</td></tr>
                    </table>
                    
                    <h3>Formules importantes</h3>
                    <p>sin²(x) + cos²(x) = 1</p>
                    <p>cos(a - b) = cos(a)cos(b) + sin(a)sin(b)</p>
                    <p>sin(a - b) = sin(a)cos(b) - cos(a)sin(b)</p>
                    ''',
                    'examples': [
                        'sin(30°) = 1/2',
                        'cos(45°) = √2/2',
                        'tan(45°) = 1'
                    ]
                },
                {
                    'id': 7,
                    'title': 'Suites Numériques',
                    'content': '''
                    <h3>Définition d'une suite</h3>
                    <p>Une suite (u_n) est une fonction de ℕ dans ℝ</p>
                    
                    <h3>Suites arithmétiques</h3>
                    <p>u_{n+1} = u_n + r (raison r)</p>
                    <p>Terme général : u_n = u_0 + nr</p>
                    <p>Somme des n premiers termes : S_n = n(u_0 + u_n)/2</p>
                    
                    <h3>Suites géométriques</h3>
                    <p>u_{n+1} = q × u_n (raison q)</p>
                    <p>Terme général : u_n = u_0 × q^n</p>
                    <p>Somme des n premiers termes : S_n = u_0(1 - q^n)/(1 - q)</p>
                    
                    <h3>Limites de suites</h3>
                    <ul>
                        <li>Si -1 < q < 1, alors lim q^n = 0</li>
                        <li>Si q > 1, alors lim q^n = +∞</li>
                        <li>Si q = 1, alors lim q^n = 1</li>
                    </ul>
                    ''',
                    'examples': [
                        'Suite arithmétique : 2, 5, 8, 11... (r = 3)',
                        'Suite géométrique : 3, 6, 12, 24... (q = 2)',
                        'u_n = 2^n → lim = +∞'
                    ]
                },
                {
                    'id': 8,
                    'title': 'Probabilités',
                    'content': '''
                    <h3>Vocabulaire des probabilités</h3>
                    <p><strong>Univers Ω</strong> : ensemble de tous les résultats possibles</p>
                    <p><strong>Événement A</strong> : sous-ensemble de Ω</p>
                    <p><strong>P(A)</strong> : probabilité de l'événement A</p>
                    
                    <h3>Propriétés fondamentales</h3>
                    <ul>
                        <li>0 ≤ P(A) ≤ 1</li>
                        <li>P(Ω) = 1</li>
                        <li>P(∅) = 0</li>
                        <li>P(A̅) = 1 - P(A) (événement contraire)</li>
                    </ul>
                    
                    <h3>Probabilité conditionnelle</h3>
                    <p>P(A|B) = P(A ∩ B) / P(B)</p>
                    
                    <h3>Formule de Bayes</h3>
                    <p>P(A|B) = P(B|A) × P(A) / P(B)</p>
                    ''',
                    'examples': [
                        'Lancer un dé : P(obtenir 6) = 1/6',
                        'P(obtenir un nombre pair) = 3/6 = 1/2',
                        'Si P(A) = 0.3 et P(B) = 0.4, alors P(A ∪ B) ≤ 0.7'
                    ]
                }
            ]
        }
    },
    'philosophie': {
        'college': {
            'title': 'Philosophie - Niveau Collège',
            'chapters': [
                {
                    'id': 9,
                    'title': 'Introduction à la Philosophie',
                    'content': '''
                    <h3>Qu\'est-ce que la philosophie ?</h3>
                    <p>La philosophie est l\'amour de la sagesse (philos = amour, sophia = sagesse)</p>
                    
                    <h3>Les grandes questions philosophiques</h3>
                    <ul>
                        <li>Qui suis-je ? (question de l\'identité)</li>
                        <li>D\'où venons-nous ? (question de l\'origine)</li>
                        <li>Où allons-nous ? (question du devenir)</li>
                        <li>Comment devons-nous vivre ? (question morale)</li>
                    </ul>
                    
                    <h3>Les branches de la philosophie</h3>
                    <p><strong>Métaphysique</strong> : étude de l\'être et du réel</p>
                    <p><strong>Éthique</strong> : étude de la morale et des valeurs</p>
                    <p><strong>Logique</strong> : étude du raisonnement</p>
                    <p><strong>Épistémologie</strong> : étude de la connaissance</p>
                    ''',
                    'examples': [
                        'Socrate : "Connais-toi toi-même"',
                        'La question du sens de la vie',
                        'Le débat entre libre arbitre et déterminisme'
                    ]
                },
                {
                    'id': 10,
                    'title': 'La Morale au Quotidien',
                    'content': '''
                    <h3>Qu\'est-ce que la morale ?</h3>
                    <p>Ensemble des règles qui gouvernent la conduite humaine</p>
                    
                    <h3>Les valeurs morales fondamentales</h3>
                    <ul>
                        <li><strong>Honnêteté</strong> : dire la vérité</li>
                        <li><strong>Respect</strong> : traiter les autres avec dignité</li>
                        <li><strong>Justice</strong> : traiter équitablement chacun</li>
                        <li><strong>Courage</strong> : surmonter ses peurs</li>
                        <li><strong>Empathie</strong> : comprendre les sentiments des autres</li>
                    </ul>
                    
                    <h3>Dilemmes moraux courants</h3>
                    <p>Faut-il toujours dire la vérité ?</p>
                    <p>Peut-on désobéir à une loi injuste ?</p>
                    <p>Quelles sont nos responsabilités envers les autres ?</p>
                    ''',
                    'examples': [
                        'Le dilemme du tramway : sauver une personne ou cinq personnes ?',
                        'Mentir pour protéger quelqu\'un : est-ce justifiable ?',
                        'Le vol pour survivre : est-ce moralement acceptable ?'
                    ]
                },
                {
                    'id': 11,
                    'title': 'La Conscience et la Réalité',
                    'content': '''
                    <h3>Qu\'est-ce que la conscience ?</h3>
                    <p>La conscience est la capacité de percevoir soi-même et le monde</p>
                    
                    <h3>La perception du réel</h3>
                    <p>Nos sens nous donnent une image du monde, mais est-elle fiable ?</p>
                    
                    <h3>Rêve et réalité</h3>
                    <p>Comment savoir si nous rêvons ou si nous sommes éveillés ?</p>
                    
                    <h3>La vérité</h3>
                    <ul>
                        <li>Vérité objective : ce qui est indépendant de notre opinion</li>
                        <li>Vérité subjective : ce qui dépend de notre point de vue</li>
                        <li>Vérité relative : ce qui dépend du contexte</li>
                    </ul>
                    
                    <h3>Le biais de confirmation</h3>
                    <p>Nous avons tendance à chercher les informations qui confirment nos croyances</p>
                    ''',
                    'examples': [
                        'L\'illusion d\'optique : ce que nous voyons n\'est pas toujours la réalité',
                        'Le paradoxe du menteur : "Cette phrase est fausse"',
                        'La question de la réalité : vivons-nous dans une simulation ?'
                    ]
                }
            ]
        },
        'lycee': {
            'title': 'Philosophie - Niveau Lycée',
            'chapters': [
                {
                    'id': 12,
                    'title': 'La Théorie de la Connaissance',
                    'content': '''
                    <h3>L\'épistémologie</h3>
                    <p>Étude critique des sciences et de la connaissance</p>
                    
                    <h3>Sources de la connaissance</h3>
                    <ul>
                        <li><strong>L\'expérience sensible</strong> : perception par les sens</li>
                        <li><strong>La raison</strong> : déduction logique</li>
                        <li><strong>L\'intuition</strong> : connaissance immédiate</li>
                        <li><strong>Le témoignage</strong> : connaissance par autrui</li>
                    </ul>
                    
                    <h3>Le problème de l\'induction</h3>
                    <p>Peut-on passer de cas particuliers à une loi générale ?</p>
                    
                    <h3>Le scepticisme</h3>
                    <p>Doute systématique sur la possibilité de connaître</p>
                    
                    <h3>Le rationalisme vs l\'empirisme</h3>
                    <p>Rationalisme : la connaissance vient de la raison</p>
                    <p>Empirisme : la connaissance vient de l\'expérience</p>
                    ''',
                    'examples': [
                        'Le "cygne noir" : tous les cygnes étaient blancs jusqu\'à découvrir des cygnes noirs',
                        'Le problème de l\'induction de Hume : le soleil se lèvera-t-il demain ?',
                        'Le cogito de Descartes : "Je pense, donc je suis"'
                    ]
                },
                {
                    'id': 13,
                    'title': 'Liberté et Déterminisme',
                    'content': '''
                    <h3>Le problème du libre arbitre</h3>
                    <p>Sommes-nous vraiment libres de nos choix ?</p>
                    
                    <h3>Le déterminisme</h3>
                    <p>Tout événement a une cause et pourrait être prédit</p>
                    
                    <h3>Les arguments pour le libre arbitre</h3>
                    <ul>
                        <li>L\'expérience de la décision</li>
                        <li>La responsabilité morale</li>
                        <li>La créativité et l\'innovation</li>
                    </ul>
                    
                    <h3>Les arguments contre le libre arbitre</h3>
                    <ul>
                        <li>Le déterminisme scientifique</li>
                        <li>L\'influence de l\'éducation et de l\'environnement</li>
                        <li>Les facteurs biologiques et génétiques</li>
                    </ul>
                    
                    <h3>Solutions philosophiques</h3>
                    <p>Compatibilisme : liberté et déterminisme peuvent coexister</p>
                    <p>Liberté comme absence de contrainte externe</p>
                    ''',
                    'examples': [
                        'L\'expérience de pensée de Frankfort : deux hommes avec les mêmes désirs',
                        'Le déterminisme laplacien : un esprit qui connaîtrait tout pourrait prédire l\'avenir',
                        'Le dilemme de la prison : un prisonnier est-il responsable de s\'évader ?'
                    ]
                },
                {
                    'id': 14,
                    'title': 'Justice et État',
                    'content': '''
                    <h3>Qu\'est-ce que la justice ?</h3>
                    <p>Donner à chacun ce qui lui est dû</p>
                    
                    <h3>Théories de la justice</h3>
                    <ul>
                        <li><strong>Justice utilitariste</strong> : le plus grand bonheur pour le plus grand nombre</li>
                        <li><strong>Justice déontologique</strong> : respect des droits et devoirs</li>
                        <li><strong>Justice égalitaire</strong> : égalité des chances et des résultats</li>
                    </ul>
                    
                    <h3>Le contrat social</h3>
                    <p>Pourquoi obéissons-nous aux lois de l\'État ?</p>
                    
                    <h3>La justice distributive</h3>
                    <p>Comment répartir équitablement les ressources ?</p>
                    
                    <h3>Démocratie et justice</h3>
                    <p>La démocratie est-elle le meilleur régime pour assurer la justice ?</p>
                    ''',
                    'examples': [
                        'Le voile de l\'ignorance de Rawls : quelles règles choisirions-nous sans connaître notre position ?',
                        'Le dilemme du prisonnier : pourquoi la coopération est difficile',
                        'La théorie de la justice de Nozick : droits de propriété et État minimal'
                    ]
                }
            ]
        }
    },
    'litterature': {
        'college': {
            'title': 'Littérature - Niveau Collège',
            'chapters': [
                {
                    'id': 7,
                    'title': 'Les Genres Littéraires',
                    'content': '''
                    <h3>Les principaux genres littéraires</h3>
                    
                    <p><strong>Le roman</strong> : œuvre narrative en prose</p>
                    <ul>
                        <li>Roman d\'aventures</li>
                        <li>Roman historique</li>
                        <li>Roman de science-fiction</li>
                        <li>Roman policier</li>
                    </ul>
                    
                    <p><strong>Le théâtre</strong> : dialogue destiné à être joué</p>
                    <ul>
                        <li>Tragédie</li>
                        <li>Comédie</li>
                        <li>Drame</li>
                    </ul>
                    
                    <p><strong>La poésie</strong> : langage rythmé et imagé</p>
                    <ul>
                        <li>Sonnet (14 vers)</li>
                        <li>Haïku (5-7-5 syllabes)</li>
                        <li>Poème en vers libres</li>
                    </ul>
                    
                    <h3>Les figures de style</h3>
                    <ul>
                        <li><strong>Métaphore</strong> : "La mer est un miroir"</li>
                        <li><strong>Comparaison</strong> : "Les yeux comme des étoiles"</li>
                        <li><strong>Personnification</strong> : "Le vent murmure"</li>
                    </ul>
                    ''',
                    'examples': [
                        '"Les Misérables" - Victor Hugo (roman historique)',
                        '"Le Cid" - Corneille (tragédie)',
                        '"Les Fleurs du mal" - Baudelaire (poésie)'
                    ]
                }
            ]
        },
        'lycee': {
            'title': 'Littérature - Niveau Lycée',
            'chapters': [
                {
                    'id': 8,
                    'title': 'Le Mouvement Romantique',
                    'content': '''
                    <h3>Le Romantisme (fin XVIIIe - XIXe siècle)</h3>
                    <p>Réaction contre le classicisme et la raison des Lumières</p>
                    
                    <h3>Caractéristiques principales</h3>
                    <ul>
                        <li><strong>Culte du moi</strong> : expression des sentiments personnels</li>
                        <li><strong>Mélancolie</strong> : spleen, nostalgie</li>
                        <li><strong>Nature</strong> : refuge, miroir de l\'âme</li>
                        <li><strong>Rêve et imaginaire</strong> : évasion, fantastique</li>
                        <li><strong>Liberté</strong> : politique, artistique, amoureuse</li>
                    </ul>
                    
                    <h3>Auteurs et œuvres majeures</h3>
                    <p><strong>Victor Hugo</strong> : "Les Misérables", "Notre-Dame de Paris"</p>
                    <p><strong>Alphonse de Lamartine</strong> : "Méditations Poétiques"</p>
                    <p><strong>Alfred de Musset</strong> : "Les Nuits"</p>
                    <p><strong>George Sand</strong> : "Lélia"</p>
                    
                    <h3>Thèmes romantiques</h3>
                    <p>L\'amour impossible, la mort, l\'exil, la révolte</p>
                    <p>Le "mal du siècle" : désillusion de la jeunesse post-napoléonienne</p>
                    ''',
                    'examples': [
                        '"Le Lac" - Lamartine (mélancolie, temps)',
                        '"Confession d\'un enfant du siècle" - Musset (mal du siècle)',
                        '"Demain, dès l\'aube..." - Hugo (amour, deuil)'
                    ]
                }
            ]
        }
    },
    'histoire_geo': {
        'college': {
            'title': 'Histoire-Géographie - Niveau Collège',
            'chapters': [
                {
                    'id': 9,
                    'title': 'La Révolution Française',
                    'content': '''
                    <h3>Les causes de la Révolution</h3>
                    <ul>
                        <li><strong>Causes économiques</strong> : crise financière, impôts inégaux</li>
                        <li><strong>Causes sociales</strong> : privilèges nobiliaires, inégalités</li>
                        <li><strong>Causes politiques</strong> : monarchie absolue, absence de libertés</li>
                        <li><strong>Causes intellectuelles</strong> : Lumières, critique de l\'absolutisme</li>
                    </ul>
                    
                    <h3>Les grands événements</h3>
                    <p><strong>1789</strong> : États-Généraux, prise de la Bastille (14 juillet)</p>
                    <p><strong>1789-1791</strong> : Assemblée Constituante, Déclaration des droits</p>
                    <p><strong>1792-1795</strong> : Convention, Terreur, Directoire</p>
                    <p><strong>1799-1815</strong> : Consulat et Empire de Napoléon</p>
                    
                    <h3>Les acquis révolutionnaires</h3>
                    <ul>
                        <li>Déclaration des Droits de l\'Homme et du Citoyen</li>
                        <li>Abolition des privilèges (4 août 1789)</li>
                        <li>Égalité devant la loi</li>
                        <li>Suffrage censitaire masculin</li>
                    </ul>
                    ''',
                    'examples': [
                        '"Liberté, Égalité, Fraternité" - devise républicaine',
                        'La Marseillaise - hymne national',
                        'Le drapeau tricolore'
                    ]
                }
            ]
        },
        'lycee': {
            'title': 'Histoire-Géographie - Niveau Lycée',
            'chapters': [
                {
                    'id': 10,
                    'title': 'La Guerre Froide (1947-1991)',
                    'content': '''
                    <h3>Un monde bipolaire</h3>
                    <p><strong>Bloc de l\'Ouest</strong> : États-Unis, Europe de l\'Ouest, capitalisme</p>
                    <p><strong>Bloc de l\'Est</strong> : URSS, Europe de l\'Est, communisme</p>
                    
                    <h3>Les crises majeures</h3>
                    <ul>
                        <li><strong>Blocus de Berlin (1948-1949)</strong> : première confrontation</li>
                        <li><strong>Guerre de Corée (1950-1953)</strong> : premier conflit par procuration</li>
                        <li><strong>Crise de Cuba (1962)</strong> : au bord de la guerre nucléaire</li>
                        <li><strong>Guerre du Vietnam (1965-1975)</strong> : défaite américaine</li>
                        <li><strong>Mur de Berlin (1961-1989)</strong> : symbole de la division</li>
                    </ul>
                    
                    <h3>La dissuasion nucléaire</h3>
                    <p><strong>Équilibre de la terreur</strong> : MAD (Mutual Assured Destruction)</p>
                    <p>Doctrine : "qui frappe en premier meurt en second"</p>
                    
                    <h3>La fin de la Guerre Froide</h3>
                    <p><strong>Gorbatchev</strong> : perestroïka et glasnost</p>
                    <p><strong>Chute du Mur (1989)</strong> : réunification allemande</p>
                    <p><strong>Disparition de l\'URSS (1991)</strong> : fin du bipolaire</p>
                    ''',
                    'examples': [
                        'La crise des missiles de Cuba - 13 jours au bord du gouffre',
                        'La course à l\'espace - Spoutnik et Apollo',
                        'La doctrine Truman et le plan Marshall'
                    ]
                }
            ]
        }
    },
    'culture_generale': {
        'college': {
            'title': 'Culture Générale - Niveau Collège',
            'chapters': [
                {
                    'id': 11,
                    'title': 'Sciences et Découvertes',
                    'content': '''
                    <h3>Les grandes découvertes scientifiques</h3>
                    
                    <p><strong>Physique</strong></p>
                    <ul>
                        <li>Newton : gravitation universelle (1687)</li>
                        <li>Einstein : relativité (1905, 1915)</li>
                        <li>Curie : radioactivité (1898)</li>
                    </ul>
                    
                    <p><strong>Biologie</strong></p>
                    <ul>
                        <li>Darwin : théorie de l\'évolution (1859)</li>
                        <li>Pasteur : vaccins, pasteurisation</li>
                        <li>Watson et Crick : structure de l\'ADN (1953)</li>
                    </ul>
                    
                    <p><strong>Astronomie</strong></p>
                    <ul>
                        <li>Galilée : lunette astronomique, héliocentrisme</li>
                        <li>Hubble : expansion de l\'univers</li>
                        <li>Armstrong : premier pas sur la Lune (1969)</li>
                    </ul>
                    
                    <h3>Les inventions qui ont changé le monde</h3>
                    <ul>
                        <li>Imprimerie (Gutenberg, XVe siècle)</li>
                        <li>Machine à vapeur (James Watt, 1769)</li>
                        <li>Électricité (Edison, Tesla)</li>
                        <li>Internet (ARPANET, 1969)</li>
                    </ul>
                    ''',
                    'examples': [
                        'E = mc² - équation d\'Einstein',
                        'La pomme de Newton - découverte de la gravité',
                        'La pénicilline - Fleming (1928)'
                    ]
                }
            ]
        },
        'lycee': {
            'title': 'Culture Générale - Niveau Lycée',
            'chapters': [
                {
                    'id': 12,
                    'title': 'L\'Art et les Civilisations',
                    'content': '''
                    <h3>Les grandes périodes artistiques</h3>
                    
                    <p><strong>Antiquité</strong></p>
                    <ul>
                        <li>Art égyptien : pyramides, hiéroglyphes</li>
                        <li>Art grec : Parthénon, sculptures classiques</li>
                        <li>Art romain : Colisée, aqueducs</li>
                    </ul>
                    
                    <p><strong>Moyen Âge</strong></p>
                    <ul>
                        <li>Art roman : voûtes en berceau, sculptures</li>
                        <li>Art gothique : cathédrales, vitraux</li>
                        <li>Manuscrits enluminés</li>
                    </ul>
                    
                    <p><strong>Renaissance</strong></p>
                    <ul>
                        <li>Léonard de Vinci : Joconde, Homme de Vitruve</li>
                        <li>Michel-Ange : David, chapelle Sixtine</li>
                        <li>Raphaël : Écoles d\'Athènes</li>
                    </ul>
                    
                    <p><strong>Époque moderne</strong></p>
                    <ul>
                        <li>Impressionnisme : Monet, Renoir</li>
                        <li>Cubisme : Picasso</li>
                        <li>Surréalisme : Dalí, Magritte</li>
                    </ul>
                    
                    <h3>Les civilisations majeures</h3>
                    <p><strong>Mésopotamie</strong> : invention de l\'écriture</p>
                    <p><strong>Égypte</strong> : pharaons, hiéroglyphes</p>
                    <p><strong>Chine</strong> : Grande Muraille, inventions</p>
                    <p><strong>Grèce</strong> : démocratie, philosophie</p>
                    <p><strong>Rome</strong> : droit latin, ingénierie</p>
                    ''',
                    'examples': [
                        'La Joconde - chef-d\'œuvre de la Renaissance',
                        'Les pyramides de Gizeh - merveilles du monde',
                        'Le Parthénon - temple d\'Athènes'
                    ]
                }
            ]
        }
    }
}

# Citations inspirantes pour la philosophie et la culture
CITATIONS = {
    'philosophie': [
        {'auteur': 'Socrate', 'texte': 'Je sais que je ne sais rien'},
        {'auteur': 'Platon', 'texte': 'La connaissance est la nourriture de l\'âme'},
        {'auteur': 'Aristote', 'texte': 'Nous sommes ce que nous faisons répétitivement'},
        {'auteur': 'Descartes', 'texte': 'Je pense, donc je suis'},
        {'auteur': 'Kant', 'texte': 'Sapere aude ! Ose savoir !'},
        {'auteur': 'Sartre', 'texte': 'L\'homme est condamné à être libre'},
        {'auteur': 'Nietzsche', 'texte': 'Ce qui ne me tue pas me rend plus fort'},
        {'auteur': 'Montaigne', 'texte': 'Que sais-je ?'}
    ],
    'motivation': [
        {'auteur': 'Albert Camus', 'texte': 'Au milieu de l\'hiver, j\'ai découvert en moi un invincible été'},
        {'auteur': 'Victor Hugo', 'texte': 'Même les plus sombres nuits finissent par prendre fin'},
        {'auteur': 'Marie Curie', 'texte': 'La vie n\'est pas facile pour aucun d\'entre nous'},
        {'auteur': 'Einstein', 'texte': 'Le monde ne sera pas détruit par ceux qui font le mal'},
        {'auteur': 'Martin Luther King', 'texte': 'J\'ai fait un rêve'}
    ]
}

@app.route('/content/<subject>/<level>')
def get_content(subject, level):
    """Obtenir le contenu éducatif pour une matière et un niveau"""
    if subject not in CONTENT_DB or level not in CONTENT_DB[subject]:
        return jsonify({'error': 'Sujet ou niveau non trouvé'}), 404
    
    content = CONTENT_DB[subject][level]
    return jsonify(content)

@app.route('/content/<subject>/<level>/chapter/<int:chapter_id>')
def get_chapter(subject, level, chapter_id):
    """Obtenir un chapitre spécifique"""
    if subject not in CONTENT_DB or level not in CONTENT_DB[subject]:
        return jsonify({'error': 'Sujet ou niveau non trouvé'}), 404
    
    chapters = CONTENT_DB[subject][level]['chapters']
    chapter = next((c for c in chapters if c['id'] == chapter_id), None)
    
    if not chapter:
        return jsonify({'error': 'Chapitre non trouvé'}), 404
    
    return jsonify(chapter)

@app.route('/quotes/<category>')
def get_quotes(category):
    """Obtenir des citations inspirantes"""
    if category not in CITATIONS:
        return jsonify({'error': 'Catégorie non trouvée'}), 404
    
    # Retourner 3 citations aléatoires
    quotes = random.sample(CITATIONS[category], min(3, len(CITATIONS[category])))
    return jsonify({'quotes': quotes})

@app.route('/subjects')
def get_subjects():
    """Lister toutes les matières disponibles"""
    return jsonify({
        'subjects': list(CONTENT_DB.keys()),
        'levels': ['college', 'lycee']
    })

@app.route('/api/external/fact')
def get_random_fact():
    """API externe - fait culturel aléatoire (simulation)"""
    facts = [
        "Le cerveau humain contient environ 86 milliards de neurones",
        "La Tour Eiffel mesure 330 mètres de hauteur avec ses antennes",
        "Le mot ordinateur vient du latin 'ordinare' qui signifie mettre en ordre",
        "Le premier ordinateur électronique pesait 30 tonnes",
        "Internet a été inventé en 1969 sous le nom d'ARPANET",
        "Le nombre π a été calculé avec plus de 31 billions de décimales",
        "La vitesse de la lumière est d'environ 300 000 km/s",
        "Le corps humain produit environ 25 milliards de cellules chaque jour"
    ]
    
    return jsonify({
        'fact': random.choice(facts),
        'source': 'DEVNET Culture API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Endpoint de health check pour le monitoring"""
    return jsonify({
        'service': 'content-service',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_chapters': sum(len(data['chapters']) for subject_data in CONTENT_DB.values() for data in subject_data.values()),
        'total_quotes': sum(len(quotes) for quotes in CITATIONS.values())
    })

@app.route('/api/stats')
def get_stats():
    """Statistiques du service de contenu"""
    stats = {}
    for subject, levels in CONTENT_DB.items():
        stats[subject] = {}
        for level, data in levels.items():
            stats[subject][level] = {
                'chapters': len(data['chapters']),
                'title': data['title']
            }
    
    return jsonify({
        'content_statistics': stats,
        'quotes_statistics': {cat: len(quotes) for cat, quotes in CITATIONS.items()},
        'total_content_items': sum(len(data['chapters']) for subject_data in CONTENT_DB.values() for data in subject_data.values())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
