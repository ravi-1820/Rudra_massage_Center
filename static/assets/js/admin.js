/**
 * Rudra Massage & Wellness Admin Console Controller
 * Manages demo CRUD state, table searching, modals, appointments, offers, and responsive sidebar.
 */

// Initial Mock Admin Data
const INITIAL_ADMIN_DATA = {
  services: [
    { id: "wt-101", name: "AyurSpine Lumbar Decompression Belt", category: "Therapy Machines", price: 4999, status: "Active" },
    { id: "wt-102", name: "Pure Vedic Bronze Kansa Vataki Foot Massager", category: "Kansa Therapy", price: 3299, status: "Active" },
    { id: "wt-103", name: "OrthoRelief Infrared Knee Guard", category: "Therapy Machines", price: 3899, status: "Active" },
    { id: "wt-104", name: "CervicalFlex Smart Trapezius Massager", category: "Massagers", price: 2799, status: "Active" },
    { id: "wt-105", name: "OcuRest Air-Pressure Eye Massager", category: "Massagers", price: 2499, status: "Draft" },
    { id: "wt-106", name: "AyurShiro Shirodhara Console", category: "Therapy Machines", price: 34999, status: "Active" }
  ],
  enquiries: [
    { id: "ENQ-901", name: "Kavita Shah", email: "kavita.s@example.com", phone: "+91 98250 12345", service: "AyurSpine Decompression Belt", date: "2026-10-12", status: "New" },
    { id: "ENQ-902", name: "Bhavesh Mehtalia", email: "bhavesh.m@example.com", phone: "+91 98980 54321", service: "Kansa Vataki Massager", date: "2026-10-11", status: "Contacted" },
    { id: "ENQ-903", name: "Dr. Alpesh Trivedi", email: "alpesh.t@example.com", phone: "+91 94260 77889", service: "AyurShiro Shirodhara Console", date: "2026-10-10", status: "In Discussion" },
    { id: "ENQ-904", name: "Meena Parikh", email: "meena.p@example.com", phone: "+91 97270 33445", service: "OrthoRelief Knee Guard", date: "2026-10-09", status: "Resolved" }
  ],
  appointments: [
    { id: "APT-401", client: "Sanjay Solanki", date: "2026-10-15", time: "10:30 AM", type: "Home Demo", service: "AyurSpine Lumbar Belt", status: "Confirmed" },
    { id: "APT-402", client: "Dr. Hemal Bhatt", date: "2026-10-16", time: "02:00 PM", type: "Clinic Consultation", service: "Shirodhara Automated Console", status: "Pending" },
    { id: "APT-403", client: "Geeta Desai", date: "2026-10-18", time: "11:00 AM", type: "Home Demo", service: "OrthoRelief Knee Guard", status: "Confirmed" }
  ],
  offers: [
    { code: "FESTIVE25", title: "Navratri & Diwali Festive Wellness Bundle", discount: "Flat 25% OFF", status: "Active" },
    { code: "SENIORCARE", title: "Senior Citizens Spine & Joint Care Special", discount: "Extra ₹1,500 OFF", status: "Active" },
    { code: "CLINICPRO", title: "Centre & Clinic Bulk Trial Demo Package", discount: "Free Trial Demo", status: "Active" }
  ]
};

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

function safeStorageGet(key, defaultData) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return [...defaultData];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [...defaultData];
  } catch (err) {
    console.warn(`Failed to parse localStorage key "${key}":`, err);
    return [...defaultData];
  }
}

class AdminController {
  constructor() {
    this.services = safeStorageGet("admin_services", INITIAL_ADMIN_DATA.services);
    this.enquiries = safeStorageGet("admin_enquiries", INITIAL_ADMIN_DATA.enquiries);
    this.appointments = safeStorageGet("admin_appointments", INITIAL_ADMIN_DATA.appointments);
    this.offers = safeStorageGet("admin_offers", INITIAL_ADMIN_DATA.offers);

    this.init();
  }

