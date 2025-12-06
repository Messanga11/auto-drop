# Implementation Plan: Admin Dashboard Application

**Branch**: `002-admin-dashboard` | **Date**: 2024-12-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-admin-dashboard/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Application d'administration pour suivre et piloter la plateforme dropshipping automatisée. L'application permet aux administrateurs de visualiser les métriques en temps réel, gérer les produits, campagnes et commandes, et déclencher des actions système (scraping, scoring, génération de créatives). Approche technique: frontend Next.js 15 avec WebSocket pour les mises à jour temps réel, backend FastAPI avec endpoints REST et serveur WebSocket, authentification par session avec token, et intégration avec les services existants de la plateforme.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.6+ (frontend), Node.js 20+  
**Primary Dependencies**: FastAPI 0.115.0+, Next.js 15.1.0+, React 19+, SQLAlchemy 2.0 (async), WebSocket (websockets ou fastapi-websocket), JWT pour sessions, bcrypt pour hashage mots de passe  
**Storage**: PostgreSQL 16+ (entités admin: AdminUser, AdminSession, AdminAction), SQLite en développement  
**Testing**: pytest, pytest-asyncio, httpx (backend), Jest/React Testing Library (frontend)  
**Target Platform**: Linux server (production), macOS/Linux (développement), Docker containers  
**Project Type**: Web application (frontend + backend séparés, nouvelle app admin)  
**Performance Goals**:

- Dashboard affiche les métriques en moins de 2 secondes
- Mises à jour WebSocket en temps réel (< 1 seconde de latence)
- Reconnexion WebSocket automatique en moins de 5 secondes
- Support de 5 administrateurs simultanés sans dégradation
- Filtrage de 1000+ produits en moins de 10 secondes

**Constraints**:

- Toutes les communications temps réel via WebSocket (pas de polling)
- Reconnexion automatique avec backoff exponentiel (500ms → 60s, tentatives illimitées)
- Authentification WebSocket via token dans query string
- Rejeu de tous les événements manqués lors de la reconnexion
- Gestion des conflits concurrents: dernière modification gagne
- Toutes les opérations I/O doivent être asynchrones

**Scale/Scope**:

- 1-10 comptes administrateurs
- 5 administrateurs simultanés maximum
- Dashboard avec métriques principales (produits, campagnes, commandes)
- Gestion de 1000+ produits scrapés
- Gestion de 100+ campagnes actives
- Gestion de 1000+ commandes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Vérifier la conformité avec les principes de la constitution:

- [x] **Clean Architecture**: La fonctionnalité respecte la séparation en couches (Présentation → Application → Domain → Infrastructure). Structure backend avec `app/api/routes/admin/` (Présentation), `app/services/admin/` (Application), `app/models/admin.py` (Domain), et WebSocket isolé dans Infrastructure. Frontend avec `src/app/admin/` (pages), `src/components/admin/` (composants), `src/lib/websocket/` (WebSocket client).

- [x] **Stack Technologique**: Utilisation de Next.js 15.1.0+ (frontend) et FastAPI 0.115.0+ (backend). PostgreSQL 16+ (SQLite en dev) et Redis 7.4+ conformes à la constitution. WebSocket via `websockets` ou intégration FastAPI native.

- [x] **Modularité**: L'application admin est un module indépendant avec ses propres routes (`/admin/*`), services (`admin_service.py`), modèles (`AdminUser`, `AdminSession`, `AdminAction`), et endpoints WebSocket. Communication avec les modules existants via interfaces définies (services, événements).

- [x] **Tests**: Tests unitaires (pytest) et d'intégration prévus pour tous les services admin, endpoints REST, et connexions WebSocket. Les services de la plateforme principale seront mockés dans les tests. Tests frontend pour les composants admin et la logique WebSocket.

- [x] **Performance**: Toutes les opérations I/O utilisent async/await (SQLAlchemy async, WebSocket async). Les opérations longues (scraping, scoring) déclenchées depuis l'admin sont exécutées en arrière-plan. WebSocket pour mises à jour temps réel sans polling.

## Project Structure

### Documentation (this feature)

