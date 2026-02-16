import { useCallback, useEffect, useRef, useState } from "react";

import {
  fetchBrowseGenres,
  fetchBrowseTitles,
  type BrowseGenreOption,
} from "../api/browseApi";
import type { TitleItem } from "../models/Title";
import Movie from "../components/Movie";
import Viewer from "../components/Viewer";

interface HomePageProps {
  searchText: string | null;
}

const DEFAULT_PAGE_SIZE = 40;
const SEARCH_PAGE_SIZE = 28;
const HORIZONTAL_MAX_ITEMS = 14;

function HomePage({ searchText }: HomePageProps) {
  const [titles, setTitles] = useState<TitleItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isLoadingMore, setIsLoadingMore] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [genreOptions, setGenreOptions] = useState<BrowseGenreOption[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<string>("");
  const [selectedReleaseYear, setSelectedReleaseYear] = useState<string>("");
  const [nextSearchOffset, setNextSearchOffset] = useState<number>(SEARCH_PAGE_SIZE);
  const [hasMoreSearchResults, setHasMoreSearchResults] = useState<boolean>(false);
  const loadMoreSentinelRef = useRef<HTMLDivElement | null>(null);
  const isSearchActive = Boolean(searchText && searchText.trim() !== "");
  const currentYear = new Date().getUTCFullYear();

  const releaseYearOptions = Array.from(
    { length: currentYear - 1800 },
    (_, index) => String(currentYear - 1 - index),
  );

  // Load genre options only when search mode is active; reset filter state otherwise.
  useEffect(() => {
    if (!isSearchActive) {
      setSelectedGenre("");
      setSelectedReleaseYear("");
      setGenreOptions([]);
      return;
    }

    let isMounted = true;
    const loadGenreOptions = async () => {
      try {
        const genres = await fetchBrowseGenres();
        if (!isMounted) {
          return;
        }
        setGenreOptions(genres);
      } catch {
        if (!isMounted) {
          return;
        }
        setGenreOptions([]);
      }
    };

    void loadGenreOptions();

    return () => {
      isMounted = false;
    };
  }, [isSearchActive]);

  const loadMoreSearchResults = useCallback(async () => {
    if (!isSearchActive || !hasMoreSearchResults || isLoadingMore || isLoading) {
      return;
    }

    setIsLoadingMore(true);
    try {
      const data = await fetchBrowseTitles({
        search_text: searchText,
        page_size: SEARCH_PAGE_SIZE,
        offset: nextSearchOffset,
        release_year: selectedReleaseYear ? Number(selectedReleaseYear) : undefined,
        genre: selectedGenre ? Number(selectedGenre) : undefined,
      });

      setTitles((prevTitles) => [...prevTitles, ...data.results]);
      setHasMoreSearchResults(data.results.length === SEARCH_PAGE_SIZE);
      setNextSearchOffset((prevOffset) => prevOffset + SEARCH_PAGE_SIZE);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to fetch more browse data.");
      setHasMoreSearchResults(false);
    } finally {
      setIsLoadingMore(false);
    }
  }, [
    hasMoreSearchResults,
    isLoading,
    isLoadingMore,
    isSearchActive,
    nextSearchOffset,
    searchText,
    selectedGenre,
    selectedReleaseYear,
  ]);

  // Fetch browse results whenever search mode/filter inputs change.
  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);
    setIsLoadingMore(false);
    setErrorMessage(null);

    const loadBrowseData = async () => {
      try {
        const browseParams = isSearchActive
          ? {
              search_text: searchText,
              page_size: SEARCH_PAGE_SIZE,
              offset: 0,
              release_year: selectedReleaseYear ? Number(selectedReleaseYear) : undefined,
              genre: selectedGenre ? Number(selectedGenre) : undefined,
            }
          : { page_size: DEFAULT_PAGE_SIZE, offset: 0 };
        const data = await fetchBrowseTitles(browseParams);
        if (!isMounted) {
          return;
        }
        setTitles(data.results);
        setNextSearchOffset(SEARCH_PAGE_SIZE);
        setHasMoreSearchResults(isSearchActive && data.results.length === SEARCH_PAGE_SIZE);
        setErrorMessage(null);
      } catch (error) {
        if (!isMounted) {
          return;
        }
        setTitles([]);
        setHasMoreSearchResults(false);
        setErrorMessage(error instanceof Error ? error.message : "Failed to fetch browse data.");
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    void loadBrowseData();

    return () => {
      isMounted = false;
    };
  }, [isSearchActive, searchText, selectedGenre, selectedReleaseYear]);

  // In search mode, observe a bottom sentinel to auto-load more results while scrolling.
  useEffect(() => {
    if (!isSearchActive || !hasMoreSearchResults) {
      return;
    }

    const sentinelNode = loadMoreSentinelRef.current;
    if (!sentinelNode) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          void loadMoreSearchResults();
        }
      },
      { rootMargin: "220px 0px" },
    );

    observer.observe(sentinelNode);

    return () => {
      observer.disconnect();
    };
  }, [hasMoreSearchResults, isSearchActive, loadMoreSearchResults]);

  return (
    <main className="mx-auto w-full max-w-6xl">
      <div>
        {!isSearchActive && (
          <div className="mb-6">
            <h1 className="text-6xl font-bold tracking-tight md:text-7xl">
              Discover Movies. Follow the People Behind Them.
            </h1>
            <p className="mt-3 text-3xl text-slate-600 dark:text-slate-300">
              Explore any genre, find any contributor, and jump through connected titles.
            </p>
          </div>
        )}
        {isSearchActive && (
          <section className="mb-4 mt-2 flex flex-wrap items-center gap-3 text-sm">
            <span className="font-semibold">Filters:</span>
            <label className="flex items-center gap-2">
              <span className="text-slate-700 dark:text-slate-200">Release Year</span>
              <select
                value={selectedReleaseYear}
                onChange={(event) => setSelectedReleaseYear(event.target.value)}
                className="rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
              >
                <option value="">All years</option>
                {releaseYearOptions.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </label>
            <label className="flex items-center gap-2">
              <span className="text-slate-700 dark:text-slate-200">Genre</span>
              <select
                value={selectedGenre}
                onChange={(event) => setSelectedGenre(event.target.value)}
                className="rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
              >
                <option value="">All genres</option>
                {genreOptions.map((genreOption) => (
                  <option key={genreOption.id} value={String(genreOption.id)}>
                    {genreOption.name}
                  </option>
                ))}
              </select>
            </label>
          </section>
        )}
        <Viewer<TitleItem>
          data={isSearchActive ? titles : titles.slice(0, HORIZONTAL_MAX_ITEMS)}
          isLoading={isLoading}
          errorMessage={errorMessage}
          horizontal={!isSearchActive}
          headingText=""
          emptyStateText={isSearchActive ? "No movies found." : "No movies available."}
          ItemComponent={Movie}
        />
        {isSearchActive && hasMoreSearchResults && !errorMessage && (
          <div ref={loadMoreSentinelRef} className="h-8" />
        )}
        {isSearchActive && isLoadingMore && (
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Loading more results...</p>
        )}
      </div>
    </main>
  );
}

export default HomePage;
