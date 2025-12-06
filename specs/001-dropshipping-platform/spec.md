# Feature Specification: Plateforme Dropshipping Automatisée

**Feature Branch**: `001-dropshipping-platform`  
**Created**: 2024-12-01  
**Status**: Draft  
**Input**: User description: "read this before @techincal-doc.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Découverte et sélection automatique des produits gagnants (Priority: P1)

En tant qu'opérateur de dropshipping, je veux que le système identifie automatiquement les 5 meilleurs produits chaque mois à partir de milliers de publicités, afin de me concentrer uniquement sur les produits à fort potentiel de vente sans avoir à analyser manuellement des centaines d'annonces.

**Why this priority**: C'est le cœur de la valeur business - sans sélection automatique de produits performants, le reste du système n'a pas de sens. Cette fonctionnalité permet de transformer des milliers de données brutes en opportunités concrètes.

**Independent Test**: Le système peut être testé indépendamment en lui fournissant un ensemble de données de publicités scrapées et en vérifiant qu'il identifie correctement les 5 meilleurs produits selon les critères définis. La valeur est démontrable même si aucun autre module n'est implémenté.

**Acceptance Scenarios**:

1. **Given** le système a collecté 1000 publicités depuis Facebook Ads Library et TikTok Ads Library, **When** le processus de scoring s'exécute, **Then** le système identifie automatiquement les 5 produits avec les scores les plus élevés
2. **Given** une publicité pour un produit électronique complexe, **When** le scoring s'exécute, **Then** le produit est exclu automatiquement des résultats
3. **Given** une publicité pour un produit maison/déco avec un format problème→solution, **When** le scoring s'exécute, **Then** le produit reçoit un bonus de score significatif
4. **Given** plusieurs publicités pour le même produit, **When** le scoring s'exécute, **Then** le système détecte le multi-posting et applique un bonus approprié

---

### User Story 2 - Génération automatique de créatives vidéo et landing pages (Priority: P2)

En tant qu'opérateur de dropshipping, je veux que le système génère automatiquement des créatives vidéo publicitaires et des landing pages pour chaque produit sélectionné, afin de lancer rapidement des campagnes sans avoir à créer manuellement le contenu marketing.

**Why this priority**: Une fois les produits identifiés, la génération automatique de contenu marketing permet de passer rapidement à la phase de lancement. Sans cette automatisation, chaque produit nécessiterait des heures de travail créatif manuel.

**Independent Test**: Le système peut être testé en lui fournissant un produit sélectionné et en vérifiant qu'il génère 2-4 créatives vidéo différentes et une landing page fonctionnelle. La valeur est démontrable même si les campagnes ne sont pas encore lancées.

**Acceptance Scenarios**:

1. **Given** un produit a été sélectionné dans le top 5, **When** le processus de génération de créatives est déclenché, **Then** le système génère automatiquement 4 créatives vidéo de styles différents (UGC, Problem-Solution, Short Hook, Carousel)
2. **Given** les créatives vidéo sont générées, **When** le processus de création de landing page s'exécute, **Then** une landing page complète est créée avec formulaire de commande et intégration des vidéos
3. **Given** une landing page est créée, **When** un utilisateur visite la page, **Then** il peut voir les informations produit, les vidéos créatives et soumettre une commande
4. **Given** un utilisateur soumet une commande, **When** le formulaire est validé, **Then** la commande est enregistrée et l'utilisateur est redirigé vers WhatsApp

---

### User Story 3 - Lancement automatique de campagnes publicitaires (Priority: P2)

En tant qu'opérateur de dropshipping, je veux que le système lance automatiquement des campagnes publicitaires sur Meta Ads et TikTok Ads pour chaque produit, afin de générer du trafic vers les landing pages sans configuration manuelle répétitive.

**Why this priority**: L'automatisation du lancement de campagnes permet de scaler rapidement et de tester plusieurs produits simultanément. C'est l'étape qui transforme le contenu généré en trafic réel.

