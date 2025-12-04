<!--
Sync Impact Report:
Version change: N/A (initial) → 1.0.0
Modified principles: N/A (initial creation)
Added sections: Core Principles (5), Stack Requirements, Development Workflow, Governance
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section references constitution
  ✅ spec-template.md - No direct references, but aligns with principles
  ✅ tasks-template.md - No direct references, but aligns with principles
Follow-up TODOs: None
-->

# Plateforme Dropshipping Automatisée Constitution

## Core Principles

### I. Clean Architecture (NON-NEGOTIABLE)

Toute fonctionnalité DOIT respecter la séparation en couches: Présentation → Application → Domain → Infrastructure. Les dépendances pointent uniquement vers l'intérieur (vers Domain). Les services externes (APIs tierces, base de données) sont isolés dans la couche Infrastructure. Les use cases métier résident dans Application Layer, indépendants des frameworks.

**Rationale**: Permet la testabilité, la maintenabilité et l'évolutivité. Les changements d'APIs externes ou de frameworks n'affectent pas la logique métier.

### II. Stack Technologique Prescrit

Le frontend DOIT utiliser Next.js 15.1.0+ avec App Router, TypeScript, Tailwind CSS. Le backend DOIT utiliser FastAPI 0.115.0+ avec async/await. La base de données DOIT être PostgreSQL 16+ avec SQLAlchemy 2.0 (async). Le cache DOIT utiliser Redis 7.4+. L'IA locale DOIT utiliser Ollama avec modèle llama3.2:3b ou équivalent.

**Rationale**: Stack validé et documenté pour garantir la cohérence, la performance et la facilité de maintenance. Les versions spécifiques évitent les incompatibilités.

### III. Modularité par Modules Fonctionnels

Chaque module (Scraping, Scoring, Créatives, Landing Pages, Campagnes, Chatbot) DOIT être indépendant avec ses propres services, modèles et endpoints. Les modules communiquent via des interfaces définies (services, événements, ou appels API). Aucun couplage direct entre modules.

**Rationale**: Permet le développement parallèle, les tests isolés et le remplacement/amélioration d'un module sans impact sur les autres.

### IV. Tests et Validation (NON-NEGOTIABLE)

Tous les services DOIT avoir des tests unitaires (pytest). Les endpoints API DOIT avoir des tests d'intégration. Les tests DOIT être exécutables indépendamment et en parallèle. Les tests DOIT précéder l'implémentation (TDD recommandé). Les tests DOIT utiliser des mocks pour les APIs externes.

**Rationale**: Garantit la qualité, détecte les régressions et facilite les refactorings. Les mocks isolent les tests des dépendances externes instables.

### V. Gestion Asynchrone et Performance

Toutes les opérations I/O (base de données, APIs externes, fichiers) DOIT utiliser async/await. Les tâches longues (scraping, génération vidéo) DOIT être exécutées en arrière-plan (BackgroundTasks, Celery, ou APScheduler). Les landing pages DOIT utiliser ISR (Incremental Static Regeneration) avec revalidation horaire. Les requêtes lourdes DOIT être mises en cache (Redis).

**Rationale**: Optimise les performances, évite les blocages et améliore l'expérience utilisateur. L'ISR réduit la charge serveur tout en gardant le contenu à jour.

## Stack Requirements

### Technologies Obligatoires

- **Frontend**: Next.js 15.1.0+, React 19+, TypeScript 5.6+, Tailwind CSS 3.4+
- **Backend**: FastAPI 0.115.0+, Python 3.11+, SQLAlchemy 2.0 (async), asyncpg
- **Base de données**: PostgreSQL 16+
- **Cache**: Redis 7.4+
- **IA**: Ollama avec modèle local (llama3.2:3b minimum)
- **Tests**: pytest, pytest-asyncio, httpx

### APIs Externes Requises

- Apify (scraping Facebook/TikTok Ads)
- Creatify (génération vidéos)
- Meta Ads API v22.0+
- TikTok Ads API v1.3+
- WhatsApp Cloud API v22.0+

### Structure de Projet

Le projet DOIT suivre la structure frontend/backend avec:

- `frontend/`: Next.js avec App Router, composants dans `src/components/`, pages dans `src/app/`
- `backend/`: FastAPI avec structure Clean Architecture (`app/services/`, `app/models/`, `app/api/routes/`)
- `tests/`: Tests organisés par type (unit/, integration/, contract/)

## Development Workflow

### Code Review Requirements

Tous les PRs DOIT vérifier la conformité avec la constitution. Les violations DOIT être documentées dans "Complexity Tracking" avec justification. Les tests DOIT passer avant merge. Les migrations Alembic DOIT être validées.

### Quality Gates

- Tests unitaires: couverture minimale 70% pour les services
- Tests d'intégration: tous les endpoints critiques
- Linting: ESLint (frontend), flake8/black (backend)
- Type checking: TypeScript strict mode, mypy pour Python

### Deployment Process

Les déploiements DOIT utiliser Docker Compose en production. Les migrations DOIT être appliquées automatiquement au démarrage. Les variables d'environnement DOIT être validées au démarrage. Les healthchecks DOIT être configurés pour tous les services.

## Governance

La constitution prime sur toutes les autres pratiques et documentations. Les amendements nécessitent:

1. Documentation de la raison du changement
2. Plan de migration si rétro-incompatible
3. Mise à jour de la version (semver)
4. Validation par review

Tous les PRs/reviews DOIT vérifier la conformité avec la constitution. La complexité DOIT être justifiée dans "Complexity Tracking" si elle viole un principe. Utiliser `techincal-doc.md` pour les détails d'implémentation spécifiques.

**Version**: 1.0.0 | **Ratified**: 2024-12-01 | **Last Amended**: 2024-12-01
