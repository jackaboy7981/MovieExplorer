import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import Contributor from "../../components/Contributor";
import type { ContributorItem } from "../../models/Contributor";

describe("Contributor", () => {
  it("renders contributor details and links to contributor page", () => {
    const item: ContributorItem = {
      id: 7,
      imdb_reference_id: "nm0000206",
      name: "Keanu Reeves",
      roles: ["Actor"],
    };

    render(
      <MemoryRouter>
        <Contributor item={item} />
      </MemoryRouter>,
    );

    const link = screen.getByRole("link");
    expect(link).toHaveAttribute("href", "/contributor/7");
    expect(screen.getByText("Keanu Reeves")).toBeInTheDocument();
    expect(screen.getByText("Actor")).toBeInTheDocument();
  });

  it("shows role fallback when roles are empty", () => {
    const item: ContributorItem = {
      id: 1,
      imdb_reference_id: null,
      name: "Unknown",
      roles: [],
    };

    render(
      <MemoryRouter>
        <Contributor item={item} />
      </MemoryRouter>,
    );

    expect(screen.getByText("Role not available")).toBeInTheDocument();
  });
});
