import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import ContributorPage from "../../pages/ContributorPage";
import { fetchContributorDetails } from "../../api/contributorApi";

vi.mock("../../api/contributorApi", () => ({
  fetchContributorDetails: vi.fn(),
}));

const mockedFetchContributorDetails = vi.mocked(fetchContributorDetails);

describe("ContributorPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("redirects to home when route id is invalid", () => {
    render(
      <MemoryRouter initialEntries={["/contributor/0"]}>
        <Routes>
          <Route path="/" element={<div>Home</div>} />
          <Route path="/contributor/:id" element={<ContributorPage />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Home")).toBeInTheDocument();
  });

  it("fetches and renders contributor details and related titles", async () => {
    mockedFetchContributorDetails.mockResolvedValue({
      id: 7,
      imdb_reference_id: "nm0000206",
      name: "Keanu Reeves",
      titles: [
        {
          id: 10,
          imdb_reference_id: "tt0133093",
          title: "The Matrix",
          release_year: 1999,
          media_type: "movie",
          roles: ["Actor"],
        },
      ],
    });

    render(
      <MemoryRouter initialEntries={["/contributor/7"]}>
        <Routes>
          <Route path="/contributor/:id" element={<ContributorPage />} />
        </Routes>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(mockedFetchContributorDetails).toHaveBeenCalledWith(7);
    });

    expect(screen.getByRole("heading", { name: "Keanu Reeves" })).toBeInTheDocument();
    expect(screen.getByText("Contributions:")).toBeInTheDocument();
    expect(screen.getByText("Actor")).toBeInTheDocument();
    expect(
      screen.getByText("Movies worked on will be displayed here on screen."),
    ).toBeInTheDocument();
    expect(screen.getByText("The Matrix")).toBeInTheDocument();
  });
});
