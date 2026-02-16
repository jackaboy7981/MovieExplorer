export const API_BASE_URL = "http://localhost:8000/";

export function buildApiUrl(path: string): URL {
  return new URL(path, API_BASE_URL);
}
