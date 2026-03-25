#!/usr/bin/env python3
"""
Application Principale de Révision - Service Frontend
Projet DEVNET - L3 RI ISI Keur Massar
Application de révision pour lycéens et collégiens
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

app = Flask(__name__)
app.secret_key = 'devnet_revision_secret_key_2024'

# Configuration des services
QUIZ_SERVICE_URL = os.environ.get('QUIZ_SERVICE_URL', 'http://quiz-service:5001')
API_SERVICE_URL = os.environ.get('API_SERVICE_URL', 'http://api-service:5002')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'revision_app')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

def get_db_connection():
    """Établir la connexion à la base de données PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def init_database():
    """Initialiser la base de données avec les tables nécessaires"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Table des utilisateurs
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255),
                        level VARCHAR(50), -- 'college' ou 'lycee'
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Table des matières sélectionnées par utilisateur
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_subjects (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                        subject VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, subject)
                    )
                """)
                
                # Table des résultats de quiz
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_results (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID REFERENCES users(id),
                        subject VARCHAR(100),
                        level VARCHAR(50),
                        score INTEGER,
                        total_questions INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Table des sessions de révision
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS revision_sessions (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID REFERENCES users(id),
                        subject VARCHAR(100),
                        duration_minutes INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                print("Base de données initialisée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")
        finally:
            conn.close()

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        level = request.form.get('level')
        subjects = request.form.getlist('subjects')
        
        if not subjects:
            return render_template('register.html', error="Veuillez sélectionner au moins une matière")
        
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    # Vérifier si l'utilisateur existe déjà
                    cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                    existing_user = cur.fetchone()
                    
                    if existing_user:
                        return render_template('register.html', error="Ce nom d'utilisateur ou cet email est déjà utilisé")
                    
                    # Créer l'utilisateur
                    cur.execute("""
                        INSERT INTO users (username, email, level)
                        VALUES (%s, %s, %s)
                    """, (username, email, level))
                    conn.commit()
                    
                    # Récupérer l'ID de l'utilisateur créé
                    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                    user = cur.fetchone()
                    user_id = user[0]
                    
                    # Sauvegarder les matières sélectionnées
                    for subject in subjects:
                        cur.execute("""
                            INSERT INTO user_subjects (user_id, subject)
                            VALUES (%s, %s)
                        """, (user_id, subject))
                    
                    conn.commit()
                    
                    session['user_id'] = user_id
                    session['username'] = username
                    session['level'] = level
                    
                    return redirect(url_for('dashboard'))
            except Exception as e:
                return render_template('register.html', error=f"Erreur: {e}")
            finally:
                conn.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Tableau de bord de l'utilisateur"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Récupérer les statistiques et matières de l'utilisateur
    conn = get_db_connection()
    user_stats = {}
    user_subjects = []
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Récupérer les matières sélectionnées
                cur.execute("""
                    SELECT subject FROM user_subjects 
                    WHERE user_id = %s
                """, (session['user_id'],))
                subjects_result = cur.fetchall()
                user_subjects = [row['subject'] for row in subjects_result]
                
                # Statistiques des quiz
                cur.execute("""
                    SELECT subject, AVG(score) as avg_score, COUNT(*) as quiz_count
                    FROM quiz_results 
                    WHERE user_id = %s
                    GROUP BY subject
                """, (session['user_id'],))
                user_stats['quiz_stats'] = cur.fetchall()
                
                # Sessions de révision
                cur.execute("""
                    SELECT subject, SUM(duration_minutes) as total_time, COUNT(*) as session_count
                    FROM revision_sessions 
                    WHERE user_id = %s
                    GROUP BY subject
                """, (session['user_id'],))
                user_stats['revision_stats'] = cur.fetchall()
                
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
        finally:
            conn.close()
    
    return render_template('dashboard.html', user_stats=user_stats, user_subjects=user_subjects)

@app.route('/revision/<subject>')
def revision(subject):
    """Page de révision pour une matière"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Récupérer le contenu de révision depuis le service API
    try:
        response = requests.get(f"{API_SERVICE_URL}/content/{subject}/{session['level']}")
        if response.status_code == 200:
            content = response.json()
        else:
            content = {'error': 'Contenu non disponible'}
    except Exception as e:
        content = {'error': f'Erreur de connexion au service API: {e}'}
    
    return render_template('revision.html', subject=subject, content=content)

@app.route('/quiz/<subject>')
def quiz(subject):
    """Page de quiz pour une matière"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Récupérer les questions depuis le service de quiz
    try:
        response = requests.get(f"{QUIZ_SERVICE_URL}/quiz/{subject}/{session['level']}")
        if response.status_code == 200:
            quiz_data = response.json()
        else:
            quiz_data = {'error': 'Quiz non disponible'}
    except Exception as e:
        quiz_data = {'error': f'Erreur de connexion au service de quiz: {e}'}
    
    return render_template('quiz.html', subject=subject, quiz_data=quiz_data)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    """Soumettre une question personnalisée"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    question_text = request.form.get('question_text')
    subject = request.form.get('subject')
    
    if not question_text or not subject:
        return jsonify({'error': 'Question et matière requis'}), 400
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Insérer la question personnalisée
                cur.execute("""
                    INSERT INTO user_questions (user_id, question_text, subject, created_at)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """, (session['user_id'], question_text, subject))
                conn.commit()
                
                return jsonify({'success': True, 'message': 'Question soumise avec succès'})
        except Exception as e:
            return jsonify({'error': f"Erreur: {e}"}), 500
        finally:
            conn.close()
    
    return jsonify({'error': 'Erreur de connexion à la base de données'}), 500

@app.route('/get_user_questions/<subject>')
def get_user_questions(subject):
    """Récupérer les questions des utilisateurs pour une matière"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT uq.question_text, uq.created_at, u.username
                    FROM user_questions uq
                    JOIN users u ON uq.user_id = u.id
                    WHERE uq.subject = %s
                    ORDER BY uq.created_at DESC
                    LIMIT 20
                """, (subject,))
                questions = cur.fetchall()
                
                return jsonify({'questions': [dict(q) for q in questions]})
        except Exception as e:
            return jsonify({'error': f"Erreur: {e}"}), 500
        finally:
            conn.close()
    
    return jsonify({'error': 'Erreur de connexion à la base de données'}), 500

@app.route('/other_questions/<subject>')
def other_questions(subject):
    """Page des questions personnalisées des utilisateurs"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Vérifier si l'utilisateur a sélectionné cette matière
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT subject FROM user_subjects 
                    WHERE user_id = %s AND subject = %s
                """, (session['user_id'], subject))
                if not cur.fetchone():
                    return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            conn.close()
    
    # Informations sur la matière
    subjects_info = {
        'mathematiques': {'title': 'Mathématiques', 'icon': '📐'},
        'philosophie': {'title': 'Philosophie', 'icon': '🤔'},
        'litterature': {'title': 'Littérature', 'icon': '📖'},
        'histoire_geo': {'title': 'Histoire-Géographie', 'icon': '🌍'},
        'culture_generale': {'title': 'Culture Générale', 'icon': '🎯'}
    }
    
    subject_info = subjects_info.get(subject, {'title': subject, 'icon': '📚'})
    
    return render_template('other_questions.html', subject=subject, subject_info=subject_info)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """Soumettre les résultats d'un quiz"""
    if 'user_id' not in session:
        return jsonify({'error': 'Non connecté'}), 401
    
    subject = request.form.get('subject')
    answers = request.form.getlist('answers')
    
    # Convertir les réponses en entiers
    answers = [int(answer) for answer in answers]
    
    # Envoyer les réponses au service de quiz pour correction
    try:
        response = requests.post(f"{QUIZ_SERVICE_URL}/correct", json={
            'subject': subject,
            'level': session['level'],
            'answers': answers
        })
        
        if response.status_code == 200:
            result = response.json()
            
            # Sauvegarder le résultat dans la base de données
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO quiz_results (user_id, subject, level, score, total_questions)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            session['user_id'],
                            subject,
                            session['level'],
                            result['score'],
                            result['total_questions']
                        ))
                        conn.commit()
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde du résultat: {e}")
                finally:
                    conn.close()
            
            return jsonify(result)
        else:
            return jsonify({'error': 'Erreur lors de la correction'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erreur de connexion: {e}'}), 500

@app.route('/track_session', methods=['POST'])
def track_session():
    """Suivre une session de révision"""
    if 'user_id' not in session:
        return jsonify({'error': 'Non connecté'}), 401
    
    subject = request.form.get('subject')
    duration = request.form.get('duration')
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO revision_sessions (user_id, subject, duration_minutes)
                    VALUES (%s, %s, %s)
                """, (session['user_id'], subject, duration))
                conn.commit()
                return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({'error': 'Erreur de base de données'}), 500

@app.route('/api/health')
def health_check():
    """Endpoint de health check pour le monitoring"""
    return jsonify({
        'service': 'main-app',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'dependencies': {
            'quiz_service': QUIZ_SERVICE_URL,
            'api_service': API_SERVICE_URL,
            'database': DB_HOST
        }
    })

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
