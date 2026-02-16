import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi, beforeEach } from "vitest";

import App from "../App";

vi.mock("../pages/HomePage", () => ({
  default: ({ searchText }: { searchText: string | null }) => (
    <div>HomePage:{searchText ?? "none"}</div>
  ),
}));

vi.mock("../pages/MoviePage", () => ({
  default: () => <div>MoviePage</div>,
}));

vi.mock("../pages/ContributorPage", () => ({
  default: () => <div>ContributorPage</div>,
}));

vi.mock("../components/TopBar", () => ({
  default: ({
    theme,
    onToggleTheme,
    onSearch,
    onClearSearch,
  }: {
    theme: "light" | "dark";
    onToggleTheme: () => void;
    onSearch: (text: string) => void;
    onClearSearch: () => void;
  }) => (
    <div>
      <span>theme:{theme}</span>
      <button onClick={onToggleTheme}>toggle</button>
      <button onClick={() => onSearch("matrix")}>search</button>
      <button onClick={onClearSearch}>clear</button>
    </div>
  ),
}));

describe("App", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renders home for unknown routes via fallback redirect", () => {
    render(
      <MemoryRouter initialEntries={["/unknown"]}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByText("HomePage:none")).toBeInTheDocument();
  });

  it("toggles theme and persists search text through callbacks", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByText("theme:light")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "toggle" }));
    expect(screen.getByText("theme:dark")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "search" }));
    expect(screen.getByText("HomePage:matrix")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "clear" }));
    expect(screen.getByText("HomePage:none")).toBeInTheDocument();
  });
});
