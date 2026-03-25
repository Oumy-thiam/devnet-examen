#!/bin/bash

# Script pour initialiser et pousser le projet sur GitHub
echo "🚀 Initialisation du repository GitHub pour DEVNET..."

# Configuration
GITHUB_USERNAME="votre-username-github"
REPO_NAME="devnet-examen"
GITHUB_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Veuillez installer Git d'abord."
    exit 1
fi

# Initialiser Git (si pas déjà fait)
if [ ! -d .git ]; then
    echo "📝 Initialisation de Git..."
    git init
    git config user.name "DEVNET Team"
    git config user.email "devnet@example.com"
fi

# Ajouter les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Créer .gitignore s'il n'existe pas
if [ ! -f .gitignore ]; then
    echo "📝 Création du .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.production

# SSL certificates
ssl/
*.pem
*.key
EOF
    git add .gitignore
fi

# Premier commit
echo "💾 Premier commit..."
git commit -m "🚀 Initial commit - Application DEVNET complète

✅ Fonctionnalités:
- 65 questions enrichies (5 matières)
- Quiz interactifs avec correction
- Révisions par chapitres
- 'Autres Questions' collaboratives
- Microservices Dockerisés
- Base PostgreSQL persistante

🐳 Architecture:
- main-app: Flask principal
- quiz-service: API quiz distribué
- api-service: Contenu éducatif
- network-monitor: Monitoring réseau
- db: PostgreSQL

🔧 Technologies:
- Flask, PostgreSQL, Docker
- Bootstrap 5, JavaScript
- Microservices, API REST"

# Ajouter le remote GitHub
echo "🔗 Configuration du remote GitHub..."
git remote add origin ${GITHUB_URL} 2>/dev/null || git remote set-url origin ${GITHUB_URL}

# Pousser sur GitHub
echo "📤 Pousser sur GitHub..."
git push -u origin main

echo "✅ Repository GitHub créé avec succès !"
echo ""
echo "🌐 Accès à votre repository :"
echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. Visitez votre repository GitHub"
echo "   2. Vérifiez que tous les fichiers sont présents"
echo "   3. Configurez les secrets GitHub Actions si nécessaire"
echo "   4. Partagez l'URL de votre repository"
echo ""
echo "🎯 Votre projet DEVNET est maintenant public sur GitHub !"
