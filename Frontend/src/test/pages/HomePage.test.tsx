import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi, beforeEach } from "vitest";

import HomePage from "../../pages/HomePage";
import { fetchBrowseGenres, fetchBrowseTitles } from "../../api/browseApi";

vi.mock("../../api/browseApi", () => ({
  fetchBrowseTitles: vi.fn(),
  fetchBrowseGenres: vi.fn(),
}));

const mockedFetchBrowseTitles = vi.mocked(fetchBrowseTitles);
const mockedFetchBrowseGenres = vi.mocked(fetchBrowseGenres);

function renderHomePage(searchText: string | null) {
  return render(
    <MemoryRouter>
      <HomePage searchText={searchText} />
    </MemoryRouter>,
  );
}

describe("HomePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("loads default browse data and shows home hero when search is not active", async () => {
    mockedFetchBrowseTitles.mockResolvedValue({
      offset: 0,
      page_size: 40,
      results: [
        {
          id: 1,
          imdb_reference_id: "tt1",
          title: "Movie One",
          release_year: 2000,
          media_type: "movie",
          roles: [],
        },
      ],
    });

    renderHomePage(null);

    expect(
      screen.getByText("Discover Movies. Follow the People Behind Them."),
    ).toBeInTheDocument();

    await waitFor(() => {
      expect(mockedFetchBrowseTitles).toHaveBeenCalledWith({ page_size: 40, offset: 0 });
    });
    expect(mockedFetchBrowseGenres).not.toHaveBeenCalled();
    expect(screen.getByText("Movie One")).toBeInTheDocument();
  });

  it("loads search data and filter options when search is active", async () => {
    mockedFetchBrowseTitles.mockResolvedValue({
      offset: 0,
      page_size: 28,
      results: [
        {
          id: 2,
          imdb_reference_id: "tt2",
          title: "The Matrix",
          release_year: 1999,
          media_type: "movie",
          roles: [],
        },
      ],
    });
    mockedFetchBrowseGenres.mockResolvedValue([{ id: 1, name: "Action" }]);

    renderHomePage("matrix");

    await waitFor(() => {
      expect(mockedFetchBrowseTitles).toHaveBeenCalledWith({
        search_text: "matrix",
        page_size: 28,
        offset: 0,
        release_year: undefined,
        genre: undefined,
      });
    });
    await waitFor(() => {
      expect(mockedFetchBrowseGenres).toHaveBeenCalledTimes(1);
    });

    expect(screen.getByText("Filters:")).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "Action" })).toBeInTheDocument();
    expect(screen.getByText("The Matrix")).toBeInTheDocument();
  });

  it("applies selected filters to browse API", async () => {
    mockedFetchBrowseTitles.mockResolvedValue({
      offset: 0,
      page_size: 28,
      results: [],
    });
    mockedFetchBrowseGenres.mockResolvedValue([{ id: 3, name: "Drama" }]);

    renderHomePage("neo");

    await waitFor(() => {
      expect(mockedFetchBrowseTitles).toHaveBeenCalledTimes(1);
    });

    const releaseYearSelect = screen.getAllByRole("combobox")[0];
    const genreSelect = screen.getAllByRole("combobox")[1];
    fireEvent.change(releaseYearSelect, { target: { value: "2020" } });
    fireEvent.change(genreSelect, { target: { value: "3" } });

    await waitFor(() => {
      expect(mockedFetchBrowseTitles).toHaveBeenLastCalledWith({
        search_text: "neo",
        page_size: 28,
        offset: 0,
        release_year: 2020,
        genre: 3,
      });
    });
  });
});
