import { buildApiUrl } from "./config/constants";
import type { TitleDetailsResponse } from "../models/Title";

export async function fetchTitleDetails(titleId: number): Promise<TitleDetailsResponse> {
  const titleUrl = buildApiUrl(`title/${titleId}`);
  const response = await fetch(titleUrl.toString());

  if (!response.ok) {
    throw new Error(`Title request failed with status ${response.status}`);
  }

  return (await response.json()) as TitleDetailsResponse;
}