```text
specs/002-admin-dashboard/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── admin/
│   │           ├── __init__.py
│   │           ├── auth.py          # Routes d'authentification (/admin/login, /admin/logout)
│   │           ├── dashboard.py    # Routes dashboard (/admin/dashboard/stats)
│   │           ├── products.py     # Routes produits (/admin/products)
│   │           ├── campaigns.py    # Routes campagnes (/admin/campaigns)
│   │           ├── creatives.py    # Routes créatives (/admin/creatives)
│   │           ├── orders.py       # Routes commandes (/admin/orders)
│   │           └── actions.py      # Routes actions de pilotage (/admin/actions/scraping, /admin/actions/scoring)
│   ├── services/
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── auth_service.py      # Service d'authentification admin
│   │       ├── dashboard_service.py  # Service métriques dashboard
│   │       ├── websocket_service.py # Service WebSocket (gestion connexions, événements)
│   │       └── action_service.py    # Service actions de pilotage
│   ├── models/
│   │   └── admin.py                  # Modèles: AdminUser, AdminSession, AdminAction
│   └── websocket/
│       ├── __init__.py
│       ├── manager.py                # Gestionnaire WebSocket (connexions actives, broadcast)
│       └── events.py                 # Types d'événements WebSocket
│
frontend/
├── src/
│   ├── app/
│   │   └── admin/
│   │       ├── layout.tsx            # Layout admin avec navigation
│   │       ├── login/
│   │       │   └── page.tsx          # Page de connexion
│   │       ├── dashboard/
│   │       │   └── page.tsx          # Page dashboard avec métriques
│   │       ├── products/
│   │       │   └── page.tsx          # Page liste produits
│   │       ├── campaigns/
│   │       │   └── page.tsx          # Page liste campagnes
│   │       ├── creatives/
│   │       │   └── page.tsx          # Page liste créatives
│   │       ├── orders/
│   │       │   └── page.tsx          # Page liste commandes
│   │       └── actions/
│   │           └── page.tsx          # Page actions de pilotage
│   ├── components/
│   │   └── admin/
│   │       ├── DashboardStats.tsx    # Composant métriques dashboard
│   │       ├── ProductList.tsx        # Composant liste produits
│   │       ├── CampaignList.tsx       # Composant liste campagnes
│   │       ├── OrderList.tsx          # Composant liste commandes
│   │       ├── ConnectionStatus.tsx  # Indicateur statut WebSocket
│   │       └── ActionButtons.tsx      # Boutons actions de pilotage
│   ├── lib/
│   │   ├── admin/
│   │   │   ├── api.ts                # Client API admin (fetch)
│   │   │   └── auth.ts                # Gestion authentification (tokens, sessions)
│   │   └── websocket/
│   │       ├── client.ts              # Client WebSocket avec reconnexion
│   │       ├── hooks.ts               # React hooks pour WebSocket
│   │       └── events.ts              # Types d'événements WebSocket
│   └── types/
│       └── admin.ts                   # Types TypeScript pour admin
│
tests/
├── backend/
│   ├── unit/
│   │   └── services/
│   │       └── admin/
│   │           ├── test_auth_service.py
│   │           ├── test_dashboard_service.py
│   │           └── test_websocket_service.py
│   └── integration/
│       └── api/
│           └── admin/
│               ├── test_auth.py
│               ├── test_dashboard.py
│               └── test_websocket.py
└── frontend/
    ├── components/
    │   └── admin/
    │       ├── DashboardStats.test.tsx
    │       └── ConnectionStatus.test.tsx
    └── lib/
        └── websocket/
            └── client.test.ts
```

**Structure Decision**: Application web avec frontend Next.js 15 et backend FastAPI. L'application admin est un module séparé avec ses propres routes (`/admin/*`), services, et modèles. WebSocket intégré dans le backend FastAPI et client React dans le frontend. Structure respecte Clean Architecture avec séparation claire des couches.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

Aucune violation de la constitution détectée. L'application admin respecte tous les principes:
- Clean Architecture: séparation en couches respectée
- Stack technologique: Next.js 15+ et FastAPI 0.115+ utilisés
- Modularité: module admin indépendant
- Tests: tests unitaires et d'intégration prévus
- Performance: async/await et WebSocket pour temps réel
