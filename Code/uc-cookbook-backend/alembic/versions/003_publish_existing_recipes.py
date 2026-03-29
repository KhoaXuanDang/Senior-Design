"""Set is_published for recipes created before publish workflow

Revision ID: 003
Revises: 002
Create Date: 2026-03-28

Migration 002 added is_published with server_default false, so legacy rows were
all unpublished and disappeared from GET /recipes. Restore discoverability for
existing data; new recipes still default via application logic where appropriate.
"""

from alembic import op


revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE recipes SET is_published = 1")


def downgrade() -> None:
    op.execute("UPDATE recipes SET is_published = 0")
