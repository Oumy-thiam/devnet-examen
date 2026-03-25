# 📚 Application de Révision Distribuée - DEVNET

## 🎯 Projet d'Examen DEVNET - L3 RI ISI Keur Massar

Application web de révision pour lycéens et collégiens avec architecture réseau distribuée utilisant Flask, Docker et PostgreSQL.

## 📋 Description

Cette application permet aux élèves de :
- **Réviser** 5 matières : Mathématiques, Philosophie, Littérature, Histoire-Géographie, Culture Générale
- **Tester** leurs connaissances avec des quiz QCM interactifs
- **Suivre** leurs progrès avec des statistiques détaillées
- **Accéder** à du contenu éducatif structuré par niveau (Collège/Lycée)

## 🏗️ Architecture Technique

### Services distribués :
- **main-app** (Port 5000) : Interface principale et gestion des utilisateurs
- **quiz-service** (Port 5001) : Service spécialisé pour les quiz QCM
- **api-service** (Port 5002) : Service de contenu éducatif et culturel
- **network-monitor** (Port 5003) : Monitoring réseau et métriques système
- **postgres** (Port 5432) : Base de données PostgreSQL

### Réseau Docker :
- **appnet** : Réseau Docker personnalisé (172.20.0.0/16)
- Communication inter-services via le réseau Docker
- Isolation et sécurité des services

## 🚀 Installation et Démarrage Rapide

