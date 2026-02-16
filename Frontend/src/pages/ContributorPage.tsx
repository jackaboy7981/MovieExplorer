import { useEffect, useMemo, useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import { fetchContributorDetails } from "../api/contributorApi";
import contributorImage from "../assets/contributor.jpg";
import Movie from "../components/Movie";
import Viewer from "../components/Viewer";
import type { ContributorDetailsResponse } from "../models/Contributor";
import type { TitleItem } from "../models/Title";

function ContributorPage() {
  const { id } = useParams();
  const numericId = Number(id);
  const [contributorData, setContributorData] = useState<ContributorDetailsResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadContributorData = async () => {
      try {
        const data = await fetchContributorDetails(numericId);
        if (!isMounted) {
          return;
        }
        setContributorData(data);
        setErrorMessage(null);
      } catch (error) {
        if (!isMounted) {
          return;
        }
        setContributorData(null);
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to fetch contributor data.",
        );
      } finally {
        if (!isMounted) {
          return;
        }
        setIsLoading(false);
      }
    };

    void loadContributorData();

    return () => {
      isMounted = false;
    };
  }, [numericId]);

  if (!id || Number.isNaN(numericId) || numericId <= 0) {
    return <Navigate to="/" replace />;
  }

  const contributions = useMemo(() => {
    const uniqueRoles = new Set(
      (contributorData?.titles ?? []).flatMap((title) => title.roles ?? []),
    );
    return [...uniqueRoles];
  }, [contributorData]);

  const workedMovies: TitleItem[] = contributorData?.titles ?? [];

  return (
    <main className="mx-auto w-full max-w-6xl">
      <div>
        <img
          className="h-[420px] w-full rounded-2xl object-cover shadow-md shadow-slate-300/50 dark:shadow-black/30"
          src={contributorImage}
          alt={`${contributorData?.name ?? "Contributor"} profile`}
        />
        <h1 className="mt-4 text-3xl font-semibold tracking-tight">
          {contributorData?.name ?? "Contributor Page"}
        </h1>
        <div className="mt-2 text-sm text-slate-700 dark:text-slate-300">
          <span className="font-semibold">Contributions:</span>{" "}
          {contributions.length > 0 ? contributions.join(", ") : "Not available"}
        </div>
        <Viewer<TitleItem>
          data={workedMovies}
          isLoading={isLoading}
          errorMessage={errorMessage}
          headingText="Movies worked on will be displayed here on screen."
          ItemComponent={Movie}
        />
      </div>
    </main>
  );
}

export default ContributorPage;
