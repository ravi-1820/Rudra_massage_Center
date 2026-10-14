/**
 * Rudra Massage & Wellness - Main Global Script: Mint Signal Theme
 * Manages sticky header, announcement bar, toast helper, search overlay, and Light/Dark Theme Controller
 */

function escapeToastText(str) {
  if (typeof str !== "string") return String(str || "");
  return str.replace(/[&<>"']/g, s => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[s]));
}

// Global Toast Notification Helper
function showToast(title, message, type = "success") {
  let container = document.getElementById("vedaToastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "vedaToastContainer";
    container.className = "veda-toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  const typeClass = type === "error" ? "toast-error" : (type === "gold" ? "toast-gold" : "toast-success");
  const iconClass = type === "error" ? "bi-exclamation-triangle-fill text-danger" : (type === "gold" ? "bi-award-fill text-warning" : "bi-check-circle-fill text-success");

  toast.className = `veda-toast ${typeClass}`;
  toast.innerHTML = `
    <i class="bi ${iconClass} toast-icon"></i>
    <div class="toast-content">
      <h6>${escapeToastText(title)}</h6>
      <p>${escapeToastText(message)}</p>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(-20px)";
    setTimeout(() => toast.remove(), 300);
  }, 4200);
}

// Theme Controller (Mint Signal Light / Dark Theme)
const ThemeController = {
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

    // Update all toggle buttons
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
    showToast("Theme Updated", `Switched to ${next === "dark" ? "Dark" : "Light"} Mint Signal theme`, "gold");
  },

  init() {
    const theme = this.getPreferredTheme();
    this.applyTheme(theme);

    // Bind event listeners to all theme toggle buttons safely
    document.querySelectorAll(".theme-toggle-btn, #themeToggleBtn").forEach(btn => {
      if (btn._hasThemeListener) return;
      btn._hasThemeListener = true;
      btn.addEventListener("click", () => this.toggle());
    });

    // Listen to OS system preference changes if user hasn't explicitly set a preference
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
        try {
          if (!localStorage.getItem(this.storageKey)) {
            this.applyTheme(e.matches ? "dark" : "light");
          }
        } catch (err) {}
      });
    }
  }
};

window.ThemeController = ThemeController;

// Apply theme immediately on script execution to prevent FOUC
try {
  const initialTheme = ThemeController.getPreferredTheme();
  ThemeController.applyTheme(initialTheme);
} catch (e) {}

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Theme Toggle interactions
  ThemeController.init();

  // Sticky Header Effect with Glassmorphism
  const header = document.querySelector(".site-header");
  if (header) {
    const handleScroll = () => {
      if (window.scrollY > 15) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
  }

  // Dismissible Announcement Bar
  const closeAnnouncement = document.getElementById("closeAnnouncement");
  const announcementBar = document.getElementById("announcementBar");
  if (closeAnnouncement && announcementBar) {
    if (sessionStorage.getItem("hideAnnouncement") === "true") {
      announcementBar.style.display = "none";
    }
    closeAnnouncement.addEventListener("click", () => {
      announcementBar.style.display = "none";
      sessionStorage.setItem("hideAnnouncement", "true");
    });
  }

  // Global Search Modal or Input Trigger
  const globalSearchBtn = document.getElementById("globalSearchBtn");
  if (globalSearchBtn) {
    globalSearchBtn.addEventListener("click", () => {
      const modalEl = document.getElementById("globalSearchModal");
      if (modalEl && typeof bootstrap !== "undefined") {
        const searchModal = bootstrap.Modal.getOrCreateInstance(modalEl);
        searchModal.show();
      }
    });
  }

  // Handle global search form
  const globalSearchForm = document.getElementById("globalSearchForm");
  if (globalSearchForm) {
    globalSearchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const inputEl = document.getElementById("globalSearchInput");
      const query = inputEl ? inputEl.value.trim() : "";
      if (query) {
        window.location.href = `services.html?q=${encodeURIComponent(query)}`;
      }
    });
  }
});
