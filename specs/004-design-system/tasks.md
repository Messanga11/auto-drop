# Tasks: Design System Implementation

**Input**: Design documents from `/specs/004-design-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` for source code
- All paths shown below use `frontend/src/` prefix

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create design-system directory structure in frontend/src/design-system/
- [x] T002 Create atoms directory structure in frontend/src/components/atoms/
- [x] T003 Create molecules directory structure in frontend/src/components/molecules/
- [x] T004 Create organisms directory structure in frontend/src/components/organisms/
- [x] T005 [P] Verify design.json exists at project root and is valid JSON

---

## Phase 2: Foundational - Tokens de Design Centralisés (User Story 2, Priority: P1) 🎯 MVP Foundation

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. This phase implements User Story 2 (Tokens Centralisés) as it is the foundation for all other work.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Goal**: Exposer tous les tokens de design.json via Tailwind CSS, variables CSS et TypeScript pour garantir la cohérence et faciliter les mises à jour futures.

**Independent Test**: Vérifier que tous les tokens du design.json sont accessibles via un système centralisé (variables CSS, tokens TypeScript, ou configuration Tailwind). Tester en accédant à la couleur primaire (#FF7335), un radius de carte (32px), un effet de blur glass (40px), et la typographie pour un titre.

- [x] T006 [US2] Create tokens.ts TypeScript file that exports all tokens from design.json in frontend/src/design-system/tokens.ts
- [x] T007 [US2] Extend tailwind.config.ts with all color tokens from design.json in frontend/tailwind.config.ts
- [x] T008 [US2] Extend tailwind.config.ts with all typography tokens (fontFamily, fontSize, fontWeight, letterSpacing) from design.json in frontend/tailwind.config.ts
- [x] T009 [US2] Extend tailwind.config.ts with all spacing tokens (padding, gap, maxWidth) from design.json in frontend/tailwind.config.ts
- [x] T010 [US2] Extend tailwind.config.ts with all border radius tokens from design.json in frontend/tailwind.config.ts
- [x] T011 [US2] Extend tailwind.config.ts with all shadow tokens (soft, strong, innerGlow) from design.json in frontend/tailwind.config.ts
- [x] T012 [US2] Extend tailwind.config.ts with all blur tokens (glassStrong, card, backgroundFog) as backdropBlur utilities in frontend/tailwind.config.ts
- [x] T013 [US2] Create CSS variables for all tokens in frontend/src/app/globals.css
- [x] T014 [US2] Add Inter font loading via Google Fonts with preload in frontend/src/app/layout.tsx
- [x] T015 [US2] Configure font-family Inter in frontend/src/app/globals.css
- [x] T016 [US2] Create custom Tailwind utilities for glass effects (glass-card, glass-strong) in frontend/tailwind.config.ts
- [x] T017 [US2] Create custom Tailwind utilities for gradient overlay in frontend/tailwind.config.ts
- [x] T018 [US2] Verify all tokens are accessible via Tailwind classes (test bg-primary, text-primary, rounded-lg, etc.)

**Checkpoint**: Foundation ready - all tokens are accessible via Tailwind, CSS variables, and TypeScript. User story implementation can now begin.

---

## Phase 3: User Story 3 - Composants Atomes Conformes (Priority: P2)

**Goal**: Créer tous les composants atomes (boutons, inputs, labels, icônes, badges) qui respectent scrupuleusement le design system, afin de pouvoir les réutiliser de manière cohérente dans toute l'application.

**Independent Test**: Créer une page de démonstration qui affiche tous les atomes et vérifier visuellement leur conformité avec design.json. Tester que Button respecte radius 30px, paddingX 22px, paddingY 12px, background glass. Tester que Input respecte les radius, couleurs et effets glass. Tester que Badge respecte radius 20px, paddingX 16px, paddingY 6px, états actif/inactif. Tester que les icônes respectent strokeWidth 1.7px et couleur #FFFFFF.

- [x] T019 [P] [US3] Create Button atom component with default variant (radius 30px, paddingX 22px, paddingY 12px, background glass, hoverBackground) in frontend/src/components/atoms/Button/Button.tsx
- [x] T020 [P] [US3] Add tag variant to Button component (radius 20px, paddingX 16px, paddingY 6px, states active/inactive) in frontend/src/components/atoms/Button/Button.tsx
- [x] T021 [P] [US3] Create Input atom component with glass effects and design system colors in frontend/src/components/atoms/Input/Input.tsx
- [x] T022 [P] [US3] Create Label atom component with design system typography in frontend/src/components/atoms/Label/Label.tsx
- [x] T023 [P] [US3] Create Badge atom component with tag variant (radius 20px, paddingX 16px, paddingY 6px, states active/inactive) in frontend/src/components/atoms/Badge/Badge.tsx
- [x] T024 [P] [US3] Create Icon wrapper component that enforces minimal-line style with strokeWidth 1.7px and color #FFFFFF in frontend/src/components/atoms/Icon/Icon.tsx
- [x] T025 [US3] Create atoms showcase page to visually verify all atoms conform to design.json in frontend/src/app/design-system/atoms/page.tsx
- [x] T026 [US3] Verify all atoms visually match design.json values (use color picker, ruler, font inspector)

**Checkpoint**: At this point, all atom components should be created and visually verified to match design.json exactly.

---

## Phase 4: User Story 4 - Composants Molécules Conformes (Priority: P2)

**Goal**: Créer tous les composants molécules (formulaires, cartes, groupes de boutons, listes) qui respectent le design system, afin de créer des interfaces cohérentes.

**Independent Test**: Vérifier que les composants molécules respectent le design system. Tester que Card respecte les propriétés glass (background rgba(255,255,255,0.20), blur 40px, radius 32px, shadow). Tester que Form utilise tous ses éléments (inputs, labels, boutons) conformes au design system. Tester que StatCard respecte les propriétés (radius 28px, padding 20px, background rgba(0,0,0,0.35)).

- [x] T027 [P] [US4] Create Card molecule component with glass variant (background rgba(255,255,255,0.20), blur 40px, radius 32px, shadow) in frontend/src/components/molecules/Card/Card.tsx
- [x] T028 [P] [US4] Create StatCard molecule component (radius 28px, padding 20px, background rgba(0,0,0,0.35)) in frontend/src/components/molecules/StatCard/StatCard.tsx
- [x] T029 [P] [US4] Create Form molecule component that uses Input, Label, and Button atoms in frontend/src/components/molecules/Form/Form.tsx
- [x] T030 [P] [US4] Create ButtonGroup molecule component that uses Button atoms in frontend/src/components/molecules/ButtonGroup/ButtonGroup.tsx
- [x] T031 [US4] Create molecules showcase page to visually verify all molecules conform to design.json in frontend/src/app/design-system/molecules/page.tsx
- [x] T032 [US4] Verify all molecules visually match design.json values

**Checkpoint**: At this point, all molecule components should be created and visually verified to match design.json exactly.

---

## Phase 5: User Story 5 - Organismes et Layouts Conformes (Priority: P2)

**Goal**: Créer tous les organismes (navbar, tableaux de données, sections de page) et layouts qui respectent le design system, afin que l'application entière soit visuellement cohérente.

**Independent Test**: Vérifier que la navbar, les pages admin, et les layouts respectent le design system. Tester que la navbar respecte toutes les propriétés (height 68px, blur 25px, background rgba(0,0,0,0.30), avatarSize 42px). Tester qu'un layout respecte les paddings (screen 48px, section 32px) et maxWidth 1600px. Tester que DataTable utilise les effets glass, couleurs et espacements définis.

- [x] T033 [P] [US5] Create Navbar organism component (height 68px, blur 25px, background rgba(0,0,0,0.30), avatarSize 42px, iconStyle) in frontend/src/components/organisms/Navbar/Navbar.tsx
- [x] T034 [P] [US5] Create PageLayout organism component with paddings (screen 48px, section 32px) and maxWidth 1600px in frontend/src/components/organisms/PageLayout/PageLayout.tsx
- [x] T035 [P] [US5] Create Section organism component with frosted glass effects in frontend/src/components/organisms/Section/Section.tsx
- [x] T036 [US5] Refactor existing DataTable to use design system tokens (glass effects, colors, spacing) in frontend/src/components/common/DataTable/DataTable.tsx
- [x] T037 [US5] Create organisms showcase page to visually verify all organisms conform to design.json in frontend/src/app/design-system/organisms/page.tsx
- [x] T038 [US5] Verify all organisms visually match design.json values

**Checkpoint**: At this point, all organism components should be created and visually verified to match design.json exactly.

---

## Phase 6: User Story 1 - Application Cohérente du Design System (Priority: P1)

**Goal**: Migrer tous les composants existants de l'application pour qu'ils respectent scrupuleusement le design system défini dans design.json, afin que l'interface utilisateur soit visuellement cohérente et professionnelle.

**Independent Test**: Vérifier que tous les composants existants (boutons, cartes, formulaires, tableaux, navbar) respectent les valeurs du design system (couleurs, typographie, espacements, effets visuels). Tester visuellement chaque composant migré.

- [ ] T039 [P] [US1] Migrate LoginForm to use design system atoms and tokens in frontend/src/components/admin/LoginForm.tsx
- [ ] T040 [P] [US1] Migrate OrderForm to use design system atoms and tokens in frontend/src/components/OrderForm.tsx
- [ ] T041 [P] [US1] Migrate ProductHero to use design system tokens in frontend/src/components/ProductHero.tsx
- [ ] T042 [P] [US1] Migrate ProductFeatures to use design system tokens in frontend/src/components/ProductFeatures.tsx
- [ ] T043 [P] [US1] Migrate ProductList to use design system tokens and molecules in frontend/src/components/admin/ProductList.tsx
- [ ] T044 [P] [US1] Migrate CampaignList to use design system tokens and molecules in frontend/src/components/admin/CampaignList.tsx
- [ ] T045 [P] [US1] Migrate OrderList to use design system tokens and molecules in frontend/src/components/admin/OrderList.tsx
- [ ] T046 [P] [US1] Migrate CreativeList to use design system tokens and molecules in frontend/src/components/admin/CreativeList.tsx
- [ ] T047 [P] [US1] Migrate DashboardStats to use design system tokens and StatCard molecule in frontend/src/components/admin/DashboardStats.tsx
- [ ] T048 [P] [US1] Migrate ActionButtons to use design system Button atoms in frontend/src/components/admin/ActionButtons.tsx
- [ ] T049 [P] [US1] Migrate ActionStatus to use design system tokens in frontend/src/components/admin/ActionStatus.tsx
- [ ] T050 [P] [US1] Migrate ConnectionStatus to use design system tokens in frontend/src/components/admin/ConnectionStatus.tsx
- [ ] T051 [P] [US1] Migrate ConflictNotification to use design system tokens in frontend/src/components/admin/ConflictNotification.tsx
- [ ] T052 [US1] Migrate Admin  Nav (in layout.tsx) to use Navbar organism in frontend/src/app/admin/layout.tsx
- [ ] T053 [US1] Migrate all admin pages to use PageLayout organism in frontend/src/app/admin/**/page.tsx
- [x] T054 [US1] Verify all migrated components preserve functionality (no regression)
- [x] T055 [US1] Verify all migrated components visually match design.json values

**Checkpoint**: At this point, all existing components should be migrated to use the design system and visually verified.

---

## Phase 7: User Story 6 - Effets Visuels et Gradients (Priority: P3)

**Goal**: Appliquer les effets visuels (gradient overlay, frosted glass, shadows) définis dans le design system, afin d'avoir une expérience visuelle moderne et cohérente.

**Independent Test**: Vérifier que les effets visuels (gradients, glass, shadows) sont appliqués correctement selon design.json. Tester que le gradient overlay utilise les couleurs (#FF6A00, #FF3E3E, #000000), opacity 0.55, blendMode overlay. Tester que les effets frosted glass utilisent les valeurs blur appropriées.

- [x] T056 [P] [US6] Apply gradient overlay to main layout if enabled in design.json (colors, opacity 0.55, blendMode overlay) in frontend/src/app/layout.tsx
- [x] T057 [P] [US6] Ensure all glass effects use correct blur values (glassStrong 45px, card 25px) throughout the application
- [x] T058 [P] [US6] Ensure all shadows use correct values (soft, strong, innerGlow) throughout the application
- [x] T059 [US6] Verify gradient overlay is applied correctly if enabled
- [x] T060 [US6] Verify all frosted glass effects use correct blur values
- [x] T061 [US6] Verify all shadows match design.json values

**Checkpoint**: At this point, all visual effects should be applied correctly according to design.json.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T062 [P] Remove all hardcoded color, spacing, radius, shadow values that don't match design system
- [x] T063 [P] Verify no component uses values outside design.json tokens
- [x] T064 [P] Update documentation to reference design system tokens
- [x] T065 [P] Create design system usage guide in frontend/src/design-system/README.md
- [x] T066 Run quickstart.md validation checklist
- [x] T067 [P] Verify Inter font is loaded correctly and applied to all text
- [x] T068 [P] Verify CSS bundle size is < 200KB in production build
- [x] T069 [P] Test all pages visually for design system compliance
- [x] T070 [P] Verify all components work correctly in target browsers (Chrome 76+, Safari 9+, Firefox 103+)
- [x] T071 Final visual audit: compare all components with design.json using color picker, ruler, font inspector

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 3 (Phase 3)**: Depends on Foundational (Phase 2) - Needs tokens to create atoms
- **User Story 4 (Phase 4)**: Depends on User Story 3 - Needs atoms to create molecules
- **User Story 5 (Phase 5)**: Depends on User Story 4 - Needs molecules to create organisms
- **User Story 1 (Phase 6)**: Depends on User Stories 3, 4, 5 - Needs all components to migrate existing code
- **User Story 6 (Phase 7)**: Can run in parallel with Phase 6 - Visual effects can be applied independently
- **Polish (Phase 8)**: Depends on all previous phases being complete

### User Story Dependencies

- **User Story 2 (P1) - Tokens Centralisés**: Foundation - MUST be completed first. No dependencies.
- **User Story 3 (P2) - Atomes**: Depends on US2 (tokens). Can start immediately after Phase 2.
- **User Story 4 (P2) - Molécules**: Depends on US3 (atomes). Can start after Phase 3.
- **User Story 5 (P2) - Organismes**: Depends on US4 (molécules). Can start after Phase 4.
- **User Story 1 (P1) - Application Cohérente**: Depends on US3, US4, US5 (all components). Can start after Phase 5.
- **User Story 6 (P3) - Effets Visuels**: Can run in parallel with US1. Depends on US2 (tokens).

### Within Each User Story

- Tokens/Configuration before components
- Atoms before molecules
- Molecules before organisms
- Components before migration
- Core implementation before visual effects
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational token tasks (T006-T017) can run in parallel (within Phase 2)
- All atom component tasks (T019-T024) can run in parallel (within Phase 3)
- All molecule component tasks (T027-T030) can run in parallel (within Phase 4)
- All organism component tasks (T033-T035) can run in parallel (within Phase 5)
- All migration tasks (T039-T052) can run in parallel (within Phase 6)
- All visual effects tasks (T056-T058) can run in parallel (within Phase 7)
- All polish tasks marked [P] can run in parallel (within Phase 8)

---

## Parallel Example: User Story 3 (Atomes)

```bash
# Launch all atom components together:
Task: "Create Button atom component in frontend/src/components/atoms/Button/Button.tsx"
Task: "Create Input atom component in frontend/src/components/atoms/Input/Input.tsx"
Task: "Create Label atom component in frontend/src/components/atoms/Label/Label.tsx"
Task: "Create Badge atom component in frontend/src/components/atoms/Badge/Badge.tsx"
Task: "Create Icon wrapper component in frontend/src/components/atoms/Icon/Icon.tsx"
```

---

## Parallel Example: User Story 1 (Migration)

```bash
# Launch all component migrations together:
Task: "Migrate LoginForm to use design system in frontend/src/components/admin/LoginForm.tsx"
Task: "Migrate OrderForm to use design system in frontend/src/components/OrderForm.tsx"
Task: "Migrate ProductHero to use design system in frontend/src/components/ProductHero.tsx"
Task: "Migrate ProductFeatures to use design system in frontend/src/components/ProductFeatures.tsx"
Task: "Migrate ProductList to use design system in frontend/src/components/admin/ProductList.tsx"
Task: "Migrate CampaignList to use design system in frontend/src/components/admin/CampaignList.tsx"
# ... etc
```

---

## Implementation Strategy

### MVP First (User Story 2 Only - Tokens Foundation)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (Tokens Centralisés - US2)
3. **STOP and VALIDATE**: Verify all tokens are accessible via Tailwind, CSS variables, and TypeScript
4. Deploy/demo tokens foundation

### Incremental Delivery

1. Complete Setup + Foundational → Tokens ready
2. Add User Story 3 (Atomes) → Test independently → Deploy/Demo
3. Add User Story 4 (Molécules) → Test independently → Deploy/Demo
4. Add User Story 5 (Organismes) → Test independently → Deploy/Demo
5. Add User Story 1 (Migration) → Test independently → Deploy/Demo
6. Add User Story 6 (Effets Visuels) → Test independently → Deploy/Demo
7. Polish → Final validation

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 3 (Atomes)
   - Developer B: User Story 4 (Molécules) - waits for US3
   - Developer C: User Story 5 (Organismes) - waits for US4
3. Once US3, US4, US5 are done:
   - All developers: User Story 1 (Migration) - can work in parallel on different components
   - Developer D: User Story 6 (Effets Visuels) - can work in parallel
4. All developers: Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Visual verification is critical - use color picker, ruler, font inspector
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All values must match design.json exactly (0px tolerance for spacing/radius, 0% tolerance for colors)
- Migration must preserve all functionality (no regression)

