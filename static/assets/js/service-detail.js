/**
 * Rudra Massage & Wellness - Service / Product Detail Controller
 * Loads product details from URL param '?id=...', handles thumbnail gallery,
 * safety precautions, specs table, and related services recommendations.
 */

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const rawId = urlParams.get("id");
  const productId = rawId || "wt-101";

  if (typeof WELLNESS_PRODUCTS === "undefined" || WELLNESS_PRODUCTS.length === 0) return;

  const foundProduct = WELLNESS_PRODUCTS.find(p => p.id === productId);
  const product = foundProduct || WELLNESS_PRODUCTS[0];

  // If a specific ID was passed in URL that does not exist, notify user gracefully
  if (rawId && !foundProduct) {
    const detailContainer = document.querySelector(".service-detail-section .container") || document.querySelector("main .container");
    if (detailContainer) {
      const alertDiv = document.createElement("div");
      alertDiv.className = "alert alert-warning alert-dismissible fade show mb-4 rounded-3 border shadow-sm";
      alertDiv.setAttribute("role", "alert");
      alertDiv.innerHTML = `
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-exclamation-triangle-fill fs-5 text-warning"></i>
          <div>
            <strong>Product Not Found:</strong> The requested item <code>${escapeHtml(rawId)}</code> does not exist in our catalogue. Displaying our flagship solution <strong>${escapeHtml(product.name)}</strong> below.
            <a href="/services/" class="alert-link ms-2">Back to Catalogue &rarr;</a>
          </div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      detailContainer.prepend(alertDiv);
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, s => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[s]));
  }

  // Set Page Titles & Breadcrumbs
  document.title = `${product.name} | Rudra Massage & Wellness`;
  const breadcrumbCurrent = document.getElementById("breadcrumbCurrentProduct");
  if (breadcrumbCurrent) breadcrumbCurrent.textContent = product.name;

  // Basic Information
  const titleEl = document.getElementById("detailTitle");
  if (titleEl) titleEl.textContent = product.name;

  const badgeEl = document.getElementById("detailBadge");
  if (badgeEl) badgeEl.textContent = product.badge;

  const categoryEl = document.getElementById("detailCategory");
  if (categoryEl) categoryEl.textContent = product.category;

  const ratingEl = document.getElementById("detailRating");
  if (ratingEl) ratingEl.innerHTML = `<i class="bi bi-star-fill text-warning me-1"></i>${product.rating} (${product.reviewsCount} verified reviews)`;

  const shortDescEl = document.getElementById("detailShortDesc");
  if (shortDescEl) shortDescEl.textContent = product.shortDesc;

  const fullDescEl = document.getElementById("detailFullDesc");
  if (fullDescEl) fullDescEl.textContent = product.description;

  // Pricing
  const formattedPrice = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(product.price);
  const formattedOriginal = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(product.originalPrice);
  const discountPercent = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);

  const priceEl = document.getElementById("detailPrice");
  if (priceEl) priceEl.textContent = formattedPrice;

  const originalPriceEl = document.getElementById("detailOriginalPrice");
  if (originalPriceEl) originalPriceEl.textContent = formattedOriginal;

  const discountEl = document.getElementById("detailDiscount");
  if (discountEl) discountEl.textContent = `${discountPercent}% OFF`;

  // Gallery Main Image & Thumbnails
  const mainImg = document.getElementById("detailMainImage");
  if (mainImg) {
    mainImg.src = product.image;
    mainImg.alt = product.name;
  }

  const thumbContainer = document.getElementById("detailThumbnails");
  if (thumbContainer && product.thumbnails) {
    thumbContainer.innerHTML = product.thumbnails.map((thumbUrl, idx) => `
      <div class="thumb-item ${idx === 0 ? 'active' : ''}" style="width: 72px; height: 72px; border-radius: 8px; overflow: hidden; cursor: pointer; border: 2px solid ${idx === 0 ? 'var(--color-primary)' : 'var(--color-border)'};">
        <img src="${thumbUrl}" alt="Thumbnail ${idx + 1}" style="width: 100%; height: 100%; object-fit: cover;">
      </div>
    `).join("");

    thumbContainer.querySelectorAll(".thumb-item").forEach(item => {
      item.addEventListener("click", () => {
        thumbContainer.querySelectorAll(".thumb-item").forEach(t => {
          t.classList.remove("active");
          t.style.borderColor = "var(--color-border)";
        });
        item.classList.add("active");
        item.style.borderColor = "var(--color-primary)";
        if (mainImg) {
          mainImg.src = item.querySelector("img").src;
        }
      });
    });
  }

  // Key Features List
  const featuresList = document.getElementById("detailFeaturesList");
  if (featuresList && product.features) {
    featuresList.innerHTML = product.features.map(f => `
      <li class="d-flex align-items-start gap-3 mb-3">
        <i class="bi bi-check-circle-fill text-success fs-5 mt-1"></i>
        <span>${f}</span>
      </li>
    `).join("");
  }

  // Specifications Table
  const specsTbody = document.getElementById("detailSpecsBody");
  if (specsTbody && product.specifications) {
    specsTbody.innerHTML = Object.entries(product.specifications).map(([key, val]) => `
      <tr>
        <th class="py-2 text-muted fw-semibold" style="width: 35%;">${key}</th>
        <td class="py-2 fw-medium">${val}</td>
      </tr>
    `).join("");
  }

  // Precautions & Safety
  const precautionsEl = document.getElementById("detailPrecautions");
  if (precautionsEl && product.precautions) {
    precautionsEl.textContent = product.precautions;
  }

  // Tags & Quick Meta
  const tagsContainer = document.getElementById("detailTags");
  if (tagsContainer && product.tags) {
    tagsContainer.innerHTML = product.tags.map(tag => `
      <span class="badge-custom badge-sage me-2 mb-2">${tag}</span>
    `).join("");
  }

  // Pre-fill CTAs
  const enquireBtn = document.getElementById("detailEnquireBtn");
  if (enquireBtn) {
    enquireBtn.href = `/enquiry/?service=${product.id}`;
  }

  const demoBtn = document.getElementById("detailDemoBtn");
  if (demoBtn) {
    demoBtn.href = `/appointment/?service=${product.id}`;
  }

  // Render Related Products
  const relatedContainer = document.getElementById("relatedProductsGrid");
  if (relatedContainer) {
    const related = WELLNESS_PRODUCTS.filter(p => p.id !== product.id && (p.need === product.need || p.category === product.category)).slice(0, 3);
    if (related.length > 0) {
      relatedContainer.innerHTML = related.map(p => `
        <div class="col-md-4 mb-4">
          <div class="product-card">
            <div class="product-image-box">
              <span class="product-badge-float badge-custom badge-forest">${p.badge}</span>
              <img src="${p.image}" alt="${p.name}" loading="lazy">
            </div>
            <div class="product-body">
              <h5 class="product-title">${p.name}</h5>
              <p class="product-desc">${p.shortDesc}</p>
              <div class="product-price-row">
                <span class="current-price">₹${p.price.toLocaleString('en-IN')}</span>
                <span class="price-save">${p.need}</span>
              </div>
              <div class="product-actions-row">
                <a href="/service-detail/?id=${p.id}" class="btn-veda-outline btn-veda-sm text-center">View</a>
                <a href="/appointment/?service=${p.id}" class="btn-veda-gold btn-veda-sm text-center">Book Appointment</a>
              </div>
            </div>
          </div>
        </div>
      `).join("");
    }
  }
});
