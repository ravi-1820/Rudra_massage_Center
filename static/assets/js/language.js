/**
 * Language Translation Engine (English <-> Gujarati)
 * Persisted with localStorage.
 * Handles UI keys with [data-i18n] attributes.
 */

const TRANSLATIONS = {
  en: {
    // Navigation
    "nav.home": "Home",
    "nav.about": "About Us",
    "nav.services": "Catalogue",
    "nav.products": "Products & Services",
    "nav.categories": "Categories",
    "nav.gallery": "Gallery",
    "nav.reviews": "Reviews",
    "nav.journal": "Health Journal",
    "nav.faq": "FAQ",
    "nav.bmi": "BMI Calculator",
    "nav.offers": "Offers",
    "nav.contact": "Contact Us",
    "nav.support": "Support",
    "nav.profile": "Digital Profile",
    "nav.book": "Book Appointment",
    "nav.admin": "Admin Portal",

    // Header & Announcement
    "top.announcement": "✨ Festive Wellness Special: Flat 25% Off on Vedic Kansa & Lumbar Therapy. Code: FESTIVE25",
    "top.viewOffers": "View Offers",
    "top.searchPlaceholder": "Search therapy machines, needs, body parts...",
    "top.callUs": "Call Support",
    "top.bookDemo": "Book a Demo",

    // Hero Section
    "hero.badge": "Rooted in Ayurveda • Backed by Modern Ergonomics",
    "hero.title": "Harmonize Body & Soul with Restorative Therapy",
    "hero.subtitle": "Experience clinical spinal decompression, sacred bronze Kansa rituals, and targeted infrared therapy machines designed for rejuvenating daily living.",
    "hero.exploreCta": "Explore Services",
    "hero.bookCta": "Book Consultation",
    "hero.trust1": "Certified Ergonomic Quality",
    "hero.trust2": "Doorstep Home & Clinic Demos",
    "hero.trust3": "Verified Ayurvedic Craftsmanship",

    // Sections
    "section.needTitle": "Explore Therapy by Need",
    "section.needSubtitle": "Find targeted solutions tailored to your specific wellness concerns without complex medical jargon.",
    "section.catTitle": "Explore Our 18 Wellness Disciplines",
    "section.catSubtitle": "A comprehensive spectrum of therapy devices, Ayurvedic tools, and mobility aids.",
    "section.featTitle": "Featured Therapy & Wellness Solutions",
    "section.featSubtitle": "Handpicked machines and handcrafted traditional instruments trusted across India.",
    "section.howTitle": "Three Simple Steps to Wholeness",
    "section.howSubtitle": "Discover how convenient personalized therapy can be.",
    "section.howStep1": "1. Explore Solutions",
    "section.howStep1Desc": "Browse our curated catalogue filtered by your pain point, body part, or usage setting.",
    "section.howStep2": "2. Consult or Try Demo",
    "section.howStep2Desc": "Speak with our wellness advisors or schedule a hands-on live product demonstration.",
    "section.howStep3": "3. Reclaim Vitality",
    "section.howStep3Desc": "Incorporate soothing restorative routines into your daily rhythm with comprehensive care guides.",

    // Buttons & CTAs
    "btn.viewDetails": "View Details",
    "btn.enquireNow": "Enquire Now",
    "btn.allCategories": "View All 18 Categories",
    "btn.fullCatalogue": "Open Full Catalogue",
    "btn.submitEnquiry": "Send Enquiry",
    "btn.bookAppointment": "Confirm Appointment",
    "btn.calculateBmi": "Calculate My BMI",
    "btn.clearFilters": "Clear All Filters",
    "btn.copyCode": "Copy Promo Code",

    // Forms
    "form.fullName": "Full Name",
    "form.email": "Email Address",
    "form.phone": "Mobile Number (+91)",
    "form.city": "City",
    "form.date": "Preferred Date",
    "form.time": "Preferred Time",
    "form.service": "Select Service / Machine",
    "form.message": "Your Message / Specific Concerns",
    "form.demoNotice": "Notice: This form runs client-side demo validation. Form data will be logged and demo feedback displayed.",

    // Footer
    "footer.tagline": "Empowering healthier families through genuine Ayurvedic metallurgy and modern physiotherapy technology.",
    "footer.quickLinks": "Quick Navigation",
    "footer.categories": "Core Categories",
    "footer.getInTouch": "Get in Touch",
    "footer.rights": "All rights reserved. Designed for holistic wellness."
  },
  gu: {
    // Navigation
    "nav.home": "મુખ્ય પૃષ્ઠ",
    "nav.about": "અમારા વિશે",
    "nav.services": "સૂચિ (કેટલોગ)",
    "nav.products": "ઉત્પાદનો અને સેવાઓ",
    "nav.categories": "શ્રેણીઓ",
    "nav.gallery": "ગેલેરી",
    "nav.reviews": "અભિપ્રાયો",
    "nav.journal": "સ્વાસ્થ્ય પત્રિકા",
    "nav.faq": "પ્રશ્નોત્તરી (FAQ)",
    "nav.bmi": "BMI કેલ્ક્યુલેટર",
    "nav.offers": "ઑફર્સ",
    "nav.contact": "સંપર્ક",
    "nav.support": "સહાયતા",
    "nav.profile": "ડિજિટલ પ્રોફાઇલ",
    "nav.book": "મુલાકાત બુક કરો",
    "nav.admin": "એડમિન પોર્ટલ",

    // Header & Announcement
    "top.announcement": "✨ તહેવાર સ્પેશ્યલ: કાંસા થેરાપી અને કમર સારવાર સાધનો પર ફ્લેટ 25% છૂટ. કોડ: FESTIVE25",
    "top.viewOffers": "ઑફર્સ જુઓ",
    "top.searchPlaceholder": "થેરાપી મશીન, દુખાવો અથવા અંગ શોધો...",
    "top.callUs": "સહાયતા માટે કૉલ કરો",
    "top.bookDemo": "ડેમો બુક કરો",

    // Hero Section
    "hero.badge": "આયુર્વેદિક પરંપરા • આધુનિક અર્ગોનોમિક્સનું સંગમ",
    "hero.title": "કુદરતી થેરાપી વડે શરીર અને મનને સ્વસ્થ બનાવો",
    "hero.subtitle": "સ્પાઇનલ ડીકોમ્પ્રેશન, પ્રાચીન કાંસા વટકી માલિશ અને ઇન્ફ્રારેડ હીટ થેરાપી સાથે રોજિંદા જીવનમાં તાજગી અને આરામ મેળવો.",
    "hero.exploreCta": "સેવાઓ જુઓ",
    "hero.bookCta": "સલાહ મેળવો",
    "hero.trust1": "પ્રમાણિત અર્ગોનોમિક ગુણવત્તા",
    "hero.trust2": "ઘરે અને ક્લિનિકમાં ડેમો સુવિધા",
    "hero.trust3": "શુદ્ધ આયુર્વેદિક ધાતુ કારીગરી",

    // Sections
    "section.needTitle": "તમારી જરૂરિયાત મુજબ થેરાપી પસંદ કરો",
    "section.needSubtitle": "કોઈપણ જટિલ તબીબી શબ્દો વિના તમારા દુખાવા મુજબ યોગ્ય ઉપાય મેળવો.",
    "section.catTitle": "અમારી 18 વેલનેસ શાખાઓ",
    "section.catSubtitle": "થેરાપી મશીન, આયુર્વેદિક સાધનો અને વડીલો માટેની વિશેષ સુવિધાઓ.",
    "section.featTitle": "વિશેષ થેરાપી સાધનો અને સેવાઓ",
    "section.featSubtitle": "સમગ્ર ભારતમાં વિશ્વાસપાત્ર ગુણવત્તા સાથે ઉપયોગમાં લેવાતા ઉપકરણો.",
    "section.howTitle": "સ્વસ્થ જીવન માટે ત્રણ સરળ પગલાં",
    "section.howSubtitle": "જાણો કેવી રીતે સરળતાથી થેરાપી શરૂ કરી શકાય છે.",
    "section.howStep1": "1. ઉપાય શોધો",
    "section.howStep1Desc": "તમારા દુખાવા, અંગ અથવા ઘર/ક્લિનિક ઉપયોગ મુજબ યોગ્ય સાધન પસંદ કરો.",
    "section.howStep2": "2. સલાહ અથવા ડેમો લો",
    "section.howStep2Desc": "અમારા તજજ્ઞો સાથે વાત કરો અથવા લાઈવ ડેમો સત્ર નક્કી કરો.",
    "section.howStep3": "3. નિરોગી બનો",
    "section.howStep3Desc": "માર્ગદર્શિકા સાથે સરળતાથી રોજિંદા જીવનમાં આરામદાયક સારવાર અપનાવો.",

    // Buttons & CTAs
    "btn.viewDetails": "વિગતો જુઓ",
    "btn.enquireNow": "પૂછપરછ કરો",
    "btn.allCategories": "તમામ 18 શ્રેણીઓ",
    "btn.fullCatalogue": "સંપૂર્ણ સૂચિ ખોલો",
    "btn.submitEnquiry": "પૂછપરછ મોકલો",
    "btn.bookAppointment": "મુલાકાત કન્ફર્મ કરો",
    "btn.calculateBmi": "મારું BMI ગણો",
    "btn.clearFilters": "ફિલ્ટર્સ દૂર કરો",
    "btn.copyCode": "કોડ કૉપી કરો",

    // Forms
    "form.fullName": "પૂરું નામ",
    "form.email": "ઈમેલ એડ્રેસ",
    "form.phone": "મોબાઇલ નંબર (+91)",
    "form.city": "શહેર",
    "form.date": "પસંદગીની તારીખ",
    "form.time": "પસંદગીનો સમય",
    "form.service": "સાધન અથવા સેવા પસંદ કરો",
    "form.message": "તમારો સંદેશ અથવા વિગત",
    "form.demoNotice": "નોંધ: આ ફોર્મ ક્લાયન્ટ સાઈડ ડેમો છે. ડેટા બ્રાઉઝરમાં ચકાસણી સાથે દર્શાવાશે.",

    // Footer
    "footer.tagline": "શુદ્ધ કાંસા ધાતુ અને આધુનિક ફિઝિયોથેરાપી દ્વારા પરિવારોને સ્વસ્થ બનાવવાનો સંકલ્પ.",
    "footer.quickLinks": "ઝડપી લિંક્સ",
    "footer.categories": "મુખ્ય શ્રેણીઓ",
    "footer.getInTouch": "સંપર્ક કરો",
    "footer.rights": "સર્વાધિકાર સુરક્ષિત. સર્વાંગી કલ્યાણ માટે સમર્પિત."
  }
};

