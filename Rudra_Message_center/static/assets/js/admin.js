/**
 * Rudra Massage & Wellness Admin Console Controller
 * Handles theme toggling, responsive sidebar, and UI helpers.
 * Fully database-driven: no mock customer data or client-side storage overrides.
 */

// Flush legacy prototype mock data from previous sessions
(function cleanLegacyStorage() {
  const legacyKeys = ["admin_services", "admin_enquiries", "admin_appointments", "admin_offers"];
  legacyKeys.forEach(k => {
    try {
      localStorage.removeItem(k);
    } catch (e) {}
  });
})();

// Theme Controller for Admin Portal (Mint Signal)
const AdminThemeController = {
  storageKey: "rudra_theme",

  getPreferredTheme() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored === "dark" || stored === "light") return stored;
      if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        return "dark";
      }
    } catch (e) {
      console.warn("Storage access failed for theme preference:", e);
    }
    return "light";
  },

  applyTheme(theme) {
    const isDark = theme === "dark";
    if (isDark) {
      document.documentElement.classList.add("dark");
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      document.documentElement.setAttribute("data-theme", "light");
    }

    document.querySelectorAll(".theme-toggle-btn, #themeToggleBtn").forEach(btn => {
      btn.innerHTML = isDark ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars"></i>';
      btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
      btn.setAttribute("title", isDark ? "Switch to light mode" : "Switch to dark mode");
    });
  },

  setTheme(theme) {
    try {
      localStorage.setItem(this.storageKey, theme);
    } catch (e) {
      console.warn("Unable to save theme to localStorage:", e);
    }
    this.applyTheme(theme);
  },

  toggle() {
    const current = document.documentElement.classList.contains("dark") ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    this.setTheme(next);
    if (typeof showToast === "function") {
      showToast("Theme Updated", `Switched to ${next === "dark" ? "Dark" : "Light"} Mint Signal theme`, "gold");
    }
  },

  init() {
    if (window.ThemeController) {
      window.ThemeController.init();
      return;
    }
    const theme = this.getPreferredTheme();
    this.applyTheme(theme);

    document.querySelectorAll(".theme-toggle-btn, #themeToggleBtn").forEach(btn => {
      if (btn._hasThemeListener) return;
      btn._hasThemeListener = true;
      btn.addEventListener("click", () => this.toggle());
    });
  }
};

try {
  AdminThemeController.applyTheme(AdminThemeController.getPreferredTheme());
} catch (e) {}

class AdminController {
  constructor() {
    this.init();
  }

  init() {
    AdminThemeController.init();
    this.setupSidebarToggle();
  }

  setupSidebarToggle() {
    const toggleBtn = document.getElementById("adminSidebarToggle");
    const sidebar = document.querySelector(".admin-sidebar");
    const closeBtn = document.getElementById("adminSidebarClose");

    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("show");
      });
    }

    if (closeBtn && sidebar) {
      closeBtn.addEventListener("click", () => {
        sidebar.classList.remove("show");
      });
    }

    // Close on mobile when navigating
    document.querySelectorAll(".admin-sidebar-nav .nav-link").forEach(link => {
      link.addEventListener("click", () => {
        if (sidebar && window.innerWidth < 992) {
          sidebar.classList.remove("show");
        }
      });
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector(".admin-layout")) {
    window.adminApp = new AdminController();
  }
});
