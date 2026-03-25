#!/usr/bin/env python3
"""
Service de Quiz Distribué - Service Quiz
Projet DEVNET - L3 RI ISI Keur Massar
Service spécialisé pour la gestion des quiz QCM
"""

from flask import Flask, jsonify, request
import random
import json
import os
from datetime import datetime

app = Flask(__name__)

# Base de données des questions par matière et niveau
QUESTIONS_DB = {
    'mathematiques': {
        'college': [
            {
                'id': 1,
                'question': 'Quelle est la valeur de x dans l\'équation 2x + 5 = 13 ?',
                'options': ['x = 4', 'x = 8', 'x = 3', 'x = 6'],
                'correct': 0,
                'explanation': '2x + 5 = 13 → 2x = 8 → x = 4'
            },
            {
                'id': 2,
                'question': 'Quel est le périmètre d\'un carré de côté 5 cm ?',
                'options': ['10 cm', '15 cm', '20 cm', '25 cm'],
                'correct': 2,
                'explanation': 'Périmètre = 4 × côté = 4 × 5 = 20 cm'
            },
            {
                'id': 3,
                'question': 'Calculez: (3/4) × (8/9)',
                'options': ['2/3', '1/2', '3/4', '5/6'],
                'correct': 0,
                'explanation': '(3×8)/(4×9) = 24/36 = 2/3'
            },
            {
                'id': 22,
                'question': 'Quelle est l\'aire d\'un rectangle de 6m sur 4m ?',
                'options': ['10 m²', '24 m²', '12 m²', '20 m²'],
                'correct': 1,
                'explanation': 'Aire = longueur × largeur = 6 × 4 = 24 m²'
            },
            {
                'id': 23,
                'question': 'Calculez: 15% de 200',
                'options': ['15', '25', '30', '35'],
                'correct': 2,
                'explanation': '15% de 200 = 200 × 15/100 = 30'
            },
            {
                'id': 24,
                'question': 'Simplifiez la fraction 12/18',
                'options': ['2/3', '3/4', '4/6', '6/9'],
                'correct': 0,
                'explanation': '12/18 = (12÷6)/(18÷6) = 2/3'
            },
            {
                'id': 25,
                'question': 'Quel est le volume d\'un cube de 3 cm d\'arête ?',
                'options': ['9 cm³', '18 cm³', '27 cm³', '36 cm³'],
                'correct': 2,
                'explanation': 'Volume = côté³ = 3³ = 27 cm³'
            },
            {
                'id': 26,
                'question': 'Calculez: (-3) × (-4)',
                'options': ['-12', '-7', '12', '7'],
                'correct': 2,
                'explanation': 'Le produit de deux nombres négatifs est positif: (-3) × (-4) = 12'
            }
        ],
        'lycee': [
            {
                'id': 4,
                'question': 'Quelle est la dérivée de f(x) = 3x² + 2x - 5 ?',
                'options': ['f\'(x) = 6x + 2', 'f\'(x) = 3x + 2', 'f\'(x) = 6x² + 2', 'f\'(x) = 6x'],
                'correct': 0,
                'explanation': 'f\'(x) = 6x + 2 (dérivée de 3x² est 6x, de 2x est 2, de -5 est 0)'
            },
            {
                'id': 5,
                'question': 'Résolvez: sin(x) = 1/2 pour x ∈ [0, 2π]',
                'options': ['π/6 et 5π/6', 'π/3 et 2π/3', 'π/4 et 3π/4', 'π/2 et 3π/2'],
                'correct': 0,
                'explanation': 'sin(x) = 1/2 → x = π/6 ou x = 5π/6 dans [0, 2π]'
            },
            {
                'id': 27,
                'question': 'Quelle est la primitive de f(x) = 2x ?',
                'options': ['x² + C', '2x² + C', 'x + C', '2x + C'],
                'correct': 0,
                'explanation': 'La primitive de 2x est x² + C'
            },
            {
                'id': 28,
                'question': 'Calculez la limite: lim (x→0) sin(x)/x',
                'options': ['0', '1', '∞', '-1'],
                'correct': 1,
                'explanation': 'lim (x→0) sin(x)/x = 1 (limite remarquable)'
            },
            {
                'id': 29,
                'question': 'Quelle est la dérivée de f(x) = ln(x) ?',
                'options': ['f\'(x) = 1/x', 'f\'(x) = x', 'f\'(x) = ln(x)', 'f\'(x) = 1/x²'],
                'correct': 0,
                'explanation': 'La dérivée de ln(x) est 1/x'
            },
            {
                'id': 30,
                'question': 'Résolvez l\'équation: x² - 9 = 0',
                'options': ['x = 3 et x = -3', 'x = 3', 'x = -3', 'x = 9'],
                'correct': 0,
                'explanation': 'x² = 9 → x = ±3'
            },
            {
                'id': 31,
                'question': 'Quelle est la somme des termes d\'une suite arithmétique de 3 termes : 2, 5, 8 ?',
                'options': ['15', '13', '18', '20'],
                'correct': 0,
                'explanation': 'Somme = 2 + 5 + 8 = 15'
            },
            {
                'id': 32,
                'question': 'Calculez: ∫[0,1] x dx',
                'options': ['1/2', '1', '0', '2'],
                'correct': 0,
                'explanation': '∫[0,1] x dx = [x²/2]₀¹ = 1/2 - 0 = 1/2'
            }
        ]
    },
    'philosophie': {
        'college': [
            {
                'id': 6,
                'question': 'Qui a dit "Je pense, donc je suis" ?',
                'options': ['Platon', 'Descartes', 'Socrate', 'Aristote'],
                'correct': 1,
                'explanation': 'Cette phrase célèbre a été prononcée par René Descartes'
            },
            {
                'id': 7,
                'question': 'Qu\'est-ce que l\'épistémologie ?',
                'options': ['L\'étude de la connaissance', 'L\'étude de la morale', 'L\'étude de la politique', 'L\'étude de l\'art'],
                'correct': 0,
                'explanation': 'L\'épistémologie est la branche de la philosophie qui étudie la connaissance'
            },
            {
                'id': 33,
                'question': 'Quelle est la signification de "connais-toi toi-même" ?',
                'options': ['Connais tes limites', 'Sois arrogant', 'Ignore les autres', 'Change de personnalité'],
                'correct': 0,
                'explanation': 'Cette phrase de Socrate invite à l\'introspection et à la connaissance de soi'
            },
            {
                'id': 34,
                'question': 'Qu\'est-ce que la morale ?',
                'options': ['L\'étude des règles de conduite', 'L\'étude des nombres', 'L\'étude des étoiles', 'L\'étude des plantes'],
                'correct': 0,
                'explanation': 'La morale est l\'ensemble des règles qui gouvernent la conduite humaine'
            },
            {
                'id': 35,
                'question': 'Lequel de ces philosophes était Grec ?',
                'options': ['Socrate', 'Descartes', 'Kant', 'Nietzsche'],
                'correct': 0,
                'explanation': 'Socrate était un philosophe grec de l\'Antiquité (Ve siècle av. J.-C.)'
            },
            {
                'id': 36,
                'question': 'Qu\'est-ce que l\'éthique ?',
                'options': ['La réflexion sur la morale', 'L\'étude des animaux', 'La pratique sportive', 'La cuisine'],
                'correct': 0,
                'explanation': 'L\'éthique est la réflexion philosophique sur la morale et les valeurs'
            }
        ],
        'lycee': [
            {
                'id': 8,
                'question': 'Selon Kant, qu\'est-ce que l\'impératif catégorique ?',
                'options': ['Un principe moral universel', 'Une loi religieuse', 'Une règle sociale', 'Une opinion personnelle'],
                'correct': 0,
                'explanation': 'L\'impératif catégorique est un principe moral qui s\'applique universellement selon Kant'
            },
            {
                'id': 9,
                'question': 'Quelle est la différence entre éthique et morale ?',
                'options': ['L\'éthique est théorique, la morale est pratique', 'La morale est théorique, l\'éthique est pratique', 'Elles sont identiques', 'L\'éthique est religieuse, la morale est laïque'],
                'correct': 0,
                'explanation': 'L\'éthique est la réflexion philosophique sur la morale, qui est l\'ensemble des règles de conduite'
            },
            {
                'id': 37,
                'question': 'Qu\'est-ce que le rationalisme ?',
                'options': ['La connaissance vient de la raison', 'La connaissance vient des sens', 'La connaissance vient de Dieu', 'La connaissance vient de l\'expérience'],
                'correct': 0,
                'explanation': 'Le rationalisme affirme que la raison est la source principale de la connaissance'
            },
            {
                'id': 38,
                'question': 'Qu\'est-ce que l\'empirisme ?',
                'options': ['La connaissance vient de l\'expérience', 'La connaissance vient de la raison', 'La connaissance est innée', 'La connaissance vient de l\'intuition'],
                'correct': 0,
                'explanation': 'L\'empirisme soutient que toute connaissance vient de l\'expérience sensible'
            },
            {
                'id': 39,
                'question': 'Quel est le problème du libre arbitre ?',
                'options': ['Sommes-nous vraiment libres ?', 'Quelle est la meilleure religion ?', 'Comment devenir riche ?', 'Faut-il croire en Dieu ?'],
                'correct': 0,
                'explanation': 'Le problème du libre arbitre questionne si nous sommes vraiment libres de nos choix'
            },
            {
                'id': 40,
                'question': 'Qu\'est-ce que la justice selon Rawls ?',
                'options': ['L\'équité derrière un voile d\'ignorance', 'La loi du plus fort', 'La vengeance privée', 'L\'égalité parfaite'],
                'correct': 0,
                'explanation': 'Pour Rawls, la justice est ce que nous choisirions sans connaître notre position sociale'
            },
            {
                'id': 41,
                'question': 'Qu\'est-ce que le déterminisme ?',
                'options': ['Tout événement a une cause', 'Tout est hasard', 'Tout est magique', 'Tout est divin'],
                'correct': 0,
                'explanation': 'Le déterminisme affirme que tout événement a des causes et pourrait être prédit'
            }
        ]
    },
    'litterature': {
        'college': [
            {
                'id': 10,
                'question': 'Qui a écrit "Les Misérables" ?',
                'options': ['Victor Hugo', 'Alexandre Dumas', 'Émile Zola', 'Gustave Flaubert'],
                'correct': 0,
                'explanation': 'Victor Hugo a écrit "Les Misérables" en 1862'
            },
            {
                'id': 22,
                'question': 'Quel est le genre de "Roméo et Juliette" ?',
                'options': ['Tragédie', 'Comédie', 'Poésie', 'Roman'],
                'correct': 0,
                'explanation': 'Roméo et Juliette est une tragédie écrite par William Shakespeare'
            },
            {
                'id': 42,
                'question': 'Qui a écrit "Le Petit Prince" ?',
                'options': ['Antoine de Saint-Exupéry', 'Jules Verne', 'Marcel Pagnol', 'Albert Camus'],
                'correct': 0,
                'explanation': 'Antoine de Saint-Exupéry a écrit "Le Petit Prince" en 1943'
            },
            {
                'id': 43,
                'question': 'Qu\'est-ce qu\'un sonnet ?',
                'options': ['Un poème de 14 vers', 'Un poème de 12 vers', 'Un roman court', 'Une pièce de théâtre'],
                'correct': 0,
                'explanation': 'Un sonnet est un poème de 14 vers, généralement en deux quatrains et deux tercets'
            },
            {
                'id': 44,
                'question': 'Quel écrivain français a écrit "Candide" ?',
                'options': ['Voltaire', 'Rousseau', 'Montaigne', 'La Fontaine'],
                'correct': 0,
                'explanation': 'Voltaire a écrit "Candide ou l\'Optimisme" en 1759'
            },
            {
                'id': 45,
                'question': 'Qu\'est-ce que la métaphore ?',
                'options': ['Une figure de style', 'Un type de roman', 'Un personnage', 'Un lieu'],
                'correct': 0,
                'explanation': 'La métaphore est une figure de style qui établit une comparaison sans "comme"'
            }
        ],
        'lycee': [
            {
                'id': 23,
                'question': 'Quel mouvement littéraire est associé à Baudelaire ?',
                'options': ['Le symbolisme', 'Le romantisme', 'Le classicisme', 'Le surréalisme'],
                'correct': 0,
                'explanation': 'Baudelaire est un poète symboliste, auteur des "Fleurs du Mal"'
            },
            {
                'id': 24,
                'question': 'Qui a écrit "L\'Étranger" ?',
                'options': ['Albert Camus', 'Jean-Paul Sartre', 'Marcel Proust', 'André Malraux'],
                'correct': 0,
                'explanation': 'Albert Camus a publié "L\'Étranger" en 1942'
            },
            {
                'id': 46,
                'question': 'Qu\'est-ce que l\'absurde selon Camus ?',
                'options': ['La confrontation entre l\'homme et le silence du monde', 'La joie de vivre', 'La croyance en Dieu', 'L\'optimisme'],
                'correct': 0,
                'explanation': 'Pour Camus, l\'absurde naît de la confrontation entre l\'homme et le silence du monde'
            },
            {
                'id': 47,
                'question': 'Quel est le narrateur de "Du côté de chez Swann" ?',
                'options': ['Marcel', 'Charles Swann', 'Le narrateur anonyme', 'Proust lui-même'],
                'correct': 2,
                'explanation': 'Le narrateur de "À la recherche du temps perdu" est anonyme'
            },
            {
                'id': 48,
                'question': 'Qu\'est-ce que le théâtre de l\'absurde ?',
                'options': ['Un théâtre qui rejette les conventions', 'Un théâtre comique', 'Un théâtre historique', 'Un théâtre musical'],
                'correct': 0,
                'explanation': 'Le théâtre de l\'absurde rejette les conventions dramatiques traditionnelles'
            },
            {
                'id': 49,
                'question': 'Qui a écrit "Les Fleurs du Mal" ?',
                'options': ['Charles Baudelaire', 'Paul Verlaine', 'Arthur Rimbaud', 'Stéphane Mallarmé'],
                'correct': 0,
                'explanation': 'Charles Baudelaire a publié "Les Fleurs du Mal" en 1857'
            }
        ]
    },
    'histoire_geo': {
        'college': [
            {
                'id': 14,
                'question': 'En quelle année a commencé la Révolution française ?',
                'options': ['1789', '1776', '1799', '1804'],
                'correct': 0,
                'explanation': 'La Révolution française a commencé en 1789 avec la prise de la Bastille'
            },
            {
                'id': 15,
                'question': 'Quel est le plus long fleuve du monde ?',
                'options': ['Le Nil', 'L\'Amazone', 'Le Mississippi', 'Le Yangtsé'],
                'correct': 0,
                'explanation': 'Le Nil est traditionnellement considéré comme le plus long fleuve du monde'
            },
            {
                'id': 50,
                'question': 'Qui était le premier président des États-Unis ?',
                'options': ['George Washington', 'Thomas Jefferson', 'Abraham Lincoln', 'Benjamin Franklin'],
                'correct': 0,
                'explanation': 'George Washington a été le premier président des États-Unis (1789-1797)'
            },
            {
                'id': 51,
                'question': 'Quelle est la capitale du Japon ?',
                'options': ['Tokyo', 'Kyoto', 'Osaka', 'Nagoya'],
                'correct': 0,
                'explanation': 'Tokyo est la capitale du Japon depuis 1868'
            },
            {
                'id': 52,
                'question': 'En quelle année a eu lieu la chute du mur de Berlin ?',
                'options': ['1989', '1985', '1991', '1979'],
                'correct': 0,
                'explanation': 'Le mur de Berlin est tombé le 9 novembre 1989'
            },
            {
                'id': 53,
                'question': 'Quel continent est le plus peuplé ?',
                'options': ['L\'Asie', 'L\'Afrique', 'L\'Europe', 'L\'Amérique'],
                'correct': 0,
                'explanation': 'L\'Asie est le continent le plus peuplé avec plus de 4 milliards d\'habitants'
            }
        ],
        'lycee': [
            {
                'id': 16,
                'question': 'Quelle était la cause principale de la Première Guerre mondiale ?',
                'options': ['L\'assassinat de l\'archiduc François-Ferdinand', 'La crise économique', 'La révolution russe', 'La découverte de l\'Amérique'],
                'correct': 0,
                'explanation': 'L\'assassinat de l\'archiduc François-Ferdinand le 28 juin 1914 a déclenché la Première Guerre mondiale'
            },
            {
                'id': 17,
                'question': 'Quel est le plus grand océan du monde ?',
                'options': ['L\'océan Pacifique', 'L\'océan Atlantique', 'L\'océan Indien', 'L\'océan Arctique'],
                'correct': 0,
                'explanation': 'L\'océan Pacifique est le plus grand océan du monde'
            },
            {
                'id': 54,
                'question': 'Quelle est la théorie de la tectonique des plaques ?',
                'options': ['La surface terrestre est divisée en plaques mobiles', 'La Terre est plate', 'Les continents sont immobiles', 'Les océans sont des plaques'],
                'correct': 0,
                'explanation': 'La théorie de la tectonique des plaques explique que la surface terrestre est divisée en plaques mobiles'
            },
            {
                'id': 55,
                'question': 'Qu\'est-ce que la Guerre Froide ?',
                'options': ['La confrontation entre blocs de l\'Ouest et de l\'Est', 'Une guerre très froide', 'Une guerre en hiver', 'Une guerre commerciale'],
                'correct': 0,
                'explanation': 'La Guerre Froide (1947-1991) était la confrontation entre les blocs occidental et communiste'
            },
            {
                'id': 56,
                'question': 'Quel pays a le plus grand PIB au monde ?',
                'options': ['Les États-Unis', 'La Chine', 'Le Japon', 'L\'Allemagne'],
                'correct': 0,
                'explanation': 'Les États-Unis ont le plus grand PIB nominal au monde'
            },
            {
                'id': 57,
                'question': 'Qu\'est-ce que la mondialisation ?',
                'options': ['L\'intégration économique mondiale', 'La création d\'un seul pays', 'La fin des frontières', 'La domination d\'un pays'],
                'correct': 0,
                'explanation': 'La mondialisation est le processus d\'intégration économique et culturelle à l\'échelle mondiale'
            }
        ]
    },
    'culture_generale': {
        'college': [
            {
                'id': 19,
                'question': 'Quel est l\'organe le plus grand du corps humain ?',
                'options': ['La peau', 'Le foie', 'Le cœur', 'Les poumons'],
                'correct': 0,
                'explanation': 'La peau est le plus grand organe du corps humain avec une surface d\'environ 2m²'
            },
            {
                'id': 58,
                'question': 'Qui a peint la Joconde ?',
                'options': ['Léonard de Vinci', 'Picasso', 'Van Gogh', 'Monet'],
                'correct': 0,
                'explanation': 'Léonard de Vinci a peint la Joconde (Mona Lisa) entre 1503 et 1519'
            },
            {
                'id': 59,
                'question': 'Quelle est la vitesse de la lumière ?',
                'options': ['Environ 300 000 km/s', 'Environ 150 000 km/s', 'Environ 1 000 km/s', 'Environ 500 000 km/s'],
                'correct': 0,
                'explanation': 'La vitesse de la lumière dans le vide est d\'environ 300 000 km/s'
            },
            {
                'id': 60,
                'question': 'Quel est l\'instrument le plus aigu d\'un orchestre ?',
                'options': ['Le piccolo', 'La flûte traversière', 'Le violon', 'La trompette'],
                'correct': 0,
                'explanation': 'Le piccolo est l\'instrument le plus aigu, jouant une octave au-dessus de la flûte'
            },
            {
                'id': 61,
                'question': 'Combien de continents y a-t-il sur Terre ?',
                'options': ['7', '5', '6', '8'],
                'correct': 0,
                'explanation': 'Il y a 7 continents : Afrique, Amérique, Asie, Europe, Océanie, Antarctique'
            }
        ],
        'lycee': [
            {
                'id': 20,
                'question': 'Qu\'est-ce que l\'ADN ?',
                'options': ['La molécule contenant l\'information génétique', 'Une hormone', 'Une vitamine', 'Un minéral'],
                'correct': 0,
                'explanation': 'L\'ADN (Acide Désoxyribonucléique) contient l\'information génétique des êtres vivants'
            },
            {
                'id': 21,
                'question': 'Quel est le principe de la relativité d\'Einstein ?',
                'options': ['Le temps et l\'espace sont relatifs', 'La vitesse de la lumière est variable', 'La masse est constante', 'L\'énergie est infinie'],
                'correct': 0,
                'explanation': 'La théorie de la relativité montre que le temps et l\'espace sont relatifs à l\'observateur'
            },
            {
                'id': 62,
                'question': 'Qu\'est-ce que la photosynthèse ?',
                'options': ['La production de glucose à partir de lumière', 'La respiration des plantes', 'La croissance des racines', 'La reproduction des fleurs'],
                'correct': 0,
                'explanation': 'La photosynthèse est le processus par lequel les plantes produisent du glucose à partir de lumière'
            },
            {
                'id': 63,
                'question': 'Quel est le plus grand mammifère ?',
                'options': ['La baleine bleue', 'L\'éléphant', 'Le girafe', 'Le rhinocéros'],
                'correct': 0,
                'explanation': 'La baleine bleue est le plus grand animal ayant jamais existé'
            },
            {
                'id': 64,
                'question': 'Qu\'est-ce que l\'effet de serre ?',
                'options': ['Le réchauffement de l\'atmosphère', 'La culture en serre', 'L\'effet de la chaleur sur les plantes', 'La protection des plantes'],
                'correct': 0,
                'explanation': 'L\'effet de serre est le réchauffement de l\'atmosphère dû à certains gaz'
            },
            {
                'id': 65,
                'question': 'Qui a développé la théorie de l\'évolution ?',
                'options': ['Charles Darwin', 'Albert Einstein', 'Isaac Newton', 'Louis Pasteur'],
                'correct': 0,
                'explanation': 'Charles Darwin a développé la théorie de l\'évolution par sélection naturelle'
            }
        ]
    }
}

