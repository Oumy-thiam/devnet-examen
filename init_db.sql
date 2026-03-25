-- Script d'initialisation de la base de données PostgreSQL
-- Projet DEVNET - Application de Révision

-- Extension pour les UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    level VARCHAR(50) CHECK (level IN ('college', 'lycee')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des matières sélectionnées par utilisateur
CREATE TABLE IF NOT EXISTS user_subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, subject)
);

-- Table des questions personnalisées des utilisateurs
CREATE TABLE IF NOT EXISTS user_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des résultats de quiz
CREATE TABLE IF NOT EXISTS quiz_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0),
    total_questions INTEGER NOT NULL CHECK (total_questions > 0),
    percentage INTEGER GENERATED ALWAYS AS (ROUND((score::FLOAT / total_questions) * 100)) STORED,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des sessions de révision
CREATE TABLE IF NOT EXISTS revision_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des métriques réseau (pour le monitoring)
CREATE TABLE IF NOT EXISTS network_metrics (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    cpu_usage FLOAT CHECK (cpu_usage >= 0 AND cpu_usage <= 100),
    memory_usage FLOAT CHECK (memory_usage >= 0 AND memory_usage <= 100),
    disk_usage FLOAT CHECK (disk_usage >= 0 AND disk_usage <= 100),
    network_sent BIGINT,
    network_recv BIGINT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des logs de communication inter-services
CREATE TABLE IF NOT EXISTS service_logs (
    id SERIAL PRIMARY KEY,
    source_service VARCHAR(100) NOT NULL,
    target_service VARCHAR(100) NOT NULL,
    request_type VARCHAR(50) NOT NULL,
    response_status INTEGER,
    response_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour optimiser les performances
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_quiz_results_user_id ON quiz_results(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_subject ON quiz_results(subject);
CREATE INDEX IF NOT EXISTS idx_revision_sessions_user_id ON revision_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_network_metrics_hostname ON network_metrics(hostname);
CREATE INDEX IF NOT EXISTS idx_network_metrics_timestamp ON network_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_service_logs_timestamp ON service_logs(timestamp);

-- Insérer des données de test (optionnel)
INSERT INTO users (username, email, level) VALUES 
('eleve_college1', 'college1@example.com', 'college'),
('eleve_lycee1', 'lycee1@example.com', 'lycee'),
('demo_user', 'demo@example.com', 'college')
ON CONFLICT (username) DO NOTHING;

-- Afficher un message de confirmation
DO $$
BEGIN
    RAISE NOTICE 'Base de données revision_app initialisée avec succès';
    RAISE NOTICE 'Tables créées: users, quiz_results, revision_sessions, network_metrics, service_logs';
END $$;
