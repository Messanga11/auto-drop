# 🚀 Guide de démarrage rapide

## Prérequis

- Python 3.11+
- Node.js 20+
- SQLite 3+ (inclus avec Python, utilisé en développement)
- Redis 7.4+ (optionnel en développement, ou Docker)
- Ollama (optionnel, pour le chatbot WhatsApp)

**Note** : En développement, SQLite est utilisé par défaut (pas besoin de PostgreSQL).

## Installation rapide

### Option 1 : Script automatique

```bash
./start-dev.sh
```

### Option 2 : Installation manuelle

#### 1. Backend

```bash
cd backend

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env (copier depuis .env.example et modifier)
cp .env.example .env
# Éditer .env avec vos credentials

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Créer le fichier .env.local (copier depuis .env.example et modifier)
cp .env.example .env.local
# Éditer .env.local

# Lancer le serveur de développement
npm run dev
```

## Services

Une fois lancés, les services sont disponibles sur :

- **Backend API** : http://localhost:8000
- **Frontend** : http://localhost:3000
- **Documentation API (Swagger)** : http://localhost:8000/docs
- **Documentation API (ReDoc)** : http://localhost:8000/redoc

## Base de données

### Développement (SQLite)

Par défaut, le projet utilise **SQLite** en développement. Aucune installation supplémentaire n'est nécessaire !

Le fichier de base de données `dropshipping.db` sera créé automatiquement dans le dossier `backend/`.

### Production (PostgreSQL)

Pour la production, utilisez PostgreSQL :

```bash
# Avec Docker
docker run --name postgres-dropshipping \
  -e POSTGRES_PASSWORD=dropshipping_password \
  -e POSTGRES_DB=dropshipping \
  -e POSTGRES_USER=dropshipping \
  -p 5432:5432 \
  -d postgres:16-alpine
```

Puis modifiez `DATABASE_URL` dans `.env` :
```env
DATABASE_URL=postgresql+asyncpg://dropshipping:dropshipping_password@localhost:5432/dropshipping
```

### Redis (optionnel)

```bash
docker run --name redis-dropshipping \
  -p 6379:6379 \
  -d redis:7.4-alpine
```

### Appliquer les migrations

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Vérification

### Test du backend

```bash
curl http://localhost:8000/health
# Devrait retourner: {"status":"healthy"}
```

### Test du frontend

Ouvrir http://localhost:3000 dans votre navigateur.

## Configuration minimale

Pour un démarrage rapide sans toutes les intégrations externes, le fichier `.env` minimal doit contenir :

```env
# SQLite pour développement (créé automatiquement)
DATABASE_URL=sqlite+aiosqlite:///./dropshipping.db

# Redis (optionnel en développement)
REDIS_URL=redis://localhost:6379/0

SECRET_KEY=dev-secret-key
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

**Note** : Avec SQLite, vous n'avez pas besoin de démarrer PostgreSQL !

Les autres variables (Apify, Creatify, Meta, TikTok, WhatsApp) sont optionnelles et peuvent être ajoutées plus tard.

## Dépannage

### Erreur "Module not found"

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Erreur de connexion à la base de données

Vérifier que PostgreSQL est démarré et que les credentials dans `.env` sont corrects.

### Erreur de connexion à Redis

Vérifier que Redis est démarré et accessible sur le port 6379.

## Prochaines étapes

1. Configurer les credentials API (Apify, Creatify, Meta, TikTok, WhatsApp)
2. Lancer un scraping de test : `POST /scraping/start`
3. Calculer les scores : `POST /scoring/calculate`
4. Voir les top produits : `GET /scoring/top-products`

