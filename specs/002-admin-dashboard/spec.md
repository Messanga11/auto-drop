# Feature Specification: Admin Dashboard Application

**Feature Branch**: `002-admin-dashboard`  
**Created**: 2024-12-04  
**Status**: Draft  
**Input**: User description: "j'ai besoin d'une nouvelle app admin qui me permet de suivre et piloter la plateforme (crée un compte admin par défaut dans la bd)"

## Clarifications

### Session 2024-12-04

- Q: Communication temps réel et reconnexion automatique → A: Toutes les communications doivent utiliser WebSocket avec reconnexion automatique en cas de déconnexion
- Q: Stratégie de reconnexion WebSocket (délai initial, max, tentatives) → A: Backoff exponentiel avec délai initial 500ms, max 60s, tentatives illimitées
- Q: Gestion des conflits concurrents (plusieurs admins modifiant la même ressource) → A: Dernière modification gagne avec notification WebSocket aux autres admins
- Q: Authentification de la connexion WebSocket → A: Token dans query string lors de la connexion WebSocket (ws://...?token=...)
- Q: Gestion des messages manqués pendant déconnexion → A: Rejouer tous les événements manqués avec historique complet depuis la dernière connexion
- Q: Types d'événements à envoyer via WebSocket → A: Tous les événements de changement d'état (nouveaux produits, scores calculés, créatives générées, campagnes modifiées, nouvelles commandes, changements de statut)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authentification Admin (Priority: P1)

En tant qu'administrateur, je veux me connecter à l'application admin avec un compte par défaut pour accéder au dashboard de pilotage.

**Why this priority**: L'authentification est la base de sécurité et d'accès à toutes les fonctionnalités admin. Sans elle, aucune autre fonctionnalité n'est accessible.

**Independent Test**: Un administrateur peut se connecter avec les identifiants par défaut et accéder au dashboard. Le compte admin par défaut est créé automatiquement lors de l'initialisation de la base de données.

**Acceptance Scenarios**:

1. **Given** la base de données est initialisée, **When** l'application démarre, **Then** un compte admin par défaut est créé automatiquement avec email `admin@dropshipping.local` et mot de passe configurable
2. **Given** un compte admin existe, **When** l'administrateur saisit les identifiants corrects, **Then** il est authentifié et redirigé vers le dashboard
3. **Given** un compte admin existe, **When** l'administrateur saisit des identifiants incorrects, **Then** un message d'erreur est affiché et l'accès est refusé
4. **Given** un administrateur est authentifié, **When** il accède à une page protégée, **Then** il peut voir le contenu sans être redirigé vers la page de connexion

---

### User Story 2 - Dashboard de Monitoring (Priority: P1)

En tant qu'administrateur, je veux voir un tableau de bord avec les métriques clés de la plateforme pour suivre l'état du système en temps réel.

**Why this priority**: Le monitoring est essentiel pour comprendre l'état de la plateforme, identifier les problèmes et prendre des décisions éclairées. C'est la première chose qu'un admin doit voir après connexion.

**Independent Test**: Un administrateur authentifié peut voir le dashboard avec les statistiques principales (nombre de produits scrapés, top produits, campagnes actives, commandes récentes) sans erreur.

**Acceptance Scenarios**:

1. **Given** un administrateur est authentifié, **When** il accède au dashboard, **Then** il voit les métriques principales : nombre total de produits scrapés, nombre de produits scorés, top 5 produits, nombre de campagnes actives, nombre de commandes en attente
2. **Given** le dashboard est affiché et connecté via WebSocket, **When** les données changent en temps réel, **Then** les métriques sont mises à jour automatiquement via WebSocket sans rafraîchissement manuel
3. **Given** la connexion WebSocket est perdue, **When** le système détecte la déconnexion, **Then** la reconnexion automatique est tentée et l'interface affiche un indicateur de reconnexion
4. **Given** le dashboard est affiché, **When** aucune donnée n'existe encore, **Then** des valeurs par défaut (0) sont affichées avec des messages appropriés

---

### User Story 3 - Gestion des Produits et Campagnes (Priority: P2)

En tant qu'administrateur, je veux visualiser, filtrer et gérer les produits scrapés, les scores, les créatives et les campagnes pour piloter la plateforme.

**Why this priority**: Permet à l'administrateur de comprendre quels produits sont identifiés, quelles campagnes sont lancées, et de prendre des actions (activer/désactiver des campagnes, relancer le scraping, etc.).

**Independent Test**: Un administrateur peut naviguer dans les sections produits, campagnes et créatives, voir les détails de chaque élément, et effectuer des actions de base (activer/désactiver, voir les détails).

**Acceptance Scenarios**:

1. **Given** un administrateur est authentifié, **When** il accède à la section "Produits", **Then** il voit la liste des produits scrapés avec leurs scores, plateforme d'origine, et statut
2. **Given** la liste des produits est affichée, **When** l'administrateur filtre par plateforme ou score, **Then** la liste est mise à jour selon les critères
3. **Given** la liste des produits est affichée et connectée via WebSocket, **When** un nouveau produit est scrapé ou un score est calculé, **Then** la liste est mise à jour automatiquement en temps réel
4. **Given** un administrateur est authentifié, **When** il accède à la section "Campagnes", **Then** il voit la liste des campagnes avec leur statut, budget, et performance
5. **Given** une campagne est en pause, **When** l'administrateur clique sur "Activer", **Then** la campagne est activée et le statut est mis à jour en temps réel via WebSocket
6. **Given** un administrateur est authentifié, **When** il accède à la section "Créatives", **Then** il voit la liste des créatives générées avec leur type, statut et produit associé
7. **Given** la liste des campagnes est affichée et connectée via WebSocket, **When** le statut d'une campagne change (par un autre admin ou automatiquement), **Then** la liste est mise à jour automatiquement en temps réel

---

### User Story 4 - Actions de Pilotage (Priority: P2)

En tant qu'administrateur, je veux pouvoir déclencher manuellement des actions système (scraping, scoring, génération de créatives) pour piloter la plateforme.

**Why this priority**: Permet à l'administrateur de contrôler le workflow de la plateforme, de relancer des processus en cas d'erreur, ou de forcer l'exécution de tâches.

**Independent Test**: Un administrateur peut déclencher un scraping, un calcul de scores, ou une génération de créatives depuis l'interface admin et voir le statut de l'opération.

**Acceptance Scenarios**:

1. **Given** un administrateur est authentifié, **When** il clique sur "Lancer le scraping", **Then** le scraping est démarré en arrière-plan et un message de confirmation est affiché
2. **Given** un scraping est en cours, **When** l'administrateur consulte la page de statut connectée via WebSocket, **Then** il voit le progrès et le nombre d'ads récupérées mis à jour en temps réel
3. **Given** un administrateur est authentifié, **When** il clique sur "Calculer les scores", **Then** le calcul est lancé et les top 5 produits sont identifiés
4. **Given** un produit est sélectionné, **When** l'administrateur clique sur "Générer les créatives", **Then** la génération est lancée et le statut est visible

---

### User Story 5 - Gestion des Commandes (Priority: P3)

En tant qu'administrateur, je veux voir et gérer les commandes reçues pour suivre les ventes et mettre à jour leur statut.

**Why this priority**: Permet de suivre les résultats business de la plateforme et de gérer le cycle de vie des commandes (validation, traitement, expédition).

**Independent Test**: Un administrateur peut voir la liste des commandes, filtrer par statut, voir les détails d'une commande, et mettre à jour son statut.

**Acceptance Scenarios**:

1. **Given** un administrateur est authentifié, **When** il accède à la section "Commandes", **Then** il voit la liste des commandes avec client, produit, quantité, statut et date
2. **Given** la liste des commandes est affichée, **When** l'administrateur filtre par statut (pending, processing, completed), **Then** la liste est mise à jour
3. **Given** une commande est en statut "pending", **When** l'administrateur change le statut à "processing", **Then** le statut est mis à jour en temps réel via WebSocket et l'historique est enregistré
4. **Given** la liste des commandes est affichée et connectée via WebSocket, **When** une nouvelle commande est créée ou le statut change, **Then** la liste est mise à jour automatiquement en temps réel

---

### Edge Cases

- Que se passe-t-il si le compte admin par défaut existe déjà lors de l'initialisation ? (ne pas créer de doublon)
- Comment gérer la session admin expirée ? (redirection vers login avec message)
- Que se passe-t-il si une action de pilotage échoue ? (affichage d'un message d'erreur avec détails)
- Comment gérer l'accès concurrent à la même ressource ? (dernière modification gagne, notification WebSocket aux autres admins)
- Que se passe-t-il si la base de données est inaccessible ? (affichage d'un message d'erreur système)
- Que se passe-t-il si la connexion WebSocket est perdue ? (reconnexion automatique avec indicateur visuel)
- Comment gérer les mises à jour concurrentes de la même ressource par plusieurs admins ? (notification de conflit ou dernière modification gagne)
- Que se passe-t-il si la reconnexion WebSocket échoue après plusieurs tentatives ? (affichage d'un message d'erreur et possibilité de rafraîchissement manuel)
- Comment gérer les événements manqués pendant la déconnexion ? (rejouer tous les événements depuis la dernière connexion lors de la reconnexion)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT créer automatiquement un compte admin par défaut lors de l'initialisation de la base de données avec email `admin@dropshipping.local` et mot de passe configurable via variable d'environnement
- **FR-002**: Le système DOIT permettre l'authentification des administrateurs via email et mot de passe
- **FR-003**: Le système DOIT maintenir une session authentifiée pour les administrateurs avec expiration configurable
- **FR-004**: Le système DOIT protéger toutes les routes admin et rediriger vers la page de connexion si non authentifié
- **FR-024**: Le système DOIT authentifier les connexions WebSocket via token dans la query string et rejeter les connexions non authentifiées
- **FR-025**: Le système DOIT rejouer tous les événements manqués depuis la dernière connexion WebSocket lors de la reconnexion pour maintenir la cohérence des données
- **FR-026**: Le système DOIT envoyer via WebSocket tous les événements de changement d'état : nouveaux produits scrapés, scores calculés, créatives générées, campagnes modifiées, nouvelles commandes, changements de statut de commande
- **FR-005**: Le système DOIT afficher un dashboard avec les métriques principales : nombre de produits scrapés, produits scorés, top 5 produits, campagnes actives, commandes en attente
- **FR-006**: Le système DOIT permettre de visualiser la liste des produits scrapés avec filtres par plateforme, score, et statut
- **FR-007**: Le système DOIT permettre de visualiser la liste des campagnes avec leur statut, budget, et performance
- **FR-008**: Le système DOIT permettre d'activer ou désactiver une campagne depuis l'interface admin
- **FR-009**: Le système DOIT permettre de déclencher manuellement le scraping depuis l'interface admin
- **FR-010**: Le système DOIT permettre de déclencher manuellement le calcul des scores depuis l'interface admin
- **FR-011**: Le système DOIT permettre de déclencher manuellement la génération de créatives pour un produit depuis l'interface admin
- **FR-012**: Le système DOIT afficher le statut et le progrès des opérations en cours (scraping, scoring, génération) mis à jour en temps réel via WebSocket
- **FR-018**: Le système DOIT utiliser WebSocket pour toutes les communications temps réel entre le frontend admin et le backend
- **FR-019**: Le système DOIT implémenter une reconnexion automatique en cas de perte de connexion WebSocket avec stratégie de backoff exponentiel (délai initial 500ms, maximum 60s, tentatives illimitées)
- **FR-020**: Le système DOIT afficher un indicateur visuel de l'état de la connexion WebSocket (connecté, déconnecté, reconnexion en cours)
- **FR-021**: Le système DOIT mettre à jour automatiquement toutes les listes (produits, campagnes, créatives, commandes) en temps réel via WebSocket lorsqu'un changement survient
- **FR-022**: Le système DOIT mettre à jour automatiquement les métriques du dashboard en temps réel via WebSocket
- **FR-023**: Le système DOIT gérer les modifications concurrentes en appliquant la dernière modification et notifier les autres administrateurs via WebSocket
- **FR-013**: Le système DOIT permettre de visualiser la liste des commandes avec filtres par statut et date
- **FR-014**: Le système DOIT permettre de mettre à jour le statut d'une commande depuis l'interface admin
- **FR-015**: Le système DOIT enregistrer l'historique des actions administratives (qui a fait quoi et quand)
- **FR-016**: Le système DOIT afficher des messages d'erreur clairs en cas d'échec d'une opération
- **FR-017**: Le système DOIT valider les permissions avant d'autoriser toute action administrative

### Key Entities *(include if feature involves data)*

- **AdminUser**: Représente un compte administrateur avec email, mot de passe hashé, date de création, dernière connexion, et statut (actif/inactif)
- **AdminSession**: Représente une session d'authentification avec token, admin associé, date d'expiration, et adresse IP
- **AdminAction**: Représente une action administrative effectuée (type d'action, admin responsable, ressource concernée, timestamp, résultat)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un administrateur peut se connecter à l'application admin en moins de 30 secondes après l'initialisation de la base de données
- **SC-002**: Le dashboard affiche les métriques principales en moins de 2 secondes après le chargement de la page
- **SC-003**: Un administrateur peut déclencher une action de pilotage (scraping, scoring, génération) en moins de 3 clics depuis le dashboard
- **SC-004**: Le statut des opérations en cours est visible et mis à jour en temps réel via WebSocket sans délai perceptible (< 1 seconde)
- **SC-011**: La reconnexion WebSocket s'effectue automatiquement en moins de 5 secondes après une déconnexion
- **SC-012**: L'indicateur de statut de connexion WebSocket reflète l'état réel avec une précision de 100%
- **SC-005**: Un administrateur peut filtrer et trouver un produit spécifique dans une liste de 1000+ produits en moins de 10 secondes
- **SC-006**: Les actions administratives sont enregistrées avec un taux de succès de 100% (toutes les actions sont tracées)
- **SC-007**: L'application admin supporte au moins 5 administrateurs simultanés sans dégradation de performance
- **SC-008**: Un administrateur peut mettre à jour le statut d'une commande en moins de 5 secondes
- **SC-009**: Le système bloque 100% des tentatives d'accès non autorisées aux routes admin
- **SC-010**: Les erreurs système sont affichées avec des messages compréhensibles dans 100% des cas

## Dependencies

- L'application admin dépend de l'existence des entités de la plateforme principale (ScrapedAd, ProductScore, Creative, Campaign, Order)
- L'authentification admin nécessite un système de gestion de sessions
- Les actions de pilotage utilisent les endpoints API existants de la plateforme
- La communication temps réel nécessite un serveur WebSocket compatible avec le backend FastAPI
- La reconnexion automatique nécessite une gestion d'état côté client pour maintenir la cohérence

## Assumptions

- Un seul compte admin par défaut est suffisant pour démarrer (d'autres comptes peuvent être créés manuellement)
- Le mot de passe admin par défaut sera changé lors du premier déploiement en production
- Les administrateurs ont accès à toutes les fonctionnalités (pas de granularité de permissions dans le MVP)
- L'interface admin est accessible uniquement en interne (pas d'exposition publique prévue)