### Prérequis
- Docker Desktop installé
- Docker Compose
- Git

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <votre-repository-url>
cd DEVNET_examen
```

2. **Construire et démarrer les services**
```bash
docker-compose up --build -d
```

3. **Vérifier le statut des services**
```bash
docker-compose ps
```

4. **Accéder à l'application**
- Interface principale : http://localhost:5000
- Service Quiz : http://localhost:5001
- Service API : http://localhost:5002
- Monitoring : http://localhost:5003

### Arrêter les services
```bash
docker-compose down
```

## 📊 Services et Endpoints

### Main App (Port 5000)
- `GET /` : Page d'accueil et inscription
- `POST /register` : Inscription d'un utilisateur
- `GET /dashboard` : Tableau de bord personnel
- `GET /revision/<subject>` : Page de révision
- `GET /quiz/<subject>` : Page de quiz
- `POST /submit_quiz` : Soumission des réponses
- `GET /api/health` : Health check

### Quiz Service (Port 5001)
- `GET /quiz/<subject>/<level>` : Générer un quiz
- `POST /correct` : Corriger les réponses
- `GET /subjects` : Lister les matières
- `GET /api/health` : Health check
- `GET /api/stats` : Statistiques du service

### API Service (Port 5002)
- `GET /content/<subject>/<level>` : Contenu éducatif
- `GET /quotes/<category>` : Citations inspirantes
- `GET /api/external/fact` : Fait culturel aléatoire
- `GET /api/health` : Health check

### Network Monitor (Port 5003)
- `GET /api/metrics` : Métriques système
- `GET /api/services` : Statut des services
- `GET /api/history` : Historique des métriques

## 🗄️ Base de Données

### Tables PostgreSQL :
- `users` : Informations des utilisateurs
- `quiz_results` : Résultats des quiz
- `revision_sessions` : Sessions de révision
- `network_metrics` : Métriques réseau
- `service_logs` : Logs de communication inter-services

### Données de test :
- 3 utilisateurs de démonstration
- 21 questions QCM réparties par matière et niveau
- Contenu éducatif structuré

## 🔧 Configuration

### Variables d'environnement
```bash
DB_HOST=postgres
DB_NAME=revision_app
DB_USER=postgres
DB_PASSWORD=password
QUIZ_SERVICE_URL=http://quiz-service:5001
API_SERVICE_URL=http://api-service:5002
```

### Personnalisation
- Modifier `init_db.sql` pour ajouter des données
- Éditer les fichiers Python pour ajouter des fonctionnalités
- Adapter les templates HTML pour le design

## 🌐 Aspect Réseau du Projet

### Communication inter-services
- Les services communiquent via le réseau Docker `appnet`
- API RESTful pour l'échange de données
- Monitoring des communications et performances

### Monitoring réseau
- Métriques en temps réel (CPU, mémoire, réseau)
- Logs de communication entre services
- Health checks automatiques

### Scalabilité
- Architecture microservices
- Conteneurs isolés mais communicants
- Possibilité d'ajouter des instances supplémentaires

## 📱 Fonctionnalités

### Pour les élèves
- ✅ Inscription avec nom, prénom, niveau et matières
- ✅ Accès au contenu de révision structuré
- ✅ Quiz QCM avec correction immédiate
- ✅ Suivi des progrès et statistiques
- ✅ Interface moderne et responsive

### Pour l'administration
- ✅ Monitoring des services
- ✅ Métriques réseau et système
- ✅ Logs de communication
- ✅ Base de données centralisée

## 🎨 Design et Interface

- **Framework** : Bootstrap 5
- **Icons** : Font Awesome 6
- **Style** : Moderne avec dégradés et animations
- **Responsive** : Compatible mobile/desktop

## 🧪 Tests et Débogage

### Vérifier les services
```bash
curl http://localhost:5000/api/health
curl http://localhost:5001/api/health
curl http://localhost:5002/api/health
```

### Logs des services
```bash
docker-compose logs main-app
docker-compose logs quiz-service
docker-compose logs postgres
```

### Accès à la base de données
```bash
docker-compose exec postgres psql -U postgres -d revision_app
```

## 📈 Monitoring et Performance

### Métriques disponibles
- Utilisation CPU et mémoire
- Traffic réseau inter-services
- Temps de réponse des API
- Statistiques d'utilisation

### Health checks
- Vérification automatique toutes les 30 secondes
- Redémarrage automatique en cas d'échec
- Logs détaillés pour le débogage

## 🚀 Déploiement sur Docker Hub

### Construction des images
```bash
docker build -f Dockerfile.main -t votrenom/revision-main:latest .
docker build -f Dockerfile.quiz -t votrenom/revision-quiz:latest .
docker build -f Dockerfile.content -t votrenom/revision-content:latest .
docker build -f Dockerfile.monitor -t votrenom/revision-monitor:latest .
```

### Push vers Docker Hub
```bash
docker push votrenom/revision-main:latest
docker push votrenom/revision-quiz:latest
docker push votrenom/revision-content:latest
docker push votrenom/revision-monitor:latest
```

## 🔄 CI/CD (Optionnel)

### GitHub Actions
- Build automatique des images Docker
- Push vers Docker Hub sur chaque push
- Tests automatisés des services

### Pipeline de déploiement
1. Code push sur GitHub
2. Build des images Docker
3. Push vers Docker Hub
4. Déploiement automatique

## 📚 Support de Présentation

### Points clés à présenter
1. **Problème résolu** : Accès équitable à l'éducation
2. **Architecture** : Microservices distribués
3. **Aspect réseau** : Communication Docker, monitoring
4. **Technologies** : Flask, PostgreSQL, Docker
5. **Démonstration** : Fonctionnement complet

### Démonstration en direct
- Inscription d'un utilisateur
- Navigation dans les matières
- Passage d'un quiz QCM
- Monitoring des services
- Communication réseau

## 🐛 Dépannage

### Problèmes courants
- **Port déjà utilisé** : `netstat -ano | findstr :5000`
- **Docker ne démarre pas** : Vérifier Docker Desktop
- **Base de données inaccessible** : Vérifier les logs postgres
- **Services ne communiquent pas** : Vérifier le réseau appnet

### Solutions
- Redémarrer Docker Desktop
- Recréer le réseau : `docker network rm appnet`
- Reconstruire les images : `docker-compose build --no-cache`
- Vérifier les variables d'environnement

## 📝 Licence

Projet réalisé dans le cadre de l'examen DEVNET - L3 RI ISI Keur Massar

## 👥 Auteur

[Nom de l'étudiant] - Licence 3 Réseaux et Informatique

---

**Note** : Ce projet démontre la maîtrise des concepts réseaux, de la conteneurisation, et du développement web distribué, répondant à toutes les exigences du projet DEVNET.
