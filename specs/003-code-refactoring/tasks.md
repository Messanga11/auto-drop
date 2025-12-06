# Tasks: Harmonisation du Code avec SOLID et DRY

**Input**: Design documents from `/specs/003-code-refactoring/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the specification. Focus on implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`
- Paths follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for refactoring

- [x] T001 Create directory structure for common components in frontend/src/components/common/
- [x] T002 Create directory structure for reusable hooks in frontend/src/hooks/
- [x] T003 Create directory structure for centralized API service in frontend/src/lib/api/
- [x] T004 Create directory structure for backend helpers in backend/app/utils/
- [x] T005 [P] Create DataTable component directory structure in frontend/src/components/common/DataTable/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core generic components and hooks that MUST be complete before refactoring user stories

**⚠️ CRITICAL**: No user story refactoring can begin until this phase is complete

- [x] T006 [P] Create TypeScript types for DataTable in frontend/src/components/common/DataTable/types.ts (ColumnDef, ActionDef, FilterConfig, DataTableProps)
- [x] T007 [P] Create DataTableFilters component in frontend/src/components/common/DataTable/DataTableFilters.tsx
- [x] T008 [P] Create DataTablePagination component in frontend/src/components/common/DataTable/DataTablePagination.tsx
- [x] T009 Create DataTable main component in frontend/src/components/common/DataTable/DataTable.tsx with React.memo and useMemo optimizations
- [x] T010 Create ErrorDisplay component in frontend/src/components/common/ErrorDisplay.tsx
- [x] T011 Create useDataList hook in frontend/src/hooks/useDataList.ts with generic type support
- [x] T012 Create ApiClient class in frontend/src/lib/api/client.ts with error handling
- [x] T013 Create errorHandler utility in frontend/src/lib/api/errorHandler.ts
- [x] T014 Create API types in frontend/src/lib/api/types.ts
- [x] T015 [P] Create pagination helper in backend/app/utils/pagination.py (apply_pagination, get_total_count)
- [x] T016 [P] Create filtering helper in backend/app/utils/filtering.py (apply_filters)
- [x] T017 [P] Create response formatter helper in backend/app/utils/response.py (format_list_response)
- [x] T018 Create error handler middleware in backend/app/middleware/error_handler.py

**Checkpoint**: Foundation ready - generic components and hooks are available for refactoring

---

## Phase 3: User Story 1 - Refactorisation des Composants de Liste (Priority: P1) 🎯 MVP

**Goal**: Refactoriser tous les composants de liste (ProductList, CampaignList, OrderList, CreativeList) pour utiliser le composant générique DataTable, réduisant la duplication de code de 60%+

**Independent Test**: Créer DataTable et refactoriser ProductList pour l'utiliser. Le composant refactorisé doit conserver exactement les mêmes fonctionnalités (filtres, pagination, chargement, WebSocket sync) que l'original.

### Implementation for User Story 1

- [x] T019 [US1] Refactoriser ProductList pour utiliser DataTable dans frontend/src/components/admin/ProductList.tsx (définir colonnes, filtres, actions)
- [x] T020 [US1] Vérifier que ProductList conserve toutes les fonctionnalités existantes (filtres platform/scored/min_score, pagination, WebSocket sync)
- [x] T021 [US1] Refactoriser CampaignList pour utiliser DataTable dans frontend/src/components/admin/CampaignList.tsx (inclure actions activate/deactivate)
- [x] T022 [US1] Vérifier que CampaignList conserve toutes les fonctionnalités existantes (filtres status/platform, actions activate/deactivate, WebSocket sync)
- [x] T023 [US1] Refactoriser OrderList pour utiliser DataTable dans frontend/src/components/admin/OrderList.tsx (inclure actions de mise à jour de statut)
- [x] T024 [US1] Vérifier que OrderList conserve toutes les fonctionnalités existantes (filtres status/date, actions update status, WebSocket sync)
- [x] T025 [US1] Refactoriser CreativeList pour utiliser DataTable dans frontend/src/components/admin/CreativeList.tsx
- [x] T026 [US1] Vérifier que CreativeList conserve toutes les fonctionnalités existantes (filtres product_id/status, WebSocket sync)
- [x] T027 [US1] Mesurer la réduction de code : comparer lignes de code avant/après refactorisation (objectif: 60%+ réduction)

**Checkpoint**: Tous les composants de liste utilisent DataTable et conservent 100% des fonctionnalités. Réduction de code mesurée et validée.

---

## Phase 4: User Story 2 - Centralisation de la Logique API (Priority: P1)

**Goal**: Centraliser toute la logique de communication avec le backend dans des hooks/services réutilisables (useDataList, ApiClient), éliminant la duplication des patterns de fetch, error handling et WebSocket sync.

