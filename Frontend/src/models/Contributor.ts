import type { TitleItem } from "./Title";

export interface ContributorItem {
  id: number;
  imdb_reference_id: string | null;
  name: string;
  roles: string[];
}

export interface ContributorDetailsResponse {
  id: number;
  imdb_reference_id: string | null;
  name: string;
  titles: TitleItem[];
}
