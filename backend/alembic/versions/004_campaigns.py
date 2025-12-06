"""Add Campaign table

Revision ID: 004_campaigns
Revises: 001_initial
Create Date: 2024-12-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '004_campaigns'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # La table campaigns est déjà créée dans 001_initial.py
    # Cette migration ajoute uniquement un index supplémentaire pour optimiser les requêtes
    # Index composite pour les requêtes fréquentes sur product_id + platform
    op.create_index(
        'idx_campaigns_product_platform',
        'campaigns',
        ['product_id', 'platform'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index('idx_campaigns_product_platform', 'campaigns')

