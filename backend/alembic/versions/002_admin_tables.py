"""Add admin tables

Revision ID: 002_admin_tables
Revises: 001_initial
Create Date: 2024-12-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import context


# revision identifiers, used by Alembic.
revision = '002_admin_tables'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Détecter le type de base de données pour utiliser le bon type JSON
    bind = context.get_bind()
    if bind.dialect.name == 'postgresql':
        json_type = postgresql.JSONB
    else:
        json_type = sa.Text  # SQLite: store JSON as text
    
    # Table admin_users
    op.create_table(
        'admin_users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index('idx_admin_user_email', 'admin_users', ['email'], unique=True)
    op.create_index('idx_admin_user_active', 'admin_users', ['is_active'])
    
    # Table admin_sessions
    op.create_table(
        'admin_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(512), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['admin_id'], ['admin_users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_admin_session_token', 'admin_sessions', ['token'], unique=True)
    op.create_index('idx_admin_session_admin', 'admin_sessions', ['admin_id'])
    op.create_index('idx_admin_session_expires', 'admin_sessions', ['expires_at'])
    
    # Table admin_actions
    op.create_table(
        'admin_actions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=True),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('result', sa.String(20), nullable=False),  # success, failure, partial
        sa.Column('details', json_type, nullable=True),  # JSON stored as text for SQLite
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['admin_id'], ['admin_users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_admin_action_admin', 'admin_actions', ['admin_id'])
    op.create_index('idx_admin_action_type', 'admin_actions', ['action_type'])
    op.create_index('idx_admin_action_resource', 'admin_actions', ['resource_type', 'resource_id'])
    op.create_index('idx_admin_action_created', 'admin_actions', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_admin_action_created', table_name='admin_actions')
    op.drop_index('idx_admin_action_resource', table_name='admin_actions')
    op.drop_index('idx_admin_action_type', table_name='admin_actions')
    op.drop_index('idx_admin_action_admin', table_name='admin_actions')
    op.drop_table('admin_actions')
    
    op.drop_index('idx_admin_session_expires', table_name='admin_sessions')
    op.drop_index('idx_admin_session_admin', table_name='admin_sessions')
    op.drop_index('idx_admin_session_token', table_name='admin_sessions')
    op.drop_table('admin_sessions')
    
    op.drop_index('idx_admin_user_active', table_name='admin_users')
    op.drop_index('idx_admin_user_email', table_name='admin_users')
    op.drop_table('admin_users')

