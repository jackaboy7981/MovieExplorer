"""Load sample CSV data into Postgres tables created by Alembic migrations."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Iterable

import psycopg2

SCRIPT_DIR = Path(__file__).resolve().parent
MOVIES_CSV = SCRIPT_DIR / "movies_sample.csv"
PEOPLE_CSV = SCRIPT_DIR / "people_sample.csv"


def normalize(value: str | None) -> str | None:
    """Trim and normalize empty-like strings."""
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in {"", "\\N"}:
        return None
    return cleaned


def parse_year(value: str | None) -> int | None:
    """Parse year from CSV values like '2024' or '2024.0'."""
    normalized = normalize(value)
    if normalized is None:
        return None
    try:
        return int(float(normalized))
    except ValueError:
        return None


def parse_list(value: str | None) -> list[str]:
    """Parse comma-separated string into cleaned values."""
    normalized = normalize(value)
    if normalized is None:
        return []
    return [item.strip() for item in normalized.split(",") if item.strip()]


def ensure_lookup(cur, table_name: str, name: str) -> int:
    """Return lookup id by name, creating the row if needed."""
    cur.execute(
        f"SELECT id FROM {table_name} WHERE lower(name) = lower(%s) LIMIT 1",
        (name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        f"INSERT INTO {table_name} (name) VALUES (%s) RETURNING id",
        (name,),
    )
    return cur.fetchone()[0]


def ensure_contributor(cur, name: str) -> int:
    """Return contributor id by name, creating if missing."""
    cur.execute(
        "SELECT id FROM contributor WHERE name = %s LIMIT 1",
        (name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO contributor (name) VALUES (%s) RETURNING id",
        (name,),
    )
    return cur.fetchone()[0]


def ensure_title(cur, title_name: str, media_type_id: int, release_year: int | None) -> int:
    """Return title id for (title, media_type, release_year), creating if missing."""
    cur.execute(
        """
        SELECT id
        FROM title
        WHERE title = %s
          AND media_type = %s
          AND (
              (release_year IS NULL AND %s IS NULL)
              OR release_year = %s
          )
        LIMIT 1
        """,
        (title_name, media_type_id, release_year, release_year),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO title (title, media_type, release_year)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (title_name, media_type_id, release_year),
    )
    return cur.fetchone()[0]


def ensure_mapping(cur, table_name: str, left_col: str, right_col: str, left_id: int, right_id: int) -> None:
    """Insert mapping row only if it does not already exist."""
    cur.execute(
        f"""
        SELECT id
        FROM {table_name}
        WHERE {left_col} = %s AND {right_col} = %s
        LIMIT 1
        """,
        (left_id, right_id),
    )
    if cur.fetchone():
        return

    cur.execute(
        f"INSERT INTO {table_name} ({left_col}, {right_col}) VALUES (%s, %s)",
        (left_id, right_id),
    )


def ensure_contributor_title_mapping(
    cur,
    contributor_id: int,
    type_id: int,
    title_id: int,
) -> bool:
    """Insert contributor-title-type mapping if missing; return True when inserted."""
    cur.execute(
        """
        SELECT 1
        FROM contributor_title_mapping
        WHERE contributor_id = %s AND type_id = %s AND title_id = %s
        LIMIT 1
        """,
        (contributor_id, type_id, title_id),
    )
    if cur.fetchone():
        return False

    cur.execute(
        """
        INSERT INTO contributor_title_mapping (contributor_id, type_id, title_id)
        VALUES (%s, %s, %s)
        """,
        (contributor_id, type_id, title_id),
    )
    return True


def read_csv_rows(path: Path) -> Iterable[dict[str, str]]:
    """Yield rows from CSV file."""
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for standalone execution."""
    parser = argparse.ArgumentParser(
        description="Insert movie/person sample CSV data into Postgres tables.",
    )
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL", ""),
        help="Postgres connection URL. Defaults to env var DATABASE_URL.",
    )
    parser.add_argument(
        "--movies-csv",
        default=str(MOVIES_CSV),
        help="Path to movies_sample.csv",
    )
    parser.add_argument(
        "--people-csv",
        default=str(PEOPLE_CSV),
        help="Path to people_sample.csv",
    )
    return parser.parse_args()


