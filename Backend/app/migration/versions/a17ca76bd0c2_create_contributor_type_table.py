"""create_contributor_type_table

Revision ID: a17ca76bd0c2
Revises: 9bd1dfb274a7
Create Date: 2026-02-14 11:41:07.858330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17ca76bd0c2'
down_revision: Union[str, Sequence[str], None] = '9bd1dfb274a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "contributor_type_lkup",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
    )

    contributor_type_lkup = sa.table(
        "contributor_type_lkup",
        sa.column("name", sa.String(length=100)),
    )
    op.bulk_insert(
        contributor_type_lkup,
        [{"name": "actor"}, {"name": "actress"}, {"name": "director"}],
    )

    op.create_table(
        "contributor_title_mapping",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("contributor_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("title_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["contributor_id"], ["contributor.id"]),
        sa.ForeignKeyConstraint(["type_id"], ["contributor_type_lkup.id"]),
        sa.ForeignKeyConstraint(["title_id"], ["title.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("contributor_title_mapping")
    op.drop_table("contributor_type_lkup")
