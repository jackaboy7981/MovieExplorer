import { useState } from "react";
import type { FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";

interface TopBarProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
  onSearch: (searchText: string) => void;
  onClearSearch: () => void;
}

function TopBar({ theme, onToggleTheme, onSearch, onClearSearch }: TopBarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const showHomeButton = location.pathname !== "/" && location.pathname !== "/home";
  const [searchInput, setSearchInput] = useState<string>("");
  const trimmedSearchInput = searchInput.trim();

  const handleSearchSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSearch(searchInput);
  };

  const handleSearchInputChange = (nextValue: string) => {
    setSearchInput(nextValue);
    if (nextValue.trim() === "") {
      onClearSearch();
    }
  };

  return (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-900/90">
      <div className="relative mx-auto flex max-w-6xl items-center justify-center px-4 py-3">
        <div className="absolute left-4 flex items-center gap-2">
          <button
            type="button"
            onClick={onToggleTheme}
            className="min-w-[96px] rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
          >
            {theme === "dark" ? "Light mode" : "Dark mode"}
          </button>
          {showHomeButton && (
            <button
              type="button"
              onClick={() => navigate("/")}
              className="min-w-[72px] rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
            >
              Home
            </button>
          )}
        </div>

        <form
          className="flex w-full max-w-md items-center gap-2"
          onSubmit={handleSearchSubmit}
        >
          <input
            type="search"
            placeholder="Search"
            value={searchInput}
            onChange={(event) => handleSearchInputChange(event.target.value)}
            className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 outline-none ring-0 focus:border-slate-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:placeholder:text-slate-400 dark:focus:border-slate-500"
          />
          <button
            type="submit"
            disabled={!trimmedSearchInput}
            className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
          >
            Go
          </button>
        </form>
      </div>
    </header>
  );
}

export default TopBar;
