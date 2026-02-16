import { buildApiUrl } from "./config/constants";
import type { BrowseQueryParams, BrowseResponse } from "../models/Browse";

type Nullable<T> = T | null | undefined;

export async function fetchBrowseTitles(
  params: BrowseQueryParams = {},
): Promise<BrowseResponse> {
  const releaseYear = params.release_year ?? params.release_yeax;
  const searchParams = new URLSearchParams();

  appendQueryParamIfProvided(searchParams, "offset", params.offset);
  appendQueryParamIfProvided(searchParams, "page_size", params.page_size);
  appendQueryParamIfProvided(searchParams, "search_text", params.search_text);
  appendQueryParamIfProvided(searchParams, "release_year", releaseYear);
  appendQueryParamIfProvided(searchParams, "genre", params.genre);

  const browseUrl = buildApiUrl("browse");
  const queryString = searchParams.toString();
  if (queryString) {
    browseUrl.search = queryString;
  }

  const response = await fetch(browseUrl.toString());
  if (!response.ok) {
    throw new Error(`Browse request failed with status ${response.status}`);
  }
  return (await response.json()) as BrowseResponse;
}

export interface BrowseGenreOption {
  id: number;
  name: string;
}

export async function fetchBrowseGenres(): Promise<BrowseGenreOption[]> {
  const genreUrl = buildApiUrl("browse/genres");
  const response = await fetch(genreUrl.toString());
  if (!response.ok) {
    throw new Error(`Browse genre request failed with status ${response.status}`);
  }
  const payload = (await response.json()) as Array<BrowseGenreOption | string>;

  return payload.map((genreOption, index) => {
    if (typeof genreOption === "string") {
      return {
        id: index + 1,
        name: genreOption,
      };
    }

    return genreOption;
  });
}

function appendQueryParamIfProvided(
  searchParams: URLSearchParams,
  key: string,
  value: Nullable<string | number>,
): void {
  if (value === null || value === undefined) {
    return;
  }

  if (typeof value === "string" && value.trim() === "") {
    return;
  }

  searchParams.append(key, String(value));
}
