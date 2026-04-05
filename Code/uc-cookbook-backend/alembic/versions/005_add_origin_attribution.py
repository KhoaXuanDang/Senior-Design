"""Add origin attribution fields to recipes

Revision ID: 005
Revises: 004
Create Date: 2026-04-04

"""
from alembic import op
import sqlalchemy as sa


revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    cols = {c["name"] for c in insp.get_columns("recipes")}
    if "origin_recipe_id" not in cols:
        with op.batch_alter_table("recipes") as batch:
            batch.add_column(sa.Column("origin_recipe_id", sa.Integer(), nullable=True))
            batch.create_foreign_key(
                "fk_recipes_origin_recipe_id_recipes",
                "recipes",
                ["origin_recipe_id"],
                ["recipes.id"],
            )

    if "origin_author_id" not in cols:
        with op.batch_alter_table("recipes") as batch:
            batch.add_column(sa.Column("origin_author_id", sa.Integer(), nullable=True))
            batch.create_foreign_key(
                "fk_recipes_origin_author_id_users",
                "users",
                ["origin_author_id"],
                ["users.id"],
            )
    # Add index on origin_recipe_id for faster fork lookups
    insp = sa.inspect(conn)
    idxs = {i['name'] for i in insp.get_indexes('recipes')}
    if 'ix_recipes_origin_recipe_id' not in idxs:
        op.create_index('ix_recipes_origin_recipe_id', 'recipes', ['origin_recipe_id'])


def downgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    cols = {c["name"] for c in insp.get_columns("recipes")}
    if "origin_author_id" in cols:
        with op.batch_alter_table("recipes") as batch:
            batch.drop_constraint("fk_recipes_origin_author_id_users", type_="foreignkey")
            batch.drop_column("origin_author_id")

    if "origin_recipe_id" in cols:
        with op.batch_alter_table("recipes") as batch:
            batch.drop_constraint("fk_recipes_origin_recipe_id_recipes", type_="foreignkey")
            batch.drop_column("origin_recipe_id")
