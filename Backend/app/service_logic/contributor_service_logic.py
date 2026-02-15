"""Service layer for contributor-related workflows."""

from __future__ import annotations

from collections import defaultdict

from app.core.exceptions import ContributorNotFound
from app.data_providers.contributor_data_provider import fetch_contributor_by_id
from app.data_providers.title_data_provider import fetch_titles_by_contributor_id


def get_contributor_details(contributor_id: int) -> dict:
    """Return contributor details with associated titles and roles."""
    contributor_row = fetch_contributor_by_id(contributor_id)

    if not contributor_row:
        raise ContributorNotFound(contributor_id)

    title_rows = fetch_titles_by_contributor_id(contributor_id)

    titles_map: dict[int, dict] = defaultdict(
        lambda: {
            "id": 0,
            "imdb_reference_id": None,
            "title": "",
            "release_year": None,
            "media_type": "",
            "roles": [],
        }
    )

    for title_id, title_imdb_ref_id, title_name, release_year, media_type, role_name in title_rows:
        title = titles_map[title_id]
        title["id"] = title_id
        title["imdb_reference_id"] = title_imdb_ref_id
        title["title"] = title_name
        title["release_year"] = release_year
        title["media_type"] = media_type
        if role_name not in title["roles"]:
            title["roles"].append(role_name)

    return {
        "id": contributor_row[0],
        "imdb_reference_id": contributor_row[1],
        "name": contributor_row[2],
        "titles": list(titles_map.values()),
    }
