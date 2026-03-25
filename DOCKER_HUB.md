# 🐳 Publication sur Docker Hub - Application DEVNET

## 📋 Vue d'ensemble

Ce guide explique comment publier votre application DEVNET sur Docker Hub pour la rendre accessible à tous.

## 🚀 Méthodes de publication

### 1. Publication Manuelle (Recommandé pour débutants)

#### Prérequis
- Compte Docker Hub créé
- Docker Desktop installé
- Terminal/PowerShell configuré

#### Étapes

1. **Configurer le script**
   ```bash
   # Éditer build-and-push.sh
   # Remplacer "votre-username-dockerhub" par votre vrai username
   ```

2. **Se connecter à Docker Hub**
   ```bash
   docker login
   # Entrer votre username et mot de passe Docker Hub
   ```

3. **Lancer la publication**
   ```bash
   chmod +x build-and-push.sh
   ./build-and-push.sh
   ```

### 2. Publication Automatique (GitHub Actions)

#### Prérequis
- Repository GitHub avec le code
- Secrets GitHub configurés
- Workflow GitHub Actions

#### Configuration des secrets GitHub
1. Allez dans votre repository GitHub
2. Settings → Secrets and variables → Actions
3. Ajoutez ces secrets :
   - `DOCKER_USERNAME`: Votre username Docker Hub
   - `DOCKER_PASSWORD`: Votre mot de passe Docker Hub (ou access token)

#### Déclenchement automatique
- ✅ **Push sur main** : Build et publication automatique
- ✅ **Tag de version** : Publication avec tag de version
- ✅ **Pull Request** : Build sans publication

## 📦 Images publiées

### Images principales
- `votre-username/devnet-examen:latest` : Image principale multi-arch
- `votre-username/devnet-examen:v1.0.0` : Version spécifique

### Services individuels
- `votre-username/devnet-examen-quiz:latest` : Service quiz
- `votre-username/devnet-examen-api:latest` : Service API de contenu
- `votre-username/devnet-examen-monitor:latest` : Service monitoring

## 🌐 Utilisation des images

### Pull simple
```bash
# Image principale
docker pull votre-username/devnet-examen:latest

# Service spécifique
docker pull votre-username/devnet-examen-quiz:latest
```

### Lancement avec Docker Compose
```yaml
version: '3.8'

services:
  app:
    image: votre-username/devnet-examen:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DB_HOST=db
      - DB_PASSWORD=votre_mot_de_passe
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: devnet
      POSTGRES_USER: devnet_user
      POSTGRES_PASSWORD: votre_mot_de_passe
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔧 Configuration avancée

### Multi-architecture supportée
- ✅ **linux/amd64** : Intel/AMD standard
- ✅ **linux/arm64** : ARM (Apple M1/M2, Raspberry Pi)

### Tags automatiques
- `latest` : Dernière version stable
- `v1.0.0` : Version spécifique
- `main` : Dernier commit sur la branche main

## 📊 Monitoring sur Docker Hub

### Statistiques publiques
- **Pulls** : Nombre de téléchargements
- **Stars** : Favoris des utilisateurs
- **Description** : Documentation visible
- **Tags** : Historique des versions

### Lien vers votre repository
```
https://hub.docker.com/r/votre-username/devnet-examen
```

## 🔒 Bonnes pratiques

### Sécurité
- ✅ **Jamais de mots de passe dans le code**
- ✅ **Utilisation des secrets GitHub**
- ✅ **Images de base officielles**
- ✅ **Scans de vulnérabilités**

### Performance
- ✅ **Multi-stage builds** : Images optimisées
- ✅ **Health checks** : Surveillance automatique
- ✅ **Labels structurés** : Métadonnées complètes

## 🚨 Dépannage

### Problèmes courants
1. **Permission denied** : `docker login` requis
2. **Repository not found** : Vérifier le nom du repository
3. **Build failed** : Logs dans GitHub Actions
4. **Push denied** : Permissions insuffisantes

### Commandes utiles
```bash
# Vérifier les images locales
docker images | grep devnet-examen

# Nettoyer les images locales
docker system prune -f

# Tester localement avant push
docker run -p 5000:5000 votre-username/devnet-examen:latest
```

## 📞 Support

Pour toute question sur la publication Docker Hub :
1. Vérifier les logs GitHub Actions
2. Consulter la documentation Docker Hub
3. Vérifier la configuration des secrets

---

**🐳 Votre application DEVNET prête pour Docker Hub !**
