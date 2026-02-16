import { useEffect, useState } from "react";
import { Navigate, Route, Routes, useNavigate } from "react-router-dom";

import TopBar from "./components/TopBar";
import { getInitialTheme, persistTheme, type ThemeMode } from "./helpers/userDataStorage";
import ContributorPage from "./pages/ContributorPage";
import HomePage from "./pages/HomePage";
import MoviePage from "./pages/MoviePage";

function App() {
  const navigate = useNavigate();
  const [theme, setTheme] = useState<ThemeMode>(() => getInitialTheme());
  const [homeSearchText, setHomeSearchText] = useState<string | null>(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    persistTheme(theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "dark" ? "light" : "dark"));
  };

  const handleSearch = (rawSearchText: string) => {
    const trimmedSearchText = rawSearchText.trim();
    if (!trimmedSearchText) {
      setHomeSearchText(null);
      navigate("/");
      return;
    }

    setHomeSearchText(trimmedSearchText);
    navigate("/");
  };

  const handleClearSearch = () => {
    setHomeSearchText(null);
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100">
      <TopBar
        theme={theme}
        onToggleTheme={toggleTheme}
        onSearch={handleSearch}
        onClearSearch={handleClearSearch}
      />
      <div className="px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage searchText={homeSearchText} />} />
          <Route path="/home" element={<HomePage searchText={homeSearchText} />} />
          <Route path="/movie" element={<Navigate to="/" replace />} />
          <Route path="/movie/:id" element={<MoviePage />} />
          <Route path="/contributor" element={<Navigate to="/" replace />} />
          <Route path="/contributor/:id" element={<ContributorPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
