import pandas as pd
import requests
import gzip
import shutil

# -----------------------------
# Step 1: Download the IMDb files
# -----------------------------
def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print(f"Downloaded {local_filename}")

# URLs
title_url = "https://datasets.imdbws.com/title.basics.tsv.gz"
name_url = "https://datasets.imdbws.com/name.basics.tsv.gz"

# Local paths
title_gz = "title.basics.tsv.gz"
name_gz = "name.basics.tsv.gz"

download_file(title_url, title_gz)
download_file(name_url, name_gz)

# -----------------------------
# Step 2: Unzip the files
# -----------------------------
def unzip_gz(gz_path, out_path):
    with gzip.open(gz_path, 'rb') as f_in:
        with open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Unzipped {gz_path} -> {out_path}")

title_tsv = "title.basics.tsv"
name_tsv = "name.basics.tsv"

unzip_gz(title_gz, title_tsv)
unzip_gz(name_gz, name_tsv)

# -----------------------------
# Step 3: Load TSV into pandas
# -----------------------------
# Only read relevant columns for efficiency
title_cols = ["tconst", "titleType", "primaryTitle", "startYear", "genres"]
title_df = pd.read_csv(title_tsv, sep='\t', usecols=title_cols, na_values='\\N')

name_cols = ["nconst", "primaryName", "primaryProfession", "knownForTitles"]
name_df = pd.read_csv(name_tsv, sep='\t', usecols=name_cols, na_values='\\N')

# -----------------------------
# Step 4: Filter only movies and latest years
# -----------------------------
latest_years = [2023, 2024]
movies_df = title_df[
    (title_df['titleType'] == 'movie') &
    (title_df['startYear'].isin(latest_years))
].copy()

# Take only first 100 movies
movies_df = movies_df.head(100).reset_index(drop=True)

# -----------------------------
# Step 5: Map actors/directors/producers
# -----------------------------
# Collect all tconst IDs for the 100 movies
movie_ids = set(movies_df['tconst'].tolist())

# Filter people whose knownForTitles intersects with selected movies
def is_linked_to_movie(row):
    if pd.isna(row['knownForTitles']):
        return False
    titles = row['knownForTitles'].split(',')
    return any(t in movie_ids for t in titles)

people_df = name_df[name_df.apply(is_linked_to_movie, axis=1)].reset_index(drop=True)

# -----------------------------
# Step 5b: Keep only allowed roles per person
# -----------------------------
allowed_roles = {"actor", "actress", "director"}

def filter_roles(professions):
    if pd.isna(professions):
        return None
    roles = professions.split(',')
    filtered = [r for r in roles if r in allowed_roles]
    return ','.join(filtered) if filtered else None

# Apply filtering
people_df['primaryProfession'] = people_df['primaryProfession'].apply(filter_roles)

# Drop rows without any allowed role
people_df = people_df.dropna(subset=['primaryProfession']).reset_index(drop=True)

# -----------------------------
# Step 6: Save smaller CSVs
# -----------------------------
movies_df.to_csv("movies_sample.csv", index=False)
people_df.to_csv("people_sample.csv", index=False)

print("Saved movies_sample.csv and people_sample.csv")
print(f"Movies: {len(movies_df)} rows")
print(f"People (filtered by allowed roles): {len(people_df)} rows")

# -----------------------------
# Step 7: Genres in movies
# -----------------------------
# Drop missing genres
movies_genre_df = movies_df.dropna(subset=['genres'])

# Split by comma and flatten
all_genres = movies_genre_df['genres'].str.split(',').explode()

# Count frequency
genre_counts = all_genres.value_counts()

print("\n=== Genres in movies_sample.csv ===")
print(genre_counts)
print("\nTotal unique genres:", genre_counts.shape[0])

# -----------------------------
# Step 8: Roles in people
# -----------------------------
# Split by comma and flatten
all_roles = people_df['primaryProfession'].str.split(',').explode()

# Count frequency
role_counts = all_roles.value_counts()

print("\n=== Roles in people_sample.csv ===")
print(role_counts)
print("\nTotal unique roles:", role_counts.shape[0])