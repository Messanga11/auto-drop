# Tasks: Plateforme Dropshipping Automatisée

**Input**: Design documents from `/specs/001-dropshipping-platform/`
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

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure (backend/app/, backend/tests/, backend/alembic/)
- [x] T002 Create frontend project structure (frontend/src/app/, frontend/src/components/, frontend/src/lib/)
- [x] T003 [P] Initialize backend Python project with FastAPI 0.115.0+ in backend/requirements.txt
- [x] T004 [P] Initialize frontend Next.js 15.1.0+ project with TypeScript in frontend/package.json
- [x] T005 [P] Configure ESLint and Prettier for frontend in frontend/.eslintrc.json
- [x] T006 [P] Configure flake8 and black for backend in backend/pyproject.toml
- [x] T007 [P] Setup TypeScript configuration in frontend/tsconfig.json
- [x] T008 [P] Setup Tailwind CSS configuration in frontend/tailwind.config.ts
- [x] T009 Create .env.example files for backend and frontend with required variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Setup PostgreSQL database connection with SQLAlchemy 2.0 async in backend/app/database.py
- [x] T011 Setup Redis connection for cache in backend/app/cache.py
- [x] T012 Create Alembic migrations directory structure in backend/alembic/versions/
- [x] T013 [P] Create base database models file in backend/app/models/__init__.py
- [x] T014 [P] Setup FastAPI application structure in backend/app/main.py
- [x] T015 [P] Configure CORS middleware in backend/app/main.py
- [x] T016 [P] Setup error handling and logging infrastructure in backend/app/exceptions.py
- [x] T017 [P] Create environment configuration management in backend/app/config.py
- [x] T018 [P] Setup Next.js App Router base layout in frontend/src/app/layout.tsx
- [x] T019 [P] Create API client utilities in frontend/src/lib/api-client.ts
- [x] T020 Create initial Alembic migration for database schema in backend/alembic/versions/001_initial.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Découverte et sélection automatique des produits gagnants (Priority: P1) 🎯 MVP

**Goal**: Système identifie automatiquement les 5 meilleurs produits chaque mois à partir de milliers de publicités scrapées depuis Facebook et TikTok

**Independent Test**: Fournir un ensemble de données de publicités scrapées et vérifier que le système identifie correctement les 5 meilleurs produits selon les critères définis. Tester avec curl: `POST /scraping/start` puis `POST /scoring/calculate` et vérifier `GET /scoring/top-products?limit=5` retourne 5 produits avec scores.

### Implementation for User Story 1

- [x] T021 [P] [US1] Create ScrapedAd model in backend/app/models/ads.py with all fields from data-model.md
- [x] T022 [P] [US1] Create ProductScore model in backend/app/models/ads.py with relationship to ScrapedAd
- [x] T023 [US1] Implement ScrapingService with Apify client integration in backend/app/services/scraping_service.py
- [x] T024 [US1] Add scrape_facebook_ads method in backend/app/services/scraping_service.py
- [x] T025 [US1] Add scrape_tiktok_ads method in backend/app/services/scraping_service.py
- [x] T026 [US1] Add normalize_facebook_ad method in backend/app/services/scraping_service.py
- [x] T027 [US1] Add normalize_tiktok_ad method in backend/app/services/scraping_service.py
- [x] T028 [US1] Implement ScoringService with scoring algorithm in backend/app/services/scoring_service.py
- [x] T029 [US1] Add calculate_scores_for_all_ads method in backend/app/services/scoring_service.py
- [x] T030 [US1] Add _is_excluded_category method in backend/app/services/scoring_service.py
- [x] T031 [US1] Add _is_priority_category method in backend/app/services/scoring_service.py
- [x] T032 [US1] Add _is_problem_solution method in backend/app/services/scoring_service.py
- [x] T033 [US1] Add _calculate_recency_score method in backend/app/services/scoring_service.py
- [x] T034 [US1] Create scraping endpoints in backend/app/api/routes/scraping.py
- [x] T035 [US1] Add POST /scraping/start endpoint in backend/app/api/routes/scraping.py
- [x] T036 [US1] Add GET /scraping/status endpoint in backend/app/api/routes/scraping.py
- [x] T037 [US1] Create scoring endpoints in backend/app/api/routes/scoring.py
- [x] T038 [US1] Add POST /scoring/calculate endpoint in backend/app/api/routes/scoring.py
- [x] T039 [US1] Add GET /scoring/top-products endpoint in backend/app/api/routes/scoring.py
- [x] T040 [US1] Register scraping and scoring routers in backend/app/main.py
- [x] T041 [US1] Add database migration for ScrapedAd and ProductScore tables in backend/alembic/versions/002_scraping_scoring.py
- [x] T042 [US1] Implement APScheduler for monthly scraping job in backend/app/scheduler.py
- [x] T043 [US1] Add monthly_scraping_job function in backend/app/scheduler.py
- [x] T044 [US1] Add error handling and retry logic for Apify API calls in backend/app/services/scraping_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Can scrape ads, calculate scores, and identify top 5 products.

---

## Phase 4: User Story 2 - Génération automatique de créatives vidéo et landing pages (Priority: P2)

