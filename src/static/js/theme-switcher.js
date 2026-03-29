(() => {
    const STORAGE_KEY = "ostrov-theme";
    const root = document.documentElement;
    const themeColorMeta = document.querySelector('meta[name="theme-color"]');
    const themeButtons = Array.from(document.querySelectorAll("[data-theme-choice]"));
    const colorMap = {
        light: "#f5efe2",
        dark: "#0b1016",
    };
    const mediaQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

    function readPreference() {
        try {
            const stored = window.localStorage.getItem(STORAGE_KEY);
            if (stored === "light" || stored === "dark" || stored === "system") {
                return stored;
            }
        } catch (error) {
        }

        return "system";
    }

    function writePreference(preference) {
        try {
            window.localStorage.setItem(STORAGE_KEY, preference);
        } catch (error) {
        }
    }

    function resolveTheme(preference) {
        if (preference === "light" || preference === "dark") {
            return preference;
        }

        return mediaQuery && mediaQuery.matches ? "dark" : "light";
    }

    function syncButtons(preference) {
        themeButtons.forEach((button) => {
            const isActive = button.dataset.themeChoice === preference;
            button.classList.toggle("is-active", isActive);
            button.setAttribute("aria-pressed", String(isActive));
        });
    }

    function applyTheme(preference) {
        const resolvedTheme = resolveTheme(preference);

        root.dataset.themePreference = preference;
        root.dataset.resolvedTheme = resolvedTheme;

        if (preference === "system") {
            root.removeAttribute("data-theme");
        } else {
            root.dataset.theme = preference;
        }

        if (themeColorMeta) {
            themeColorMeta.setAttribute("content", colorMap[resolvedTheme]);
        }

        syncButtons(preference);
    }

    function setPreference(preference) {
        writePreference(preference);
        applyTheme(preference);
    }

    themeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            setPreference(button.dataset.themeChoice || "system");
        });
    });

    if (mediaQuery) {
        const handleSystemThemeChange = () => {
            if (readPreference() === "system") {
                applyTheme("system");
            }
        };

        if (typeof mediaQuery.addEventListener === "function") {
            mediaQuery.addEventListener("change", handleSystemThemeChange);
        } else if (typeof mediaQuery.addListener === "function") {
            mediaQuery.addListener(handleSystemThemeChange);
        }
    }

    applyTheme(readPreference());
})();
