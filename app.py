#!/usr/bin/env python3
"""
Application de Surveillance Réseau Distribuée
Projet DEVNET - L3 RI ISI Keur Massar
"""

from flask import Flask, render_template, jsonify, request
import psutil
import socket
import time
import requests
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuration de la base de données
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'network_monitor')
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
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS network_metrics (
                        id SERIAL PRIMARY KEY,
                        hostname VARCHAR(255),
                        cpu_usage FLOAT,
                        memory_usage FLOAT,
                        disk_usage FLOAT,
                        network_sent BIGINT,
                        network_recv BIGINT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS service_status (
                        id SERIAL PRIMARY KEY,
                        service_name VARCHAR(255),
                        hostname VARCHAR(255),
                        status VARCHAR(50),
                        response_time FLOAT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                print("Base de données initialisée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")
        finally:
            conn.close()

def get_system_metrics():
    """Collecter les métriques système"""
    hostname = socket.gethostname()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    
    return {
        'hostname': hostname,
        'cpu_usage': cpu_usage,
        'memory_usage': memory.percent,
        'disk_usage': disk.percent,
        'network_sent': network.bytes_sent,
        'network_recv': network.bytes_recv,
        'timestamp': datetime.now().isoformat()
    }

def save_metrics_to_db(metrics):
    """Sauvegarder les métriques dans la base de données"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO network_metrics 
                    (hostname, cpu_usage, memory_usage, disk_usage, network_sent, network_recv)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    metrics['hostname'],
                    metrics['cpu_usage'],
                    metrics['memory_usage'],
                    metrics['disk_usage'],
                    metrics['network_sent'],
                    metrics['network_recv']
                ))
                conn.commit()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des métriques: {e}")
        finally:
            conn.close()

def check_service_status(service_url, service_name):
    """Vérifier le statut d'un service distant"""
    try:
        start_time = time.time()
        response = requests.get(f"{service_url}/health", timeout=5)
        response_time = time.time() - start_time
        
        status = 'UP' if response.status_code == 200 else 'DOWN'
        
        # Sauvegarder le statut dans la base de données
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO service_status 
                        (service_name, hostname, status, response_time)
                        VALUES (%s, %s, %s, %s)
                    """, (service_name, socket.gethostname(), status, response_time))
                    conn.commit()
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du statut du service: {e}")
            finally:
                conn.close()
        
        return {
            'service_name': service_name,
            'status': status,
            'response_time': response_time,
            'url': service_url
        }
    except Exception as e:
        return {
            'service_name': service_name,
            'status': 'DOWN',
            'response_time': None,
            'url': service_url,
            'error': str(e)
        }

@app.route('/')
def index():
    """Page principale de l'application"""
    return render_template('index.html')

@app.route('/api/metrics')
def get_metrics():
    """API pour obtenir les métriques système actuelles"""
    metrics = get_system_metrics()
    save_metrics_to_db(metrics)
    return jsonify(metrics)

@app.route('/api/health')
def health_check():
    """Endpoint de health check pour le monitoring"""
    return jsonify({
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/services')
def check_services():
    """API pour vérifier le statut des services distants"""
    services = [
        {'name': 'Service Principal', 'url': 'http://localhost:5001'},
        {'name': 'Service Backup', 'url': 'http://localhost:5002'}
    ]
    
    results = []
    for service in services:
        result = check_service_status(service['url'], service['name'])
        results.append(result)
    
    return jsonify(results)

@app.route('/api/history')
def get_history():
    """API pour obtenir l'historique des métriques"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM network_metrics 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                """)
                results = cur.fetchall()
                return jsonify([dict(row) for row in results])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    # Initialiser la base de données au démarrage
    init_database()
    
    # Démarrer l'application Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