  init() {
    AdminThemeController.init();
    this.setupSidebarToggle();
    this.renderStats();
    this.renderServicesTable();
    this.renderEnquiriesTable();
    this.renderAppointmentsTable();
    this.renderOffersTable();
    this.setupServiceModal();
    this.setupOfferModal();
    this.setupSearchFilters();
  }

  saveState() {
    try {
      localStorage.setItem("admin_services", JSON.stringify(this.services));
      localStorage.setItem("admin_enquiries", JSON.stringify(this.enquiries));
      localStorage.setItem("admin_appointments", JSON.stringify(this.appointments));
      localStorage.setItem("admin_offers", JSON.stringify(this.offers));
    } catch (err) {
      console.warn("Storage save failed:", err);
    }
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

  renderStats() {
    const totalEnquiries = document.getElementById("statTotalEnquiries");
    if (totalEnquiries) totalEnquiries.textContent = this.enquiries.length;

    const totalAppointments = document.getElementById("statTotalAppointments");
    if (totalAppointments) totalAppointments.textContent = this.appointments.length;

    const totalServices = document.getElementById("statTotalServices");
    if (totalServices) totalServices.textContent = this.services.length;
  }

  renderServicesTable(list = this.services) {
    const tbody = document.getElementById("adminServicesTbody");
    if (!tbody) return;

    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No solutions found matching criteria.</td></tr>`;
      return;
    }

    tbody.innerHTML = list.map(item => `
      <tr>
        <td class="fw-bold text-forest">${escapeHtml(item.name)}</td>
        <td><span class="badge bg-light text-dark border">${escapeHtml(item.category)}</span></td>
        <td class="fw-semibold">₹${Number(item.price).toLocaleString('en-IN')}</td>
        <td>
          <span class="badge ${item.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${escapeHtml(item.status)}</span>
        </td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-secondary me-1" onclick="window.adminApp.editService('${escapeHtml(item.id)}')" title="Edit" aria-label="Edit service">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" onclick="window.adminApp.deleteService('${escapeHtml(item.id)}')" title="Delete" aria-label="Delete service">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      </tr>
    `).join("");
  }

  renderEnquiriesTable(list = this.enquiries) {
    const tbody = document.getElementById("adminEnquiriesTbody");
    if (!tbody) return;

    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No enquiries found.</td></tr>`;
      return;
    }

    tbody.innerHTML = list.map(item => `
      <tr>
        <td class="fw-bold">${escapeHtml(item.id)}</td>
        <td>
          <div class="fw-semibold">${escapeHtml(item.name)}</div>
          <small class="text-muted">${escapeHtml(item.phone)}</small>
        </td>
        <td>${escapeHtml(item.service)}</td>
        <td>${escapeHtml(item.date)}</td>
        <td>
          <select class="form-select form-select-sm" onchange="window.adminApp.updateEnquiryStatus('${escapeHtml(item.id)}', this.value)" style="width: 140px;" aria-label="Update status for enquiry ${escapeHtml(item.id)}">
            <option value="New" ${item.status === 'New' ? 'selected' : ''}>New</option>
            <option value="Contacted" ${item.status === 'Contacted' ? 'selected' : ''}>Contacted</option>
            <option value="In Discussion" ${item.status === 'In Discussion' ? 'selected' : ''}>In Discussion</option>
            <option value="Resolved" ${item.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
          </select>
        </td>
      </tr>
    `).join("");
  }

  renderAppointmentsTable(list = this.appointments) {
    const tbody = document.getElementById("adminAppointmentsTbody");
    if (!tbody) return;

    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">No scheduled appointments found.</td></tr>`;
      return;
    }

