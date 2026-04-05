"""Add index on origin_recipe_id

Revision ID: 006
Revises: 005
Create Date: 2026-04-04

"""
from alembic import op
import sqlalchemy as sa


revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    idxs = {i["name"] for i in insp.get_indexes("recipes")}
    if "ix_recipes_origin_recipe_id" not in idxs:
        op.create_index("ix_recipes_origin_recipe_id", "recipes", ["origin_recipe_id"])


def downgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    idxs = {i["name"] for i in insp.get_indexes("recipes")}
    if "ix_recipes_origin_recipe_id" in idxs:
        op.drop_index("ix_recipes_origin_recipe_id", table_name="recipes")
