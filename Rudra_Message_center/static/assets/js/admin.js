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

// Theme Controller for Admin Portal (Enforcing Light Theme)
const AdminThemeController = {
  applyTheme() {
    try {
      localStorage.removeItem("rudra_theme");
    } catch (e) {}
    document.documentElement.classList.remove("dark");
    document.documentElement.setAttribute("data-theme", "light");
  },

  init() {
    this.applyTheme();
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
