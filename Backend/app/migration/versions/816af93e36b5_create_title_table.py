"""create_title_table

Revision ID: 816af93e36b5
Revises: 0b594e3e1bf2
Create Date: 2026-02-14 11:06:54.072839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '816af93e36b5'
down_revision: Union[str, Sequence[str], None] = '0b594e3e1bf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "media_type_lkup",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
    )

    media_type_lkup = sa.table(
        "media_type_lkup",
        sa.column("name", sa.String(length=100)),
    )
    op.bulk_insert(media_type_lkup, [{"name": "movie"}])

    op.create_table(
        "title",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("media_type", sa.Integer(), nullable=False),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["media_type"], ["media_type_lkup.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("title")
    op.drop_table("media_type_lkup")