def main() -> None:
    """Load movies and people samples into normalized tables."""
    args = parse_args()
    database_url = args.database_url.strip()
    movies_csv = Path(args.movies_csv).expanduser().resolve()
    people_csv = Path(args.people_csv).expanduser().resolve()

    if not database_url:
        raise RuntimeError(
            "Database URL not provided. Set DATABASE_URL or pass --database-url.",
        )

    if not movies_csv.exists() or not people_csv.exists():
        raise FileNotFoundError(
            f"CSV files not found. movies={movies_csv} people={people_csv}",
        )

    inserted_titles = 0
    inserted_contributors = 0
    contributor_title_links = 0
    title_genre_links = 0

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            movie_media_type_id = ensure_lookup(cur, "media_type_lkup", "movie")
            title_ids_by_tconst: dict[str, int] = {}

            for row in read_csv_rows(movies_csv):
                tconst = normalize(row.get("tconst"))
                title_name = normalize(row.get("primaryTitle"))
                if not title_name:
                    continue

                release_year = parse_year(row.get("startYear"))
                title_id_before = None
                cur.execute(
                    """
                    SELECT id FROM title
                    WHERE title = %s AND media_type = %s
                      AND ((release_year IS NULL AND %s IS NULL) OR release_year = %s)
                    LIMIT 1
                    """,
                    (title_name, movie_media_type_id, release_year, release_year),
                )
                row_before = cur.fetchone()
                if row_before:
                    title_id_before = row_before[0]

                title_id = ensure_title(cur, title_name, movie_media_type_id, release_year)
                if title_id_before is None:
                    inserted_titles += 1
                if tconst:
                    title_ids_by_tconst[tconst] = title_id

                genres = parse_list(row.get("genres"))
                for genre_name in genres:
                    genre_id = ensure_lookup(cur, "genre_type_lkup", genre_name)

                    cur.execute(
                        "SELECT 1 FROM title_genre WHERE title_id = %s AND genre_id = %s LIMIT 1",
                        (title_id, genre_id),
                    )
                    if not cur.fetchone():
                        ensure_mapping(
                            cur,
                            "title_genre",
                            "title_id",
                            "genre_id",
                            title_id,
                            genre_id,
                        )
                        title_genre_links += 1

            for row in read_csv_rows(people_csv):
                person_name = normalize(row.get("primaryName"))
                if not person_name:
                    continue

                cur.execute(
                    "SELECT id FROM contributor WHERE name = %s LIMIT 1",
                    (person_name,),
                )
                existing = cur.fetchone()
                contributor_id = existing[0] if existing else ensure_contributor(cur, person_name)
                if not existing:
                    inserted_contributors += 1

                roles = parse_list(row.get("primaryProfession"))
                known_titles = parse_list(row.get("knownForTitles"))
                for role_name in roles:
                    role_id = ensure_lookup(cur, "contributor_type_lkup", role_name)
                    for known_title in known_titles:
                        title_id = title_ids_by_tconst.get(known_title)
                        if title_id is None:
                            continue
                        inserted = ensure_contributor_title_mapping(
                            cur,
                            contributor_id=contributor_id,
                            type_id=role_id,
                            title_id=title_id,
                        )
                        if inserted:
                            contributor_title_links += 1

    print(f"Inserted titles: {inserted_titles}")
    print(f"Inserted contributors: {inserted_contributors}")
    print(f"Inserted title->genre links: {title_genre_links}")
    print(f"Inserted contributor->title->type links: {contributor_title_links}")


if __name__ == "__main__":
    main()
