export interface ContributorItem {
  id: number;
  imdb_reference_id: string | null;
  name: string;
  roles: string[];
}

export interface ContributorTitleItem {
  id: number;
  imdb_reference_id: string | null;
  title: string;
  release_year: number | null;
  media_type: string;
  roles: string[];
}

export interface ContributorDetailsResponse {
  id: number;
  imdb_reference_id: string | null;
  name: string;
  titles: ContributorTitleItem[];
}