    tbody.innerHTML = list.map(item => `
      <tr>
        <td class="fw-bold">${escapeHtml(item.id)}</td>
        <td>${escapeHtml(item.client)}</td>
        <td>${escapeHtml(item.date)} <br><small class="text-muted">${escapeHtml(item.time)}</small></td>
        <td>${escapeHtml(item.service)}</td>
        <td><span class="badge bg-info text-dark">${escapeHtml(item.type)}</span></td>
        <td>
          <select class="form-select form-select-sm" onchange="window.adminApp.updateAppointmentStatus('${escapeHtml(item.id)}', this.value)" style="width: 135px;" aria-label="Update status for appointment ${escapeHtml(item.id)}">
            <option value="Confirmed" ${item.status === 'Confirmed' ? 'selected' : ''}>Confirmed</option>
            <option value="Pending" ${item.status === 'Pending' ? 'selected' : ''}>Pending</option>
            <option value="Completed" ${item.status === 'Completed' ? 'selected' : ''}>Completed</option>
            <option value="Cancelled" ${item.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
          </select>
        </td>
      </tr>
    `).join("");
  }

  renderOffersTable(list = this.offers) {
    const tbody = document.getElementById("adminOffersTbody");
    if (!tbody) return;

    if (list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No active promotional campaigns found.</td></tr>`;
      return;
    }

    tbody.innerHTML = list.map(item => `
      <tr>
        <td class="fw-bold text-forest">${escapeHtml(item.code)}</td>
        <td>${escapeHtml(item.title)}</td>
        <td>${escapeHtml(item.discount)}</td>
        <td><span class="badge bg-success">${escapeHtml(item.status || 'Active')}</span></td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-danger" onclick="window.adminApp.deleteOffer('${escapeHtml(item.code)}')" title="Deactivate" aria-label="Delete voucher ${escapeHtml(item.code)}">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      </tr>
    `).join("");
  }

  setupServiceModal() {
    const form = document.getElementById("serviceModalForm");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const id = document.getElementById("modalServiceId").value;
      const name = document.getElementById("modalServiceName").value.trim();
      const category = document.getElementById("modalServiceCategory").value;
      const price = parseFloat(document.getElementById("modalServicePrice").value);
      const status = document.getElementById("modalServiceStatus").value;

      if (!name || isNaN(price) || price < 0) {
        showToast("Error", "Please provide a valid solution name and positive price.", "error");
        return;
      }

      if (id) {
        // Edit existing
        const idx = this.services.findIndex(s => s.id === id);
        if (idx !== -1) {
          this.services[idx] = { ...this.services[idx], name, category, price, status };
          showToast("Updated", `Solution "${name}" was updated successfully.`, "success");
        }
      } else {
        // Add new
        const newId = `wt-${Date.now().toString().slice(-3)}`;
        this.services.unshift({ id: newId, name, category, price, status });
        showToast("Created", `New solution "${name}" added to catalogue.`, "success");
      }

      this.saveState();
      this.renderServicesTable();
      this.renderStats();

      const modalEl = document.getElementById("serviceModal");
      if (modalEl && typeof bootstrap !== "undefined") {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      form.reset();
    });
  }

  setupOfferModal() {
    const form = document.getElementById("offerModalForm");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const code = document.getElementById("modalOfferCode").value.trim().toUpperCase();
      const title = document.getElementById("modalOfferTitle").value.trim();
      const discount = document.getElementById("modalOfferDiscount").value.trim();

      if (!code || !title || !discount) {
        showToast("Error", "Please complete all voucher fields.", "error");
        return;
      }

      this.offers.unshift({ code, title, discount, status: "Active" });
      this.saveState();
      this.renderOffersTable();
      showToast("Voucher Created", `Promo voucher ${code} created successfully.`, "success");

      const modalEl = document.getElementById("offerModal");
      if (modalEl && typeof bootstrap !== "undefined") {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
      form.reset();
    });
  }

  openAddServiceModal() {
    const idInput = document.getElementById("modalServiceId");
    if (idInput) idInput.value = "";
    const titleEl = document.getElementById("modalServiceTitle");
    if (titleEl) titleEl.textContent = "Add New Therapy Solution";
    const form = document.getElementById("serviceModalForm");
    if (form) form.reset();
    const modalEl = document.getElementById("serviceModal");
    if (modalEl && typeof bootstrap !== "undefined") {
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    }
  }

  openAddOfferModal() {
    const form = document.getElementById("offerModalForm");
    if (form) form.reset();
    const modalEl = document.getElementById("offerModal");
    if (modalEl && typeof bootstrap !== "undefined") {
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    }
  }

  editService(id) {
    const item = this.services.find(s => s.id === id);
    if (!item) return;

    const idInput = document.getElementById("modalServiceId");
    if (idInput) idInput.value = item.id;
    const titleEl = document.getElementById("modalServiceTitle");
    if (titleEl) titleEl.textContent = "Edit Solution";
    const nameInput = document.getElementById("modalServiceName");
    if (nameInput) nameInput.value = item.name;
    const catInput = document.getElementById("modalServiceCategory");
    if (catInput) catInput.value = item.category;
    const priceInput = document.getElementById("modalServicePrice");
    if (priceInput) priceInput.value = item.price;
    const statusInput = document.getElementById("modalServiceStatus");
    if (statusInput) statusInput.value = item.status;

    const modalEl = document.getElementById("serviceModal");
    if (modalEl && typeof bootstrap !== "undefined") {
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    }
  }

  deleteService(id) {
    if (confirm("Are you sure you want to delete this service in demo state?")) {
      this.services = this.services.filter(s => s.id !== id);
      this.saveState();
      this.renderServicesTable();
      this.renderStats();
      showToast("Deleted", "Service record removed from demo state.", "gold");
    }
  }

  deleteOffer(code) {
    if (confirm(`Are you sure you want to deactivate voucher ${code}?`)) {
      this.offers = this.offers.filter(o => o.code !== code);
      this.saveState();
      this.renderOffersTable();
      showToast("Deactivated", `Voucher ${code} removed from demo campaigns.`, "gold");
    }
  }

  updateEnquiryStatus(id, newStatus) {
    const item = this.enquiries.find(e => e.id === id);
    if (item) {
      item.status = newStatus;
      this.saveState();
      showToast("Status Updated", `Enquiry ${id} set to ${newStatus}.`, "success");
    }
  }

  updateAppointmentStatus(id, newStatus) {
    const item = this.appointments.find(a => a.id === id);
    if (item) {
      item.status = newStatus;
      this.saveState();
      showToast("Status Updated", `Appointment ${id} set to ${newStatus}.`, "success");
    }
  }

  setupSearchFilters() {
    const searchServicesInput = document.getElementById("adminServiceSearch");
    if (searchServicesInput) {
      searchServicesInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        const filtered = this.services.filter(s => s.name.toLowerCase().includes(q) || s.category.toLowerCase().includes(q));
        this.renderServicesTable(filtered);
      });
    }

    const searchEnquiriesInput = document.getElementById("adminEnquiriesSearch");
    if (searchEnquiriesInput) {
      searchEnquiriesInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        const filtered = this.enquiries.filter(enq => enq.name.toLowerCase().includes(q) || enq.phone.includes(q) || enq.service.toLowerCase().includes(q));
        this.renderEnquiriesTable(filtered);
      });
    }

    const searchAppointmentsInput = document.getElementById("adminAppointmentsSearch");
    if (searchAppointmentsInput) {
      searchAppointmentsInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        const filtered = this.appointments.filter(apt => apt.client.toLowerCase().includes(q) || apt.service.toLowerCase().includes(q) || apt.id.toLowerCase().includes(q));
        this.renderAppointmentsTable(filtered);
      });
    }
  }
}

function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str.replace(/[&<>"']/g, s => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[s]));
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector(".admin-layout")) {
    window.adminApp = new AdminController();
  }
});
