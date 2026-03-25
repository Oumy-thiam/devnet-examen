# Guide de Déploiement - Application DEVNET

## 🚀 Déploiement Rapide

### Prérequis
- Docker Desktop installé
- Git (optionnel)

### 1. Préparation
```bash
# Cloner ou naviguer vers le projet
cd "C:\Users\dell\Desktop\DEVNET _examen"

# Configurer les variables d'environnement
cp .env.example .env  # ou éditer directement .env
```

### 2. Configuration
Éditez le fichier `.env` avec vos configurations :
```env
DB_PASSWORD=votre_mot_de_passe_securise
FLASK_ENV=production
SECRET_KEY=votre_cle_secrete
```

### 3. Déploiement
```bash
# Utiliser le script de déploiement
chmod +x deploy.sh
./deploy.sh

# Ou manuellement
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🌐 Accès à l'Application

- **URL principale** : http://localhost:5000
- **Health check** : http://localhost:5000/api/health

## 📊 Gestion des Services

### Vérifier l'état
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Voir les logs
```bash
# Tous les services
docker-compose -f docker-compose.prod.yml logs

# Service spécifique
docker-compose -f docker-compose.prod.yml logs main-app

# Logs en temps réel
docker-compose -f docker-compose.prod.yml logs -f
```

### Redémarrer un service
```bash
docker-compose -f docker-compose.prod.yml restart main-app
```

### Arrêter l'application
```bash
docker-compose -f docker-compose.prod.yml down
```

## 🔧 Maintenance

### Mise à jour
```bash
# Tirer les dernières modifications
git pull

# Reconstruire et redémarrer
docker-compose -f docker-compose.prod.yml up -d --build
```

### Sauvegarde de la base de données
```bash
# Créer une sauvegarde
docker exec devnet_db_prod pg_dump -U devnet_user devnet_prod > backup.sql

# Restaurer une sauvegarde
docker exec -i devnet_db_prod psql -U devnet_user devnet_prod < backup.sql
```

## 🌍 Déploiement Cloud

### AWS ECS
1. Pousser les images sur AWS ECR
2. Utiliser AWS ECS avec Fargate
3. Configurer Application Load Balancer

### Google Cloud Run
1. Pousser les images sur Google Container Registry
2. Déployer avec Cloud Run
3. Configurer Cloud Load Balancing

### Azure Container Instances
1. Pousser les images sur Azure Container Registry
2. Déployer avec Azure Container Instances
3. Configurer Azure Load Balancer

## 🔒 Sécurité

### Certificats SSL
```bash
# Générer des certificats auto-signés (développement)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem

# Utiliser Let's Encrypt (production)
certbot --nginx -d votre-domaine.com
```

### Variables d'environnement
- Ne jamais exposer les mots de passe dans le code
- Utiliser des secrets Docker ou des services de gestion des secrets
- Rotation régulière des clés et mots de passe

## 📈 Monitoring

### Métriques
- Utiliser Docker Desktop pour surveiller les conteneurs
- Configurer Prometheus + Grafana pour le monitoring avancé
- Activer les logs structurés

### Alertes
- Configurer des alertes sur l'état des services
- Surveiller l'utilisation CPU/Mémoire
- Alertes sur les erreurs 5xx

## 🚨 Dépannage

### Problèmes courants
1. **Port déjà utilisé** : Vérifier qu'aucune autre application n'utilise le port 5000
2. **Base de données inaccessible** : Vérifier le mot de passe dans .env
3. **Services ne démarrent pas** : Vérifier les logs avec `docker-compose logs`

### Commandes utiles
```bash
# Nettoyer tout (attention, supprime les données)
docker-compose -f docker-compose.prod.yml down -v

# Recréer les conteneurs
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Vérifier les réseaux
docker network ls
```

## 📞 Support

Pour toute question de déploiement :
1. Vérifier les logs
2. Consulter ce guide
3. Vérifier la documentation Docker

---

**Développé avec ❤️ pour DEVNET**
