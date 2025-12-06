# Research: Plateforme Dropshipping Automatisée

**Created**: 2024-12-01  
**Feature**: [spec.md](./spec.md)

## Décisions Techniques

### Stack Technologique

**Decision**: Utiliser Next.js 15.1.0+ (frontend) et FastAPI 0.115.0+ (backend) avec PostgreSQL 16+ et Redis 7.4+.

**Rationale**: 
- Next.js 15 offre ISR (Incremental Static Regeneration) nécessaire pour les landing pages statiques avec revalidation
- FastAPI 0.115+ supporte nativement async/await requis pour les performances
- PostgreSQL 16+ avec SQLAlchemy 2.0 async offre les performances nécessaires pour 1000+ publicités
- Redis 7.4+ pour cache et queues de tâches asynchrones

**Alternatives considérées**:
- Django: Plus lourd, moins performant pour async
- Express.js: Pas de support ISR natif, moins adapté pour landing pages statiques
- MongoDB: Moins adapté pour relations complexes entre produits, scores, campagnes

### Architecture des Modules

**Decision**: 6 modules indépendants (Scraping, Scoring, Créatives, Landing Pages, Campagnes, Chatbot) communiquant via services et événements.

**Rationale**: 
- Permet développement parallèle par équipe
- Tests isolés par module
- Remplacement/amélioration d'un module sans impact sur les autres
- Conforme au principe de modularité de la constitution

**Alternatives considérées**:
- Architecture monolithique: Plus difficile à tester et maintenir
- Microservices: Overhead inutile pour cette échelle

### Gestion des Tâches Asynchrones

**Decision**: Utiliser BackgroundTasks de FastAPI pour tâches courtes (< 5 min) et APScheduler pour tâches planifiées (scraping mensuel).

**Rationale**:
- BackgroundTasks intégré à FastAPI, simple pour génération créatives
- APScheduler pour planification mensuelle automatique
- Évite la complexité de Celery pour cette échelle

**Alternatives considérées**:
- Celery: Plus complexe, nécessite broker Redis dédié
- Queue simple: Pas de planification intégrée

### Intégration APIs Externes

**Decision**: Utiliser les clients officiels (apify-client, facebook-business) avec retry et fallback.

**Rationale**:
- Clients officiels maintenus et documentés
- Retry automatique pour gérer les erreurs temporaires
- Fallback pour éviter les blocages complets

**Alternatives considérées**:
- Appels HTTP directs: Plus de code à maintenir, moins robuste
- Wrappers custom: Overhead inutile

### Génération de Créatives Vidéo

**Decision**: Utiliser Creatify API pour génération automatique de 4 styles de vidéos par produit.

**Rationale**:
- API spécialisée dans la génération vidéo automatisée
- Support de multiples formats (UGC, Problem-Solution, etc.)
- Intégration simple via API REST

**Alternatives considérées**:
- Génération manuelle: Non scalable, trop de temps
- Autres APIs vidéo: Creatify offre le meilleur rapport qualité/prix

### Chatbot WhatsApp avec IA Locale

**Decision**: Utiliser Ollama avec modèle llama3.2:3b pour génération de réponses contextuelles.

**Rationale**:
- IA locale évite les coûts d'API externes
- Modèle léger (3b) suffisant pour réponses contextuelles simples
- Pas de dépendance à des services externes (OpenAI, etc.)
- Respect de la vie privée (données locales)

**Alternatives considérées**:
- OpenAI API: Coûts récurrents, dépendance externe
- Règles simples: Pas assez flexible pour contexte variable
- Autres modèles locaux: llama3.2:3b offre bon équilibre performance/taille

### Scoring Algorithmique

**Decision**: Formule de scoring combinant engagement normalisé, catégories prioritaires, format problème-solution, multi-posting, et récence.

**Rationale**:
- Formule simple et explicable
- Poids ajustables selon résultats
- Détection automatique de catégories via mots-clés
- Bonus pour produits récents (tendance)

**Alternatives considérées**:
- Machine Learning: Overkill, nécessite données d'entraînement
- Scoring simple (engagement uniquement): Ignore le contexte produit

### Structure de Base de Données

**Decision**: 5 tables principales (scraped_ads, product_scores, creatives, campaigns, orders) avec relations claires.

**Rationale**:
- Structure normalisée évite redondance
- Index sur colonnes fréquemment requêtées (platform, scored, status)
- JSONB pour métadonnées flexibles (campaigns.meta_data)

**Alternatives considérées**:
- NoSQL: Moins adapté pour relations complexes
- Tables dénormalisées: Risque d'incohérence

### Gestion des Erreurs

**Decision**: Retry avec backoff exponentiel pour APIs externes, fallback gracieux, logging structuré.

**Rationale**:
- Retry gère erreurs temporaires (rate limits, timeouts)
- Fallback évite blocage complet du système
- Logging structuré facilite debugging

**Alternatives considérées**:
- Retry simple: Moins robuste
- Pas de retry: Trop d'échecs

