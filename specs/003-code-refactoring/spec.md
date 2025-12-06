# Feature Specification: Harmonisation du Code avec SOLID et DRY

**Feature Branch**: `003-code-refactoring`  
**Created**: 2024-12-19  
**Status**: Draft  
**Input**: User description: "amorniser l'application avec les bests practices solid et surtout NEVER REPEAT YOUSELF"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Refactorisation des Composants de Liste (Priority: P1)

En tant que développeur, je veux que tous les composants de liste (ProductList, CampaignList, OrderList, CreativeList) utilisent un composant générique réutilisable, afin de réduire la duplication de code et faciliter la maintenance.

**Why this priority**: Les composants de liste représentent la plus grande duplication de code dans l'application frontend. Ils partagent tous la même structure (filtres, pagination, chargement, erreurs, WebSocket sync) avec seulement des variations dans les colonnes et les actions. Cette refactorisation aura l'impact le plus immédiat sur la qualité du code.

**Independent Test**: Peut être testé indépendamment en créant un composant générique `DataTable` et en refactorisant un seul composant de liste (par exemple ProductList) pour l'utiliser. Le composant refactorisé doit conserver exactement les mêmes fonctionnalités et comportements que l'original.

**Acceptance Scenarios**:

1. **Given** un composant générique DataTable existe, **When** ProductList utilise ce composant, **Then** toutes les fonctionnalités existantes (filtres, pagination, chargement, WebSocket sync) fonctionnent identiquement
2. **Given** DataTable est utilisé par ProductList, **When** on refactorise CampaignList pour utiliser DataTable, **Then** CampaignList conserve toutes ses fonctionnalités spécifiques (activate/deactivate) tout en partageant la logique commune
3. **Given** tous les composants de liste utilisent DataTable, **When** on modifie la logique de pagination dans DataTable, **Then** tous les composants de liste bénéficient automatiquement de la modification

---

### User Story 2 - Centralisation de la Logique API (Priority: P1)

En tant que développeur, je veux que toute la logique de communication avec le backend soit centralisée dans des hooks ou services réutilisables, afin d'éviter la duplication des patterns de fetch, error handling et WebSocket sync.

**Why this priority**: Chaque composant de liste répète le même pattern : fetch data, gérer loading/error, synchroniser avec WebSocket. Cette duplication rend les modifications difficiles et propage les bugs. La centralisation permettra une maintenance plus facile et une cohérence garantie.

**Independent Test**: Peut être testé en créant un hook générique `useDataList` qui encapsule la logique de fetch, loading, error, et WebSocket sync. Un composant de liste peut être refactorisé pour utiliser ce hook et doit conserver exactement le même comportement.

**Acceptance Scenarios**:

1. **Given** un hook `useDataList` existe, **When** ProductList utilise ce hook, **Then** la logique de fetch, loading, error et WebSocket sync est identique à l'implémentation originale
2. **Given** `useDataList` est utilisé, **When** on modifie la gestion d'erreur dans le hook, **Then** tous les composants utilisant le hook bénéficient automatiquement de la modification
3. **Given** `useDataList` centralise la logique API, **When** on ajoute une nouvelle fonctionnalité (par exemple retry automatique), **Then** tous les composants utilisant le hook bénéficient de cette fonctionnalité sans modification

---

### User Story 3 - Refactorisation des Routes Backend (Priority: P2)

En tant que développeur, je veux que les routes backend suivent les principes SOLID avec une séparation claire des responsabilités, afin de réduire la duplication et améliorer la testabilité.

**Why this priority**: Les routes backend contiennent probablement des patterns répétés pour la validation, la gestion d'erreur, et la transformation de données. La refactorisation améliorera la maintenabilité et la testabilité du backend.

