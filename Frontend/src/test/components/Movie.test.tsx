import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import Movie from "../../components/Movie";
import type { TitleItem } from "../../models/Title";

describe("Movie", () => {
  it("renders title and links to movie details page", () => {
    const item: TitleItem = {
      id: 42,
      imdb_reference_id: "tt0133093",
      title: "The Matrix",
      release_year: 1999,
      media_type: "movie",
      roles: [],
    };

    render(
      <MemoryRouter>
        <Movie item={item} />
      </MemoryRouter>,
    );

    const link = screen.getByRole("link");
    expect(link).toHaveAttribute("href", "/movie/42");
    expect(screen.getByText("The Matrix")).toBeInTheDocument();
  });
});
