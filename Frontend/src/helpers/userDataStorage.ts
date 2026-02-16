const USER_SETTINGS_STORAGE_KEY = "user_settings";

export type ThemeMode = "light" | "dark";

interface StoredUserSettings {
  theme_mode: 0 | 1;
}

export function getInitialTheme(): ThemeMode {
  const rawSettings = localStorage.getItem(USER_SETTINGS_STORAGE_KEY);
  if (!rawSettings) {
    return "light";
  }

  try {
    const parsed = JSON.parse(rawSettings) as Partial<StoredUserSettings>;
    return parsed.theme_mode === 1 ? "dark" : "light";
  } catch {
    return "light";
  }
}

export function persistTheme(theme: ThemeMode): void {
  const settings: StoredUserSettings = { theme_mode: theme === "dark" ? 1 : 0 };
  localStorage.setItem(USER_SETTINGS_STORAGE_KEY, JSON.stringify(settings));
}
