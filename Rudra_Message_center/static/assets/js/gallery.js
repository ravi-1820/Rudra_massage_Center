/**
 * Rudra Massage & Wellness - Gallery Filter & Lightbox Viewer
 */

document.addEventListener("DOMContentLoaded", () => {
  const filterBtns = document.querySelectorAll(".gallery-filter-btn, .gallery-filter-pill");
  const galleryItems = document.querySelectorAll(".gallery-item-wrap");
  const lightbox = document.getElementById("galleryLightbox");
  const lightboxImg = document.getElementById("lightboxImage");
  const lightboxTitle = document.getElementById("lightboxTitle");
  const lightboxClose = document.getElementById("lightboxClose");

  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove("active");
      document.body.style.overflow = "";
    }
  }

  // Filter Buttons
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.dataset.filter;

      galleryItems.forEach(item => {
        if (filter === "all" || item.dataset.category === filter) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  // Lightbox Interaction
  document.querySelectorAll(".gallery-item").forEach(item => {
    item.addEventListener("click", () => {
      const img = item.querySelector("img");
      const title = item.querySelector(".gallery-caption");

      if (lightbox && lightboxImg) {
        lightboxImg.src = img.src;
        if (lightboxTitle && title) lightboxTitle.textContent = title.textContent;
        lightbox.classList.add("active");
        document.body.style.overflow = "hidden";
      }
    });
  });

  if (lightboxClose) {
    lightboxClose.addEventListener("click", closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
  }

  // Keyboard accessibility: Escape key to dismiss
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightbox && lightbox.classList.contains("active")) {
      closeLightbox();
    }
  });
});
