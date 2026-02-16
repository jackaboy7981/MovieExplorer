import { Link } from "react-router-dom";

import type { TitleItem } from "../models/Title";
import filmPoster from "../assets/film.png";

interface MovieProps {
  item: TitleItem;
}

function Movie({ item }: MovieProps) {
  return (
    <article className="min-w-[140px]">
      <Link to={`/movie/${item.id}`} className="block rounded-xl">
        <img
          className="block h-[200px] w-full rounded-xl object-cover shadow-sm shadow-slate-300/50 transition hover:opacity-90 dark:shadow-black/30"
          src={filmPoster}
          alt={`${item.title} poster`}
        />
        <p className="mt-2 line-clamp-2 text-sm font-medium hover:underline">{item.title}</p>
      </Link>
    </article>
  );
}

export default Movie;
