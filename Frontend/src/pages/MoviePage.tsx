import { useEffect, useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import { fetchTitleDetails } from "../api/titleApi";
import filmPoster from "../assets/film.png";
import Contributor from "../components/Contributor";
import Viewer from "../components/Viewer";
import type { ContributorItem } from "../models/Contributor";
import type { TitleDetailsResponse } from "../models/Title";

function MoviePage() {
  const { id } = useParams();
  const numericId = Number(id);
  const [titleData, setTitleData] = useState<TitleDetailsResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadTitleData = async () => {
      try {
        const data = await fetchTitleDetails(numericId);
        if (!isMounted) {
          return;
        }
        setTitleData(data);
        setErrorMessage(null);
      } catch (error) {
        if (!isMounted) {
          return;
        }
        setTitleData(null);
        setErrorMessage(error instanceof Error ? error.message : "Failed to fetch title data.");
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    void loadTitleData();

    return () => {
      isMounted = false;
    };
  }, [numericId]);

  if (!id || Number.isNaN(numericId) || numericId <= 0) {
    return <Navigate to="/" replace />;
  }

  return (
    <main className="mx-auto w-full max-w-6xl">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">{titleData?.title ?? "Movie Page"}</h1>
        <img
          className="mt-4 h-[420px] w-full rounded-2xl object-cover shadow-md shadow-slate-300/50 dark:shadow-black/30"
          src={filmPoster}
          alt={`${titleData?.title ?? "Movie"} poster`}
        />
        <div className="mt-3 text-sm text-slate-700 dark:text-slate-300">
          <span className="font-semibold">Genres:</span>{" "}
          {titleData?.genres && titleData.genres.length > 0
            ? titleData.genres.join(", ")
            : "Not available"}
        </div>
        <div className="mt-1 text-sm text-slate-700 dark:text-slate-300">
          <span className="font-semibold">Release Year:</span>{" "}
          {titleData?.release_year ?? "Not available"}
        </div>
        <Viewer<ContributorItem>
          data={titleData?.contributors ?? []}
          isLoading={isLoading}
          errorMessage={errorMessage}
          headingText="Contributors"
          ItemComponent={Contributor}
        />
      </div>
    </main>
  );
}

export default MoviePage;
