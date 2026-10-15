/**
 * Rudra Massage & Wellness - Interactive BMI Calculator & Wellness Advisor
 * Metric & Imperial unit support, animated gauge pointer, WHO standard ranges,
 * and tailored therapy machine suggestions.
 */

class BmiCalculator {
  constructor() {
    this.unit = "metric"; // or 'imperial'
    this.init();
  }

  init() {
    this.bindUnitSwitch();
    this.bindForm();
    // Compute initial result to synchronize the gauge and category with default inputs
    this.calculateFromInputs(false);
  }

  bindUnitSwitch() {
    const metricBtn = document.getElementById("unitMetricBtn");
    const imperialBtn = document.getElementById("unitImperialBtn");
    const metricInputs = document.getElementById("metricInputsWrap");
    const imperialInputs = document.getElementById("imperialInputsWrap");

    if (metricBtn && imperialBtn) {
      metricBtn.addEventListener("click", () => {
        if (this.unit === "metric") return;
        this.unit = "metric";
        metricBtn.classList.add("active");
        imperialBtn.classList.remove("active");
        if (metricInputs) metricInputs.classList.remove("d-none");
        if (imperialInputs) imperialInputs.classList.add("d-none");

        // Convert imperial values to metric if present
        const ft = parseFloat(document.getElementById("heightFt")?.value) || 0;
        const inch = parseFloat(document.getElementById("heightIn")?.value) || 0;
        const lbs = parseFloat(document.getElementById("weightLbs")?.value) || 0;
        const totalInches = (ft * 12) + inch;

        if (totalInches > 0) {
          const cm = Math.round(totalInches * 2.54);
          const heightCmInput = document.getElementById("heightCm");
          if (heightCmInput) heightCmInput.value = cm;
        }
        if (lbs > 0) {
          const kg = Math.round(lbs / 2.20462);
          const weightKgInput = document.getElementById("weightKg");
          if (weightKgInput) weightKgInput.value = kg;
        }
      });

      imperialBtn.addEventListener("click", () => {
        if (this.unit === "imperial") return;
        this.unit = "imperial";
        imperialBtn.classList.add("active");
        metricBtn.classList.remove("active");
        if (metricInputs) metricInputs.classList.add("d-none");
        if (imperialInputs) imperialInputs.classList.remove("d-none");

        // Convert metric values to imperial if present
        const cm = parseFloat(document.getElementById("heightCm")?.value) || 0;
        const kg = parseFloat(document.getElementById("weightKg")?.value) || 0;

        if (cm > 0) {
          const totalInches = cm / 2.54;
          const ft = Math.floor(totalInches / 12);
          const inches = Math.round(totalInches % 12);
          const heightFtInput = document.getElementById("heightFt");
          const heightInInput = document.getElementById("heightIn");
          if (heightFtInput) heightFtInput.value = ft;
          if (heightInInput) heightInInput.value = inches;
        }
        if (kg > 0) {
          const lbs = Math.round(kg * 2.20462);
          const weightLbsInput = document.getElementById("weightLbs");
          if (weightLbsInput) weightLbsInput.value = lbs;
        }
      });
    }
  }

  calculateFromInputs(shouldScroll = true) {
    let bmi = 0;

    if (this.unit === "metric") {
      const heightCm = parseFloat(document.getElementById("heightCm")?.value);
      const weightKg = parseFloat(document.getElementById("weightKg")?.value);

      if (isNaN(heightCm) || isNaN(weightKg) || heightCm <= 0 || weightKg <= 0) {
        if (shouldScroll) {
          showToast("Invalid Input", "Please enter valid positive height and weight values.", "error");
        }
        return;
      }

      const heightM = heightCm / 100;
      bmi = weightKg / (heightM * heightM);
    } else {
      const heightFt = parseFloat(document.getElementById("heightFt")?.value) || 0;
      const heightIn = parseFloat(document.getElementById("heightIn")?.value) || 0;
      const weightLbs = parseFloat(document.getElementById("weightLbs")?.value);

      const totalInches = (heightFt * 12) + heightIn;
      if (totalInches <= 0 || isNaN(weightLbs) || weightLbs <= 0) {
        if (shouldScroll) {
          showToast("Invalid Input", "Please enter valid height in feet/inches and weight in pounds.", "error");
        }
        return;
      }

      bmi = (703 * weightLbs) / (totalInches * totalInches);
    }

    this.displayResults(bmi, shouldScroll);
  }

