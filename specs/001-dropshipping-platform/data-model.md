# Data Model: Plateforme Dropshipping Automatisée

**Created**: 2024-12-01  
**Feature**: [spec.md](./spec.md)

## Entities

### ScrapedAd (Produit Scrapé)

Représente une publicité scrapée depuis Facebook Ads Library ou TikTok Ads Library.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `platform` (String(20), NOT NULL): Plateforme source ("facebook" ou "tiktok")
- `ad_id` (String(255), UNIQUE): Identifiant de la publicité sur la plateforme source
- `ad_snapshot_url` (Text): URL de capture d'écran de la publicité (Facebook)
- `video_url` (Text): URL de la vidéo publicitaire (TikTok)
- `page_name` (String(255)): Nom de la page Facebook
- `advertiser_name` (String(255)): Nom de l'advertiser TikTok
- `caption` (Text): Texte de la publicité TikTok
- `ad_creative_bodies` (Text): Corps du texte publicitaire Facebook
- `likes` (Integer, default=0): Nombre de likes
- `comments` (Integer, default=0): Nombre de commentaires
- `shares` (Integer, default=0): Nombre de partages
- `views` (Integer, default=0): Nombre de vues
- `impressions_upper_bound` (Integer): Borne supérieure d'impressions (Facebook)
- `ad_delivery_start_time` (DateTime): Date de début de diffusion (Facebook)
- `first_shown_date` (DateTime): Date de première diffusion (TikTok)
- `scraped_at` (DateTime, default=now): Date de scraping
- `scored` (Boolean, default=False): Indique si le produit a été scoré
- `selected_for_campaign` (Boolean, default=False): Indique si le produit a été sélectionné pour campagne

**Relationships**:
- One-to-Many avec `ProductScore` (un produit peut avoir un score)
- One-to-Many avec `Creative` (un produit peut avoir plusieurs créatives)
- One-to-Many avec `Campaign` (un produit peut avoir plusieurs campagnes)
- One-to-Many avec `Order` (un produit peut avoir plusieurs commandes)

**Validation Rules**:
- `platform` doit être "facebook" ou "tiktok"
- `ad_id` doit être unique par plateforme
- Au moins un de `ad_snapshot_url` ou `video_url` doit être présent

**Indexes**:
- `idx_ads_platform` sur `platform`
- `idx_ads_scored` sur `scored`

### ProductScore (Score Produit)

Représente le score calculé pour un produit scrapé.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `ad_id` (Integer, FK → ScrapedAd.id): Référence au produit
- `score` (Float, NOT NULL): Score final calculé
- `engagement_score` (Float): Composante engagement normalisé
- `problem_solution_bonus` (Float): Bonus pour format problème→solution
- `category_bonus` (Float): Bonus pour catégorie prioritaire
- `multi_posting_bonus` (Float): Bonus pour multi-posting
- `recency_score` (Float): Score de récence
- `calculated_at` (DateTime, default=now): Date de calcul

**Relationships**:
- Many-to-One avec `ScrapedAd` (un score appartient à un produit)

**Validation Rules**:
- `score` doit être >= 0
- `ad_id` doit référencer un ScrapedAd existant

**Indexes**:
- `idx_scores_score` sur `score` (DESC pour top produits)

### Creative (Créative Vidéo)

Représente une vidéo publicitaire générée via Creatify API.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `product_id` (Integer, FK → ScrapedAd.id): Référence au produit
- `video_id` (String(255)): Identifiant Creatify de la vidéo
- `video_type` (String(50)): Type de créative ("ugc", "problem_solution", "short_hook", "carousel")
- `status` (String(20)): Statut de génération ("queued", "processing", "completed", "failed")
- `download_url` (Text): URL de téléchargement de la vidéo
- `local_path` (Text): Chemin local de la vidéo téléchargée
- `created_at` (DateTime, default=now): Date de création
- `completed_at` (DateTime): Date de complétion

**Relationships**:
- Many-to-One avec `ScrapedAd` (une créative appartient à un produit)

**Validation Rules**:
- `video_type` doit être un des types valides
- `status` doit être un des statuts valides
- `product_id` doit référencer un ScrapedAd existant

**State Transitions**:
- `queued` → `processing` → `completed` ou `failed`
- Pas de retour en arrière possible

### Campaign (Campagne Publicitaire)

Représente une campagne publicitaire lancée sur Meta Ads ou TikTok Ads.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `product_id` (Integer, FK → ScrapedAd.id): Référence au produit
- `platform` (String(20)): Plateforme ("meta" ou "tiktok")
- `campaign_id` (String(255)): Identifiant externe de la campagne
- `campaign_name` (String(255)): Nom de la campagne
- `daily_budget` (Integer): Budget quotidien en centimes
- `status` (String(20)): Statut ("paused", "active", "completed")
- `created_at` (DateTime, default=now): Date de création
- `activated_at` (DateTime): Date d'activation
- `meta_data` (JSONB): Métadonnées supplémentaires (IDs adsets, ads, etc.)

**Relationships**:
- Many-to-One avec `ScrapedAd` (une campagne appartient à un produit)

**Validation Rules**:
- `platform` doit être "meta" ou "tiktok"
- `status` doit être un des statuts valides
- `daily_budget` doit être > 0
- `product_id` doit référencer un ScrapedAd existant

**Indexes**:
- `idx_campaigns_status` sur `status`

**State Transitions**:
- `paused` → `active` → `completed`
- Pas de retour de `active` à `paused` (seulement vers `completed`)

### Order (Commande)

Représente une commande client soumise via une landing page.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `product_id` (Integer, FK → ScrapedAd.id): Référence au produit commandé
- `product_name` (String(255)): Nom du produit (copie pour historique)
- `full_name` (String(255), NOT NULL): Nom complet du client
- `phone` (String(20), NOT NULL): Numéro de téléphone WhatsApp
- `address` (Text, NOT NULL): Adresse complète de livraison
- `city` (String(100)): Ville
- `quantity` (Integer, default=1): Quantité commandée
- `status` (String(20), default='pending'): Statut ("pending", "confirmed", "shipped", "delivered")
- `created_at` (DateTime, default=now): Date de création
- `updated_at` (DateTime): Date de dernière mise à jour

**Relationships**:
- Many-to-One avec `ScrapedAd` (une commande appartient à un produit)

**Validation Rules**:
- `phone` doit être au format valide (10-15 chiffres, optionnel +)
- `quantity` doit être entre 1 et 10
- `status` doit être un des statuts valides
- `product_id` doit référencer un ScrapedAd existant

**Indexes**:
- `idx_orders_phone` sur `phone` (pour recherche par client)
- `idx_orders_status` sur `status`

**State Transitions**:
- `pending` → `confirmed` → `shipped` → `delivered`
- Pas de retour en arrière (workflow linéaire)

## Relationships Summary

```
ScrapedAd (1) ──< (Many) ProductScore
ScrapedAd (1) ──< (Many) Creative
ScrapedAd (1) ──< (Many) Campaign
ScrapedAd (1) ──< (Many) Order
```

## Data Flow

1. **Scraping**: Publicités scrapées → `ScrapedAd` créées
2. **Scoring**: `ScrapedAd` non scorées → `ProductScore` créé → Top 5 identifiés
3. **Créatives**: `ScrapedAd` sélectionné → `Creative` créées (4 par produit)
4. **Campagnes**: `Creative` complétées → `Campaign` créées (Meta + TikTok)
5. **Commandes**: Utilisateur soumet formulaire → `Order` créée