**Independent Test**: Le système peut être testé en vérifiant qu'il crée correctement des campagnes sur les plateformes publicitaires avec les créatives générées et les budgets configurés. La valeur est démontrable même si les campagnes sont créées en mode "paused" pour validation manuelle.

**Acceptance Scenarios**:

1. **Given** un produit a des créatives vidéo prêtes et une landing page active, **When** le processus de lancement de campagne est déclenché, **Then** le système crée automatiquement des campagnes sur Meta Ads et TikTok Ads
2. **Given** des campagnes sont créées, **When** elles sont configurées, **Then** chaque créative vidéo est associée à un groupe de publicités distinct avec budget alloué
3. **Given** des campagnes sont créées en mode "paused", **When** l'opérateur les active manuellement, **Then** les publicités commencent à diffuser vers les audiences ciblées
4. **Given** une campagne est active, **When** un utilisateur clique sur une publicité, **Then** il est redirigé vers la landing page correspondante avec tracking pixel activé

---

### User Story 4 - Gestion des commandes via chatbot WhatsApp intelligent (Priority: P3)

En tant que client, je veux pouvoir commander un produit via WhatsApp et recevoir des réponses automatiques intelligentes à mes questions, afin d'avoir une expérience d'achat fluide et rassurante sans attendre un opérateur humain.

**Why this priority**: Bien que moins critique que les autres stories, cette fonctionnalité améliore significativement l'expérience client et réduit la charge de travail manuel pour la gestion des commandes. Elle peut être implémentée après que le flux principal soit opérationnel.

**Independent Test**: Le système peut être testé en envoyant des messages WhatsApp simulés et en vérifiant que le chatbot répond de manière appropriée avec le contexte des commandes. La valeur est démontrable même si les autres modules ne sont pas complets.

**Acceptance Scenarios**:

1. **Given** un client a soumis une commande via la landing page, **When** il envoie un message WhatsApp, **Then** le chatbot reconnaît sa commande et fournit des informations contextuelles
2. **Given** un client pose une question sur un produit, **When** le chatbot reçoit le message, **Then** il génère une réponse pertinente en français sans nécessiter d'intervention humaine
3. **Given** un client demande le statut de sa commande, **When** le chatbot reçoit la demande, **Then** il fournit le statut actuel basé sur les données de la base de données
4. **Given** le chatbot ne comprend pas une question, **When** il ne peut pas répondre, **Then** il oriente poliment le client vers le service client humain

---

### Edge Cases

- Que se passe-t-il si aucune publicité ne correspond aux critères de sélection après le scraping mensuel?
- Comment le système gère-t-il les erreurs lors de la génération de créatives vidéo (échec API, timeout)?
- Que se passe-t-il si une landing page est créée mais les créatives vidéo ne sont pas encore prêtes?
- Comment le système gère-t-il les échecs de création de campagnes publicitaires (quota API dépassé, credentials invalides)?
- Que se passe-t-il si le chatbot WhatsApp ne peut pas se connecter à l'API de génération IA?
- Comment le système gère-t-il les doublons de produits (même produit scrapé depuis plusieurs sources)?
- Que se passe-t-il si un produit sélectionné n'a pas d'URL de landing page valide?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT scraper automatiquement au moins 1000 publicités par mois depuis Facebook Ads Library et TikTok Ads Library
- **FR-002**: Le système DOIT identifier automatiquement les 5 meilleurs produits chaque mois selon des critères de scoring prédéfinis
- **FR-003**: Le système DOIT exclure automatiquement certains types de produits (électronique complexe, cosmétiques à risque, produits nécessitant certifications)
- **FR-004**: Le système DOIT privilégier certains types de produits (maison/déco, accessoires pratiques, mode simple, sport/bien-être)
- **FR-005**: Le système DOIT calculer un score pour chaque produit basé sur l'engagement (likes, commentaires, partages), le type de produit, et la récence
- **FR-006**: Le système DOIT générer automatiquement 2-4 créatives vidéo par produit sélectionné avec différents styles (UGC, Problem-Solution, Short Hook, Carousel)
- **FR-007**: Le système DOIT créer automatiquement une landing page pour chaque produit avec formulaire de commande
- **FR-008**: Le système DOIT permettre aux utilisateurs de soumettre des commandes via le formulaire de la landing page
- **FR-009**: Le système DOIT enregistrer toutes les commandes avec les informations client (nom, téléphone, adresse, ville, quantité)
- **FR-010**: Le système DOIT lancer automatiquement des campagnes publicitaires sur Meta Ads et TikTok Ads pour chaque produit
- **FR-011**: Le système DOIT créer les campagnes en mode "paused" pour permettre une validation manuelle avant activation
- **FR-012**: Le système DOIT associer chaque créative vidéo à un groupe de publicités distinct avec budget alloué
- **FR-013**: Le système DOIT intégrer les pixels de tracking Meta et TikTok sur les landing pages
- **FR-014**: Le système DOIT rediriger les utilisateurs vers WhatsApp après soumission d'une commande
- **FR-015**: Le système DOIT gérer les messages WhatsApp entrants via un chatbot intelligent
- **FR-016**: Le chatbot DOIT générer des réponses contextuelles en français basées sur les commandes du client
- **FR-017**: Le système DOIT exécuter le scraping mensuel automatiquement selon un calendrier prédéfini
- **FR-018**: Le système DOIT gérer les erreurs d'APIs externes avec des mécanismes de retry et de fallback appropriés
- **FR-019**: Le système DOIT permettre la collecte de commandes sans paiement en ligne (paiement à la livraison uniquement)
- **FR-020**: Le système DOIT exclure le tracking de colis (géré manuellement en dehors du système)

