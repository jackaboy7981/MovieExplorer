"""Service layer for title-related workflows."""

from __future__ import annotations

from collections import defaultdict

from app.core.exceptions import TitleNotFound
from app.data_providers.contributor_data_provider import fetch_contributors_by_title_id
from app.data_providers.title_data_provider import fetch_genres_by_title_id, fetch_title_by_id


def get_title_details(title_id: int) -> dict:
    """Return title details with contributors and their roles."""
    title_row = fetch_title_by_id(title_id)

    if not title_row:
        raise TitleNotFound(title_id)

    genre_names = fetch_genres_by_title_id(title_id)
    contributor_rows = fetch_contributors_by_title_id(title_id)

    contributors_map: dict[int, dict] = defaultdict(
        lambda: {"id": 0, "imdb_reference_id": None, "name": "", "roles": []}
    )
    
    for contributor_id, contributor_imdb_ref_id, contributor_name, role_name in contributor_rows:
        contributor = contributors_map[contributor_id]
        contributor["id"] = contributor_id
        contributor["imdb_reference_id"] = contributor_imdb_ref_id
        contributor["name"] = contributor_name
        if role_name not in contributor["roles"]:
            contributor["roles"].append(role_name)

    return {
        "id": title_row[0],
        "imdb_reference_id": title_row[1],
        "title": title_row[2],
        "release_year": title_row[3],
        "media_type": title_row[4],
        "genres": genre_names,
        "contributors": list(contributors_map.values()),
    }
