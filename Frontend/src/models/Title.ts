import type { ContributorItem } from "./Contributor";

export interface TitleItem {
  id: number;
  imdb_reference_id: string | null;
  title: string;
  release_year: number | null;
  media_type: string;
}

export interface TitleDetailsResponse {
  id: number;
  imdb_reference_id: string | null;
  title: string;
  release_year: number | null;
  media_type: string;
  contributors: ContributorItem[];
}
