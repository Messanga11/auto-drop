# Tasks: Admin Dashboard Application

**Input**: Design documents from `/specs/002-admin-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/api.yaml

**Tests**: Tests are not explicitly requested in the specification. Focus on implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`
- Paths follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for admin application

- [x] T001 Create admin backend structure (backend/app/api/routes/admin/, backend/app/services/admin/, backend/app/models/admin.py, backend/app/websocket/)
- [x] T002 Create admin frontend structure (frontend/src/app/admin/, frontend/src/components/admin/, frontend/src/lib/admin/, frontend/src/lib/websocket/)
- [x] T003 [P] Add WebSocket dependencies to backend/requirements.txt (websockets or fastapi-websocket, python-jose for JWT)
- [x] T004 [P] Add WebSocket client dependencies to frontend/package.json (if needed, native WebSocket API used)
- [x] T005 [P] Create TypeScript types for admin in frontend/src/types/admin.ts
- [x] T006 [P] Create WebSocket event types in backend/app/websocket/events.py
- [x] T007 [P] Create WebSocket event types in frontend/src/lib/websocket/events.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create AdminUser model in backend/app/models/admin.py
- [x] T009 Create AdminSession model in backend/app/models/admin.py
- [x] T010 Create AdminAction model in backend/app/models/admin.py
- [x] T011 Create Alembic migration for admin tables (admin_users, admin_sessions, admin_actions) in backend/alembic/versions/002_admin_tables.py
- [x] T012 Implement admin seed data script to create default admin user in backend/app/scripts/seed_admin.py
- [x] T013 [P] Create WebSocket manager in backend/app/websocket/manager.py (connection management, broadcast)
- [x] T014 [P] Create WebSocket client with reconnection logic in frontend/src/lib/websocket/client.ts
- [x] T015 [P] Create WebSocket React hooks in frontend/src/lib/websocket/hooks.ts
- [x] T016 Create admin API client in frontend/src/lib/admin/api.ts
- [x] T017 Create admin auth utilities in frontend/src/lib/admin/auth.ts (token management, session)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentification Admin (Priority: P1) 🎯 MVP

**Goal**: Permettre aux administrateurs de se connecter à l'application admin avec un compte par défaut

**Independent Test**: Un administrateur peut se connecter avec les identifiants par défaut et accéder au dashboard. Le compte admin par défaut est créé automatiquement lors de l'initialisation de la base de données.

### Implementation for User Story 1

- [x] T018 [US1] Implement AdminAuthService in backend/app/services/admin/auth_service.py (login, logout, token validation, password hashing)
- [x] T019 [US1] Implement login endpoint in backend/app/api/routes/admin/auth.py (POST /admin/auth/login)
- [x] T020 [US1] Implement logout endpoint in backend/app/api/routes/admin/auth.py (POST /admin/auth/logout)
- [x] T021 [US1] Implement me endpoint in backend/app/api/routes/admin/auth.py (GET /admin/auth/me)
- [x] T022 [US1] Create admin authentication middleware in backend/app/middleware/admin_auth.py (JWT validation, session check)
- [x] T023 [US1] Create login page in frontend/src/app/admin/login/page.tsx
- [x] T024 [US1] Implement login form component in frontend/src/components/admin/LoginForm.tsx
- [x] T025 [US1] Implement authentication context/provider in frontend/src/lib/admin/AuthContext.tsx
- [x] T026 [US1] Add protected route wrapper in frontend/src/lib/admin/ProtectedRoute.tsx
- [x] T027 [US1] Integrate seed admin script in backend startup (call seed_admin.py on app init)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Admin can login and access protected routes.

---

## Phase 4: User Story 2 - Dashboard de Monitoring (Priority: P1) 🎯 MVP

**Goal**: Afficher un tableau de bord avec les métriques clés de la plateforme en temps réel

**Independent Test**: Un administrateur authentifié peut voir le dashboard avec les statistiques principales (nombre de produits scrapés, top produits, campagnes actives, commandes récentes) sans erreur, avec mises à jour en temps réel via WebSocket.

### Implementation for User Story 2

- [x] T028 [US2] Implement DashboardService in backend/app/services/admin/dashboard_service.py (get stats: total products, scored products, top 5, active campaigns, pending orders)
- [x] T029 [US2] Implement dashboard stats endpoint in backend/app/api/routes/admin/dashboard.py (GET /admin/dashboard/stats)
- [x] T030 [US2] Create WebSocket endpoint for admin connections in backend/app/api/routes/admin/websocket.py (WebSocket /admin/ws?token=...)
- [x] T031 [US2] Integrate WebSocket endpoint with WebSocket manager in backend/app/api/routes/admin/websocket.py
- [x] T032 [US2] Implement WebSocket event broadcasting for dashboard stats updates in backend/app/websocket/manager.py
- [x] T033 [US2] Create dashboard page in frontend/src/app/admin/dashboard/page.tsx
- [x] T034 [US2] Create DashboardStats component in frontend/src/components/admin/DashboardStats.tsx
- [x] T035 [US2] Create ConnectionStatus component in frontend/src/components/admin/ConnectionStatus.tsx (WebSocket connection indicator)
- [x] T036 [US2] Implement WebSocket hook for dashboard stats in frontend/src/lib/websocket/hooks.ts (useDashboardStats)
- [x] T037 [US2] Connect dashboard page to WebSocket for real-time updates in frontend/src/app/admin/dashboard/page.tsx
- [x] T038 [US2] Add admin layout with navigation in frontend/src/app/admin/layout.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Admin can login and see real-time dashboard metrics.

