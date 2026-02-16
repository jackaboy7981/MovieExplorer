import type { ComponentProps } from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import TopBar from "../../components/TopBar";

function renderTopBar(initialPath: string, props?: Partial<ComponentProps<typeof TopBar>>) {
  const onToggleTheme = vi.fn();
  const onSearch = vi.fn();
  const onClearSearch = vi.fn();

  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route
          path="*"
          element={
            <TopBar
              theme="light"
              onToggleTheme={onToggleTheme}
              onSearch={onSearch}
              onClearSearch={onClearSearch}
              {...props}
            />
          }
        />
      </Routes>
    </MemoryRouter>,
  );

  return { onToggleTheme, onSearch, onClearSearch };
}

describe("TopBar", () => {
  it("disables Go button when search is empty and submits when text is provided", () => {
    const { onSearch } = renderTopBar("/");

    const input = screen.getByPlaceholderText("Search");
    const goButton = screen.getByRole("button", { name: "Go" });

    expect(goButton).toBeDisabled();

    fireEvent.change(input, { target: { value: "matrix" } });
    expect(goButton).not.toBeDisabled();

    fireEvent.click(goButton);
    expect(onSearch).toHaveBeenCalledWith("matrix");
  });

  it("calls clear callback when input is cleared", () => {
    const { onClearSearch } = renderTopBar("/");
    const input = screen.getByPlaceholderText("Search");

    fireEvent.change(input, { target: { value: "keanu" } });
    fireEvent.change(input, { target: { value: "" } });

    expect(onClearSearch).toHaveBeenCalledTimes(1);
  });

  it("shows Home button on non-home routes", () => {
    renderTopBar("/movie/1");
    expect(screen.getByRole("button", { name: "Home" })).toBeInTheDocument();
  });

  it("hides Home button on home route", () => {
    renderTopBar("/");
    expect(screen.queryByRole("button", { name: "Home" })).not.toBeInTheDocument();
  });
});
