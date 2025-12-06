# Quickstart: Plateforme Dropshipping Automatisée

**Created**: 2024-12-01  
**Feature**: [spec.md](./spec.md)

## Vue d'ensemble

Ce guide permet de démarrer rapidement la plateforme de dropshipping automatisée et de valider le fonctionnement de base.

## Prérequis

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7.4+
- Docker & Docker Compose
- Ollama (pour chatbot WhatsApp)

## Installation Rapide

### 1. Cloner et configurer

```bash
# Cloner le repository
git clone <repo-url>
cd auto-drop

# Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos credentials

# Frontend
cd ../frontend
npm install
cp .env.example .env.local
# Éditer .env.local
```

### 2. Démarrer les services

```bash
# PostgreSQL et Redis (Docker)
docker run --name postgres-dropshipping \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=dropshipping \
  -p 5432:5432 \
  -d postgres:16-alpine

docker run --name redis-dropshipping \
  -p 6379:6379 \
  -d redis:7.4-alpine

# Ollama
ollama serve
ollama pull llama3.2:3b
```

### 3. Initialiser la base de données

```bash
cd backend
alembic upgrade head
```

### 4. Lancer l'application

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Validation du Fonctionnement

### Test 1: Scraping manuel

```bash
# Lancer un scraping test (10 ads par plateforme)
curl -X POST http://localhost:8000/scraping/start \
  -H "Content-Type: application/json" \
  -d '{"facebook_max": 10, "tiktok_max": 10}'

# Vérifier le statut
curl http://localhost:8000/scraping/status
```

**Résultat attendu**: `total_ads` > 0 après quelques minutes

### Test 2: Scoring

```bash
# Calculer les scores
curl -X POST http://localhost:8000/scoring/calculate

# Récupérer le top 5
curl http://localhost:8000/scoring/top-products?limit=5
```

**Résultat attendu**: Liste de 5 produits avec scores > 0

### Test 3: Génération de créatives

```bash
# Générer créatives pour le premier produit (remplacer 1 par un product_id réel)
curl -X POST http://localhost:8000/creatives/generate/1

# Vérifier le statut
curl http://localhost:8000/creatives/status/1
```

**Résultat attendu**: 4 créatives en statut "queued" ou "processing"

### Test 4: Landing page

1. Ouvrir `http://localhost:3000/p/[slug]` (remplacer [slug] par un slug de produit)
2. Vérifier que la page s'affiche avec formulaire de commande
3. Soumettre une commande test

**Résultat attendu**: Redirection vers WhatsApp avec message pré-rempli

### Test 5: Webhook WhatsApp

```bash
# Vérifier le webhook (remplacer verify_token)
curl "http://localhost:8000/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=your_token&hub.challenge=test123"
```

**Résultat attendu**: Retourne "test123"

## Checklist de Validation

- [ ] Backend démarre sans erreur (port 8000)
- [ ] Frontend démarre sans erreur (port 3000)
- [ ] PostgreSQL accessible (port 5432)
- [ ] Redis accessible (port 6379)
- [ ] Ollama répond (port 11434)
- [ ] Scraping récupère au moins 1 ad
- [ ] Scoring identifie au moins 1 produit
- [ ] Landing page s'affiche correctement
- [ ] Formulaire de commande fonctionne
- [ ] Webhook WhatsApp répond

## Prochaines Étapes

1. Configurer les credentials APIs externes (Apify, Creatify, Meta, TikTok, WhatsApp)
2. Lancer un scraping complet (1000 ads)
3. Générer créatives pour les top 5 produits
4. Créer et activer des campagnes test
5. Tester le chatbot WhatsApp avec messages réels

## Dépannage

### Erreur de connexion PostgreSQL

```bash
# Vérifier que le container tourne
docker ps | grep postgres

# Vérifier les logs
docker logs postgres-dropshipping
```

### Erreur Ollama

```bash
# Vérifier que Ollama tourne
curl http://localhost:11434/api/tags

# Redémarrer si nécessaire
ollama serve
```

### Erreur APIs externes

Vérifier les variables d'environnement dans `.env`:
- `APIFY_API_TOKEN`
- `CREATIFY_API_ID` et `CREATIFY_API_KEY`
- `META_ACCESS_TOKEN`
- `TIKTOK_ACCESS_TOKEN`
- `WHATSAPP_ACCESS_TOKEN`