**Goal**: Système génère automatiquement 4 créatives vidéo et une landing page pour chaque produit sélectionné

**Independent Test**: Fournir un produit sélectionné et vérifier que le système génère 4 créatives vidéo différentes et une landing page fonctionnelle. Tester avec curl: `POST /creatives/generate/{product_id}` puis vérifier `GET /creatives/status/{product_id}` et visiter la landing page.

### Implementation for User Story 2

- [x] T045 [P] [US2] Create Creative model in backend/app/models/ads.py with relationship to ScrapedAd
- [x] T046 [P] [US2] Create Order model in backend/app/models/orders.py with relationship to ScrapedAd
- [x] T047 [US2] Implement CreatifyService with API integration in backend/app/services/creatify_service.py
- [x] T048 [US2] Add generate_video_from_url method in backend/app/services/creatify_service.py
- [x] T049 [US2] Add get_video_status method in backend/app/services/creatify_service.py
- [x] T050 [US2] Add download_video method in backend/app/services/creatify_service.py
- [x] T051 [US2] Add generate_all_creatives_for_product method in backend/app/services/creatify_service.py
- [x] T052 [US2] Create creatives endpoints in backend/app/api/routes/creatives.py
- [x] T053 [US2] Add POST /creatives/generate/{product_id} endpoint in backend/app/api/routes/creatives.py
- [x] T054 [US2] Add GET /creatives/status/{product_id} endpoint in backend/app/api/routes/creatives.py
- [x] T055 [US2] Register creatives router in backend/app/main.py
- [x] T056 [US2] Create product page template in frontend/src/app/p/[slug]/page.tsx
- [x] T057 [US2] Add generateStaticParams function in frontend/src/app/p/[slug]/page.tsx
- [x] T058 [US2] Add generateMetadata function in frontend/src/app/p/[slug]/page.tsx
- [x] T059 [US2] Create ProductHero component in frontend/src/components/ProductHero.tsx
- [x] T060 [US2] Create ProductFeatures component in frontend/src/components/ProductFeatures.tsx
- [x] T061 [US2] Create OrderForm component in frontend/src/components/OrderForm.tsx
- [x] T062 [US2] Add form validation with react-hook-form and zod in frontend/src/components/OrderForm.tsx
- [x] T063 [US2] Create order API route in frontend/src/app/api/orders/route.ts
- [x] T064 [US2] Add POST handler for order submission in frontend/src/app/api/orders/route.ts
- [x] T065 [US2] Create product API client in frontend/src/lib/product-api.ts
- [x] T066 [US2] Add getProductBySlug function in frontend/src/lib/product-api.ts
- [x] T067 [US2] Add Meta Pixel integration in frontend/src/app/p/[slug]/page.tsx
- [x] T068 [US2] Add TikTok Pixel integration in frontend/src/app/p/[slug]/page.tsx
- [x] T069 [US2] Create WhatsApp redirect utility in frontend/src/lib/whatsapp.ts
- [x] T070 [US2] Add database migration for Creative and Order tables in backend/alembic/versions/003_creatives_orders.py
- [x] T071 [US2] Add error handling and retry logic for Creatify API calls in backend/app/services/creatify_service.py
- [x] T072 [US2] Configure ISR with revalidate: 3600 in frontend/src/app/p/[slug]/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Can generate creatives and create landing pages with order forms.

---

## Phase 5: User Story 3 - Lancement automatique de campagnes publicitaires (Priority: P2)

**Goal**: Système lance automatiquement des campagnes publicitaires sur Meta Ads et TikTok Ads pour chaque produit

**Independent Test**: Vérifier que le système crée correctement des campagnes sur les plateformes publicitaires avec les créatives générées. Tester avec curl: `POST /campaigns/launch-for-product/{product_id}` puis vérifier les campagnes créées en mode "paused".

### Implementation for User Story 3

- [x] T073 [P] [US3] Create Campaign model in backend/app/models/campaigns.py with relationship to ScrapedAd
- [x] T074 [US3] Implement MetaAdsService with Facebook Business API in backend/app/services/meta_ads_service.py
- [x] T075 [US3] Add create_campaign method in backend/app/services/meta_ads_service.py
- [x] T076 [US3] Add create_adset method in backend/app/services/meta_ads_service.py
- [x] T077 [US3] Add upload_video_creative method in backend/app/services/meta_ads_service.py
- [x] T078 [US3] Add create_video_ad method in backend/app/services/meta_ads_service.py
- [x] T079 [US3] Add activate_campaign method in backend/app/services/meta_ads_service.py
- [x] T080 [US3] Add create_complete_campaign_for_product method in backend/app/services/meta_ads_service.py
- [x] T081 [US3] Implement TikTokAdsService with TikTok Business API in backend/app/services/tiktok_ads_service.py
- [x] T082 [US3] Add create_campaign method in backend/app/services/tiktok_ads_service.py
- [x] T083 [US3] Add create_ad_group method in backend/app/services/tiktok_ads_service.py
- [x] T084 [US3] Add upload_video method in backend/app/services/tiktok_ads_service.py
- [x] T085 [US3] Add create_ad method in backend/app/services/tiktok_ads_service.py
- [x] T086 [US3] Create campaigns endpoints in backend/app/api/routes/campaigns.py
- [x] T087 [US3] Add POST /campaigns/launch-for-product/{product_id} endpoint in backend/app/api/routes/campaigns.py
- [x] T088 [US3] Add POST /campaigns/activate/{campaign_id} endpoint in backend/app/api/routes/campaigns.py
- [x] T089 [US3] Register campaigns router in backend/app/main.py
- [x] T090 [US3] Add database migration for Campaign table in backend/alembic/versions/004_campaigns.py
- [x] T091 [US3] Add error handling and retry logic for Meta Ads API calls in backend/app/services/meta_ads_service.py
- [x] T092 [US3] Add error handling and retry logic for TikTok Ads API calls in backend/app/services/tiktok_ads_service.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Can launch campaigns on Meta and TikTok platforms.