class LanguageManager {
  constructor() {
    this.currentLang = localStorage.getItem("preferred_lang") || "en";
    this.init();
  }

  init() {
    this.applyTranslations(this.currentLang);
    this.setupListeners();
  }

  setLanguage(lang) {
    if (!TRANSLATIONS[lang]) return;
    this.currentLang = lang;
    localStorage.setItem("preferred_lang", lang);
    this.applyTranslations(lang);
    this.updateActiveButtonState();
  }

  applyTranslations(lang) {
    const dict = TRANSLATIONS[lang];
    if (!dict) return;

    // Set document lang attribute
    document.documentElement.setAttribute("lang", lang);

    // Update text in elements marked with [data-i18n]
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    // Update placeholders marked with [data-i18n-placeholder]
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (dict[key]) {
        el.setAttribute("placeholder", dict[key]);
      }
    });
  }

  setupListeners() {
    document.querySelectorAll(".lang-switch-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const targetLang = btn.getAttribute("data-lang");
        this.setLanguage(targetLang);
      });
    });
    this.updateActiveButtonState();
  }

  updateActiveButtonState() {
    document.querySelectorAll(".lang-switch-btn").forEach(btn => {
      if (btn.getAttribute("data-lang") === this.currentLang) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }
}

// Global instance
let langManager;
document.addEventListener("DOMContentLoaded", () => {
  langManager = new LanguageManager();
});
