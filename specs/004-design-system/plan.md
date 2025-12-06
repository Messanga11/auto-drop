# Implementation Plan: Design System Implementation

**Branch**: `004-design-system` | **Date**: 2024-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-design-system/spec.md`

## Summary

Implémentation complète du design system basé sur design.json avec architecture atomique (atomes, molécules, organismes). Tous les tokens de design (couleurs, typographie, espacements, effets) seront centralisés via Tailwind CSS et variables CSS. Tous les composants existants seront migrés pour respecter scrupuleusement les valeurs définies dans design.json, garantissant une cohérence visuelle à 100% à travers l'application.

## Technical Context

**Language/Version**: 
- Frontend: TypeScript 5.6+, React 19+, Next.js 16.0.7+
- CSS: Tailwind CSS 3.4.17+

**Primary Dependencies**: 
- Next.js 16.0.7+ avec App Router
- React 19+ avec TypeScript strict mode
- Tailwind CSS 3.4.17+ pour le styling
- PostCSS 8.4.49+ pour le traitement CSS
- Police Inter (à charger via Google Fonts ou localement)

**Storage**: N/A (design system frontend uniquement)

**Testing**: 
- Tests visuels manuels (vérification de conformité avec design.json)
- Tests de régression fonctionnelle (vérifier que la migration ne casse pas les fonctionnalités)
- Snapshot tests optionnels pour les composants critiques

**Target Platform**: Web application (navigateurs modernes supportant CSS backdrop-filter, gradients, et variables CSS)

**Project Type**: Web application (frontend uniquement pour cette feature)

**Performance Goals**: 
- Pas de dégradation de performance due au design system
- Chargement de la police Inter optimisé (preload ou subset)
- CSS généré par Tailwind doit rester < 200KB (production, purged)

**Constraints**: 
- Compatibilité navigateurs: Support de backdrop-filter (Chrome 76+, Safari 9+, Firefox 103+)
- Les valeurs doivent correspondre exactement à design.json (tolérance 0px pour espacements/radius, 0% pour couleurs)
- Migration progressive sans casser les fonctionnalités existantes
- Extensibilité: permettre l'ajout de variations tout en respectant les valeurs de base

**Scale/Scope**: 
- ~15 composants existants à migrer (ProductList, CampaignList, OrderList, CreativeList, DataTable, LoginForm, OrderForm, Navbar, etc.)
- ~50+ tokens de design à exposer (couleurs, typographie, espacements, effets)
- Architecture atomique: atomes (~10), molécules (~5), organismes (~5)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Vérifier la conformité avec les principes de la constitution:

- [x] **Clean Architecture**: Le design system respecte la séparation en couches. Les tokens sont dans la couche Infrastructure (configuration Tailwind/CSS). Les composants sont dans la couche Présentation. Aucune logique métier n'est affectée.
- [x] **Stack Technologique**: Utilisation de Next.js 16.0.7+ (frontend) conforme. Tailwind CSS 3.4.17+ conforme. TypeScript 5.6+ conforme. Pas de backend requis pour cette feature.
- [x] **Modularité**: Le design system est isolé dans des modules dédiés (`frontend/src/design-system/` pour les tokens, `frontend/src/components/atoms/`, `frontend/src/components/molecules/`, `frontend/src/components/organisms/`). Les tokens sont réutilisables et indépendants.
- [x] **Tests**: Tests visuels manuels prévus pour vérifier la conformité. Tests de régression fonctionnelle pour s'assurer que la migration ne casse pas les fonctionnalités. Pas d'APIs externes à mocker (design system frontend uniquement).
- [x] **Performance**: Pas d'opérations I/O asynchrones requises. Le design system utilise CSS statique et variables CSS. La police Inter sera chargée de manière optimisée (preload ou subset).

## Project Structure

### Documentation (this feature)

```text
specs/004-design-system/
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
│   ├── design-system/           # NOUVEAU: Tokens et configuration du design system
│   │   ├── tokens.ts            # Tokens TypeScript exportés depuis design.json
│   │   ├── tailwind.config.ts   # Configuration Tailwind avec tous les tokens
│   │   └── globals.css          # Variables CSS et styles globaux (Inter font, gradients)
│   ├── components/
│   │   ├── atoms/               # NOUVEAU: Composants atomes
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   └── Button.stories.tsx (optionnel)
│   │   │   ├── Input/
│   │   │   ├── Badge/
│   │   │   ├── Icon/
│   │   │   └── Label/
│   │   ├── molecules/           # NOUVEAU: Composants molécules
│   │   │   ├── Card/
│   │   │   ├── Form/
│   │   │   ├── StatCard/
│   │   │   └── ButtonGroup/
│   │   ├── organisms/           # NOUVEAU: Composants organismes
│   │   │   ├── Navbar/
│   │   │   ├── DataTable/       # Refactoriser existant
│   │   │   ├── PageLayout/
│   │   │   └── Section/
│   │   ├── admin/               # Existant - À migrer
│   │   │   ├── ProductList.tsx   # Migrer pour utiliser design system
│   │   │   ├── CampaignList.tsx # Migrer pour utiliser design system
│   │   │   ├── OrderList.tsx    # Migrer pour utiliser design system
│   │   │   ├── CreativeList.tsx # Migrer pour utiliser design system
│   │   │   ├── LoginForm.tsx    # Migrer pour utiliser design system
│   │   │   └── ...
│   │   ├── common/              # Existant - À migrer
│   │   │   └── DataTable/       # Migrer pour utiliser design system
│   │   ├── OrderForm.tsx         # Migrer pour utiliser design system
│   │   ├── ProductFeatures.tsx  # Migrer pour utiliser design system
│   │   └── ProductHero.tsx      # Migrer pour utiliser design system
│   └── app/
│       ├── layout.tsx            # Ajouter chargement police Inter
│       └── globals.css          # Migrer pour utiliser tokens design system
└── public/
    └── fonts/                    # NOUVEAU: Police Inter locale (optionnel)

design.json                        # Source de vérité pour tous les tokens
```

**Structure Decision**: Structure web application (frontend uniquement) maintenue. Ajout de modules `design-system/` pour les tokens centralisés. Organisation atomique avec `atoms/`, `molecules/`, `organisms/`. Migration progressive des composants existants vers le design system.

## Complexity Tracking

> **Aucune violation de la constitution identifiée. Le design system respecte tous les principes.**
