# Implementation Plan: Harmonisation du Code avec SOLID et DRY

**Branch**: `003-code-refactoring` | **Date**: 2024-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-code-refactoring/spec.md`

## Summary

Refactorisation complète de l'application pour éliminer la duplication de code et appliquer les principes SOLID. Les composants de liste frontend (ProductList, CampaignList, OrderList, CreativeList) seront unifiés dans un composant générique DataTable. La logique API sera centralisée dans des hooks/services réutilisables. Les routes backend seront refactorisées pour suivre SOLID avec des helpers/middlewares réutilisables. L'objectif est de réduire la duplication de 60% (frontend) et 40% (backend) tout en maintenant 100% des fonctionnalités existantes.

## Technical Context

**Language/Version**: 
- Frontend: TypeScript 5.6+, React 19+, Next.js 15.1.0+
- Backend: Python 3.11+, FastAPI 0.115.0+

**Primary Dependencies**: 
- Frontend: React, Next.js, TypeScript, Tailwind CSS, React Hooks
- Backend: FastAPI, SQLAlchemy 2.0 (async), Pydantic, asyncpg/aiosqlite

**Storage**: PostgreSQL 16+ (production), SQLite (développement), Redis 7.4+ (cache)

**Testing**: 
- Frontend: Jest, React Testing Library
- Backend: pytest, pytest-asyncio, httpx

**Target Platform**: Web application (browser-based admin dashboard)

**Project Type**: Web application (frontend + backend)

**Performance Goals**: 
- Temps de chargement des pages de liste identique ou meilleur après refactorisation
- Pas de dégradation de performance due aux couches d'abstraction
- Rendu initial < 200ms pour les tableaux de données

**Constraints**: 
- Aucune régression fonctionnelle (100% des fonctionnalités conservées)
- Compatibilité avec l'existant (pas de breaking changes pour les APIs)
- Maintenir la compatibilité avec WebSocket pour les mises à jour en temps réel

**Scale/Scope**: 
- 4 composants de liste frontend à refactoriser
- ~10 routes backend admin à analyser et refactoriser
- Réduction de 60% du code dupliqué frontend
- Réduction de 40% du code dupliqué backend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Vérifier la conformité avec les principes de la constitution:

- [x] **Clean Architecture**: La refactorisation respecte la séparation en couches. Les composants génériques (DataTable, hooks) sont dans la couche Présentation. Les services API centralisés sont dans Application. Les abstractions respectent Dependency Inversion.
- [x] **Stack Technologique**: Utilisation de Next.js 15+ (frontend) et FastAPI 0.115+ (backend). PostgreSQL 16+ et Redis 7.4+ maintenus. TypeScript strict mode.
- [x] **Modularité**: Les composants génériques sont isolés dans des modules réutilisables (`frontend/src/components/common/`, `frontend/src/hooks/`). Les helpers backend sont dans des modules dédiés (`backend/app/utils/`, `backend/app/middleware/`).
- [x] **Tests**: Tests unitaires prévus pour les composants génériques et hooks. Tests d'intégration pour vérifier que les composants refactorisés conservent les fonctionnalités. Les APIs externes seront mockées.
- [x] **Performance**: Les hooks utilisent async/await pour les appels API. Les composants génériques utilisent React.memo et useMemo pour optimiser les performances. Pas de dégradation attendue.

## Project Structure

### Documentation (this feature)

```text
specs/003-code-refactoring/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── admin/           # Composants spécifiques admin (existant)
│   │   │   ├── ProductList.tsx      # À refactoriser
│   │   │   ├── CampaignList.tsx     # À refactoriser
│   │   │   ├── OrderList.tsx        # À refactoriser
│   │   │   └── CreativeList.tsx     # À refactoriser
│   │   └── common/          # NOUVEAU: Composants génériques réutilisables
│   │       ├── DataTable/
│   │       │   ├── DataTable.tsx
│   │       │   ├── DataTableFilters.tsx
│   │       │   ├── DataTablePagination.tsx
│   │       │   └── types.ts
│   │       └── ErrorDisplay.tsx
│   ├── hooks/              # NOUVEAU: Hooks réutilisables
│   │   ├── useDataList.ts  # Hook générique pour fetch + WebSocket sync
│   │   └── useApiRequest.ts # Hook pour requêtes API avec retry/error handling
│   ├── lib/
│   │   ├── admin/
│   │   │   └── api.ts      # À refactoriser pour centraliser
│   │   └── api/            # NOUVEAU: Service API centralisé
│   │       ├── client.ts   # Client API générique
│   │       ├── errorHandler.ts
│   │       └── types.ts
│   └── app/
│       └── admin/          # Pages admin (existant)

backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── admin/      # Routes admin (existant, à refactoriser)
│   │           ├── products.py
│   │           ├── campaigns.py
│   │           ├── orders.py
│   │           └── creatives.py
│   ├── services/
│   │   └── admin/          # Services admin (existant)
│   ├── utils/              # NOUVEAU: Helpers réutilisables
│   │   ├── pagination.py   # Logique de pagination centralisée
│   │   ├── filtering.py    # Logique de filtrage centralisée
│   │   └── response.py     # Formatage de réponses centralisé
│   ├── middleware/
│   │   ├── admin_auth.py   # Existant
│   │   └── error_handler.py # NOUVEAU: Gestion d'erreur centralisée
│   └── models/             # Modèles existants (pas de changement)
│       ├── ads.py
│       ├── campaigns.py
│       ├── orders.py
│       └── admin.py
└── tests/
    ├── unit/
    │   ├── utils/          # Tests pour helpers
    │   └── middleware/      # Tests pour middlewares
    └── integration/
        └── api/
            └── admin/      # Tests pour routes refactorisées
```

**Structure Decision**: Structure web application (frontend + backend) maintenue. Ajout de modules `common/` et `hooks/` dans frontend pour les composants/hooks réutilisables. Ajout de `utils/` et amélioration de `middleware/` dans backend pour centraliser la logique répétée.

## Complexity Tracking

> **Aucune violation de la constitution identifiée. La refactorisation respecte tous les principes.**
