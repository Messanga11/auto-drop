# PLATEFORME DROPSHIPPING AUTOMATISÉE

## Documentation Technique Complète A-Z

**Version:** 1.0  
**Date:** Décembre 2024  
**Objectif:** Automatiser le lancement de 5 produits gagnants par mois avec génération de créatives et gestion de campagnes publicitaires

---

## TABLE DES MATIÈRES

1. [Vue d'ensemble du système](#vue-densemble)
2. [Architecture technique](#architecture)
3. [Stack technologique](#stack)
4. [Module 1: Scraping des publicités](#module-1)
5. [Module 2: Scoring et sélection des produits](#module-2)
6. [Module 3: Génération des créatives](#module-3)
7. [Module 4: Landing pages automatiques](#module-4)
8. [Module 5: Lancement des campagnes](#module-5)
9. [Module 6: Chatbot WhatsApp](#module-6)
10. [Installation et déploiement](#installation)
11. [Variables d'environnement](#env-variables)
12. [Base de données](#database)
13. [Tests et validation](#tests)

---

<a name="vue-densemble"></a>

## 1. VUE D'ENSEMBLE DU SYSTÈME

### 1.1 Objectifs Business

- **Scraper** 1000 produits/mois depuis Facebook Ads Library et TikTok Ads Library
- **Identifier** les 5 meilleurs produits selon des critères prédéfinis
- **Générer** automatiquement 2-4 créatives vidéo par produit via Creatify API
- **Créer** une landing page Next.js pour chaque produit
- **Lancer** automatiquement les campagnes sur Meta Ads et TikTok Ads
- **Gérer** les commandes via WhatsApp avec IA locale (Ollama)
- **Exclure** le tracking colis (géré manuellement)
- **Exclure** le paiement en ligne (collecte de commandes uniquement)

### 1.2 Workflow Complet

```
[Apify Scrapers] → [Base de données] → [Scoring automatique] → [Top 5 produits]
                                                                        ↓
[Creatify API] ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
       ↓
[Créatives vidéo] → [Landing Page Generator] → [Pages statiques]
       ↓
[Meta Ads API + TikTok Ads API] → [Campagnes actives]
       ↓
[Commandes WhatsApp] → [Ollama Chatbot] → [Base de données commandes]
```

---

<a name="architecture"></a>

## 2. ARCHITECTURE TECHNIQUE

### 2.1 Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 15)                    │
│  - Landing pages statiques (ISR)                            │
│  - Formulaires de commande                                  │
│  - Pixel tracking (Meta, TikTok)                            │
└────────────────────────┬────────────────────────────────────┘
                         │ API Routes
┌────────────────────────▼────────────────────────────────────┐
│                BACKEND API (FastAPI 0.115+)                 │
│  - Endpoints REST                                           │
│  - Webhooks (Apify, Creatify, WhatsApp)                    │
│  - Job scheduling (APScheduler)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼──────┐ ┌─────▼──────┐ ┌─────▼──────────┐
│  PostgreSQL   │ │   Redis    │ │ External APIs  │
│   Database    │ │   Cache    │ │ - Apify        │
│               │ │            │ │ - Creatify     │
└───────────────┘ └────────────┘ │ - Meta Ads     │
                                  │ - TikTok Ads   │
                                  │ - WhatsApp     │
                                  └────────────────┘
```

### 2.2 Principe de Clean Architecture

```
┌──────────────────────────────────────────┐
│         Présentation Layer              │
│  (Routes, Controllers, Webhooks)        │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│         Application Layer                │
│  (Use Cases, Business Logic)             │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│          Domain Layer                    │
│  (Entities, Value Objects)               │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│       Infrastructure Layer               │
│  (Database, External APIs, Storage)      │
└──────────────────────────────────────────┘
```

---

<a name="stack"></a>

## 3. STACK TECHNOLOGIQUE

### 3.1 Frontend

**Framework:** Next.js 15.1.0  
**Raison:** App Router moderne, ISR, SSR, meilleure performance

```bash
# Installation
npx create-next-app@15.1.0 dropshipping-frontend
cd dropshipping-frontend
```

**Configuration recommandée lors de l'installation:**

- ✅ TypeScript
- ✅ ESLint
- ✅ Tailwind CSS
- ✅ `src/` directory
- ✅ App Router
- ✅ Import alias `@/*`

**Dépendances principales:**

```json
{
  "dependencies": {
    "next": "15.1.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.6.0",
    "@radix-ui/react-dialog": "^1.1.2",
    "@radix-ui/react-label": "^2.1.1",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^0.460.0",
    "react-hook-form": "^7.53.2",
    "zod": "^3.24.1",
    "zustand": "^5.0.2"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "tailwindcss": "^3.4.17",
    "postcss": "^8.4.49",
    "autoprefixer": "^10.4.20"
  }
}
```

### 3.2 Backend

**Framework:** FastAPI 0.115.0  
**Raison:** Performance async, validation automatique, documentation OpenAPI

```bash
# Installation
pip install fastapi[all]==0.115.0 uvicorn[standard]==0.32.1
```

**Dépendances complètes:**

```txt
# requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.32.1
pydantic==2.10.3
pydantic-settings==2.6.1
sqlalchemy==2.0.36
alembic==1.14.0
asyncpg==0.30.0
psycopg2-binary==2.9.10
redis==5.2.0
celery==5.4.0
apscheduler==3.10.4
httpx==0.28.1
aiohttp==3.11.7
python-multipart==0.0.19
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
apify-client==1.8.2
boto3==1.35.76
pillow==11.0.0
requests==2.32.3
```

### 3.3 Base de données

**SGBD:** PostgreSQL 16  
**ORM:** SQLAlchemy 2.0 (async)

```bash
# Installation via Docker
docker run --name postgres-dropshipping \
  -e POSTGRES_PASSWORD=votre_mot_de_passe \
  -e POSTGRES_DB=dropshipping \
  -p 5432:5432 \
  -d postgres:16-alpine
```

### 3.4 Cache & Queue

**Cache:** Redis 7.4  
**Queue:** Celery avec Redis backend

```bash
# Installation via Docker
docker run --name redis-dropshipping \
  -p 6379:6379 \
  -d redis:7.4-alpine
```

### 3.5 IA Locale

**LLM:** Ollama  
**Modèle recommandé:** llama3.2:3b ou mistral:7b

```bash
# Installation Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger le modèle
ollama pull llama3.2:3b
```

### 3.6 APIs Externes

| Service            | Utilisation                  | Endpoint                                        | Documentation                                                   |
| ------------------ | ---------------------------- | ----------------------------------------------- | --------------------------------------------------------------- |
| Apify              | Scraping FB/TikTok Ads       | `https://api.apify.com/v2`                      | [Docs](https://docs.apify.com)                                  |
| Creatify           | Génération vidéos            | `https://api.creatify.ai`                       | [Docs](https://docs.creatify.ai)                                |
| Meta Ads API       | Campagnes Facebook/Instagram | `https://graph.facebook.com/v22.0`              | [Docs](https://developers.facebook.com/docs/marketing-api)      |
| TikTok Ads API     | Campagnes TikTok             | `https://business-api.tiktok.com/open_api/v1.3` | [Docs](https://ads.tiktok.com/marketing_api/docs)               |
| WhatsApp Cloud API | Messagerie                   | `https://graph.facebook.com/v22.0`              | [Docs](https://developers.facebook.com/docs/whatsapp/cloud-api) |

---

<a name="module-1"></a>

## 4. MODULE 1: SCRAPING DES PUBLICITÉS

### 4.1 Vue d'ensemble

Ce module utilise Apify pour scraper automatiquement les publicités Facebook et TikTok. Objectif: collecter ~1000 produits par mois.

### 4.2 Acteurs Apify à utiliser

**Facebook Ads Library Scraper:**

- **Actor ID:** `curious_coder/facebook-ads-library-scraper`
- **Coût estimé:** ~$0.20 par 1000 ads
- **Configuration:**

```json
{
  "startUrls": [
    {
      "url": "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&media_type=all"
    }
  ],
  "searchTerms": ["dropshipping", "trending product", "buy now"],
  "countries": ["FR", "US", "GB", "CA"],
  "maxItems": 500,
  "minLikes": 500,
  "minComments": 20,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

**TikTok Ads Scraper:**

- **Actor ID:** `lexis-solutions/tiktok-ads-scraper`
- **Coût estimé:** ~$0.30 par 1000 ads
- **Configuration:**

```json
{
  "queries": ["dropshipping", "trending products", "viral products"],
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "maxPages": 50,
  "regions": ["FR", "US", "GB"]
}
```

### 4.3 Code Backend - Service de Scraping

**Fichier:** `backend/app/services/scraping_service.py`

```python
from apify_client import ApifyClient
from typing import List, Dict, Any
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ScrapingService:
    def __init__(self):
        self.client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    async def scrape_facebook_ads(
        self,
        max_items: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Scrape Facebook Ads Library

        Paramètres:
        - max_items: nombre maximum d'ads à récupérer

        Retourne: Liste de dictionnaires contenant les données des ads
        """
        actor_id = "curious_coder/facebook-ads-library-scraper"

        run_input = {
            "searchTerms": [
                "dropshipping",
                "trending product",
                "buy now",
                "limited offer"
            ],
            "countries": ["FR", "US", "GB", "CA", "DE"],
            "maxItems": max_items,
            "minLikes": 500,
            "minComments": 20,
            "datePreset": "last_30d",
            "proxyConfiguration": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"]
            }
        }

        try:
            logger.info(f"Démarrage scraping Facebook Ads - Actor: {actor_id}")
            run = self.client.actor(actor_id).call(run_input=run_input)

            # Récupérer les résultats du dataset
            dataset_items = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)

            logger.info(f"Scraping Facebook terminé - {len(dataset_items)} ads récupérées")
            return dataset_items

        except Exception as e:
            logger.error(f"Erreur scraping Facebook: {str(e)}")
            raise

    async def scrape_tiktok_ads(
        self,
        max_pages: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Scrape TikTok Ads Library

        Paramètres:
        - max_pages: nombre maximum de pages à scraper

        Retourne: Liste de dictionnaires contenant les données des ads
        """
        actor_id = "lexis-solutions/tiktok-ads-scraper"

        # Dates pour les 30 derniers jours
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        run_input = {
            "queries": [
                "dropshipping",
                "trending products",
                "viral products",
                "must have"
            ],
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "maxPages": max_pages,
            "regions": ["FR", "US", "GB", "CA", "DE"]
        }

        try:
            logger.info(f"Démarrage scraping TikTok Ads - Actor: {actor_id}")
            run = self.client.actor(actor_id).call(run_input=run_input)

            # Récupérer les résultats
            dataset_items = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)

            logger.info(f"Scraping TikTok terminé - {len(dataset_items)} ads récupérées")
            return dataset_items

        except Exception as e:
            logger.error(f"Erreur scraping TikTok: {str(e)}")
            raise

    def normalize_facebook_ad(self, raw_ad: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliser les données Facebook pour la BDD"""
        return {
            "platform": "facebook",
            "ad_id": raw_ad.get("ad_id"),
            "ad_creative_link_url": raw_ad.get("ad_creative_link_url"),
            "ad_snapshot_url": raw_ad.get("ad_snapshot_url"),
            "page_name": raw_ad.get("page_name"),
            "ad_creative_bodies": raw_ad.get("ad_creative_bodies", []),
            "ad_delivery_start_time": raw_ad.get("ad_delivery_start_time"),
            "impressions_lower_bound": raw_ad.get("impressions", {}).get("lower_bound"),
            "impressions_upper_bound": raw_ad.get("impressions", {}).get("upper_bound"),
            "spend_lower_bound": raw_ad.get("spend", {}).get("lower_bound"),
            "spend_upper_bound": raw_ad.get("spend", {}).get("upper_bound"),
            "currency": raw_ad.get("currency"),
            "scraped_at": datetime.utcnow()
        }

    def normalize_tiktok_ad(self, raw_ad: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliser les données TikTok pour la BDD"""
        return {
            "platform": "tiktok",
            "ad_id": raw_ad.get("ad_id"),
            "advertiser_name": raw_ad.get("advertiser_name"),
            "caption": raw_ad.get("caption"),
            "video_url": raw_ad.get("video_url"),
            "image_url": raw_ad.get("image_url"),
            "likes": raw_ad.get("likes", 0),
            "comments": raw_ad.get("comments", 0),
            "shares": raw_ad.get("shares", 0),
            "views": raw_ad.get("views", 0),
            "first_shown_date": raw_ad.get("first_shown_date"),
            "last_shown_date": raw_ad.get("last_shown_date"),
            "scraped_at": datetime.utcnow()
        }
```

### 4.4 Endpoint API de scraping

**Fichier:** `backend/app/api/routes/scraping.py`

```python
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scraping_service import ScrapingService
from app.database import get_db
from app.models.ads import ScrapedAd
from typing import Dict, Any
import logging

router = APIRouter(prefix="/scraping", tags=["scraping"])
logger = logging.getLogger(__name__)

@router.post("/start", response_model=Dict[str, Any])
async def start_scraping(
    background_tasks: BackgroundTasks,
    facebook_max: int = 500,
    tiktok_max: int = 500,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance le scraping des publicités Facebook et TikTok en arrière-plan

    Paramètres:
    - facebook_max: nombre maximum d'ads Facebook à scraper
    - tiktok_max: nombre maximum de pages TikTok à scraper
    """

    async def run_scraping_task():
        try:
            scraper = ScrapingService()

            # Scraper Facebook
            logger.info("Démarrage scraping Facebook...")
            fb_ads = await scraper.scrape_facebook_ads(max_items=facebook_max)

            # Sauvegarder en BDD
            for raw_ad in fb_ads:
                normalized_ad = scraper.normalize_facebook_ad(raw_ad)
                ad = ScrapedAd(**normalized_ad)
                db.add(ad)

            await db.commit()
            logger.info(f"{len(fb_ads)} ads Facebook sauvegardées")

            # Scraper TikTok
            logger.info("Démarrage scraping TikTok...")
            tt_ads = await scraper.scrape_tiktok_ads(max_pages=tiktok_max)

            # Sauvegarder en BDD
            for raw_ad in tt_ads:
                normalized_ad = scraper.normalize_tiktok_ad(raw_ad)
                ad = ScrapedAd(**normalized_ad)
                db.add(ad)

            await db.commit()
            logger.info(f"{len(tt_ads)} ads TikTok sauvegardées")

            logger.info("Scraping terminé avec succès")

        except Exception as e:
            logger.error(f"Erreur lors du scraping: {str(e)}")
            raise

    # Lancer la tâche en arrière-plan
    background_tasks.add_task(run_scraping_task)

    return {
        "status": "started",
        "message": "Le scraping a été lancé en arrière-plan",
        "facebook_max": facebook_max,
        "tiktok_max": tiktok_max
    }

@router.get("/status", response_model=Dict[str, Any])
async def get_scraping_status(db: AsyncSession = Depends(get_db)):
    """Récupère le statut actuel du scraping"""
    from sqlalchemy import select, func
    from app.models.ads import ScrapedAd

    # Compter les ads par plateforme
    result = await db.execute(
        select(
            ScrapedAd.platform,
            func.count(ScrapedAd.id).label("count")
        ).group_by(ScrapedAd.platform)
    )

    counts = {row.platform: row.count for row in result}

    return {
        "total_ads": sum(counts.values()),
        "facebook_ads": counts.get("facebook", 0),
        "tiktok_ads": counts.get("tiktok", 0)
    }
```

### 4.5 Tâche planifiée (mensuelle)

**Fichier:** `backend/app/scheduler.py`

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.scraping_service import ScrapingService
from app.database import get_db
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def monthly_scraping_job():
    """
    Tâche planifiée: scraping mensuel automatique
    S'exécute le 1er de chaque mois à 2h du matin
    """
    logger.info("Démarrage du scraping mensuel automatique")

    try:
        scraper = ScrapingService()
        async for db in get_db():
            # Scraper Facebook (500 ads)
            fb_ads = await scraper.scrape_facebook_ads(max_items=500)
            for raw_ad in fb_ads:
                normalized = scraper.normalize_facebook_ad(raw_ad)
                # Sauvegarder...

            # Scraper TikTok (500 ads)
            tt_ads = await scraper.scrape_tiktok_ads(max_pages=50)
            for raw_ad in tt_ads:
                normalized = scraper.normalize_tiktok_ad(raw_ad)
                # Sauvegarder...

            await db.commit()

        logger.info("Scraping mensuel terminé avec succès")

    except Exception as e:
        logger.error(f"Erreur scraping mensuel: {str(e)}")

def start_scheduler():
    """Démarre le scheduler avec toutes les tâches planifiées"""

    # Scraping mensuel: 1er du mois à 02:00
    scheduler.add_job(
        monthly_scraping_job,
        trigger=CronTrigger(day=1, hour=2, minute=0),
        id="monthly_scraping",
        name="Scraping mensuel automatique",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler démarré - Tâches planifiées actives")
```

---

<a name="module-2"></a>

## 5. MODULE 2: SCORING ET SÉLECTION DES PRODUITS

### 5.1 Critères de sélection

Le système doit identifier automatiquement les 5 meilleurs produits selon:

**Critères d'exclusion (filtres):**

- ❌ Électronique complexe
- ❌ Cosmétiques à risque
- ❌ Produits techniques
- ❌ Aliments / compléments
- ❌ Produits nécessitant certifications

**Critères de priorité:**

- ✅ Maison & déco (problème→solution)
- ✅ Accessoires pratiques quotidiens
- ✅ Mode / vêtements simples
- ✅ Produits visuellement impressionnants
- ✅ Sport / bien-être simple
- ✅ Produits pour animaux

**Métriques d'engagement:**

- Likes (poids: 0.2)
- Commentaires (poids: 0.8)
- Partages (poids: 1.2)
- Vues / impressions
- Durée de diffusion de l'ad
- Multi-posting (publié par plusieurs pages)

### 5.2 Formule de scoring

```python
score = (
    0.2 * normalized_likes +
    0.8 * normalized_comments +
    1.2 * normalized_shares +
    20 * is_problem_solution +
    20 * is_simple_category +
    10 * multi_posting_bonus +
    15 * recency_score
)
```

### 5.3 Code - Service de Scoring

**Fichier:** `backend/app/services/scoring_service.py`

```python
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.ads import ScrapedAd, ProductScore
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)

class ScoringService:

    # Catégories à exclure
    EXCLUDED_CATEGORIES = [
        "electronic", "electronics", "tech", "smartphone",
        "cosmetic", "makeup", "skincare", "beauty",
        "supplement", "vitamin", "food", "snack",
        "certification", "license", "medical"
    ]

    # Catégories prioritaires
    PRIORITY_CATEGORIES = [
        "home", "decor", "kitchen", "organization",
        "accessory", "gadget", "tool",
        "clothing", "fashion", "apparel",
        "sport", "fitness", "yoga",
        "pet", "dog", "cat", "animal"
    ]

    # Mots-clés "problème→solution"
    PROBLEM_SOLUTION_KEYWORDS = [
        "solve", "fix", "easy", "simple", "no more",
        "stop", "prevent", "avoid", "never again",
        "finally", "instant", "quick", "fast",
        "revolutionary", "innovative", "game changer"
    ]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_scores_for_all_ads(self) -> List[Dict[str, Any]]:
        """
        Calcule le score pour toutes les ads non scorées
        Retourne la liste des 5 meilleurs produits
        """
        logger.info("Démarrage du calcul des scores")

        # Récupérer toutes les ads scraped
        result = await self.db.execute(
            select(ScrapedAd).where(ScrapedAd.scored == False)
        )
        ads = result.scalars().all()

        if not ads:
            logger.warning("Aucune ad à scorer")
            return []

        logger.info(f"Calcul des scores pour {len(ads)} ads")

        # Calculer statistiques globales pour normalisation
        all_likes = [ad.likes or 0 for ad in ads]
        all_comments = [ad.comments or 0 for ad in ads]
        all_shares = [ad.shares or 0 for ad in ads]
        all_views = [ad.views or ad.impressions_upper_bound or 1 for ad in ads]

        max_likes = max(all_likes) or 1
        max_comments = max(all_comments) or 1
        max_shares = max(all_shares) or 1
        max_views = max(all_views) or 1

        scored_ads = []

        for ad in ads:
            # Vérifier exclusions
            if self._is_excluded_category(ad):
                continue

            # Calculer les composantes du score
            norm_likes = (ad.likes or 0) / max_likes
            norm_comments = (ad.comments or 0) / max_comments
            norm_shares = (ad.shares or 0) / max_shares
            norm_engagement = (
                norm_likes * 0.2 +
                norm_comments * 0.8 +
                norm_shares * 1.2
            )

            is_priority = self._is_priority_category(ad)
            is_problem_solution = self._is_problem_solution(ad)
            multi_posting = self._calculate_multi_posting_bonus(ad)
            recency = self._calculate_recency_score(ad)

            # Score final
            final_score = (
                norm_engagement * 50 +
                (20 if is_problem_solution else 0) +
                (20 if is_priority else 0) +
                multi_posting +
                recency
            )

            # Sauvegarder le score
            product_score = ProductScore(
                ad_id=ad.id,
                score=final_score,
                engagement_score=norm_engagement * 50,
                problem_solution_bonus=20 if is_problem_solution else 0,
                category_bonus=20 if is_priority else 0,
                multi_posting_bonus=multi_posting,
                recency_score=recency,
                calculated_at=datetime.utcnow()
            )

            self.db.add(product_score)
            ad.scored = True

            scored_ads.append({
                "ad_id": ad.id,
                "platform": ad.platform,
                "score": final_score,
                "ad_url": ad.ad_snapshot_url or ad.video_url
            })

        await self.db.commit()

        # Trier par score décroissant et retourner top 5
        scored_ads.sort(key=lambda x: x["score"], reverse=True)
        top_5 = scored_ads[:5]

        logger.info(f"Top 5 produits identifiés avec scores: {[a['score'] for a in top_5]}")

        return top_5

    def _is_excluded_category(self, ad: ScrapedAd) -> bool:
        """Vérifie si l'ad appartient à une catégorie exclue"""
        text = (ad.ad_creative_bodies or ad.caption or "").lower()
        return any(keyword in text for keyword in self.EXCLUDED_CATEGORIES)

    def _is_priority_category(self, ad: ScrapedAd) -> bool:
        """Vérifie si l'ad appartient à une catégorie prioritaire"""
        text = (ad.ad_creative_bodies or ad.caption or "").lower()
        return any(keyword in text for keyword in self.PRIORITY_CATEGORIES)

    def _is_problem_solution(self, ad: ScrapedAd) -> bool:
        """Détecte si l'ad présente un produit problème→solution"""
        text = (ad.ad_creative_bodies or ad.caption or "").lower()
        return any(keyword in text for keyword in self.PROBLEM_SOLUTION_KEYWORDS)

    def _calculate_multi_posting_bonus(self, ad: ScrapedAd) -> float:
        """Bonus si le produit est posté par plusieurs pages (TikTok uniquement pour l'instant)"""
        # Pour l'instant retourne 0, à implémenter avec détection de duplicates
        return 0.0

    def _calculate_recency_score(self, ad: ScrapedAd) -> float:
        """Calcule un score de récence (ads récentes = meilleur score)"""
        start_date = ad.ad_delivery_start_time or ad.first_shown_date
        if not start_date:
            return 0.0

        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))

        days_since = (datetime.utcnow() - start_date).days

        # Décroissance exponentielle: produits récents = score élevé
        import math
        return 15 * math.exp(-days_since / 30)
```

### 5.4 Endpoint API de scoring

**Fichier:** `backend/app/api/routes/scoring.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scoring_service import ScoringService
from app.database import get_db
from typing import List, Dict, Any

router = APIRouter(prefix="/scoring", tags=["scoring"])

@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_scores(db: AsyncSession = Depends(get_db)):
    """
    Lance le calcul des scores pour toutes les ads non scorées
    Retourne les 5 meilleurs produits identifiés
    """
    scoring_service = ScoringService(db)

    try:
        top_5 = await scoring_service.calculate_scores_for_all_ads()

        if not top_5:
            raise HTTPException(
                status_code=404,
                detail="Aucun produit trouvé après scoring"
            )

        return {
            "status": "success",
            "top_5_products": top_5,
            "message": f"{len(top_5)} produits sélectionnés"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-products", response_model=List[Dict[str, Any]])
async def get_top_products(
    limit: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """Récupère les N meilleurs produits déjà scorés"""
    from sqlalchemy import select, desc
    from app.models.ads import ProductScore, ScrapedAd

    result = await db.execute(
        select(ProductScore, ScrapedAd)
        .join(ScrapedAd, ProductScore.ad_id == ScrapedAd.id)
        .order_by(desc(ProductScore.score))
        .limit(limit)
    )

    products = []
    for score, ad in result:
        products.append({
            "product_id": ad.id,
            "platform": ad.platform,
            "score": score.score,
            "ad_url": ad.ad_snapshot_url or ad.video_url,
            "page_name": ad.page_name or ad.advertiser_name,
            "caption": ad.ad_creative_bodies or ad.caption
        })

    return products
```

---

<a name="module-3"></a>

## 6. MODULE 3: GÉNÉRATION DES CRÉATIVES

### 6.1 Intégration Creatify API

Creatify transforme automatiquement une URL produit ou des images en vidéos publicitaires de qualité professionnelle.

**API Endpoint:** `https://api.creatify.ai/api/video/generate`  
**Documentation:** https://docs.creatify.ai/api-reference/generate-video

### 6.2 Configuration Creatify

**Obtenir les credentials:**

1. Créer un compte sur https://creatify.ai
2. Aller dans Settings > API
3. Générer X-API-ID et X-API-KEY
4. Choisir un plan (Starter: $39/mois, Pro: $99/mois)

### 6.3 Types de vidéos à générer

Pour chaque produit du Top 5, générer **4 créatives:**

1. **UGC Style** (User Generated Content)

   - Format: verticale 9:16
   - Durée: 15-30 secondes
   - Style: naturel, authentique

2. **Problem→Solution**

   - Format: carré 1:1 ou 16:9
   - Durée: 20-45 secondes
   - Structure: Problème → Produit → Résultat

3. **Short Hook**

   - Format: verticale 9:16
   - Durée: 6-10 secondes
   - Focus: attention rapide

4. **Carousel/Showcase**
   - Format: carré 1:1
   - Durée: 30-60 secondes
   - Multi-angles du produit

### 6.4 Code - Service Creatify

**Fichier:** `backend/app/services/creatify_service.py`

```python
import httpx
import os
from typing import List, Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class CreatifyService:
    BASE_URL = "https://api.creatify.ai/api"

    def __init__(self):
        self.api_id = os.getenv("CREATIFY_API_ID")
        self.api_key = os.getenv("CREATIFY_API_KEY")
        self.headers = {
            "X-API-ID": self.api_id,
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    async def generate_video_from_url(
        self,
        product_url: str,
        video_type: str = "ugc",
        voice_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Génère une vidéo à partir d'une URL produit

        Paramètres:
        - product_url: URL de la page produit
        - video_type: "ugc", "problem_solution", "short_hook", "carousel"
        - voice_id: ID de la voix (optionnel, Creatify choisit par défaut)

        Retourne: Dict avec video_id, status, estimated_time
        """

        video_configs = {
            "ugc": {
                "aspect_ratio": "9:16",
                "duration": "20-30",
                "style": "ugc",
                "include_captions": True
            },
            "problem_solution": {
                "aspect_ratio": "1:1",
                "duration": "30-45",
                "style": "professional",
                "structure": "problem_solution"
            },
            "short_hook": {
                "aspect_ratio": "9:16",
                "duration": "6-10",
                "style": "fast_paced",
                "hook_focused": True
            },
            "carousel": {
                "aspect_ratio": "1:1",
                "duration": "30-60",
                "style": "showcase",
                "multi_angle": True
            }
        }

        config = video_configs.get(video_type, video_configs["ugc"])

        payload = {
            "url": product_url,
            "aspect_ratio": config["aspect_ratio"],
            "duration_range": config["duration"],
            "video_style": config["style"],
            "voice_id": voice_id,
            "include_captions": config.get("include_captions", False),
            "ai_avatar": True,  # Utiliser un avatar IA
            "music_enabled": True
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/video/generate",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Vidéo {video_type} générée - ID: {data.get('video_id')}")
                return data

        except httpx.HTTPError as e:
            logger.error(f"Erreur Creatify API: {str(e)}")
            raise

    async def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """
        Vérifie le statut de génération d'une vidéo

        Statuts possibles: "queued", "processing", "completed", "failed"
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/video/{video_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération statut vidéo: {str(e)}")
            raise

    async def download_video(self, video_id: str, save_path: str) -> str:
        """
        Télécharge une vidéo terminée

        Retourne: chemin du fichier sauvegardé
        """
        # D'abord récupérer le statut pour obtenir l'URL de téléchargement
        status_data = await self.get_video_status(video_id)

        if status_data.get("status") != "completed":
            raise ValueError(f"Vidéo pas encore prête: {status_data.get('status')}")

        download_url = status_data.get("download_url")
        if not download_url:
            raise ValueError("URL de téléchargement introuvable")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(download_url)
                response.raise_for_status()

                # Sauvegarder le fichier
                with open(save_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Vidéo téléchargée: {save_path}")
                return save_path

        except httpx.HTTPError as e:
            logger.error(f"Erreur téléchargement vidéo: {str(e)}")
            raise

    async def generate_all_creatives_for_product(
        self,
        product_url: str,
        product_id: int
    ) -> List[Dict[str, Any]]:
        """
        Génère les 4 types de créatives pour un produit

        Retourne: Liste des infos des vidéos générées
        """
        video_types = ["ugc", "problem_solution", "short_hook", "carousel"]

        tasks = []
        for vtype in video_types:
            task = self.generate_video_from_url(product_url, vtype)
            tasks.append(task)

        # Lancer en parallèle
        results = await asyncio.gather(*tasks, return_exceptions=True)

        creatives = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Erreur génération {video_types[i]}: {str(result)}")
                continue

            creatives.append({
                "product_id": product_id,
                "video_id": result.get("video_id"),
                "video_type": video_types[i],
                "status": result.get("status"),
                "estimated_completion": result.get("estimated_time")
            })

        return creatives
```

### 6.5 Endpoint API créatives

**Fichier:** `backend/app/api/routes/creatives.py`

```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.creatify_service import CreatifyService
from app.database import get_db
from app.models.ads import ScrapedAd, Creative
from typing import List, Dict, Any
import logging

router = APIRouter(prefix="/creatives", tags=["creatives"])
logger = logging.getLogger(__name__)

@router.post("/generate/{product_id}", response_model=Dict[str, Any])
async def generate_creatives_for_product(
    product_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance la génération des 4 créatives pour un produit
    """
    # Récupérer le produit
    from sqlalchemy import select
    result = await db.execute(
        select(ScrapedAd).where(ScrapedAd.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    product_url = product.ad_creative_link_url or product.video_url
    if not product_url:
        raise HTTPException(
            status_code=400,
            detail="Aucune URL produit disponible"
        )

    async def generate_task():
        try:
            creatify = CreatifyService()
            creatives_data = await creatify.generate_all_creatives_for_product(
                product_url,
                product_id
            )

            # Sauvegarder en BDD
            for creative_data in creatives_data:
                creative = Creative(
                    product_id=product_id,
                    video_id=creative_data["video_id"],
                    video_type=creative_data["video_type"],
                    status=creative_data["status"]
                )
                db.add(creative)

            await db.commit()
            logger.info(f"{len(creatives_data)} créatives générées pour produit {product_id}")

        except Exception as e:
            logger.error(f"Erreur génération créatives: {str(e)}")

    background_tasks.add_task(generate_task)

    return {
        "status": "started",
        "message": f"Génération de 4 créatives lancée pour le produit {product_id}",
        "product_url": product_url
    }

@router.get("/status/{product_id}", response_model=List[Dict[str, Any]])
async def get_creatives_status(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Récupère le statut de toutes les créatives d'un produit"""
    from sqlalchemy import select

    result = await db.execute(
        select(Creative).where(Creative.product_id == product_id)
    )
    creatives = result.scalars().all()

    if not creatives:
        raise HTTPException(
            status_code=404,
            detail="Aucune créative trouvée pour ce produit"
        )

    creatify = CreatifyService()
    status_list = []

    for creative in creatives:
        try:
            status_data = await creatify.get_video_status(creative.video_id)
            status_list.append({
                "creative_id": creative.id,
                "video_type": creative.video_type,
                "status": status_data.get("status"),
                "progress": status_data.get("progress", 0),
                "download_url": status_data.get("download_url")
            })
        except Exception as e:
            logger.error(f"Erreur statut créative {creative.id}: {str(e)}")

    return status_list
```

---

<a name="module-4"></a>

## 7. MODULE 4: LANDING PAGES AUTOMATIQUES

### 7.1 Architecture Next.js

Utilisation de **Next.js 15 App Router** avec génération statique (ISR - Incremental Static Regeneration).

**Structure des dossiers:**

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── p/
│   │   │   └── [slug]/
│   │   │       └── page.tsx          # Landing page dynamique
│   │   └── api/
│   │       └── orders/
│   │           └── route.ts          # API route pour commandes
│   ├── components/
│   │   ├── ProductHero.tsx
│   │   ├── ProductFeatures.tsx
│   │   ├── OrderForm.tsx
│   │   └── WhatsAppButton.tsx
│   ├── lib/
│   │   ├── product-api.ts
│   │   └── whatsapp.ts
│   └── types/
│       └── product.ts
├── public/
│   └── products/                      # Vidéos/images produits
└── tailwind.config.ts
```

### 7.2 Configuration Next.js

**Fichier:** `frontend/next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "your-s3-bucket.s3.amazonaws.com",
      },
    ],
  },
  experimental: {
    serverActions: true,
  },
  // ISR: régénérer les pages toutes les heures
  revalidate: 3600,
};

module.exports = nextConfig;
```

### 7.3 Page produit dynamique

**Fichier:** `frontend/src/app/p/[slug]/page.tsx`

```typescript
import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import ProductHero from '@/components/ProductHero'
import ProductFeatures from '@/components/ProductFeatures'
import OrderForm from '@/components/OrderForm'
import { getProductBySlug } from '@/lib/product-api'

interface ProductPageProps {
  params: {
    slug: string
  }
}

// Génération statique des pages au build
export async function generateStaticParams() {
  // Récupérer la liste des produits depuis l'API
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/products/active`)
  const products = await response.json()

  return products.map((product: any) => ({
    slug: product.slug,
  }))
}

// Métadonnées dynamiques pour SEO
export async function generateMetadata(
  { params }: ProductPageProps
): Promise<Metadata> {
  const product = await getProductBySlug(params.slug)

  if (!product) {
    return {
      title: 'Produit introuvable',
    }
  }

  return {
    title: `${product.name} - Commandez maintenant`,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      images: [product.mainImage],
    },
  }
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await getProductBySlug(params.slug)

  if (!product) {
    notFound()
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero avec vidéo */}
      <ProductHero
        videoUrl={product.videos.ugc}
        productName={product.name}
        tagline={product.tagline}
      />

      {/* Caractéristiques */}
      <ProductFeatures
        features={product.features}
        beforeAfterImages={product.beforeAfter}
      />

      {/* Formulaire de commande */}
      <section className="py-16 px-4">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">
            Commander maintenant
          </h2>
          <OrderForm
            productId={product.id}
            productName={product.name}
          />
        </div>
      </section>

      {/* Pixel tracking Meta & TikTok */}
      <script
        dangerouslySetInnerHTML={{
          __html: `
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '${process.env.NEXT_PUBLIC_META_PIXEL_ID}');
            fbq('track', 'PageView');
            fbq('track', 'ViewContent', {
              content_name: '${product.name}',
              content_ids: ['${product.id}'],
              content_type: 'product',
            });
          `,
        }}
      />
    </main>
  )
}

// ISR: revalider la page toutes les heures
export const revalidate = 3600
```

### 7.4 Composant formulaire de commande

**Fichier:** `frontend/src/components/OrderForm.tsx`

```typescript
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

const orderSchema = z.object({
  fullName: z.string().min(2, 'Nom complet requis'),
  phone: z.string().regex(/^[+]?[0-9]{10,15}$/, 'Numéro de téléphone invalide'),
  address: z.string().min(10, 'Adresse complète requise'),
  city: z.string().min(2, 'Ville requise'),
  quantity: z.number().min(1).max(10),
})

type OrderFormData = z.infer<typeof orderSchema>

interface OrderFormProps {
  productId: number
  productName: string
}

export default function OrderForm({ productId, productName }: OrderFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<OrderFormData>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      quantity: 1,
    },
  })

  const onSubmit = async (data: OrderFormData) => {
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...data,
          productId,
          productName,
        }),
      })

      if (!response.ok) {
        throw new Error('Erreur lors de la commande')
      }

      const result = await response.json()

      // Tracking Meta Pixel
      if (typeof window !== 'undefined' && (window as any).fbq) {
        (window as any).fbq('track', 'Lead', {
          content_name: productName,
          value: result.estimatedValue,
          currency: 'EUR',
        })
      }

      setSubmitSuccess(true)
      reset()

      // Rediriger vers WhatsApp après 2 secondes
      setTimeout(() => {
        const whatsappUrl = `https://wa.me/${process.env.NEXT_PUBLIC_WHATSAPP_NUMBER}?text=${encodeURIComponent(
          `Bonjour, je viens de commander ${productName}. Référence: ${result.orderId}`
        )}`
        window.open(whatsappUrl, '_blank')
      }, 2000)

    } catch (error) {
      console.error('Erreur commande:', error)
      alert('Une erreur est survenue. Veuillez réessayer.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (submitSuccess) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-8 text-center">
        <div className="text-6xl mb-4">✅</div>
        <h3 className="text-2xl font-bold text-green-800 mb-2">
          Commande enregistrée !
        </h3>
        <p className="text-green-700">
          Nous vous contactons sur WhatsApp dans quelques instants...
        </p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Nom complet *
        </label>
        <input
          {...register('fullName')}
          type="text"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Jean Dupont"
        />
        {errors.fullName && (
          <p className="mt-1 text-sm text-red-600">{errors.fullName.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Numéro WhatsApp *
        </label>
        <input
          {...register('phone')}
          type="tel"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="+237 6 XX XX XX XX"
        />
        {errors.phone && (
          <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Adresse de livraison *
        </label>
        <input
          {...register('address')}
          type="text"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="123 Rue Example, Quartier"
        />
        {errors.address && (
          <p className="mt-1 text-sm text-red-600">{errors.address.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Ville *
        </label>
        <input
          {...register('city')}
          type="text"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Yaoundé"
        />
        {errors.city && (
          <p className="mt-1 text-sm text-red-600">{errors.city.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Quantité
        </label>
        <select
          {...register('quantity', { valueAsNumber: true })}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {[1, 2, 3, 4, 5].map((num) => (
            <option key={num} value={num}>
              {num}
            </option>
          ))}
        </select>
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Envoi en cours...' : 'Commander maintenant'}
      </button>

      <p className="text-sm text-gray-600 text-center">
        Paiement à la livraison uniquement
      </p>
    </form>
  )
}
```

---

<a name="module-5"></a>

## 8. MODULE 5: LANCEMENT AUTOMATIQUE DES CAMPAGNES

### 8.1 Configuration Meta Ads API

Meta utilise désormais l'API Marketing v22+ avec focus sur Advantage+ et simplification des objectifs de campagne.

**Étapes de configuration:**

1. **Créer un compte Meta Developer**

   - Aller sur https://developers.facebook.com
   - Créer une app de type "Business"
   - Activer "Marketing API" dans les produits

2. **Obtenir les credentials**

   - App ID
   - App Secret
   - Access Token (ads_management, ads_read permissions)

3. **Vérifier le Business Manager**
   - Compte publicitaire actif
   - Business Manager vérifié
   - Permissions API accordées

### 8.2 Service de création de campagnes Meta

**Fichier:** `backend/app/services/meta_ads_service.py`

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
import os
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class MetaAdsService:
    def __init__(self):
        self.app_id = os.getenv("META_APP_ID")
        self.app_secret = os.getenv("META_APP_SECRET")
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("META_AD_ACCOUNT_ID")

        # Initialiser l'API Facebook
        FacebookAdsApi.init(
            self.app_id,
            self.app_secret,
            self.access_token
        )

        self.ad_account = AdAccount(f"act_{self.ad_account_id}")

    async def create_campaign(
        self,
        campaign_name: str,
        daily_budget: int = 5000,  # En centimes (50€)
        objective: str = "OUTCOME_TRAFFIC"
    ) -> Dict[str, Any]:
        """
        Crée une campagne Meta Ads

        Objectifs disponibles:
        - OUTCOME_TRAFFIC (trafic vers site/WhatsApp)
        - OUTCOME_SALES (conversions)
        - OUTCOME_AWARENESS (notoriété)
        - OUTCOME_ENGAGEMENT (engagement)
        - OUTCOME_LEADS (génération de leads)
        """

        params = {
            Campaign.Field.name: campaign_name,
            Campaign.Field.objective: objective,
            Campaign.Field.status: Campaign.Status.paused,
            Campaign.Field.special_ad_categories: [],
            Campaign.Field.daily_budget: daily_budget
        }

        try:
            campaign = self.ad_account.create_campaign(params=params)

            logger.info(f"Campagne créée - ID: {campaign['id']}, Nom: {campaign_name}")

            return {
                "campaign_id": campaign['id'],
                "name": campaign_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création campagne: {str(e)}")
            raise

    async def create_adset(
        self,
        campaign_id: str,
        adset_name: str,
        daily_budget: int = 2000,  # 20€
        targeting: Dict[str, Any] = None,
        optimization_goal: str = "LINK_CLICKS"
    ) -> Dict[str, Any]:
        """
        Crée un ad set dans une campagne

        Optimization goals:
        - LINK_CLICKS (clics sur lien)
        - LANDING_PAGE_VIEWS (vues landing page)
        - IMPRESSIONS (impressions)
        - REACH (portée)
        """

        # Targeting par défaut si non spécifié
        if not targeting:
            targeting = {
                'geo_locations': {
                    'countries': ['FR', 'CM']  # France, Cameroun
                },
                'age_min': 18,
                'age_max': 65,
            }

        params = {
            AdSet.Field.name: adset_name,
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.daily_budget: daily_budget,
            AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
            AdSet.Field.optimization_goal: optimization_goal,
            AdSet.Field.bid_strategy: AdSet.BidStrategy.lowest_cost_without_cap,
            AdSet.Field.targeting: targeting,
            AdSet.Field.status: AdSet.Status.paused,
            # Placements automatiques
            AdSet.Field.promoted_object: {
                'pixel_id': os.getenv("META_PIXEL_ID")
            }
        }

        try:
            adset = AdSet(parent_id=self.ad_account_id).api_create(params=params)

            logger.info(f"AdSet créé - ID: {adset['id']}, Nom: {adset_name}")

            return {
                "adset_id": adset['id'],
                "name": adset_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création adset: {str(e)}")
            raise

    async def upload_video_creative(
        self,
        video_path: str,
        video_title: str
    ) -> str:
        """Upload une vidéo et retourne son ID"""

        try:
            video = AdVideo(parent_id=self.ad_account_id)
            video[AdVideo.Field.filepath] = video_path
            video[AdVideo.Field.name] = video_title

            video.api_create()
            video.waitUntilEncodingReady()

            logger.info(f"Vidéo uploadée - ID: {video['id']}")

            return video['id']

        except Exception as e:
            logger.error(f"Erreur upload vidéo: {str(e)}")
            raise

    async def create_video_ad(
        self,
        adset_id: str,
        ad_name: str,
        video_id: str,
        page_id: str,
        message: str,
        link: str,
        call_to_action: str = "LEARN_MORE"
    ) -> Dict[str, Any]:
        """
        Crée une publicité vidéo

        Call to actions possibles:
        - LEARN_MORE, SHOP_NOW, SIGN_UP, CONTACT_US,
        - CALL_NOW, MESSAGE_PAGE, WHATSAPP_MESSAGE
        """

        # Créer l'AdCreative
        creative = AdCreative(parent_id=self.ad_account_id)
        creative[AdCreative.Field.name] = f"{ad_name} - Creative"
        creative[AdCreative.Field.object_story_spec] = {
            'page_id': page_id,
            'video_data': {
                'video_id': video_id,
                'message': message,
                'call_to_action': {
                    'type': call_to_action,
                    'value': {
                        'link': link
                    }
                }
            }
        }

        try:
            creative.api_create()

            # Créer l'Ad
            ad = Ad(parent_id=self.ad_account_id)
            ad[Ad.Field.name] = ad_name
            ad[Ad.Field.adset_id] = adset_id
            ad[Ad.Field.creative] = {'creative_id': creative['id']}
            ad[Ad.Field.status] = Ad.Status.paused

            ad.api_create()

            logger.info(f"Ad créée - ID: {ad['id']}, Nom: {ad_name}")

            return {
                "ad_id": ad['id'],
                "creative_id": creative['id'],
                "name": ad_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création ad: {str(e)}")
            raise

    async def activate_campaign(self, campaign_id: str) -> bool:
        """Active une campagne (passe de PAUSED à ACTIVE)"""

        try:
            campaign = Campaign(campaign_id)
            campaign.api_update(params={
                Campaign.Field.status: Campaign.Status.active
            })

            logger.info(f"Campagne {campaign_id} activée")
            return True

        except Exception as e:
            logger.error(f"Erreur activation campagne: {str(e)}")
            return False

    async def create_complete_campaign_for_product(
        self,
        product_id: int,
        product_name: str,
        landing_page_url: str,
        video_paths: List[str],
        daily_budget: int = 5000
    ) -> Dict[str, Any]:
        """
        Workflow complet: crée campagne + adsets + ads pour un produit

        Paramètres:
        - product_id: ID du produit en BDD
        - product_name: Nom du produit
        - landing_page_url: URL de la landing page
        - video_paths: Liste des chemins des vidéos créatives
        - daily_budget: Budget quotidien total en centimes

        Retourne: Dict avec IDs de campagne, adsets, ads
        """

        # 1. Créer la campagne
        campaign_data = await self.create_campaign(
            campaign_name=f"Campagne - {product_name}",
            daily_budget=daily_budget,
            objective="OUTCOME_TRAFFIC"
        )

        campaign_id = campaign_data["campaign_id"]

        # 2. Créer un adset par créative (budget partagé)
        budget_per_adset = daily_budget // len(video_paths)

        ads_created = []

        for idx, video_path in enumerate(video_paths):
            video_type = video_path.split("_")[-1].split(".")[0]  # Ex: ugc, problem_solution

            # Créer adset
            adset_data = await self.create_adset(
                campaign_id=campaign_id,
                adset_name=f"{product_name} - {video_type}",
                daily_budget=budget_per_adset,
                optimization_goal="LINK_CLICKS"
            )

            # Upload vidéo
            video_id = await self.upload_video_creative(
                video_path=video_path,
                video_title=f"{product_name} - {video_type}"
            )

            # Créer ad
            ad_data = await self.create_video_ad(
                adset_id=adset_data["adset_id"],
                ad_name=f"{product_name} - Ad {idx+1}",
                video_id=video_id,
                page_id=os.getenv("META_PAGE_ID"),
                message=f"Découvrez {product_name} - Commandez maintenant!",
                link=landing_page_url,
                call_to_action="LEARN_MORE"
            )

            ads_created.append(ad_data)

        logger.info(f"Campagne complète créée pour {product_name} - {len(ads_created)} ads")

        return {
            "campaign_id": campaign_id,
            "adsets_count": len(video_paths),
            "ads": ads_created,
            "status": "ready_to_activate"
        }
```

### 8.3 Service TikTok Ads

**Fichier:** `backend/app/services/tiktok_ads_service.py`

```python
import httpx
import os
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TikTokAdsService:
    BASE_URL = "https://business-api.tiktok.com/open_api/v1.3"

    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        self.advertiser_id = os.getenv("TIKTOK_ADVERTISER_ID")

        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    async def create_campaign(
        self,
        campaign_name: str,
        budget: float = 50.0,  # En dollars
        objective: str = "TRAFFIC"
    ) -> Dict[str, Any]:
        """
        Crée une campagne TikTok Ads

        Objectifs: REACH, TRAFFIC, VIDEO_VIEWS, LEAD_GENERATION,
                   APP_PROMOTION, WEB_CONVERSIONS
        """

        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_name": campaign_name,
            "objective_type": objective,
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": budget,
            "operation_status": "DISABLE"  # Créer en pause
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/campaign/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise Exception(f"TikTok API Error: {data.get('message')}")

                campaign_id = data["data"]["campaign_id"]

                logger.info(f"Campagne TikTok créée - ID: {campaign_id}")

                return {
                    "campaign_id": campaign_id,
                    "name": campaign_name,
                    "status": "created"
                }

        except Exception as e:
            logger.error(f"Erreur création campagne TikTok: {str(e)}")
            raise

    async def create_ad_group(
        self,
        campaign_id: str,
        ad_group_name: str,
        budget: float = 20.0,
        targeting: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Crée un Ad Group (équivalent AdSet sur Meta)"""

        if not targeting:
            targeting = {
                "location_ids": ["6252001"],  # USA
                "age_groups": ["AGE_25_34", "AGE_35_44"],
                "gender": "GENDER_UNLIMITED"
            }

        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_id": campaign_id,
            "adgroup_name": ad_group_name,
            "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": budget,
            "billing_event": "CPC",
            "optimization_goal": "CLICK",
            "schedule_type": "SCHEDULE_START_END",
            "operation_status": "DISABLE",
            **targeting
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/adgroup/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise Exception(f"TikTok API Error: {data.get('message')}")

                adgroup_id = data["data"]["adgroup_id"]

                logger.info(f"Ad Group TikTok créé - ID: {adgroup_id}")

                return {
                    "adgroup_id": adgroup_id,
                    "name": ad_group_name
                }

        except Exception as e:
            logger.error(f"Erreur création ad group: {str(e)}")
            raise

    async def upload_video(
        self,
        video_path: str,
        video_title: str
    ) -> str:
        """Upload une vidéo et retourne son video_id"""

        try:
            # Étape 1: Initialiser l'upload
            init_payload = {
                "advertiser_id": self.advertiser_id,
                "upload_type": "UPLOAD_BY_FILE",
                "video_file_name": video_title,
                "video_signature": ""
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                init_response = await client.post(
                    f"{self.BASE_URL}/file/video/ad/upload/",
                    headers=self.headers,
                    json=init_payload
                )
                init_data = init_response.json()

                if init_data.get("code") != 0:
                    raise Exception(f"TikTok Upload Init Error: {init_data.get('message')}")

                # Étape 2: Upload fichier
                upload_url = init_data["data"]["upload_url"]

                with open(video_path, 'rb') as video_file:
                    files = {'video': video_file}
                    upload_response = await client.post(upload_url, files=files)

                video_id = init_data["data"]["video_id"]

                logger.info(f"Vidéo TikTok uploadée - ID: {video_id}")

                return video_id

        except Exception as e:
            logger.error(f"Erreur upload vidéo TikTok: {str(e)}")
            raise

    async def create_ad(
        self,
        adgroup_id: str,
        ad_name: str,
        video_id: str,
        landing_page_url: str,
        ad_text: str
    ) -> Dict[str, Any]:
        """Crée une publicité TikTok"""

        payload = {
            "advertiser_id": self.advertiser_id,
            "adgroup_id": adgroup_id,
            "ad_name": ad_name,
            "ad_format": "SINGLE_VIDEO",
            "ad_text": ad_text,
            "video_id": video_id,
            "landing_page_url": landing_page_url,
            "call_to_action": "LEARN_MORE",
            "operation_status": "DISABLE"
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/ad/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise Exception(f"TikTok API Error: {data.get('message')}")

                ad_id = data["data"]["ad_id"]

                logger.info(f"Ad TikTok créée - ID: {ad_id}")

                return {
                    "ad_id": ad_id,
                    "name": ad_name
                }

        except Exception as e:
            logger.error(f"Erreur création ad TikTok: {str(e)}")
            raise
```

### 8.4 Endpoint API - Lancement de campagnes

**Fichier:** `backend/app/api/routes/campaigns.py`

```python
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.meta_ads_service import MetaAdsService
from app.services.tiktok_ads_service import TikTokAdsService
from app.database import get_db
from app.models.ads import ScrapedAd, Campaign as CampaignModel
from typing import Dict, Any
import logging

router = APIRouter(prefix="/campaigns", tags=["campaigns"])
logger = logging.getLogger(__name__)

@router.post("/launch-for-product/{product_id}", response_model=Dict[str, Any])
async def launch_campaigns_for_product(
    product_id: int,
    platform: str = "both",  # "meta", "tiktok", "both"
    daily_budget: int = 5000,  # En centimes pour Meta
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance automatiquement les campagnes Meta et/ou TikTok pour un produit

    Workflow:
    1. Récupère le produit et ses créatives
    2. Upload les vidéos
    3. Crée campagne + adsets + ads
    4. Sauvegarde en BDD
    5. Active les campagnes
    """

    # Récupérer le produit
    from sqlalchemy import select
    from app.models.ads import Creative

    result = await db.execute(
        select(ScrapedAd).where(ScrapedAd.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # Récupérer les créatives
    creatives_result = await db.execute(
        select(Creative).where(
            Creative.product_id == product_id,
            Creative.status == "completed"
        )
    )
    creatives = creatives_result.scalars().all()

    if not creatives:
        raise HTTPException(
            status_code=400,
            detail="Aucune créative prête pour ce produit"
        )

    landing_page_url = f"{os.getenv('FRONTEND_URL')}/p/{product.slug}"
    video_paths = [c.local_path for c in creatives if c.local_path]

    campaigns_created = {}

    # Lancer Meta Ads
    if platform in ["meta", "both"]:
        try:
            meta_service = MetaAdsService()
            meta_campaign = await meta_service.create_complete_campaign_for_product(
                product_id=product_id,
                product_name=product.name,
                landing_page_url=landing_page_url,
                video_paths=video_paths,
                daily_budget=daily_budget
            )

            # Sauvegarder en BDD
            campaign_record = CampaignModel(
                product_id=product_id,
                platform="meta",
                campaign_id=meta_campaign["campaign_id"],
                campaign_name=f"Campagne - {product.name}",
                daily_budget=daily_budget,
                status="paused"
            )
            db.add(campaign_record)

            campaigns_created["meta"] = meta_campaign

            logger.info(f"Campagne Meta créée pour produit {product_id}")

        except Exception as e:
            logger.error(f"Erreur création campagne Meta: {str(e)}")
            campaigns_created["meta_error"] = str(e)

    # Lancer TikTok Ads
    if platform in ["tiktok", "both"]:
        try:
            tiktok_service = TikTokAdsService()

            # Créer campagne
            tt_campaign = await tiktok_service.create_campaign(
                campaign_name=f"Campagne - {product.name}",
                budget=daily_budget / 100,  # Convertir en dollars
                objective="TRAFFIC"
            )

            # Créer ad groups et ads
            ads_created = []
            budget_per_ad = (daily_budget / 100) / len(video_paths)

            for idx, video_path in enumerate(video_paths):
                # Upload vidéo
                video_id = await tiktok_service.upload_video(
                    video_path=video_path,
                    video_title=f"{product.name} - Video {idx+1}"
                )

                # Créer ad group
                ad_group = await tiktok_service.create_ad_group(
                    campaign_id=tt_campaign["campaign_id"],
                    ad_group_name=f"{product.name} - Group {idx+1}",
                    budget=budget_per_ad
                )

                # Créer ad
                ad = await tiktok_service.create_ad(
                    adgroup_id=ad_group["adgroup_id"],
                    ad_name=f"{product.name} - Ad {idx+1}",
                    video_id=video_id,
                    landing_page_url=landing_page_url,
                    ad_text=f"Découvrez {product.name}!"
                )

                ads_created.append(ad)

            # Sauvegarder en BDD
            campaign_record = CampaignModel(
                product_id=product_id,
                platform="tiktok",
                campaign_id=tt_campaign["campaign_id"],
                campaign_name=f"Campagne - {product.name}",
                daily_budget=daily_budget,
                status="paused"
            )
            db.add(campaign_record)

            campaigns_created["tiktok"] = {
                "campaign_id": tt_campaign["campaign_id"],
                "ads_count": len(ads_created)
            }

            logger.info(f"Campagne TikTok créée pour produit {product_id}")

        except Exception as e:
            logger.error(f"Erreur création campagne TikTok: {str(e)}")
            campaigns_created["tiktok_error"] = str(e)

    await db.commit()

    return {
        "status": "success",
        "product_id": product_id,
        "product_name": product.name,
        "campaigns": campaigns_created
    }

@router.post("/activate/{campaign_id}", response_model=Dict[str, Any])
async def activate_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Active une campagne créée (passe de PAUSED à ACTIVE)"""

    from sqlalchemy import select

    result = await db.execute(
        select(CampaignModel).where(CampaignModel.id == campaign_id)
    )
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne introuvable")

    success = False

    if campaign.platform == "meta":
        meta_service = MetaAdsService()
        success = await meta_service.activate_campaign(campaign.campaign_id)

    elif campaign.platform == "tiktok":
        # Implémenter activation TikTok
        pass

    if success:
        campaign.status = "active"
        await db.commit()

        return {
            "status": "activated",
            "campaign_id": campaign_id,
            "platform": campaign.platform
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'activation"
        )
```

---

<a name="module-6"></a>

## 9. MODULE 6: CHATBOT WHATSAPP AVEC IA

### 9.1 Configuration WhatsApp Business Cloud API

**Étapes:**

1. Créer un compte Meta Business
2. Aller sur developers.facebook.com > WhatsApp > Cloud API
3. Obtenir:
   - Phone Number ID
   - WhatsApp Business Account ID
   - Access Token (permanent)
4. Configurer webhook pour recevoir messages

**Documentation:** https://developers.facebook.com/docs/whatsapp/cloud-api

### 9.2 Service WhatsApp + Ollama

**Fichier:** `backend/app/services/whatsapp_service.py`

```python
import httpx
import os
from typing import Dict, Any
import logging
import subprocess

logger = logging.getLogger(__name__)

class WhatsAppService:
    BASE_URL = "https://graph.facebook.com/v22.0"

    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    async def send_message(
        self,
        to: str,  # Numéro destinataire format: 237XXXXXXXXX
        message: str
    ) -> bool:
        """Envoie un message WhatsApp"""

        url = f"{self.BASE_URL}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

                logger.info(f"Message envoyé à {to}")
                return True

        except Exception as e:
            logger.error(f"Erreur envoi WhatsApp: {str(e)}")
            return False

    async def generate_ai_response(
        self,
        user_message: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Génère une réponse avec Ollama (IA locale)

        Paramètres:
        - user_message: message du client
        - context: contexte additionnel (commande, produit, etc.)
        """

        system_prompt = """Tu es un assistant commercial pour une boutique de dropshipping.

Ton rôle:
- Répondre aux questions sur les produits
- Confirmer les commandes
- Fournir des informations de livraison
- Être courtois et professionnel

Règles:
- Réponds en français
- Sois concis (maximum 3 phrases)
- Si tu ne sais pas, oriente vers le service client
- Ne promets jamais de délais de livraison précis sans vérification
"""

        if context:
            system_prompt += f"\n\nContexte actuel:\n{context}"

        # Appel à Ollama en local
        try:
            result = subprocess.run(
                [
                    "ollama",
                    "run",
                    self.ollama_model,
                    f"{system_prompt}\n\nClient: {user_message}\n\nAssistant:"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            response = result.stdout.strip()

            logger.info(f"Réponse IA générée pour: {user_message[:50]}...")

            return response if response else "Je n'ai pas bien compris. Pouvez-vous reformuler?"

        except Exception as e:
            logger.error(f"Erreur Ollama: {str(e)}")
            return "Désolé, une erreur s'est produite. Un conseiller vous contactera rapidement."

    async def handle_incoming_message(
        self,
        from_number: str,
        message_text: str,
        db_session
    ) -> bool:
        """
        Traite un message entrant:
        1. Génère réponse IA
        2. Vérifie si commande existe
        3. Envoie réponse
        """

        # Vérifier si client a une commande en cours
        from sqlalchemy import select
        from app.models.orders import Order

        result = await db_session.execute(
            select(Order).where(Order.phone == from_number).order_by(Order.created_at.desc()).limit(1)
        )
        order = result.scalar_one_or_none()

        context = {}
        if order:
            context = {
                "order_id": order.id,
                "product_name": order.product_name,
                "status": order.status,
                "quantity": order.quantity
            }

        # Générer réponse IA
        ai_response = await self.generate_ai_response(message_text, context)

        # Envoyer réponse
        sent = await self.send_message(from_number, ai_response)

        return sent
```

### 9.3 Webhook WhatsApp

**Fichier:** `backend/app/api/routes/webhooks.py`

```python
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.whatsapp_service import WhatsAppService
from app.database import get_db
import logging

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)

@router.get("/whatsapp")
async def verify_whatsapp_webhook(request: Request):
    """Vérification du webhook par Meta (appelé une seule fois)"""

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "your_verify_token")

    if mode == "subscribe" and token == verify_token:
        logger.info("Webhook WhatsApp vérifié")
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/whatsapp")
async def handle_whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Réception des messages WhatsApp entrants
    Format de Meta: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples
    """

    try:
        body = await request.json()

        # Parser le webhook Meta
        if body.get("object") != "whatsapp_business_account":
            return {"status": "ignored"}

        entries = body.get("entry", [])

        for entry in entries:
            changes = entry.get("changes", [])

            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    from_number = message.get("from")
                    message_type = message.get("type")

                    if message_type == "text":
                        message_text = message.get("text", {}).get("body", "")

                        # Traiter le message avec l'IA
                        whatsapp_service = WhatsAppService()
                        await whatsapp_service.handle_incoming_message(
                            from_number,
                            message_text,
                            db
                        )

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Erreur traitement webhook WhatsApp: {str(e)}")
        return {"status": "error", "message": str(e)}
```

---

<a name="installation"></a>

## 10. INSTALLATION ET DÉPLOIEMENT

### 10.1 Prérequis système

- **OS:** Ubuntu 22.04 LTS (recommandé) ou macOS
- **Python:** 3.11+
- **Node.js:** 20+
- **PostgreSQL:** 16+
- **Redis:** 7+
- **Ollama:** Dernière version
- **Docker & Docker Compose:** Pour environnement complet

### 10.2 Installation pas à pas

**1. Cloner le repository (à créer)**

```bash
mkdir dropshipping-platform
cd dropshipping-platform

# Créer structure
mkdir -p backend frontend
```

**2. Installation Backend**

```bash
cd backend

# Créer environnement virtuel Python
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Créer fichier .env
cp .env.example .env
# Éditer .env avec vos credentials
```

**3. Installation Frontend**

```bash
cd ../frontend

# Installer dépendances
npm install

# Créer .env.local
cp .env.example .env.local
# Éditer .env.local
```

**4. Base de données**

```bash
# Démarrer PostgreSQL (via Docker)
docker run --name postgres-dropshipping \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=dropshipping \
  -p 5432:5432 \
  -d postgres:16-alpine

# Démarrer Redis
docker run --name redis-dropshipping \
  -p 6379:6379 \
  -d redis:7.4-alpine

# Appliquer migrations
cd backend
alembic upgrade head
```

**5. Installer Ollama**

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Télécharger modèle
ollama pull llama3.2:3b
```

**6. Lancer l'application**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Ollama
ollama serve
```

### 10.3 Docker Compose (Production)

**Fichier:** `docker-compose.yml`

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: dropshipping
      POSTGRES_USER: dropship_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dropship_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.4-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://dropship_user:${DB_PASSWORD}@postgres:5432/dropshipping
      REDIS_URL: redis://redis:6379/0
      APIFY_API_TOKEN: ${APIFY_API_TOKEN}
      CREATIFY_API_ID: ${CREATIFY_API_ID}
      CREATIFY_API_KEY: ${CREATIFY_API_KEY}
      META_APP_ID: ${META_APP_ID}
      META_APP_SECRET: ${META_APP_SECRET}
      META_ACCESS_TOKEN: ${META_ACCESS_TOKEN}
      TIKTOK_ACCESS_TOKEN: ${TIKTOK_ACCESS_TOKEN}
      WHATSAPP_ACCESS_TOKEN: ${WHATSAPP_ACCESS_TOKEN}
      OLLAMA_HOST: http://ollama:11434
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - media_files:/app/media

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
      NEXT_PUBLIC_WHATSAPP_NUMBER: ${WHATSAPP_NUMBER}
      NEXT_PUBLIC_META_PIXEL_ID: ${META_PIXEL_ID}
    ports:
      - "3000:3000"
    depends_on:
      - backend

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  postgres_data:
  redis_data:
  media_files:
  ollama_data:
```

### 10.4 Commandes de lancement

```bash
# Développement
docker-compose up -d

# Production avec build
docker-compose -f docker-compose.prod.yml up -d --build

# Vérifier logs
docker-compose logs -f backend

# Arrêter
docker-compose down
```

---

<a name="env-variables"></a>

## 11. VARIABLES D'ENVIRONNEMENT

### 11.1 Backend (.env)

```bash
# Base de données
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dropshipping
REDIS_URL=redis://localhost:6379/0

# Apify
APIFY_API_TOKEN=your_apify_token_here

# Creatify
CREATIFY_API_ID=your_api_id
CREATIFY_API_KEY=your_api_key

# Meta Ads
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_ACCESS_TOKEN=your_long_lived_token
META_AD_ACCOUNT_ID=123456789
META_PAGE_ID=your_page_id
META_PIXEL_ID=your_pixel_id

# TikTok Ads
TIKTOK_ACCESS_TOKEN=your_tiktok_token
TIKTOK_ADVERTISER_ID=your_advertiser_id

# WhatsApp
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=random_secret_string

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Application
SECRET_KEY=your_secret_key_here
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

### 11.2 Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WHATSAPP_NUMBER=237XXXXXXXXX
NEXT_PUBLIC_META_PIXEL_ID=your_pixel_id
NEXT_PUBLIC_TIKTOK_PIXEL_ID=your_tiktok_pixel
```

---

<a name="database"></a>

## 12. SCHÉMA DE BASE DE DONNÉES

### 12.1 Tables principales

**Fichier:** `backend/alembic/versions/001_initial.py`

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

def upgrade():
    # Table des ads scrapées
    op.create_table(
        'scraped_ads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('platform', sa.String(20), nullable=False),  # facebook, tiktok
        sa.Column('ad_id', sa.String(255), unique=True),
        sa.Column('ad_snapshot_url', sa.Text()),
        sa.Column('video_url', sa.Text()),
        sa.Column('page_name', sa.String(255)),
        sa.Column('advertiser_name', sa.String(255)),
        sa.Column('caption', sa.Text()),
        sa.Column('ad_creative_bodies', sa.Text()),
        sa.Column('likes', sa.Integer(), default=0),
        sa.Column('comments', sa.Integer(), default=0),
        sa.Column('shares', sa.Integer(), default=0),
        sa.Column('views', sa.Integer(), default=0),
        sa.Column('impressions_upper_bound', sa.Integer()),
        sa.Column('ad_delivery_start_time', sa.DateTime()),
        sa.Column('first_shown_date', sa.DateTime()),
        sa.Column('scraped_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('scored', sa.Boolean(), default=False),
        sa.Column('selected_for_campaign', sa.Boolean(), default=False),
    )

    # Table des scores
    op.create_table(
        'product_scores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ad_id', sa.Integer(), sa.ForeignKey('scraped_ads.id')),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('engagement_score', sa.Float()),
        sa.Column('problem_solution_bonus', sa.Float()),
        sa.Column('category_bonus', sa.Float()),
        sa.Column('multi_posting_bonus', sa.Float()),
        sa.Column('recency_score', sa.Float()),
        sa.Column('calculated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Table des créatives générées
    op.create_table(
        'creatives',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('scraped_ads.id')),
        sa.Column('video_id', sa.String(255)),  # ID Creatify
        sa.Column('video_type', sa.String(50)),  # ugc, problem_solution, etc.
        sa.Column('status', sa.String(20)),  # queued, processing, completed, failed
        sa.Column('download_url', sa.Text()),
        sa.Column('local_path', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime()),
    )

    # Table des campagnes
    op.create_table(
        'campaigns',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('scraped_ads.id')),
        sa.Column('platform', sa.String(20)),  # meta, tiktok
        sa.Column('campaign_id', sa.String(255)),  # ID externe
        sa.Column('campaign_name', sa.String(255)),
        sa.Column('daily_budget', sa.Integer()),  # En centimes
        sa.Column('status', sa.String(20)),  # paused, active, completed
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('activated_at', sa.DateTime()),
        sa.Column('meta_data', JSONB()),  # Infos supplémentaires
    )

    # Table des commandes
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('scraped_ads.id')),
        sa.Column('product_name', sa.String(255)),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('city', sa.String(100)),
        sa.Column('quantity', sa.Integer(), default=1),
        sa.Column('status', sa.String(20), default='pending'),  # pending, confirmed, shipped, delivered
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )

    # Indexes
    op.create_index('idx_ads_platform', 'scraped_ads', ['platform'])
    op.create_index('idx_ads_scored', 'scraped_ads', ['scored'])
    op.create_index('idx_scores_score', 'product_scores', ['score'])
    op.create_index('idx_campaigns_status', 'campaigns', ['status'])
    op.create_index('idx_orders_phone', 'orders', ['phone'])
    op.create_index('idx_orders_status', 'orders', ['status'])

def downgrade():
    op.drop_table('orders')
    op.drop_table('campaigns')
    op.drop_table('creatives')
    op.drop_table('product_scores')
    op.drop_table('scraped_ads')
```

---

<a name="tests"></a>

## 13. TESTS ET VALIDATION

### 13.1 Tests unitaires Backend

```bash
# Installer pytest
pip install pytest pytest-asyncio httpx

# Lancer tests
pytest tests/ -v

# Avec coverage
pytest --cov=app tests/
```

**Exemple de test:** `backend/tests/test_scoring.py`

```python
import pytest
from app.services.scoring_service import ScoringService

@pytest.mark.asyncio
async def test_scoring_calculation():
    # Test du calcul de score
    service = ScoringService(db_session)

    # Mock ad data
    test_ad = create_test_ad(likes=1000, comments=50, shares=20)

    scores = await service.calculate_scores_for_all_ads()

    assert len(scores) > 0
    assert scores[0]['score'] > 0
```

### 13.2 Tests API

```bash
# Test endpoints avec curl
curl -X POST http://localhost:8000/scraping/start \
  -H "Content-Type: application/json" \
  -d '{"facebook_max": 10, "tiktok_max": 10}'

# Test scoring
curl http://localhost:8000/scoring/top-products?limit=5

# Test création campagne
curl -X POST http://localhost:8000/campaigns/launch-for-product/1 \
  -H "Content-Type: application/json" \
  -d '{"platform": "meta", "daily_budget": 5000}'
```

---

## 14. CHECKLIST DE DÉPLOIEMENT

### 14.1 Avant le lancement

- [ ] Tous les credentials API sont configurés
- [ ] Base de données initialisée avec migrations
- [ ] Ollama installé avec modèle téléchargé
- [ ] Redis opérationnel
- [ ] Webhook WhatsApp configuré
- [ ] Pixels Meta et TikTok installés sur frontend
- [ ] Tests unitaires passent
- [ ] Tests d'intégration passent

### 14.2 Lancement progressif

**Semaine 1:**

- [ ] Lancer 1 scraping test (100 ads)
- [ ] Valider le scoring
- [ ] Sélectionner 1 produit manuellement
- [ ] Générer créatives pour 1 produit
- [ ] Créer landing page
- [ ] Lancer campagne test (10€/jour)

**Semaine 2-3:**

- [ ] Analyser résultats campagne test
- [ ] Ajuster scoring si nécessaire
- [ ] Lancer scraping complet (1000 ads)
- [ ] Sélectionner top 5 produits
- [ ] Générer toutes les créatives
- [ ] Lancer 5 campagnes (50€/jour total)

**Mois 2+:**

- [ ] Automatiser scraping mensuel
- [ ] Optimiser campagnes existantes
- [ ] Itérer sur les produits performants
- [ ] Scaler budget progressivement

---

## 15. SUPPORT ET MAINTENANCE

### 15.1 Monitoring

- **Logs:** Centralisés dans `/var/log/dropshipping/`
- **Métriques:** Utiliser Prometheus + Grafana
- **Alertes:** Configure alertes pour erreurs API, budgets dépassés

### 15.2 Backup

```bash
# Backup PostgreSQL quotidien
0 2 * * * pg_dump dropshipping > /backups/db_$(date +\%Y\%m\%d).sql

# Backup créatives/vidéos
0 3 * * * rsync -av /app/media/ /backups/media/
```

### 15.3 Mise à jour

```bash
# Mettre à jour backend
cd backend
git pull
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart dropshipping-backend

# Mettre à jour frontend
cd frontend
git pull
npm install
npm run build
sudo systemctl restart dropshipping-frontend
```

---

## CONCLUSION

Cette documentation fournit tous les éléments nécessaires pour implémenter la plateforme de dropshipping automatisée. Les développeurs juniors peuvent suivre les instructions pas à pas sans avoir besoin de consulter des documentations externes.

**Points clés:**

- Stack moderne et performant (Next.js 15, FastAPI, PostgreSQL)
- APIs tierces bien intégrées (Apify, Creatify, Meta, TikTok)
- IA locale avec Ollama pour WhatsApp
- Architecture scalable et maintenable
- Tests et validation à chaque étape

**Prochaines étapes:** Commencer par l'installation (Section 10), puis suivre la checklist de déploiement (Section 14).