@app.route('/quiz/<subject>/<level>')
def get_quiz(subject, level):
    """Générer un quiz pour une matière et un niveau donnés"""
    if subject not in QUESTIONS_DB or level not in QUESTIONS_DB[subject]:
        return jsonify({'error': 'Sujet ou niveau non trouvé'}), 404
    
    questions = QUESTIONS_DB[subject][level]
    
    # Sélectionner 5 questions aléatoires
    selected_questions = random.sample(questions, min(5, len(questions)))
    
    # Mélanger les options pour chaque question
    for question in selected_questions:
        options = question['options'].copy()
        correct_answer = options[question['correct']]
        random.shuffle(options)
        question['correct'] = options.index(correct_answer)
        question['options'] = options
    
    return jsonify({
        'subject': subject,
        'level': level,
        'questions': selected_questions,
        'total_questions': len(selected_questions)
    })

@app.route('/correct', methods=['POST'])
def correct_quiz():
    """Corriger les réponses d'un quiz"""
    data = request.get_json()
    subject = data.get('subject')
    level = data.get('level')
    user_answers = data.get('answers', [])
    
    if subject not in QUESTIONS_DB or level not in QUESTIONS_DB[subject]:
        return jsonify({'error': 'Sujet ou niveau non trouvé'}), 404
    
    questions = QUESTIONS_DB[subject][level]
    score = 0
    results = []
    
    for i, user_answer in enumerate(user_answers):
        if i < len(questions):
            question = questions[i]
            is_correct = user_answer == question['correct']
            
            if is_correct:
                score += 1
            
            results.append({
                'question_id': question['id'],
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
    
    return jsonify({
        'score': score,
        'total_questions': len(user_answers),
        'percentage': round((score / len(user_answers)) * 100, 2),
        'results': results,
        'grade': get_grade(score, len(user_answers))
    })

def get_grade(score, total):
    """Déterminer la note en fonction du score"""
    percentage = (score / total) * 100
    
    if percentage >= 90:
        return 'Excellent'
    elif percentage >= 80:
        return 'Très bien'
    elif percentage >= 70:
        return 'Bien'
    elif percentage >= 60:
        return 'Assez bien'
    elif percentage >= 50:
        return 'Passable'
    else:
        return 'À améliorer'

@app.route('/subjects')
def get_subjects():
    """Lister toutes les matières disponibles"""
    return jsonify({
        'subjects': list(QUESTIONS_DB.keys()),
        'levels': ['college', 'lycee']
    })

@app.route('/api/health')
def health_check():
    """Endpoint de health check pour le monitoring"""
    return jsonify({
        'service': 'quiz-service',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_questions': sum(len(questions) for subject_data in QUESTIONS_DB.values() for questions in subject_data.values())
    })

@app.route('/api/stats')
def get_stats():
    """Statistiques du service de quiz"""
    stats = {}
    for subject, levels in QUESTIONS_DB.items():
        stats[subject] = {}
        for level, questions in levels.items():
            stats[subject][level] = len(questions)
    
    return jsonify({
        'statistics': stats,
        'total_subjects': len(QUESTIONS_DB),
        'total_questions': sum(len(questions) for subject_data in QUESTIONS_DB.values() for questions in subject_data.values())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
