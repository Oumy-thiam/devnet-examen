#!/bin/bash

# Script de déploiement pour l'application DEVNET
echo "🚀 Déploiement de l'application DEVNET..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé. Création du fichier .env par défaut..."
    cp .env.example .env 2>/dev/null || echo "DB_PASSWORD=changez_ce_mot_de_passe" > .env
    echo "📝 Veuillez éditer le fichier .env avec vos configurations."
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose -f docker-compose.prod.yml down

# Construire les images
echo "🔨 Construction des images Docker..."
docker-compose -f docker-compose.prod.yml build

# Démarrer les services
echo "🎯 Démarrage des services..."
docker-compose -f docker-compose.prod.yml up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier l'état des services
echo "🔍 Vérification de l'état des services..."
docker-compose -f docker-compose.prod.yml ps

# Tester l'application
echo "🧪 Test de l'application..."
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ L'application est déployée avec succès !"
    echo "🌐 Accès à l'application : http://localhost:5000"
else
    echo "❌ L'application n'est pas accessible. Vérifiez les logs :"
    echo "docker-compose -f docker-compose.prod.yml logs"
fi

echo "📊 Pour voir les logs en temps réel :"
echo "docker-compose -f docker-compose.prod.yml logs -f"

echo "🛑 Pour arrêter l'application :"
echo "docker-compose -f docker-compose.prod.yml down"
