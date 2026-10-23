/**
 * VedaWellness & Therapy - Form Validation & Submission Engine
 * Strictly client-side demo implementation ready for future backend API hook.
 * Implements Indian phone validation, email checks, date safeguards, and loading feedback.
 */

class FormHandler {
  static validateIndianPhone(phone) {
    const clean = phone.replace(/[\s\-+]/g, '');
    const regex = /^(?:91|0)?[6-9]\d{9}$/;
    return regex.test(clean);
  }

  static validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  static isFutureDate(dateStr) {
    if (!dateStr) return false;
    const parts = dateStr.split("-");
    if (parts.length !== 3) return false;
    const y = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10) - 1;
    const d = parseInt(parts[2], 10);
    const selected = new Date(y, m, d);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return selected >= today;
  }

  static setupForm(formId, successCallback) {
    const form = document.getElementById(formId);
    if (!form || form.dataset.backendSubmit === "true") return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      let isValid = true;
      const submitBtn = form.querySelector("button[type='submit']");
      const errorSummary = form.querySelector(".form-error-summary");
      if (errorSummary) errorSummary.classList.add("d-none");

      // Validate Text & Required Inputs
      form.querySelectorAll("[required]").forEach(input => {
        const val = input.value.trim();
        const feedback = input.nextElementSibling;

        if (!val) {
          isValid = false;
          input.classList.add("is-invalid");
          if (feedback && feedback.classList.contains("invalid-feedback-custom")) {
            feedback.textContent = "This field is required.";
          }
        } else {
          input.classList.remove("is-invalid");
        }

        // Email check
        if (input.type === "email" && val) {
          if (!FormHandler.validateEmail(val)) {
            isValid = false;
            input.classList.add("is-invalid");
            if (feedback && feedback.classList.contains("invalid-feedback-custom")) {
              feedback.textContent = "Please enter a valid email address.";
            }
          }
        }

        // Indian Phone check
        if (input.dataset.type === "indian-phone" && val) {
          if (!FormHandler.validateIndianPhone(val)) {
            isValid = false;
            input.classList.add("is-invalid");
            if (feedback && feedback.classList.contains("invalid-feedback-custom")) {
              feedback.textContent = "Please enter a valid 10-digit Indian mobile number (starts with 6, 7, 8, or 9).";
            }
          }
        }

        // Future Date check
        if (input.type === "date" && val) {
          if (!FormHandler.isFutureDate(val)) {
            isValid = false;
            input.classList.add("is-invalid");
            if (feedback && feedback.classList.contains("invalid-feedback-custom")) {
              feedback.textContent = "Please select today or a future date.";
            }
          }
        }
      });

      if (!isValid) {
        if (errorSummary) {
          errorSummary.classList.remove("d-none");
          errorSummary.textContent = "Please resolve the highlighted errors before submitting.";
        }
        showToast("Validation Error", "Please review and complete all required fields.", "error");
        return;
      }

      // Duplicate-Submit Prevention
      if (submitBtn) {
        submitBtn.disabled = true;
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Processing Demo Submission...`;

        // Simulate backend network latency
        setTimeout(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;

          if (typeof successCallback === "function") {
            successCallback(form);
          } else {
            showToast("Demo Submitted Successfully", "Your request was processed in frontend demo mode. A representative will connect shortly.", "success");
          }

          form.reset();
        }, 1000);
      }
    });

    // Clear validation error on input change
    form.querySelectorAll("input, select, textarea").forEach(field => {
      field.addEventListener("input", () => {
        field.classList.remove("is-invalid");
      });
    });
  }
}

  // Contact form submission feedback
  FormHandler.setupForm("contactForm", () => {
    showToast("Message Sent", "Thank you for reaching out to Rudra Massage & Wellness. We have received your message.", "success");
  });
});
