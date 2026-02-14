"""create_genre_table

Revision ID: 9bd1dfb274a7
Revises: 816af93e36b5
Create Date: 2026-02-14 11:30:09.912697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bd1dfb274a7'
down_revision: Union[str, Sequence[str], None] = '816af93e36b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "genre_type_lkup",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "title_genre",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("title_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["title_id"], ["title.id"]),
        sa.ForeignKeyConstraint(["genre_id"], ["genre_type_lkup.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("title_genre")
    op.drop_table("genre_type_lkup")