---

## Phase 5: User Story 3 - Gestion des Produits et Campagnes (Priority: P2)

**Goal**: Visualiser, filtrer et gérer les produits scrapés, les scores, les créatives et les campagnes

**Independent Test**: Un administrateur peut naviguer dans les sections produits, campagnes et créatives, voir les détails de chaque élément, et effectuer des actions de base (activer/désactiver, voir les détails), avec mises à jour en temps réel.

### Implementation for User Story 3

- [x] T039 [US3] Implement products list endpoint in backend/app/api/routes/admin/products.py (GET /admin/products with filters: platform, scored, min_score, pagination)
- [x] T040 [US3] Implement campaigns list endpoint in backend/app/api/routes/admin/campaigns.py (GET /admin/campaigns with filters: status, platform)
- [x] T041 [US3] Implement campaign activate endpoint in backend/app/api/routes/admin/campaigns.py (POST /admin/campaigns/{campaign_id}/activate)
- [x] T042 [US3] Implement campaign deactivate endpoint in backend/app/api/routes/admin/campaigns.py (POST /admin/campaigns/{campaign_id}/deactivate)
- [x] T043 [US3] Implement creatives list endpoint in backend/app/api/routes/admin/creatives.py (GET /admin/creatives with filters: product_id, status)
- [x] T044 [US3] Implement WebSocket events for product updates in backend/app/websocket/events.py (product_scraped, score_calculated)
- [x] T045 [US3] Implement WebSocket events for campaign updates in backend/app/websocket/events.py (campaign_status_changed)
- [x] T046 [US3] Create products page in frontend/src/app/admin/products/page.tsx
- [x] T047 [US3] Create ProductList component in frontend/src/components/admin/ProductList.tsx (with filters, pagination, real-time updates)
- [x] T048 [US3] Create campaigns page in frontend/src/app/admin/campaigns/page.tsx
- [x] T049 [US3] Create CampaignList component in frontend/src/components/admin/CampaignList.tsx (with filters, activate/deactivate actions, real-time updates)
- [x] T050 [US3] Create creatives page in frontend/src/app/admin/creatives/page.tsx
- [x] T051 [US3] Create CreativeList component in frontend/src/components/admin/CreativeList.tsx (with filters, real-time updates)
- [x] T052 [US3] Implement WebSocket hooks for products in frontend/src/lib/websocket/hooks.ts (useProducts)
- [x] T053 [US3] Implement WebSocket hooks for campaigns in frontend/src/lib/websocket/hooks.ts (useCampaigns)
- [x] T054 [US3] Connect products page to WebSocket for real-time updates in frontend/src/app/admin/products/page.tsx
- [x] T055 [US3] Connect campaigns page to WebSocket for real-time updates in frontend/src/app/admin/campaigns/page.tsx

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Admin can manage products and campaigns with real-time updates.

---

## Phase 6: User Story 4 - Actions de Pilotage (Priority: P2)

**Goal**: Déclencher manuellement des actions système (scraping, scoring, génération de créatives) et voir le statut en temps réel

**Independent Test**: Un administrateur peut déclencher un scraping, un calcul de scores, ou une génération de créatives depuis l'interface admin et voir le statut de l'opération en temps réel via WebSocket.

### Implementation for User Story 4

- [x] T056 [US4] Implement ActionService in backend/app/services/admin/action_service.py (trigger scraping, scoring, creative generation, get status)
- [x] T057 [US4] Implement scraping start endpoint in backend/app/api/routes/admin/actions.py (POST /admin/actions/scraping/start)
- [x] T058 [US4] Implement scraping status endpoint in backend/app/api/routes/admin/actions.py (GET /admin/actions/scraping/status)
- [x] T059 [US4] Implement scoring calculate endpoint in backend/app/api/routes/admin/actions.py (POST /admin/actions/scoring/calculate)
- [x] T060 [US4] Implement creative generation endpoint in backend/app/api/routes/admin/actions.py (POST /admin/actions/creatives/generate/{product_id})
- [x] T061 [US4] Implement WebSocket events for action progress in backend/app/websocket/events.py (scraping_progress, scoring_progress, creative_progress)
- [x] T062 [US4] Integrate action service with existing platform services (scraping_service, scoring_service, creatify_service) in backend/app/services/admin/action_service.py
- [x] T063 [US4] Create actions page in frontend/src/app/admin/actions/page.tsx
- [x] T064 [US4] Create ActionButtons component in frontend/src/components/admin/ActionButtons.tsx (buttons for scraping, scoring, creative generation)
- [x] T065 [US4] Create ActionStatus component in frontend/src/components/admin/ActionStatus.tsx (progress display, real-time updates)
- [x] T066 [US4] Implement WebSocket hooks for actions in frontend/src/lib/websocket/hooks.ts (useActionStatus)
- [x] T067 [US4] Connect actions page to WebSocket for real-time progress updates in frontend/src/app/admin/actions/page.tsx
- [x] T068 [US4] Record admin actions in AdminAction model when actions are triggered in backend/app/services/admin/action_service.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently. Admin can trigger system actions and see progress in real-time.

