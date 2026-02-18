"""indexing

Revision ID: f29fb7dfe6ee
Revises: a17ca76bd0c2
Create Date: 2026-02-18 06:55:46.745452

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f29fb7dfe6ee'
down_revision: Union[str, Sequence[str], None] = 'a17ca76bd0c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "ix_contributor_title_mapping_contributor_id",
        "contributor_title_mapping",
        ["contributor_id"],
        unique=False,
    )
    op.create_index(
        "ix_contributor_title_mapping_title_id",
        "contributor_title_mapping",
        ["title_id"],
        unique=False,
    )
    op.create_index(
        "ix_contributor_title_mapping_type_id",
        "contributor_title_mapping",
        ["type_id"],
        unique=False,
    )
    op.create_index(
        "ix_title_genre_title_id_genre_id",
        "title_genre",
        ["title_id", "genre_id"],
        unique=False,
    )
    op.create_index(
        "ix_title_media_type",
        "title",
        ["media_type"],
        unique=False,
    )
    op.create_index(
        "ix_title_release_year",
        "title",
        ["release_year"],
        unique=False,
    )
    op.create_index(
        "ix_contributor_name_trgm",
        "contributor",
        ["name"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )
    op.create_index(
        "ix_title_title_trgm",
        "title",
        ["title"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )
    op.create_index(
        "ix_genre_type_lkup_name_trgm",
        "genre_type_lkup",
        ["name"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_genre_type_lkup_name_trgm", table_name="genre_type_lkup")
    op.drop_index("ix_title_title_trgm", table_name="title")
    op.drop_index("ix_contributor_name_trgm", table_name="contributor")
    op.drop_index("ix_title_release_year", table_name="title")
    op.drop_index("ix_title_media_type", table_name="title")
    op.drop_index("ix_title_genre_title_id_genre_id", table_name="title_genre")
    op.drop_index("ix_contributor_title_mapping_type_id", table_name="contributor_title_mapping")
    op.drop_index("ix_contributor_title_mapping_title_id", table_name="contributor_title_mapping")
    op.drop_index("ix_contributor_title_mapping_contributor_id", table_name="contributor_title_mapping")
