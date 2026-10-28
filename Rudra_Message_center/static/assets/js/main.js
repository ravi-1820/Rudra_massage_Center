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
  const normType = (type || "success").toLowerCase();
  let typeClass = "toast-success";
  let iconClass = "bi-check-circle-fill text-success";

  if (normType === "error" || normType === "danger") {
    typeClass = "toast-error";
    iconClass = "bi-exclamation-triangle-fill text-danger";
  } else if (normType === "gold" || normType === "warning") {
    typeClass = "toast-gold";
    iconClass = "bi-award-fill text-warning";
  } else if (normType === "info") {
    typeClass = "toast-info";
    iconClass = "bi-info-circle-fill text-primary";
  }

  toast.className = `veda-toast ${typeClass}`;
  toast.setAttribute("role", "alert");
  toast.innerHTML = `
    <i class="bi ${iconClass} toast-icon"></i>
    <div class="toast-content">
      <h6>${escapeToastText(title)}</h6>
      <p>${escapeToastText(message)}</p>
    </div>
    <button type="button" class="toast-close-btn" aria-label="Close">
      <i class="bi bi-x-lg"></i>
    </button>
  `;

  let removeTimer;
  const dismiss = () => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(-20px)";
    setTimeout(() => {
      if (toast.parentElement) toast.remove();
    }, 300);
  };

  const closeBtn = toast.querySelector(".toast-close-btn");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      clearTimeout(removeTimer);
      dismiss();
    });
  }

  toast.addEventListener("mouseenter", () => clearTimeout(removeTimer));
  toast.addEventListener("mouseleave", () => {
    removeTimer = setTimeout(dismiss, 3000);
  });

  container.appendChild(toast);
  removeTimer = setTimeout(dismiss, 4500);
}

window.showToast = showToast;


// Theme Controller (Enforcing Light Theme)
const ThemeController = {
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

window.ThemeController = ThemeController;

try {
  ThemeController.applyTheme();
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
        window.location.href = `/services/?q=${encodeURIComponent(query)}`;
      }
    });
  }

});
