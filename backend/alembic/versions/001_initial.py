"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-12-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import context


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Détecter le type de base de données pour utiliser le bon type JSON
    bind = context.get_bind()
    if bind.dialect.name == 'postgresql':
        json_type = postgresql.JSONB
    else:
        json_type = sa.JSON
    
    # Table des ads scrapées
    op.create_table(
        'scraped_ads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('platform', sa.String(20), nullable=False),
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
        sa.Column('video_id', sa.String(255)),
        sa.Column('video_type', sa.String(50)),
        sa.Column('status', sa.String(20)),
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
        sa.Column('platform', sa.String(20)),
        sa.Column('campaign_id', sa.String(255)),
        sa.Column('campaign_name', sa.String(255)),
        sa.Column('daily_budget', sa.Integer()),
        sa.Column('status', sa.String(20)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('activated_at', sa.DateTime()),
        sa.Column('meta_data', json_type()),
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
        sa.Column('status', sa.String(20), default='pending'),
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


def downgrade() -> None:
    op.drop_index('idx_orders_status', 'orders')
    op.drop_index('idx_orders_phone', 'orders')
    op.drop_index('idx_campaigns_status', 'campaigns')
    op.drop_index('idx_scores_score', 'product_scores')
    op.drop_index('idx_ads_scored', 'scraped_ads')
    op.drop_index('idx_ads_platform', 'scraped_ads')
    op.drop_table('orders')
    op.drop_table('campaigns')
    op.drop_table('creatives')
    op.drop_table('product_scores')
    op.drop_table('scraped_ads')

