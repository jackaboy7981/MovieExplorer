import type { TitleItem } from "./Title";

type Nullable<T> = T | null | undefined;

export interface BrowseQueryParams {
  offset?: Nullable<number>;
  page_size?: Nullable<number>;
  search_text?: Nullable<string>;
  release_year?: Nullable<number>;
  release_yeax?: Nullable<number>;
  genre?: Nullable<number>;
}

export interface BrowseResponse {
  offset: number;
  page_size: number;
  results: TitleItem[];
}
