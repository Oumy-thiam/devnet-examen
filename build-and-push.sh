#!/bin/bash

# Script pour construire et pousser les images sur Docker Hub
echo "🐳 Construction et publication des images DEVNET sur Docker Hub..."

# Configuration
DOCKER_USERNAME="votre-username-dockerhub"
REPO_NAME="devnet-examen"
VERSION="v1.0.0"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

# Vérifier si l'utilisateur est connecté à Docker Hub
echo "🔐 Vérification de la connexion Docker Hub..."
docker login
if [ $? -ne 0 ]; then
    echo "❌ Veuillez vous connecter à Docker Hub d'abord avec: docker login"
    exit 1
fi

# Construire l'image principale
echo "🔨 Construction de l'image principale..."
docker build -f Dockerfile.main -t ${DOCKER_USERNAME}/${REPO_NAME}:latest .
docker build -f Dockerfile.main -t ${DOCKER_USERNAME}/${REPO_NAME}:${VERSION} .

# Construire l'image quiz
echo "🔨 Construction de l'image quiz..."
docker build -f Dockerfile.quiz -t ${DOCKER_USERNAME}/${REPO_NAME}-quiz:latest .
docker build -f Dockerfile.quiz -t ${DOCKER_USERNAME}/${REPO_NAME}-quiz:${VERSION} .

# Construire l'image API
echo "🔨 Construction de l'image API..."
docker build -f Dockerfile.content -t ${DOCKER_USERNAME}/${REPO_NAME}-api:latest .
docker build -f Dockerfile.content -t ${DOCKER_USERNAME}/${REPO_NAME}-api:${VERSION} .

# Construire l'image monitoring
echo "🔨 Construction de l'image monitoring..."
docker build -f Dockerfile.monitor -t ${DOCKER_USERNAME}/${REPO_NAME}-monitor:latest .
docker build -f Dockerfile.monitor -t ${DOCKER_USERNAME}/${REPO_NAME}-monitor:${VERSION} .

# Pousser les images sur Docker Hub
echo "📤 Publication des images sur Docker Hub..."

# Image principale
echo "📤 Publication de l'image principale..."
docker push ${DOCKER_USERNAME}/${REPO_NAME}:latest
docker push ${DOCKER_USERNAME}/${REPO_NAME}:${VERSION}

# Image quiz
echo "📤 Publication de l'image quiz..."
docker push ${DOCKER_USERNAME}/${REPO_NAME}-quiz:latest
docker push ${DOCKER_USERNAME}/${REPO_NAME}-quiz:${VERSION}

# Image API
echo "📤 Publication de l'image API..."
docker push ${DOCKER_USERNAME}/${REPO_NAME}-api:latest
docker push ${DOCKER_USERNAME}/${REPO_NAME}-api:${VERSION}

# Image monitoring
echo "📤 Publication de l'image monitoring..."
docker push ${DOCKER_USERNAME}/${REPO_NAME}-monitor:latest
docker push ${DOCKER_USERNAME}/${REPO_NAME}-monitor:${VERSION}

echo "✅ Toutes les images ont été publiées avec succès !"
echo ""
echo "📋 Images publiées :"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}:latest"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}:${VERSION}"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-quiz:latest"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-quiz:${VERSION}"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-api:latest"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-api:${VERSION}"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-monitor:latest"
echo "  • ${DOCKER_USERNAME}/${REPO_NAME}-monitor:${VERSION}"
echo ""
echo "🌐 Accès sur Docker Hub : https://hub.docker.com/u/${DOCKER_USERNAME}"
