/**
 * Rudra Massage & Wellness - Catalogue Multi-Filter Engine
 * Multi-criteria dynamic filtering, keyword search, chips, sorting, and pagination
 */

class CatalogueEngine {
  constructor() {
    this.products = typeof WELLNESS_PRODUCTS !== "undefined" ? [...WELLNESS_PRODUCTS] : [];
    this.filteredProducts = [...this.products];
    this.activeFilters = {
      search: "",
      needs: new Set(),
      bodyParts: new Set(),
      types: new Set(),
      usages: new Set(),
      sortBy: "featured"
    };

    this.itemsPerPage = 9;
    this.currentPage = 1;

    this.init();
  }

  init() {
    this.readUrlParams();
    this.bindEvents();
    this.applyFilters();
  }

  readUrlParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has("q")) {
      this.activeFilters.search = params.get("q").trim();
      const searchInput = document.getElementById("catalogueSearchInput");
      if (searchInput) searchInput.value = this.activeFilters.search;
    }
    if (params.has("need")) {
      this.activeFilters.needs.add(params.get("need"));
    }
    if (params.has("category")) {
      this.activeFilters.types.add(params.get("category"));
    }
    if (params.has("body")) {
      this.activeFilters.bodyParts.add(params.get("body"));
    }
    if (params.has("usage")) {
      this.activeFilters.usages.add(params.get("usage"));
    }
    this.syncCheckboxesWithState();
  }

  syncCheckboxesWithState() {
    document.querySelectorAll(".filter-checkbox").forEach(box => {
      const type = box.dataset.filterType;
      const val = box.value;
      if (type === "need" && this.activeFilters.needs.has(val)) box.checked = true;
      if (type === "body" && this.activeFilters.bodyParts.has(val)) box.checked = true;
      if (type === "type" && this.activeFilters.types.has(val)) box.checked = true;
      if (type === "usage" && this.activeFilters.usages.has(val)) box.checked = true;
    });
  }

  bindEvents() {
    // Search input & clear button
    const searchInput = document.getElementById("catalogueSearchInput");
    const clearSearchBtn = document.getElementById("clearSearchBtn");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.activeFilters.search = e.target.value.trim();
        this.currentPage = 1;
        this.applyFilters();
        if (clearSearchBtn) {
          clearSearchBtn.style.display = this.activeFilters.search ? "block" : "none";
        }
      });
    }

    if (clearSearchBtn) {
      clearSearchBtn.addEventListener("click", () => {
        if (searchInput) searchInput.value = "";
        this.activeFilters.search = "";
        clearSearchBtn.style.display = "none";
        this.currentPage = 1;
        this.applyFilters();
      });
    }

    // Checkboxes (desktop & mobile offcanvas)
    document.querySelectorAll(".filter-checkbox").forEach(box => {
      box.addEventListener("change", (e) => {
        const fType = e.target.dataset.filterType;
        const val = e.target.value;

        if (fType === "need") {
          e.target.checked ? this.activeFilters.needs.add(val) : this.activeFilters.needs.delete(val);
        } else if (fType === "body") {
          e.target.checked ? this.activeFilters.bodyParts.add(val) : this.activeFilters.bodyParts.delete(val);
        } else if (fType === "type") {
          e.target.checked ? this.activeFilters.types.add(val) : this.activeFilters.types.delete(val);
        } else if (fType === "usage") {
          e.target.checked ? this.activeFilters.usages.add(val) : this.activeFilters.usages.delete(val);
        }

        // Mirror check states if duplicated in mobile offcanvas
        document.querySelectorAll(`.filter-checkbox[data-filter-type="${fType}"][value="${val}"]`).forEach(b => {
          b.checked = e.target.checked;
        });

        this.currentPage = 1;
        this.applyFilters();
      });
    });

    // Sort by dropdown
    const sortSelect = document.getElementById("sortProductsSelect");
    if (sortSelect) {
      sortSelect.addEventListener("change", (e) => {
        this.activeFilters.sortBy = e.target.value;
        this.applyFilters();
      });
    }

    // Clear all filters button
    const clearAllBtn = document.getElementById("clearAllFiltersBtn");
    if (clearAllBtn) {
      clearAllBtn.addEventListener("click", () => this.clearAllFilters());
    }
  }

  clearAllFilters() {
    this.activeFilters.search = "";
    this.activeFilters.needs.clear();
    this.activeFilters.bodyParts.clear();
    this.activeFilters.types.clear();
    this.activeFilters.usages.clear();
    this.activeFilters.sortBy = "featured";

    const searchInput = document.getElementById("catalogueSearchInput");
    if (searchInput) searchInput.value = "";

    document.querySelectorAll(".filter-checkbox").forEach(box => box.checked = false);

    const sortSelect = document.getElementById("sortProductsSelect");
    if (sortSelect) sortSelect.value = "featured";

    this.currentPage = 1;
    this.applyFilters();
  }

  applyFilters() {
    const q = this.activeFilters.search.toLowerCase();

    this.filteredProducts = this.products.filter(item => {
      // Search matching
      if (q) {
        const matchName = item.name.toLowerCase().includes(q);
        const matchDesc = item.description.toLowerCase().includes(q);
        const matchCat = item.category.toLowerCase().includes(q);
        const matchNeed = item.need.toLowerCase().includes(q);
        const matchTag = item.tags && item.tags.some(t => t.toLowerCase().includes(q));
        if (!matchName && !matchDesc && !matchCat && !matchNeed && !matchTag) return false;
      }

      // Need filter
      if (this.activeFilters.needs.size > 0 && !this.activeFilters.needs.has(item.need)) {
        return false;
      }

      // Body part filter
      if (this.activeFilters.bodyParts.size > 0 && !this.activeFilters.bodyParts.has(item.bodyPart)) {
        return false;
      }

      // Product Type filter
      if (this.activeFilters.types.size > 0 && !this.activeFilters.types.has(item.category)) {
        return false;
      }

      // Usage filter
      if (this.activeFilters.usages.size > 0 && !this.activeFilters.usages.has(item.usage)) {
        return false;
      }

      return true;
    });

    // Apply Sorting
    this.sortFilteredProducts();

    // Render active chips
    this.renderActiveFilterChips();

    // Render Products Grid & Result Count
    this.renderProducts();
  }

  sortFilteredProducts() {
    const sort = this.activeFilters.sortBy;
    if (sort === "price-asc") {
      this.filteredProducts.sort((a, b) => a.price - b.price);
    } else if (sort === "price-desc") {
      this.filteredProducts.sort((a, b) => b.price - a.price);
    } else if (sort === "rating") {
      this.filteredProducts.sort((a, b) => b.rating - a.rating);
    } else if (sort === "reviews") {
      this.filteredProducts.sort((a, b) => b.reviewsCount - a.reviewsCount);
    }
  }

  renderActiveFilterChips() {
    const chipsContainer = document.getElementById("activeFilterChips");
    if (!chipsContainer) return;

    chipsContainer.innerHTML = "";
    const activeList = [];

    if (this.activeFilters.search) {
      activeList.push({ label: `"${this.activeFilters.search}"`, type: "search" });
    }
    this.activeFilters.needs.forEach(val => activeList.push({ label: val, type: "need", val }));
    this.activeFilters.bodyParts.forEach(val => activeList.push({ label: val, type: "body", val }));
    this.activeFilters.types.forEach(val => activeList.push({ label: val, type: "type", val }));
    this.activeFilters.usages.forEach(val => activeList.push({ label: val, type: "usage", val }));

    if (activeList.length === 0) {
      chipsContainer.style.display = "none";
      return;
    }

    chipsContainer.style.display = "flex";

    activeList.forEach(item => {
      const chip = document.createElement("span");
      chip.className = "filter-chip";
      const safeLabel = String(item.label).replace(/[&<>"']/g, s => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[s]));
      chip.innerHTML = `
        ${safeLabel}
        <button type="button" class="filter-chip-remove" aria-label="Remove filter">&times;</button>
      `;

      chip.querySelector("button").addEventListener("click", () => {
        if (item.type === "search") {
          this.activeFilters.search = "";
          const searchInput = document.getElementById("catalogueSearchInput");
          if (searchInput) searchInput.value = "";
        } else if (item.type === "need") {
          this.activeFilters.needs.delete(item.val);
        } else if (item.type === "body") {
          this.activeFilters.bodyParts.delete(item.val);
        } else if (item.type === "type") {
          this.activeFilters.types.delete(item.val);
        } else if (item.type === "usage") {
          this.activeFilters.usages.delete(item.val);
        }
        this.syncCheckboxesWithState();
        this.applyFilters();
      });

      chipsContainer.appendChild(chip);
    });
  }

  renderProducts() {
    const grid = document.getElementById("catalogueGrid");
    const countEl = document.getElementById("resultCount");
    const emptyState = document.getElementById("emptyStateContainer");
    const paginationContainer = document.getElementById("cataloguePagination");

    if (countEl) {
      countEl.textContent = `${this.filteredProducts.length} Solutions Found`;
    }

    if (!grid) return;

    if (this.filteredProducts.length === 0) {
      grid.innerHTML = "";
      if (emptyState) emptyState.classList.remove("d-none");
      if (paginationContainer) paginationContainer.classList.add("d-none");
      return;
    }

    if (emptyState) emptyState.classList.add("d-none");

    // Slice for pagination
    const totalPages = Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    const startIdx = (this.currentPage - 1) * this.itemsPerPage;
    const endIdx = startIdx + this.itemsPerPage;
    const pageItems = this.filteredProducts.slice(startIdx, endIdx);

    grid.innerHTML = pageItems.map(p => this.createProductCardHtml(p)).join("");

    // Render pagination
    if (paginationContainer) {
      if (totalPages > 1) {
        paginationContainer.classList.remove("d-none");
        let html = `<ul class="pagination justify-content-center mb-0">`;
        html += `<li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                   <button class="page-link" onclick="window.catalogueApp.goToPage(${this.currentPage - 1})">Previous</button>
                 </li>`;
        for (let i = 1; i <= totalPages; i++) {
          html += `<li class="page-item ${this.currentPage === i ? 'active' : ''}">
                     <button class="page-link" onclick="window.catalogueApp.goToPage(${i})">${i}</button>
                   </li>`;
        }
        html += `<li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                   <button class="page-link" onclick="window.catalogueApp.goToPage(${this.currentPage + 1})">Next</button>
                 </li></ul>`;
        paginationContainer.innerHTML = html;
      } else {
        paginationContainer.classList.add("d-none");
      }
    }
  }

  goToPage(page) {
    this.currentPage = page;
    this.renderProducts();
    window.scrollTo({ top: 200, behavior: 'smooth' });
  }

  createProductCardHtml(product) {
    const formattedPrice = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(product.price);
    const formattedOriginal = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(product.originalPrice);
    const discountPercent = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);

    return `
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="product-card">
          <div class="product-image-box">
            <span class="product-badge-float badge-custom badge-forest">${product.badge}</span>
            <span class="product-category-tag">${product.category}</span>
            <img src="${product.image}" alt="${product.name}" loading="lazy">
          </div>
          <div class="product-body">
            <div class="product-rating">
              <span class="rating-stars">
                <i class="bi bi-star-fill"></i> ${product.rating}
              </span>
              <span>(${product.reviewsCount} reviews)</span>
            </div>
            <h4 class="product-title" title="${product.name}">${product.name}</h4>
            <p class="product-desc">${product.shortDesc}</p>
            <div class="product-tags-row">
              <span class="product-tag-pill"><i class="bi bi-geo-alt-fill me-1"></i>${product.bodyPart}</span>
              <span class="product-tag-pill"><i class="bi bi-heart-pulse-fill me-1"></i>${product.need}</span>
              <span class="product-tag-pill">${product.usage}</span>
            </div>
            <div class="product-price-row">
              <span class="current-price">${formattedPrice}</span>
              <span class="original-price">${formattedOriginal}</span>
              <span class="price-save">${discountPercent}% OFF</span>
            </div>
            <div class="product-actions-row">
              <a href="service-detail.html?id=${product.id}" class="btn-veda-outline btn-veda-sm text-center">
                View Details
              </a>
              <a href="enquiry.html?service=${product.id}" class="btn-veda-gold btn-veda-sm text-center">
                Enquire Now
              </a>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

// Global initialization on catalogue page
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("catalogueGrid")) {
    window.catalogueApp = new CatalogueEngine();
  }
});
