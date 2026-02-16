import { useCallback, useEffect, useRef, useState } from "react";
import type { ComponentType } from "react";

interface ViewerProps<T extends { id: number }> {
  data: T[];
  isLoading: boolean;
  errorMessage: string | null;
  horizontal?: boolean;
  headingText?: string;
  emptyStateText?: string;
  ItemComponent: ComponentType<{ item: T }>;
}

function Viewer<T extends { id: number }>({
  data,
  isLoading,
  errorMessage,
  horizontal = false,
  headingText = "",
  emptyStateText = "No results found.",
  ItemComponent,
}: ViewerProps<T>) {
  const horizontalContainerRef = useRef<HTMLDivElement | null>(null);
  const [canScrollLeft, setCanScrollLeft] = useState<boolean>(false);
  const [canScrollRight, setCanScrollRight] = useState<boolean>(false);

  const updateScrollState = useCallback(() => {
    if (!horizontalContainerRef.current) {
      setCanScrollLeft(false);
      setCanScrollRight(false);
      return;
    }

    const { scrollLeft, scrollWidth, clientWidth } = horizontalContainerRef.current;
    const maxScrollLeft = scrollWidth - clientWidth;
    const epsilon = 2;

    setCanScrollLeft(scrollLeft > epsilon);
    setCanScrollRight(scrollLeft < maxScrollLeft - epsilon);
  }, []);

  const handleScrollRight = () => {
    if (!horizontalContainerRef.current) {
      return;
    }
    horizontalContainerRef.current.scrollBy({
      left: horizontalContainerRef.current.clientWidth * 0.8,
      behavior: "smooth",
    });
  };

  const handleScrollLeft = () => {
    if (!horizontalContainerRef.current) {
      return;
    }
    horizontalContainerRef.current.scrollBy({
      left: -horizontalContainerRef.current.clientWidth * 0.8,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    if (!horizontal) {
      return;
    }

    const initialFrame = requestAnimationFrame(() => {
      updateScrollState();
    });

    const handleWindowResize = () => {
      updateScrollState();
    };
    window.addEventListener("resize", handleWindowResize);

    return () => {
      cancelAnimationFrame(initialFrame);
      window.removeEventListener("resize", handleWindowResize);
    };
  }, [horizontal, data, updateScrollState]);

  return (
    <section className="mt-4">
      {headingText ? <p className="text-base font-medium">{headingText}</p> : null}
      {isLoading && <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">Loading...</p>}
      {errorMessage && <p className="mt-3 text-sm text-red-600">{errorMessage}</p>}
      {!isLoading && !errorMessage && data.length === 0 && (
        <p className="mt-10 text-center text-lg font-medium text-slate-600 dark:text-slate-300">
          {emptyStateText}
        </p>
      )}
      {!isLoading && !errorMessage && data.length > 0 && (
        <>
          {horizontal ? (
            <div className="relative mt-4">
              <div
                ref={horizontalContainerRef}
                onScroll={updateScrollState}
                className="no-scrollbar flex gap-4 overflow-x-auto whitespace-nowrap scroll-smooth"
              >
                {data.map((item) => (
                  <ItemComponent key={item.id} item={item} />
                ))}
              </div>
              {canScrollLeft && (
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center bg-gradient-to-r from-slate-50 to-transparent px-1 dark:from-slate-950">
                  <button
                    type="button"
                    onClick={handleScrollLeft}
                    className="pointer-events-auto rounded-full border border-slate-300 bg-white p-2 text-sm font-medium text-slate-700 shadow hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
                    aria-label="Scroll left"
                  >
                    ←
                  </button>
                </div>
              )}
              {canScrollRight && (
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center bg-gradient-to-l from-slate-50 to-transparent px-1 dark:from-slate-950">
                  <button
                    type="button"
                    onClick={handleScrollRight}
                    className="pointer-events-auto rounded-full border border-slate-300 bg-white p-2 text-sm font-medium text-slate-700 shadow hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
                    aria-label="Scroll right"
                  >
                    →
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="mt-4 grid grid-cols-[repeat(auto-fill,minmax(140px,1fr))] gap-4">
              {data.map((item) => (
                <ItemComponent key={item.id} item={item} />
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}

export default Viewer;