**Independent Test**: Créer useDataList et refactoriser ProductList pour l'utiliser. La logique de fetch, loading, error et WebSocket sync doit être identique à l'implémentation originale.

### Implementation for User Story 2

- [x] T028 [US2] Refactoriser ProductList pour utiliser useDataList hook dans frontend/src/components/admin/ProductList.tsx
- [x] T029 [US2] Vérifier que ProductList utilise useDataList pour fetch, loading, error, et WebSocket sync
- [x] T030 [US2] Refactoriser CampaignList pour utiliser useDataList hook dans frontend/src/components/admin/CampaignList.tsx
- [x] T031 [US2] Vérifier que CampaignList utilise useDataList correctement
- [x] T032 [US2] Refactoriser OrderList pour utiliser useDataList hook dans frontend/src/components/admin/OrderList.tsx
- [x] T033 [US2] Vérifier que OrderList utilise useDataList correctement
- [x] T034 [US2] Refactoriser CreativeList pour utiliser useDataList hook dans frontend/src/components/admin/CreativeList.tsx
- [x] T035 [US2] Vérifier que CreativeList utilise useDataList correctement
- [x] T036 [US2] Refactoriser adminApi pour utiliser ApiClient dans frontend/src/lib/admin/api.ts
- [x] T037 [US2] Vérifier que tous les appels API utilisent ApiClient centralisé
- [x] T038 [US2] Tester que la modification de la gestion d'erreur dans useDataList bénéficie automatiquement à tous les composants

**Checkpoint**: Tous les composants utilisent useDataList et ApiClient. La logique API est centralisée et cohérente.

---

## Phase 5: User Story 3 - Refactorisation des Routes Backend (Priority: P2)

**Goal**: Refactoriser les routes backend pour utiliser des helpers réutilisables (pagination, filtering, response), réduisant la duplication de code de 40%+ et améliorant la testabilité.

**Independent Test**: Créer les helpers et refactoriser une route admin (products.py) pour les utiliser. La route doit conserver exactement le même comportement et la même interface API.

### Implementation for User Story 3

- [x] T039 [US3] Refactoriser route products pour utiliser helpers dans backend/app/api/routes/admin/products.py (utiliser apply_pagination, get_total_count, apply_filters, format_list_response)
- [x] T040 [US3] Vérifier que route products conserve exactement le même comportement et interface API
- [x] T041 [US3] Refactoriser route campaigns pour utiliser helpers dans backend/app/api/routes/admin/campaigns.py
- [x] T042 [US3] Vérifier que route campaigns conserve exactement le même comportement et interface API
- [x] T043 [US3] Refactoriser route orders pour utiliser helpers dans backend/app/api/routes/admin/orders.py
- [x] T044 [US3] Vérifier que route orders conserve exactement le même comportement et interface API
- [x] T045 [US3] Refactoriser route creatives pour utiliser helpers dans backend/app/api/routes/admin/creatives.py
- [x] T046 [US3] Vérifier que route creatives conserve exactement le même comportement et interface API
- [x] T047 [US3] Appliquer error handler middleware à toutes les routes admin dans backend/app/main.py
- [x] T048 [US3] Mesurer la réduction de code : comparer lignes de code avant/après refactorisation (objectif: 40%+ réduction)
- [x] T049 [US3] Tester que la modification des règles de validation dans les helpers bénéficie automatiquement à toutes les routes

**Checkpoint**: Toutes les routes admin utilisent les helpers. Réduction de code mesurée et validée. Gestion d'erreur centralisée.

---

## Phase 6: User Story 4 - Application des Principes SOLID (Priority: P2)

**Goal**: Analyser et refactoriser les modules existants pour respecter les principes SOLID (Single Responsibility, Open/Closed, Dependency Inversion), améliorant la maintenabilité et l'extensibilité.

**Independent Test**: Analyser un module existant, identifier les violations SOLID, le refactoriser pour respecter ces principes, et vérifier qu'il conserve exactement le même comportement fonctionnel.

### Implementation for User Story 4

