from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.ads import ScrapedAd, ProductScore
from datetime import datetime
import math
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
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except:
                return 0.0

        days_since = (datetime.utcnow() - start_date.replace(tzinfo=None)).days

        # Décroissance exponentielle: produits récents = score élevé
        return 15 * math.exp(-days_since / 30)

