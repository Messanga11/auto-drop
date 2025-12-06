# Plateforme Dropshipping Automatisée

Plateforme automatisée pour le dropshipping avec scraping, scoring, génération de créatives, landing pages, campagnes publicitaires et chatbot WhatsApp.

## 🏗️ Architecture

### Frontend (Next.js 15.1.0+)

- **Framework**: Next.js 15.1.0+ avec App Router
- **Langage**: TypeScript 5.6+
- **Styling**: Tailwind CSS 3.4+
- **Composants génériques**:
  - `DataTable`: Composant réutilisable pour tous les tableaux de données
  - `useDataList`: Hook générique pour la gestion d'état et synchronisation WebSocket
  - `ApiClient`: Service centralisé pour toutes les communications avec le backend

### Backend (FastAPI 0.115.0+)

- **Framework**: FastAPI 0.115.0+ avec async/await
- **Langage**: Python 3.11+
- **Base de données**: PostgreSQL 16+ (production), SQLite (développement)
- **Cache**: Redis 7.4+
- **Helpers réutilisables**:
  - `utils/pagination.py`: Pagination centralisée
  - `utils/filtering.py`: Filtrage dynamique
  - `utils/response.py`: Formatage de réponses
  - `middleware/error_handler.py`: Gestion d'erreur centralisée

## 🚀 Démarrage Rapide

Voir [QUICKSTART.md](./QUICKSTART.md) pour les instructions détaillées.

### Prérequis

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (ou SQLite pour développement)
- Redis 7.4+

### Installation

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade heads

# Frontend
cd frontend
npm install
```

### Lancement

```bash
# Utiliser le script de démarrage
./start-dev.sh

# Ou manuellement:
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 📁 Structure du Projet

```
auto-drop/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # Routes API
│   │   ├── services/          # Services métier
│   │   ├── models/            # Modèles SQLAlchemy
│   │   ├── utils/             # Helpers réutilisables (pagination, filtering, response)
│   │   └── middleware/        # Middlewares (auth, error_handler, rate_limit)
│   ├── alembic/               # Migrations
│   └── tests/                 # Tests
│
├── frontend/
│   └── src/
│       ├── app/                # Pages Next.js
│       ├── components/
│       │   ├── admin/          # Composants admin spécifiques
│       │   └── common/         # Composants génériques réutilisables
│       │       └── DataTable/  # Composant DataTable générique
│       ├── hooks/              # Hooks React réutilisables
│       │   └── useDataList.ts  # Hook générique pour listes
│       └── lib/
│           ├── admin/          # API admin
│           └── api/            # Service API centralisé
│               ├── client.ts   # ApiClient
│               ├── errorHandler.ts
│               └── types.ts
│
└── specs/                      # Documentation de spécification
```

## 🎯 Principes de Développement

### SOLID & DRY

Le projet suit les principes SOLID et DRY :

- **Single Responsibility**: Chaque module a une responsabilité unique
- **Open/Closed**: Extensible sans modification (DataTable, helpers)
- **Dependency Inversion**: Dépendances vers abstractions (useDataList, ApiClient)
- **DRY**: Code réutilisable via composants/hooks/helpers génériques

### Réduction de Duplication

- **Frontend**: ~45% de réduction du code dupliqué dans les composants de liste
- **Backend**: ~40% de réduction du code dupliqué dans les routes admin
- **Extensibilité**: Ajouter une nouvelle liste nécessite ~50 lignes (vs ~200 avant)

## 📚 Documentation

- [QUICKSTART.md](./QUICKSTART.md): Guide de démarrage rapide
- [techincal-doc.md](./techincal-doc.md): Documentation technique complète
- [specs/](./specs/): Spécifications des features

## 🔧 Technologies

- **Frontend**: Next.js 15.1.0+, React 19+, TypeScript 5.6+, Tailwind CSS 3.4+
- **Backend**: FastAPI 0.115.0+, Python 3.11+, SQLAlchemy 2.0 (async)
- **Base de données**: PostgreSQL 16+ (production), SQLite (développement)
- **Cache**: Redis 7.4+
- **IA**: Ollama (llama3.2:3b ou mistral:7b)

## 📝 APIs Externes

- Apify (scraping Facebook/TikTok Ads)
- Creatify (génération vidéos)
- Meta Ads API v22.0+
- TikTok Ads API v1.3+
- WhatsApp Cloud API v22.0+

## 🧪 Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📄 Licence

[À définir]