  bindForm() {
    const form = document.getElementById("bmiForm");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      this.calculateFromInputs(true);
    });
  }

  displayResults(bmi, shouldScroll = true) {
    const resultBox = document.getElementById("bmiResultBox");
    const scoreVal = document.getElementById("bmiScoreValue");
    const categoryName = document.getElementById("bmiCategoryName");
    const categoryBadge = document.getElementById("bmiCategoryBadge");
    const categoryDesc = document.getElementById("bmiCategoryDesc");
    const marker = document.getElementById("bmiGaugeMarker");
    const suggestionsWrap = document.getElementById("bmiSuggestionsWrap");

    if (!resultBox) return;

    resultBox.classList.remove("d-none");
    const roundedBmi = bmi.toFixed(1);
    if (scoreVal) scoreVal.textContent = roundedBmi;

    // Standard WHO BMI categories without boundary gaps
    let category = "";
    let badgeClass = "";
    let desc = "";
    let gaugePercent = 0;

    if (bmi < 18.5) {
      category = "Underweight";
      badgeClass = "bg-primary text-white";
      desc = "Your BMI suggests you may benefit from nourishing restorative routines, gentle marma massage, and joint strengthening exercises.";
      gaugePercent = Math.max(5, (bmi / 18.5) * 20);
    } else if (bmi < 25.0) {
      category = "Healthy / Optimal Weight";
      badgeClass = "bg-success text-white";
      desc = "Congratulations! Your BMI is within the recommended adult range. Continue balanced ergonomic posture care and mindful stress relief.";
      gaugePercent = 20 + ((bmi - 18.5) / 6.5) * 30;
    } else if (bmi < 30.0) {
      category = "Overweight";
      badgeClass = "bg-warning text-dark";
      desc = "Your weight may place additional mechanical pressure on lumbar vertebrae and knee joints. Consider gentle spinal decompression and metabolic movement.";
      gaugePercent = 50 + ((bmi - 25.0) / 5.0) * 25;
    } else {
      category = "Obesity Range";
      badgeClass = "bg-danger text-white";
      desc = "A higher BMI significantly increases daily joint and cardiovascular strain. Low-impact whole-body vibration and lymphatic compression can help without joint pounding.";
      gaugePercent = Math.min(96, 75 + ((bmi - 30.0) / 15.0) * 25);
    }

    if (categoryName) categoryName.textContent = category;
    if (categoryBadge) {
      categoryBadge.className = `badge ${badgeClass} fs-6 px-3 py-2`;
      categoryBadge.textContent = category;
    }
    if (categoryDesc) categoryDesc.textContent = desc;

    // Move Gauge Marker
    if (marker) {
      marker.style.left = `${gaugePercent}%`;
    }

    // Curated recommendations
    if (suggestionsWrap && typeof WELLNESS_PRODUCTS !== "undefined") {
      const suggested = WELLNESS_PRODUCTS.filter(p => p.need.includes("Pain") || p.category.includes("Exercise") || p.category.includes("Therapy")).slice(0, 2);
      suggestionsWrap.innerHTML = `
        <h5 class="fw-bold text-forest mb-3">Tailored Supportive Modalities</h5>
        <div class="row g-3">
          ${suggested.map(item => `
            <div class="col-md-6">
              <div class="card border p-3 h-100 rounded-3">
                <div class="d-flex align-items-center gap-3">
                  <img src="${item.image}" alt="${item.name}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;">
                  <div>
                    <h6 class="mb-1 text-forest fw-bold">${item.name}</h6>
                    <span class="badge bg-light text-dark border">${item.need}</span>
                  </div>
                </div>
                <a href="/service-detail/?id=${item.id}" class="btn-veda-outline btn-veda-sm mt-3 text-center">Explore Device</a>
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }

    if (shouldScroll) {
      resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("bmiForm")) {
    new BmiCalculator();
  }
});
