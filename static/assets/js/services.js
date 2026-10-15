/**
 * Rudra Massage & Wellness - Dynamic Services Catalogue Controller
 * Coordinates filter form submissions, search input clearing, and active filter chip removals.
 */

function clearSearchInput() {
  const searchInput = document.getElementById("catalogueSearchInput");
  if (searchInput) {
    searchInput.value = "";
  }
  const form = document.getElementById("catalogueFilterForm");
  if (form) {
    form.submit();
  }
}

function removeActiveFilter(type, val) {
  const form = document.getElementById("catalogueFilterForm");
  if (!form) return;

  if (type === "q") {
    const searchInput = document.getElementById("catalogueSearchInput");
    if (searchInput) searchInput.value = "";
  } else if (type === "category") {
    const categoryInput = document.getElementById("hiddenCategoryInput");
    if (categoryInput) categoryInput.remove();
  } else {
    // Uncheck matching checkboxes across both desktop form and mobile offcanvas
    document.querySelectorAll(`input[name="${type}"][value="${val}"]`).forEach((box) => {
      box.checked = false;
    });
  }

  form.submit();
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("catalogueFilterForm");
  const searchInput = document.getElementById("catalogueSearchInput");

  // Allow pressing Enter in search bar to submit cleanly
  if (searchInput && form) {
    searchInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        form.submit();
      }
    });
  }

  // Sync mobile drawer checkboxes with main form checkboxes on toggle
  const allCheckboxes = document.querySelectorAll(".filter-checkbox");
  allCheckboxes.forEach((box) => {
    box.addEventListener("change", (e) => {
      const name = e.target.name;
      const val = e.target.value;
      const checked = e.target.checked;
      document.querySelectorAll(`.filter-checkbox[name="${name}"][value="${val}"]`).forEach((b) => {
        if (b !== e.target) {
          b.checked = checked;
        }
      });
    });
  });
});