- [x] T050 [US4] Analyser les services admin pour violations du principe Single Responsibility dans backend/app/services/admin/
- [x] T051 [US4] Refactoriser les services admin pour respecter Single Responsibility (séparer les responsabilités si nécessaire)
- [x] T052 [US4] Analyser les hooks WebSocket pour violations du principe Single Responsibility dans frontend/src/lib/websocket/hooks.ts
- [x] T053 [US4] Refactoriser les hooks WebSocket pour respecter Single Responsibility si nécessaire
- [x] T054 [US4] Vérifier que DataTable respecte Open/Closed Principle (extensible via props sans modification)
- [x] T055 [US4] Vérifier que useDataList respecte Dependency Inversion (dépend d'abstractions fetchFn/wsHook, pas d'implémentations concrètes)
- [x] T056 [US4] Vérifier que les helpers backend respectent Dependency Inversion (fonctions pures, pas de dépendances concrètes)
- [x] T057 [US4] Analyser et refactoriser les composants admin pour respecter Interface Segregation si nécessaire
- [x] T058 [US4] Documenter les améliorations SOLID apportées dans specs/003-code-refactoring/SOLID-improvements.md
- [x] T059 [US4] Mesurer le respect des principes SOLID : au moins 90% des modules respectent Single Responsibility

**Checkpoint**: Architecture respecte les principes SOLID. Maintenabilité et extensibilité améliorées.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Améliorations finales, validation complète, et documentation

- [x] T060 [P] Vérifier que toutes les fonctionnalités existantes fonctionnent identiquement après refactorisation (aucune régression)
- [x] T061 [P] Mesurer les performances : temps de chargement des pages de liste identique ou meilleur après refactorisation
- [x] T062 [P] Vérifier que tous les composants de liste partagent au moins 80% de leur code via DataTable/useDataList
- [x] T063 [P] Vérifier la cohérence : 100% des composants de liste utilisent la même logique de gestion d'erreur et de chargement
- [x] T064 [P] Tester l'extensibilité : créer un nouveau composant de liste (ex: UserList) avec moins de 50 lignes de code spécifique
- [x] T065 [P] Valider que la modification d'une fonctionnalité commune (ex: pagination) nécessite des changements dans un seul endroit
- [x] T066 [P] Mettre à jour la documentation dans README.md avec les nouvelles abstractions
- [x] T067 [P] Exécuter quickstart.md validation pour vérifier que tout fonctionne
- [x] T068 [P] Code cleanup : supprimer le code dupliqué restant identifié
- [x] T069 [P] Vérifier que les métriques de succès sont atteintes (SC-001 à SC-010)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P1): Can start after Foundational - Should use components from US1 but can be done in parallel
  - User Story 3 (P2): Can start after Foundational - Independent from frontend stories
  - User Story 4 (P2): Depends on US1, US2, US3 completion - Analyzes refactored code
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Creates DataTable, refactors all list components
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Can be done in parallel with US1, but benefits from US1 completion
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent backend refactoring, can run in parallel with US1/US2
- **User Story 4 (P2)**: Should start after US1, US2, US3 - Analyzes and improves the refactored code

### Within Each User Story

- Generic components/hooks before refactoring existing components
- Refactor one component at a time, test it, then move to next
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes:
  - User Story 1 and User Story 2 can start in parallel (different components)
  - User Story 3 can run in parallel with US1/US2 (backend vs frontend)
- User Story 4 should wait for US1, US2, US3 completion
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Refactoriser les composants de liste en parallèle (après validation de ProductList):
Task: "Refactoriser CampaignList pour utiliser DataTable"
Task: "Refactoriser OrderList pour utiliser DataTable"
Task: "Refactoriser CreativeList pour utiliser DataTable"
```

---

## Parallel Example: Foundational Phase

```bash
# Créer les composants et helpers en parallèle:
Task: "Create TypeScript types for DataTable"
Task: "Create DataTableFilters component"
Task: "Create DataTablePagination component"
Task: "Create pagination helper in backend"
Task: "Create filtering helper in backend"
Task: "Create response formatter helper in backend"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Refactoriser ProductList avec DataTable)
4. **STOP and VALIDATE**: Tester ProductList indépendamment, vérifier 100% des fonctionnalités
5. Si validé, refactoriser les autres composants (CampaignList, OrderList, CreativeList)
6. Deploy/demo si ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (ProductList) → Test independently → Validate approach
3. Add User Story 1 (autres composants) → Test independently → Deploy/Demo (MVP!)
4. Add User Story 2 → Centraliser logique API → Test independently → Deploy/Demo
5. Add User Story 3 → Refactoriser backend → Test independently → Deploy/Demo
6. Add User Story 4 → Appliquer SOLID → Test independently → Deploy/Demo
7. Polish → Final validation → Deploy

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (ProductList, CampaignList)
   - Developer B: User Story 1 (OrderList, CreativeList)
   - Developer C: User Story 2 (useDataList, ApiClient)
   - Developer D: User Story 3 (Backend helpers, routes)
3. Once US1, US2, US3 complete:
   - Developer A: User Story 4 (Analyse SOLID)
4. All developers: Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Refactor one component at a time, test thoroughly before moving to next
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Measure code reduction: compare lines of code before/after refactoring
- Validate 100% feature preservation: all existing functionality must work identically

