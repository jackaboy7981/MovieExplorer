import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import MoviePage from "../../pages/MoviePage";
import { fetchTitleDetails } from "../../api/titleApi";

vi.mock("../../api/titleApi", () => ({
  fetchTitleDetails: vi.fn(),
}));

const mockedFetchTitleDetails = vi.mocked(fetchTitleDetails);

describe("MoviePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("redirects to home when route id is invalid", () => {
    render(
      <MemoryRouter initialEntries={["/movie/abc"]}>
        <Routes>
          <Route path="/" element={<div>Home</div>} />
          <Route path="/movie/:id" element={<MoviePage />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Home")).toBeInTheDocument();
  });

  it("fetches and renders title details and contributors", async () => {
    mockedFetchTitleDetails.mockResolvedValue({
      id: 10,
      imdb_reference_id: "tt0133093",
      title: "The Matrix",
      release_year: 1999,
      media_type: "movie",
      genres: ["Action", "Sci-Fi"],
      contributors: [
        {
          id: 1,
          imdb_reference_id: "nm0000206",
          name: "Keanu Reeves",
          roles: ["Actor"],
        },
      ],
    });

    render(
      <MemoryRouter initialEntries={["/movie/10"]}>
        <Routes>
          <Route path="/movie/:id" element={<MoviePage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(mockedFetchTitleDetails).toHaveBeenCalledWith(10);
    });

    expect(screen.getByRole("heading", { name: "The Matrix" })).toBeInTheDocument();
    expect(screen.getByText("Genres:")).toBeInTheDocument();
    expect(screen.getByText("Action, Sci-Fi")).toBeInTheDocument();
    expect(screen.getByText("Contributors")).toBeInTheDocument();
    expect(screen.getByText("Keanu Reeves")).toBeInTheDocument();
  });
});