**Independent Test**: Peut être testé en identifiant les patterns répétés dans les routes (par exemple gestion d'erreur, validation de paramètres) et en créant des middlewares ou helpers réutilisables. Une route peut être refactorisée pour utiliser ces helpers et doit conserver le même comportement.

**Acceptance Scenarios**:

1. **Given** des helpers/middlewares réutilisables existent, **When** une route admin est refactorisée pour les utiliser, **Then** la route conserve exactement le même comportement et la même interface API
2. **Given** la logique de validation est centralisée, **When** on modifie les règles de validation, **Then** toutes les routes utilisant cette logique bénéficient automatiquement de la modification
3. **Given** la gestion d'erreur est centralisée, **When** on ajoute un nouveau type d'erreur, **Then** toutes les routes gèrent automatiquement ce nouveau type d'erreur de manière cohérente

---

### User Story 4 - Application des Principes SOLID (Priority: P2)

En tant que développeur, je veux que l'architecture du code suive les principes SOLID (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion), afin d'améliorer la maintenabilité et l'extensibilité.

**Why this priority**: L'application des principes SOLID permettra de créer une architecture plus robuste et extensible. Cela facilitera l'ajout de nouvelles fonctionnalités sans modifier le code existant (Open/Closed Principle) et garantira que chaque module a une responsabilité unique (Single Responsibility).

**Independent Test**: Peut être testé en analysant les modules existants et en identifiant les violations des principes SOLID. Un module peut être refactorisé pour respecter ces principes et doit conserver exactement le même comportement fonctionnel.

**Acceptance Scenarios**:

1. **Given** un module viole le principe Single Responsibility, **When** on le refactorise pour séparer les responsabilités, **Then** le module conserve exactement le même comportement fonctionnel
2. **Given** un module est refactorisé pour respecter Open/Closed Principle, **When** on ajoute une nouvelle fonctionnalité, **Then** on peut l'ajouter sans modifier le code existant
3. **Given** les dépendances sont inversées (Dependency Inversion), **When** on remplace une implémentation par une autre, **Then** le code fonctionne sans modification grâce aux abstractions

---

### Edge Cases

- Que se passe-t-il si un composant de liste a des besoins très spécifiques qui ne rentrent pas dans le composant générique ?
- Comment gérer les cas où la logique centralisée doit avoir des variations pour certains composants ?
- Que se passe-t-il si la refactorisation casse une fonctionnalité existante ?
- Comment s'assurer que les performances ne sont pas dégradées par l'ajout de couches d'abstraction ?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT fournir un composant générique réutilisable pour tous les tableaux de données (DataTable)
- **FR-002**: Le système DOIT centraliser la logique de communication API dans des hooks/services réutilisables
- **FR-003**: Le système DOIT éliminer toute duplication de code identifiée dans les composants de liste frontend
- **FR-004**: Le système DOIT éliminer toute duplication de code identifiée dans les routes backend
- **FR-005**: Le système DOIT respecter le principe Single Responsibility : chaque module/component doit avoir une seule responsabilité
- **FR-006**: Le système DOIT respecter le principe Open/Closed : le code doit être ouvert à l'extension mais fermé à la modification
- **FR-007**: Le système DOIT respecter le principe Dependency Inversion : les modules doivent dépendre d'abstractions, pas d'implémentations concrètes
- **FR-008**: Le système DOIT maintenir exactement les mêmes fonctionnalités après refactorisation (pas de régression fonctionnelle)
- **FR-009**: Le système DOIT permettre la personnalisation des composants génériques pour des cas spécifiques sans dupliquer le code
- **FR-010**: Le système DOIT centraliser la gestion d'erreur pour garantir une cohérence dans toute l'application
- **FR-011**: Le système DOIT centraliser la logique de validation pour garantir une cohérence dans toute l'application
- **FR-012**: Le système DOIT maintenir ou améliorer les performances après refactorisation
- **FR-013**: Le système DOIT fournir des abstractions pour les dépendances externes (API, WebSocket, etc.)
- **FR-014**: Le système DOIT permettre l'ajout de nouvelles fonctionnalités sans modifier le code existant (quand applicable)

### Key Entities *(include if feature involves data)*

- **DataTable Component**: Composant générique réutilisable pour afficher des tableaux de données avec filtres, pagination, chargement, et gestion d'erreur
- **useDataList Hook**: Hook React réutilisable qui encapsule la logique de fetch, loading, error, et synchronisation WebSocket
- **API Service Layer**: Couche de service centralisée pour toutes les communications avec le backend
- **Error Handler**: Module centralisé pour la gestion et le formatage des erreurs
- **Validation Layer**: Module centralisé pour la validation des données et paramètres

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Réduction d'au moins 60% du code dupliqué dans les composants de liste frontend (mesuré en lignes de code)
- **SC-002**: Tous les composants de liste partagent au moins 80% de leur code via des composants/hooks réutilisables
- **SC-003**: Réduction d'au moins 40% du code dupliqué dans les routes backend (mesuré en lignes de code)
- **SC-004**: Aucune régression fonctionnelle : 100% des fonctionnalités existantes fonctionnent identiquement après refactorisation
- **SC-005**: Amélioration de la maintenabilité : modification d'une fonctionnalité commune (par exemple pagination) nécessite des changements dans un seul endroit pour 100% des composants concernés
- **SC-006**: Respect des principes SOLID : au moins 90% des modules respectent le principe Single Responsibility
- **SC-007**: Extensibilité : ajout d'une nouvelle liste de données nécessite moins de 50 lignes de code spécifique (le reste étant réutilisé)
- **SC-008**: Performance : temps de chargement des pages de liste identique ou meilleur après refactorisation (mesuré en temps de rendu)
- **SC-009**: Cohérence : 100% des composants de liste utilisent la même logique de gestion d'erreur et de chargement
- **SC-010**: Testabilité : augmentation d'au moins 30% de la couverture de tests grâce à la centralisation de la logique
