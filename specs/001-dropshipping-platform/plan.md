# Implementation Plan: Plateforme Dropshipping Automatisée

**Branch**: `001-dropshipping-platform` | **Date**: 2024-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-dropshipping-platform/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Plateforme automatisée pour identifier, créer du contenu marketing et lancer des campagnes publicitaires pour 5 produits gagnants par mois. Le système scrape automatiquement 1000+ publicités depuis Facebook et TikTok, identifie les meilleurs produits via scoring algorithmique, génère des créatives vidéo et landing pages, puis lance des campagnes publicitaires automatiquement. Approche technique: architecture modulaire avec frontend Next.js 15, backend FastAPI, base de données PostgreSQL, et intégration de multiples APIs externes (Apify, Creatify, Meta Ads, TikTok Ads, WhatsApp).

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.6+ (frontend), Node.js 20+  
**Primary Dependencies**: FastAPI 0.115.0+, Next.js 15.1.0+, React 19+, SQLAlchemy 2.0 (async), Redis 7.4+, Ollama  
**Storage**: PostgreSQL 16+ (base de données principale), Redis 7.4+ (cache et queues), S3-compatible storage (créatives vidéo)  
**Testing**: pytest, pytest-asyncio, httpx (backend), Jest/React Testing Library (frontend)  
**Target Platform**: Linux server (production), macOS/Linux (développement), Docker containers  
**Project Type**: Web application (frontend + backend séparés)  
**Performance Goals**:

- Scraping de 1000 publicités en moins de 2 heures
- Génération de 4 créatives vidéo par produit en moins de 2 heures
- Réponse API < 200ms p95 pour endpoints synchrones
- Chatbot WhatsApp répond en < 10 secondes dans 95% des cas
- Support de 100 commandes simultanées sans dégradation

**Constraints**:

- Toutes les opérations I/O doivent être asynchrones
- Tâches longues (scraping, génération vidéo) en arrière-plan
- Landing pages avec ISR (revalidation horaire)
- APIs externes avec retry et fallback
- Pas de paiement en ligne (collecte commandes uniquement)
- Pas de tracking colis (géré manuellement)

**Scale/Scope**:

- 1000+ publicités scrapées par mois
- 5 produits sélectionnés automatiquement par mois
- 20 créatives vidéo générées par mois (4 par produit)
- 5 landing pages générées par mois
- 10 campagnes publicitaires lancées par mois (Meta + TikTok)
- 100+ commandes gérées simultanément

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Vérifier la conformité avec les principes de la constitution:

- [x] **Clean Architecture**: La fonctionnalité respecte la séparation en couches (Présentation → Application → Domain → Infrastructure). Structure backend avec `app/api/routes/` (Présentation), `app/services/` (Application), `app/models/` (Domain), et intégrations externes isolées (Infrastructure).

- [x] **Stack Technologique**: Utilisation de Next.js 15.1.0+ (frontend) et FastAPI 0.115.0+ (backend). PostgreSQL 16+ et Redis 7.4+ conformes à la constitution.

- [x] **Modularité**: La fonctionnalité est organisée en 6 modules indépendants: Scraping, Scoring, Créatives, Landing Pages, Campagnes, Chatbot. Chaque module a ses propres services, modèles et endpoints.

- [x] **Tests**: Tests unitaires (pytest) et d'intégration prévus pour tous les services et endpoints. Les APIs externes (Apify, Creatify, Meta, TikTok, WhatsApp) seront mockées dans les tests.

- [x] **Performance**: Toutes les opérations I/O utilisent async/await (SQLAlchemy async, httpx async). Les tâches longues (scraping, génération vidéo) sont exécutées en arrière-plan (BackgroundTasks, APScheduler). Landing pages utilisent ISR avec revalidation horaire.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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
│   │       ├── scraping.py
│   │       ├── scoring.py
│   │       ├── creatives.py
│   │       ├── campaigns.py
│   │       └── webhooks.py
│   ├── services/
│   │   ├── scraping_service.py
│   │   ├── scoring_service.py
│   │   ├── creatify_service.py
│   │   ├── meta_ads_service.py
│   │   ├── tiktok_ads_service.py
│   │   └── whatsapp_service.py
│   ├── models/
│   │   ├── ads.py
│   │   ├── orders.py
│   │   └── campaigns.py
│   ├── database.py
│   ├── main.py
│   └── scheduler.py
├── alembic/
│   └── versions/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── p/
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   └── api/
│   │       └── orders/
│   │           └── route.ts
│   ├── components/
│   │   ├── ProductHero.tsx
│   │   ├── ProductFeatures.tsx
│   │   ├── OrderForm.tsx
│   │   └── WhatsAppButton.tsx
│   ├── lib/
│   │   ├── product-api.ts
│   │   └── whatsapp.ts
│   └── types/
│       └── product.ts
├── public/
│   └── products/
├── tests/
└── package.json
```

**Structure Decision**: Structure web application avec frontend et backend séparés, conforme à la constitution. Le backend suit Clean Architecture avec séparation claire des couches (routes → services → models). Le frontend utilise Next.js App Router avec structure modulaire (components, lib, types). Les tests sont organisés par type (unit, integration, contract) dans chaque projet.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

Aucune violation de la constitution. Tous les principes sont respectés:

- Clean Architecture avec séparation en couches
- Stack technologique conforme (Next.js 15+, FastAPI 0.115+, PostgreSQL 16+, Redis 7.4+)
- Modularité avec 6 modules indépendants
- Tests prévus avec mocks pour APIs externes
- Performance avec async/await et tâches en arrière-plan
