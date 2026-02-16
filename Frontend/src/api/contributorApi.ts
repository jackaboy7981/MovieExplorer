import { buildApiUrl } from "./config/constants";
import type { ContributorDetailsResponse } from "../models/Contributor";

export async function fetchContributorDetails(
  contributorId: number,
): Promise<ContributorDetailsResponse> {
  const contributorUrl = buildApiUrl(`contributor/${contributorId}`);
  const response = await fetch(contributorUrl.toString());

  if (!response.ok) {
    throw new Error(`Contributor request failed with status ${response.status}`);
  }

  return (await response.json()) as ContributorDetailsResponse;
}
