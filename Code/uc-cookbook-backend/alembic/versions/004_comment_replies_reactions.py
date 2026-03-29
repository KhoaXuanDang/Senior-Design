"""Comment parent_id for replies and comment_reactions table

Revision ID: 004
Revises: 003
Create Date: 2026-03-28

"""
from alembic import op
import sqlalchemy as sa


revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    rc_cols = {c["name"] for c in insp.get_columns("recipe_comments")}
    if "parent_id" not in rc_cols:
        with op.batch_alter_table("recipe_comments") as batch:
            batch.add_column(sa.Column("parent_id", sa.Integer(), nullable=True))

    insp = sa.inspect(conn)
    tables = insp.get_table_names()
    if "comment_reactions" not in tables:
        op.create_table(
            "comment_reactions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("comment_id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("emoji", sa.String(length=16), nullable=False),
            sa.ForeignKeyConstraint(["comment_id"], ["recipe_comments.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("comment_id", "user_id", name="uq_comment_reaction_user"),
        )
        op.create_index(op.f("ix_comment_reactions_id"), "comment_reactions", ["id"], unique=False)


def downgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    if "comment_reactions" in insp.get_table_names():
        op.drop_index(op.f("ix_comment_reactions_id"), table_name="comment_reactions")
        op.drop_table("comment_reactions")
    rc_cols = {c["name"] for c in insp.get_columns("recipe_comments")}
    if "parent_id" in rc_cols:
        with op.batch_alter_table("recipe_comments") as batch:
            batch.drop_column("parent_id")
