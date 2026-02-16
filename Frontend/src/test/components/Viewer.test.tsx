import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Viewer from "../../components/Viewer";

interface DummyItem {
  id: number;
  label: string;
}

function DummyCard({ item }: { item: DummyItem }) {
  return <div>{item.label}</div>;
}

describe("Viewer", () => {
  it("shows loading state", () => {
    render(
      <Viewer<DummyItem>
        data={[]}
        isLoading
        errorMessage={null}
        ItemComponent={DummyCard}
      />,
    );

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows error state", () => {
    render(
      <Viewer<DummyItem>
        data={[]}
        isLoading={false}
        errorMessage="Failed"
        ItemComponent={DummyCard}
      />,
    );

    expect(screen.getByText("Failed")).toBeInTheDocument();
  });

  it("shows empty state text", () => {
    render(
      <Viewer<DummyItem>
        data={[]}
        isLoading={false}
        errorMessage={null}
        emptyStateText="No items"
        ItemComponent={DummyCard}
      />,
    );

    expect(screen.getByText("No items")).toBeInTheDocument();
  });

  it("renders item component for data rows", () => {
    render(
      <Viewer<DummyItem>
        data={[
          { id: 1, label: "One" },
          { id: 2, label: "Two" },
        ]}
        isLoading={false}
        errorMessage={null}
        ItemComponent={DummyCard}
      />,
    );

    expect(screen.getByText("One")).toBeInTheDocument();
    expect(screen.getByText("Two")).toBeInTheDocument();
  });
});