---

## Phase 7: User Story 5 - Gestion des Commandes (Priority: P3)

**Goal**: Voir et gérer les commandes reçues pour suivre les ventes et mettre à jour leur statut

**Independent Test**: Un administrateur peut voir la liste des commandes, filtrer par statut, voir les détails d'une commande, et mettre à jour son statut, avec mises à jour en temps réel.

### Implementation for User Story 5

- [x] T069 [US5] Implement orders list endpoint in backend/app/api/routes/admin/orders.py (GET /admin/orders with filters: status, date_from, date_to)
- [x] T070 [US5] Implement order status update endpoint in backend/app/api/routes/admin/orders.py (PATCH /admin/orders/{order_id}/status)
- [x] T071 [US5] Implement WebSocket events for order updates in backend/app/websocket/events.py (order_created, order_status_changed)
- [x] T072 [US5] Create orders page in frontend/src/app/admin/orders/page.tsx
- [x] T073 [US5] Create OrderList component in frontend/src/components/admin/OrderList.tsx (with filters, status update, real-time updates)
- [x] T074 [US5] Implement WebSocket hooks for orders in frontend/src/lib/websocket/hooks.ts (useOrders)
- [x] T075 [US5] Connect orders page to WebSocket for real-time updates in frontend/src/app/admin/orders/page.tsx
- [x] T076 [US5] Record admin actions when order status is updated in backend/app/api/routes/admin/orders.py

**Checkpoint**: At this point, all user stories should be independently functional. Admin can manage orders with real-time updates.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T077 [P] Implement WebSocket event replay on reconnection in backend/app/websocket/manager.py (replay missed events since last connection)
- [x] T078 [P] Implement WebSocket event replay on reconnection in frontend/src/lib/websocket/client.ts (request missed events, apply updates)
- [x] T079 [P] Add error handling and retry logic for WebSocket in frontend/src/lib/websocket/client.ts
- [x] T080 [P] Add loading states and error messages in all admin pages
- [x] T081 [P] Implement conflict resolution UI (show notification when resource modified by another admin) in frontend/src/components/admin/ConflictNotification.tsx
- [x] T082 [P] Add admin action history logging for all admin operations in backend/app/services/admin/action_service.py
- [x] T083 [P] Implement session expiration handling in frontend/src/lib/admin/auth.ts
- [x] T084 [P] Add WebSocket connection status indicator in admin layout in frontend/src/app/admin/layout.tsx
- [x] T085 [P] Optimize WebSocket message handling and reduce unnecessary broadcasts in backend/app/websocket/manager.py
- [x] T086 [P] Add pagination and infinite scroll for large lists (products, orders) in frontend components
- [x] T087 [P] Run quickstart.md validation to ensure all features work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication, uses existing platform entities
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication, integrates with existing platform services
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication, uses existing Order entity

### Within Each User Story

- Models before services
- Services before endpoints
- Backend endpoints before frontend pages
- Core implementation before WebSocket integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1 and 2 can start (US1 must complete before US2)
- User Stories 3, 4, and 5 can start in parallel after US1 completes (they only depend on authentication)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (after US1)

---

## Parallel Example: User Story 1

```bash
# Launch all models together:
Task: "Create AdminUser model in backend/app/models/admin.py"
Task: "Create AdminSession model in backend/app/models/admin.py"
Task: "Create AdminAction model in backend/app/models/admin.py"

# Launch all endpoints together (after models):
Task: "Implement login endpoint in backend/app/api/routes/admin/auth.py"
Task: "Implement logout endpoint in backend/app/api/routes/admin/auth.py"
Task: "Implement me endpoint in backend/app/api/routes/admin/auth.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch backend and frontend in parallel (after US1):
Task: "Implement DashboardService in backend/app/services/admin/dashboard_service.py"
Task: "Create dashboard page in frontend/src/app/admin/dashboard/page.tsx"
Task: "Create DashboardStats component in frontend/src/components/admin/DashboardStats.tsx"
Task: "Create ConnectionStatus component in frontend/src/components/admin/ConnectionStatus.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Dashboard with WebSocket)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Authentication MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Dashboard MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication) - MUST complete first
   - Developer B: Prepares User Story 2 (Dashboard) - waits for US1
3. Once US1 is done:
   - Developer A: User Story 2 (Dashboard)
   - Developer B: User Story 3 (Products & Campaigns)
   - Developer C: User Story 4 (Actions)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- WebSocket integration is critical for real-time updates - ensure proper connection management
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All admin operations must be logged in AdminAction for audit trail
- WebSocket events must be replayed on reconnection to maintain data consistency

