# 🎯 DEVNET - Application de Révision Collaborative

## 📚 Description
Plateforme web de révision collaborative pour étudiants Collège/Lycée avec microservices Dockerisés.

## 🚀 Fonctionnalités
- ✅ **65 questions enrichies** (Maths, Philosophie, Littérature, Histoire, Culture)
- ✅ **Quiz interactifs** avec correction automatique
- ✅ **Révisions par chapitres** 
- ✅ **"Autres Questions"** : Collaboration entre élèves
- ✅ **Tableau de bord** personnalisé
- ✅ **Microservices** : 4 services + BDD PostgreSQL

## 🐳 Architecture Docker
- **main-app** : Application Flask principale
- **quiz-service** : Service de quiz distribué
- **api-service** : API de contenu
- **network-monitor** : Monitoring réseau
- **db** : PostgreSQL persistant

## 📋 Prérequis
- Docker Desktop
- Docker Compose
- Git

## 🔧 Installation

### 1. Clonez le repository
```bash
git clone https://github.com/votre-username/devnet-examen.git
cd devnet-examen
```

### 2. Lancez l'application
```bash
docker-compose up -d
```

### 3. Accédez à l'application
- **URL** : http://localhost:5000
- **Health check** : http://localhost:5000/api/health

## 🌐 Déploiement

### Local
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### Docker Hub
```bash
./build-and-push.sh
```

## 📊 Utilisation
1. **Inscrivez-vous** avec nom/email uniques
2. **Sélectionnez** vos matières
3. **Révisez** par chapitres
4. **Testez-vous** avec les quiz
5. **Collaborez** via "Autres Questions"

## 📝 Technologies
- **Backend** : Flask, PostgreSQL
- **Frontend** : Bootstrap 5, JavaScript
- **Containerisation** : Docker, Docker Compose
- **Architecture** : Microservices, API REST

## 🤝 Contributeurs
- DEVNET Team

## 📄 Licence
MIT License

---

**🚀 Prêt à l'emploi : Clonez, lancez, utilisez !**