### Key Entities

- **Produit (ScrapedAd)**: Représente une publicité scrapée depuis Facebook ou TikTok. Contient: identifiant plateforme, URL de la publicité, nom de la page/advertiser, texte de la publicité, métriques d'engagement (likes, commentaires, partages, vues), dates de diffusion, statut de scoring
- **Score Produit (ProductScore)**: Représente le score calculé pour un produit. Contient: référence au produit, score final, composantes du score (engagement, bonus catégorie, bonus problème-solution, bonus multi-posting, score récence), date de calcul
- **Créative (Creative)**: Représente une vidéo publicitaire générée. Contient: référence au produit, type de créative (UGC, Problem-Solution, etc.), identifiant vidéo externe, statut de génération, URL de téléchargement, chemin local
- **Campagne (Campaign)**: Représente une campagne publicitaire lancée. Contient: référence au produit, plateforme (Meta/TikTok), identifiant campagne externe, nom, budget quotidien, statut (paused/active/completed), dates de création/activation
- **Commande (Order)**: Représente une commande client. Contient: référence au produit, nom du produit, informations client (nom complet, téléphone, adresse, ville), quantité, statut (pending/confirmed/shipped/delivered), dates de création/mise à jour

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Le système identifie automatiquement 5 produits gagnants chaque mois à partir d'au moins 1000 publicités scrapées, avec un taux de succès de 100% (5 produits toujours identifiés)
- **SC-002**: Le système génère 4 créatives vidéo par produit en moins de 2 heures par produit (de la sélection à la disponibilité des vidéos)
- **SC-003**: Le système crée une landing page fonctionnelle pour chaque produit en moins de 5 minutes après la génération des créatives
- **SC-004**: Le système lance des campagnes publicitaires pour 5 produits en moins de 30 minutes (création complète avec toutes les créatives)
- **SC-005**: Les utilisateurs peuvent compléter une commande sur une landing page en moins de 2 minutes
- **SC-006**: Le chatbot WhatsApp répond aux messages clients en moins de 10 secondes dans 95% des cas
- **SC-007**: Le système exécute le scraping mensuel automatiquement sans intervention manuelle avec un taux de succès de 98%
- **SC-008**: Le système gère jusqu'à 100 commandes simultanées sans dégradation de performance
- **SC-009**: Les campagnes publicitaires sont créées avec un taux de succès de 95% (5% d'erreurs API acceptables avec retry)
- **SC-010**: Le processus complet de sélection à lancement de campagne pour 5 produits est complété en moins de 24 heures après le scraping mensuel