---

## Phase 6: User Story 4 - Gestion des commandes via chatbot WhatsApp intelligent (Priority: P3)

**Goal**: Système gère les messages WhatsApp entrants via un chatbot intelligent avec IA locale (Ollama)

**Independent Test**: Envoyer des messages WhatsApp simulés et vérifier que le chatbot répond de manière appropriée avec le contexte des commandes. Tester le webhook avec curl.

### Implementation for User Story 4

- [x] T093 [US4] Implement WhatsAppService with WhatsApp Cloud API in backend/app/services/whatsapp_service.py
- [x] T094 [US4] Add send_message method in backend/app/services/whatsapp_service.py
- [x] T095 [US4] Add generate_ai_response method with Ollama integration in backend/app/services/whatsapp_service.py
- [x] T096 [US4] Add handle_incoming_message method in backend/app/services/whatsapp_service.py
- [x] T097 [US4] Create webhooks endpoints in backend/app/api/routes/webhooks.py
- [x] T098 [US4] Add GET /webhooks/whatsapp endpoint for verification in backend/app/api/routes/webhooks.py
- [x] T099 [US4] Add POST /webhooks/whatsapp endpoint for message handling in backend/app/api/routes/webhooks.py
- [x] T100 [US4] Register webhooks router in backend/app/main.py
- [x] T101 [US4] Add context retrieval from Order model in backend/app/services/whatsapp_service.py
- [x] T102 [US4] Add error handling for Ollama API calls in backend/app/services/whatsapp_service.py
- [x] T103 [US4] Add fallback message when AI fails in backend/app/services/whatsapp_service.py

**Checkpoint**: All user stories should now be independently functional. Complete platform with scraping, scoring, creatives, landing pages, campaigns, and WhatsApp chatbot.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T104 [P] Add comprehensive error handling across all services
- [x] T105 [P] Add structured logging with context across all modules
- [x] T106 [P] Add request/response validation with Pydantic models
- [x] T107 [P] Add rate limiting for API endpoints
- [x] T108 [P] Add health check endpoints in backend/app/api/routes/health.py
- [x] T109 [P] Add monitoring and metrics collection
- [x] T110 [P] Add API documentation with OpenAPI/Swagger in backend/app/main.py
- [x] T111 [P] Add environment variable validation on startup
- [x] T112 [P] Add database connection pooling configuration
- [x] T113 [P] Add Redis connection pooling configuration
- [x] T114 [P] Add Docker Compose configuration for local development
- [x] T115 [P] Add Dockerfile for backend production deployment
- [x] T116 [P] Add Dockerfile for frontend production deployment
- [x] T117 Run quickstart.md validation checklist
- [x] T118 Add README.md with setup and deployment instructions
- [x] T119 Add .gitignore files for backend and frontend

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for product selection (needs ScrapedAd with selected_for_campaign=True)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US2 for creatives (needs Creative with status='completed')
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 for orders (needs Order model)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T009)
- All Foundational tasks marked [P] can run in parallel (T013-T019)
- Once Foundational phase completes:
  - Models within US1 can run in parallel (T021-T022)
  - Models within US2 can run in parallel (T045-T046)
  - Models within US3 can run in parallel (T073)
- Different user stories can be worked on in parallel by different team members after dependencies are met
- All Polish tasks marked [P] can run in parallel (T104-T116)

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create ScrapedAd model in backend/app/models/ads.py"
Task: "Create ProductScore model in backend/app/models/ads.py"

# Launch service methods in parallel (different methods, same file):
Task: "Add scrape_facebook_ads method"
Task: "Add scrape_tiktok_ads method"
Task: "Add normalize_facebook_ad method"
Task: "Add normalize_tiktok_ad method"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Scrape 10 ads from Facebook and TikTok
   - Calculate scores
   - Verify top 5 products identified
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Scraping + Scoring)
   - Developer B: User Story 2 (Creatives + Landing Pages) - waits for US1 completion
   - Developer C: User Story 3 (Campaigns) - waits for US2 completion
   - Developer D: User Story 4 (WhatsApp Chatbot) - waits for US2 completion
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All API endpoints must follow contracts/api.yaml specification
- All models must follow data-model.md specification
- All services must follow Clean Architecture principles from constitution

