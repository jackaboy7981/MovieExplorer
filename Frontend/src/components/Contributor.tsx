import { Link } from "react-router-dom";

import contributorImage from "../assets/contributor.jpg";
import type { ContributorItem } from "../models/Contributor";

interface ContributorProps {
  item: ContributorItem;
}

function Contributor({ item }: ContributorProps) {
  return (
    <article className="min-w-[140px]">
      <Link to={`/contributor/${item.id}`} className="block rounded-xl">
        <img
          className="block h-[200px] w-full rounded-xl object-cover shadow-sm shadow-slate-300/50 transition hover:opacity-90 dark:shadow-black/30"
          src={contributorImage}
          alt={`${item.name} profile`}
        />
        <p className="mt-2 line-clamp-2 text-sm font-bold hover:underline">{item.name}</p>
        <div className="mt-1 text-xs text-slate-600 dark:text-slate-300">
          {item.roles.length > 0 ? item.roles.join(", ") : "Role not available"}
        </div>
      </Link>
    </article>
  );
}

export default Contributor;
