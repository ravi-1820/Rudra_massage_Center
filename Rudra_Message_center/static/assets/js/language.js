/**
 * Rudra Massage & Wellness - Enterprise Translation Engine (English <-> Gujarati)
 *
 * Features:
 * 1. Persistent Language Preference (localStorage + Cookie sync with Django LocaleMiddleware)
 * 2. Targeted Attribute Translation ([data-i18n], [data-i18n-placeholder], [data-i18n-title], [data-i18n-html])
 * 3. Text-node safe replacement (preserves nested icons, badges, and layout hierarchy)
 * 4. Automatic UI Phrase Translation for dynamic/un-annotated content across all public pages
 * 5. Safe Preservation of Product Names, Brand Names, and Medical Specifications
 * 6. Responsive Switcher Synchronization across Desktop and Mobile
 */

const TRANSLATIONS = {
  en: {
    // Top Announcement Bar
    "top.announcement": "Special Wellness Announcement: Experience Natural Healing & Restorative Therapy",
    "top.announcementBadge": "Special Offer:",
    "top.shopNow": "Shop Now →",
    "top.viewOffers": "View Offers",
    "top.searchPlaceholder": "Search therapy machines, needs, body parts...",
    "top.callUs": "Call Support",
    "top.bookDemo": "Book a Demo",

    // Navigation & Header
    "nav.home": "Home",
    "nav.about": "About Us",
    "nav.services": "Catalogue",
    "nav.products": "Products & Services",
    "nav.allProducts": "All Products & Services",
    "nav.categories": "Categories",
    "nav.gallery": "Gallery",
    "nav.reviews": "Reviews",
    "nav.journal": "Health Journal",
    "nav.blog": "Blog",
    "nav.faq": "FAQ",
    "nav.bmi": "BMI Calculator",
    "nav.offers": "Offers",
    "nav.contact": "Contact",
    "nav.support": "Support",
    "nav.profile": "Digital Profile",
    "nav.book": "Book Appointment",
    "nav.admin": "Admin Site",
    "nav.adminTitle": "Access Admin Portal",

    // Global Search Modal
    "search.modalTitle": "Search Solutions",
    "search.placeholder": "Search by pain need, body part, or machine...",
    "search.submit": "Search",
    "search.popular": "Popular searches:",

    // Hero Section
    "hero.badge": "Your Wellness Journey Starts Here",
    "hero.title": "Natural Healing with Modern Therapy Solutions",
    "hero.subtitle": "Experience the perfect blend of traditional wellness and modern therapy solutions. Feel better, move better, live better with Rudra Massage & Wellness.",
    "hero.exploreCta": "Explore Services →",
    "hero.bookCta": "Book Appointment",
    "hero.pill1": "Authentic Ayurvedic Craft",
    "hero.pill2": "Clinical Ergonomics",
    "hero.pill3": "Doorstep Demonstrations",
    "hero.slide1Tag": "Holistic Therapy",
    "hero.slide1Title": "Full Body Deep Relaxation",
    "hero.slide1Sub": "Gentle pressure marma point recovery & stress release.",
    "hero.slide2Tag": "Vedic Metallurgy",
    "hero.slide2Title": "100% Pure Kansa Bronze",
    "hero.slide2Sub": "Bio-metallic detoxification for foot & facial vitality.",
    "hero.slide3Tag": "Orthopedic Precision",
    "hero.slide3Title": "Spinal Curvature Decompression",
    "hero.slide3Sub": "Drug-free pneumatic air bladder lumbar traction.",
    "hero.bookNow": "Book Now →",
    "hero.explore": "Explore →",
    "hero.bookDemo": "Book Demo →",

    // Feature / Trust Cards
    "trust.card1Tag": "Natural",
    "trust.card1Title": "Wellness Approach",
    "trust.card1Opt1": "Ayurvedic principles",
    "trust.card1Opt2": "Herbal therapy methods",
    "trust.card1Opt3": "Holistic body care",
    "trust.card2Tag": "Modern",
    "trust.card2Title": "Therapy Equipment",
    "trust.card2Opt1": "Clinical-grade devices",
    "trust.card2Opt2": "Advanced massage tools",
    "trust.card2Opt3": "Smart pain relief tech",
    "trust.card3Tag": "Expert Guidance",
    "trust.card3Title": "& Support",
    "trust.card3Opt1": "Trained wellness staff",
    "trust.card3Opt2": "Personalised advice",
    "trust.card3Opt3": "Post-treatment care",
    "trust.card4Tag": "Home & Centre",
    "trust.card4Title": "Usage Options",
    "trust.card4Opt1": "Home-use devices",
    "trust.card4Opt2": "Centre sessions",
    "trust.card4Opt3": "Doorstep delivery",

    // Explore by Need Section
    "need.badge": "Holistic Healing",
    "need.title": "Explore by Need",
    "need.subtitle": "Find the right solution for your wellness needs",
    "need.backPain": "Back Pain",
    "need.kneePain": "Knee Pain",
    "need.neckShoulder": "Neck & Shoulder",
    "need.eyeCare": "Eye Care",
    "need.weightMgmt": "Weight Management",
    "need.stressSleep": "Stress & Sleep",
    "need.footLeg": "Foot & Leg Fatigue",
    "need.circulation": "Circulation Support",

    // Featured Products & Services
    "feat.title": "Featured Products & Services",
    "feat.subtitle": "Handpicked solutions for your wellness journey",
    "feat.viewDetails": "View Details →",
    "feat.bookAppointment": "Book Appointment",
    "feat.empty": "Explore our full therapy solutions in the Services Catalogue.",
    "feat.featured": "Featured",

    // About Section (Homepage)
    "about.badge": "About Our Legacy",
    "about.title": "About Rudra Massage & Wellness",
    "about.desc": "We bring together the wisdom of traditional wellness and the power of modern therapy to help you feel your best. Our mission is to provide natural, safe and effective wellness solutions for a healthier and more balanced life.",
    "about.learnMore": "Learn More →",
    "about.feat1": "Holistic Wellness Approach",
    "about.feat2": "Trusted Quality Products",
    "about.feat3": "Expert Support & Guidance",

    // How It Works
    "how.badge": "Simple Process",
    "how.title": "How It Works",
    "how.subtitle": "Get started in 3 simple steps.",
    "how.step1Title": "Explore Products & Services",
    "how.step1Desc": "Browse our wide range of wellness solutions and find what suits you.",
    "how.step2Title": "Choose a Relevant Option",
    "how.step2Desc": "Select your preferred product, service or therapy.",
    "how.step3Title": "Book or Enquire",
    "how.step3Desc": "Fill in the form or book an appointment. We'll get back to you soon.",

    // Testimonials
    "test.title": "What Our Customers Say",
    "test.subtitle": "Real experiences. Better lives.",
    "test.verified": "Verified Client",

    // Blog / Journal Section
    "blog.title": "Health & Wellness Journal",
    "blog.subtitle": "Tips, guides and insights for a healthier you.",
    "blog.viewAll": "View All Articles →",
    "blog.readArticle": "Read Article →",
    "blog.wellness": "Wellness",
    "blog.lifestyle": "Lifestyle",
    "blog.nutrition": "Nutrition",

    // CTA Banner
    "cta.title": "Ready to Experience Better Well-being?",
    "cta.lead": "Book a consultation or get in touch with our wellness experts today.",
    "cta.bookBtn": "Book Appointment →",
    "cta.exploreBtn": "Explore Services",
    "cta.point1": "Personalized Solutions",
    "cta.point2": "Expert Guidance",
    "cta.point3": "Flexible Scheduling",

    // Catalogue / Services Page
    "cat.breadcrumbHome": "Home",
    "cat.breadcrumbCatalogue": "Catalogue",
    "cat.pageTitle": "Therapy & Wellness Catalogue",
    "cat.pageSubtitle": "Browse and filter verified therapy machines, Ayurvedic Kansa tools, and mobility aids.",
    "cat.solutionCount": "Solutions Found",
    "cat.mobileFilterBtn": "Filters & Categories",
    "cat.clearAll": "Clear All",
    "cat.filterBy": "Filter By",
    "cat.group1": "1. Customer Need / Pain",
    "cat.group2": "2. Body Part",
    "cat.group3": "3. Product & Service Type",
    "cat.group4": "4. Intended Usage Setting",
    "cat.searchPlaceholder": "Search by name, description, category...",
    "cat.searchBtn": "Search",
    "cat.sortBy": "Sort By:",
    "cat.sortFeatured": "Featured Relevance",
    "cat.sortNameAsc": "Name: A to Z",
    "cat.sortNameDesc": "Name: Z to A",
    "cat.sortNewest": "Newest First",
    "cat.activeFilters": "Active filters:",
    "cat.noMatchTitle": "No matching solutions found",
    "cat.noMatchDesc": "We couldn't find any therapy machines or wellness services matching your selected combination of filters. Try clearing some filters or searching with different keywords.",
    "cat.clearFiltersBtn": "Clear All Filters",
    "cat.prev": "Previous",
    "cat.next": "Next",
    "cat.filterCatalogue": "Filter Catalogue",
    "cat.reset": "Reset",
    "cat.apply": "Apply",

    // Service Detail Page
    "sd.featured": "Featured",
    "sd.signature": "Signature Wellness Therapy",
    "sd.scopeHeading": "Therapeutic Scope & Suitability:",
    "sd.bookAppointment": "Book Appointment",
    "sd.enquireNow": "Enquire Now",
    "sd.trust1": "Certified Therapists",
    "sd.trust2": "Pure Herbal Formulations",
    "sd.trust3": "Custom Consultations",
    "sd.tabDescription": "Description",
    "sd.tabBenefits": "Benefits",
    "sd.tabUsage": "Usage Instructions",
    "sd.tabPrecautions": "Precautions",
    "sd.relatedTitle": "Related Therapy Solutions",
    "sd.relatedSubtitle": "Discover complementary wellness equipment from this discipline.",

    // Appointment Form
    "apt.title": "Book Your Appointment",
    "apt.subtitle": "Choose a service and preferred time. Our team will contact you to confirm your appointment.",
    "apt.formTitle": "Request Your Wellness Consultation or Demo",
    "apt.formDesc": "Select your preferred date, time and service. Our team coordinates each session personally to ensure undivided attention.",
    "apt.personalInfo": "1. Personal Information",
    "apt.scheduleInfo": "2. Select Service & Preferred Slot",
    "apt.chooseSolution": "-- Choose Solution * --",
    "apt.demoFormat": "Demo Format",
    "apt.formatCentre": "Centre Visit (Ahmedabad Demonstration Facility)",
    "apt.formatHome": "Home Doorstep Demo (Selected Cities)",
    "apt.formatVideo": "Virtual Guided Video Consultation",
    "apt.notes": "Address (if Home Demo) / Special Requests",
    "apt.notesPlaceholder": "Enter Address / Special Requests",
    "apt.requestBtn": "Request Appointment",
    "apt.privacy": "Requests are typically confirmed within a few hours.",

    // Enquiry Form
    "enq.title": "Product & Equipment Enquiry",
    "enq.subtitle": "Connect with our wellness specialists for pricing, clinic setups, and live equipment demos.",
    "enq.formTitle": "Your details are handled with care",
    "enq.formDesc": "We use your information to respond to your enquiry and coordinate follow-up.",
    "enq.enquiryType": "What do you need help with?",
    "enq.contactMethod": "Preferred Contact Method",
    "enq.serviceMachine": "Therapy Machine / Equipment (Optional)",
    "enq.selectService": "-- Select Service / Equipment (Optional) --",
    "enq.message": "Message / Specific Requirements",
    "enq.messagePlaceholder": "Tell us about your clinic setup requirements, product questions, or demo request...",
    "enq.sendBtn": "Send Enquiry",

    // Contact Us Page
    "contact.title": "Connect with Our Wellness Advisory",
    "contact.subtitle": "Have questions regarding therapy equipment, shipping across India, or booking a clinic trial? Reach out directly.",
    "contact.visitUs": "Demonstration & Experience Lounge",
    "contact.callUs": "Phone Helpline",
    "contact.emailUs": "Email Inquiries",
    "contact.hours": "Visiting & Consultation Hours",
    "contact.sendMessage": "Send Us a Direct Message",
    "contact.sendBtn": "Send Message",
    "contact.subject": "Subject",
    "contact.subjectPlaceholder": "e.g. Inguinal Hernia support belt inquiry",

    // About Us Page
    "aboutPage.title": "Reimagining Holistic Wellness Through Science & Vedic Metallurgy",
    "aboutPage.subtitle": "Bridging three millennia of Ayurvedic padabhyanga traditions with certified orthopedic decompression engineering.",
    "aboutPage.ourStory": "Our Heritage & Story",
    "aboutPage.vision": "Our Vision",
    "aboutPage.mission": "Our Mission",

    // Generic Common Form Fields & Labels
    "form.fullName": "Full Name",
    "form.namePlaceholder": "Enter Name",
    "form.email": "Email Address",
    "form.emailPlaceholder": "Enter Email",
    "form.phone": "Mobile Number (+91)",
    "form.phonePlaceholder": "Enter Mobile Number",
    "form.city": "City",
    "form.cityPlaceholder": "Enter City",
    "form.service": "Select Service / Machine",
    "form.date": "Preferred Date",
    "form.time": "Preferred Time",
    "form.message": "Message Details",
    "form.optional": "(Optional)",
    "form.required": "*",
    "form.submit": "Submit",

    // Buttons
    "btn.viewDetails": "View Details",
    "btn.enquireNow": "Enquire Now",
    "btn.bookAppointment": "Book Appointment",
    "btn.requestAppointment": "Request Appointment",
    "btn.submitEnquiry": "Send Enquiry",
    "btn.calculateBmi": "Calculate My BMI",
    "btn.clearFilters": "Clear All Filters",
    "btn.exploreServices": "Explore Services",
    "btn.close": "Close",
    "btn.apply": "Apply",
    "btn.reset": "Reset",

    // Footer
    "footer.desc": "Your partner in natural healing and modern wellness solutions.",
    "footer.quickLinks": "Quick Links",
    "footer.servicesTitle": "Our Services",
    "footer.contactTitle": "Contact Us",
    "footer.viewAll": "View All",
    "footer.rights": "All rights reserved.",
    "footer.privacy": "Privacy Policy",
    "footer.terms": "Terms & Conditions",
    "footer.whatsappTitle": "Contact Us on WhatsApp"
  },

  gu: {
    // Top Announcement Bar
    "top.announcement": "વિશેષ વેલનેસ જાહેરાત: કુદરતી ઉપચાર અને નવજીવન આપતી થેરાપીનો અનુભવ કરો",
    "top.announcementBadge": "વિશેષ ઑફર:",
    "top.shopNow": "હમણાં ખરીદો →",
    "top.viewOffers": "ઑફર્સ જુઓ",
    "top.searchPlaceholder": "થેરાપી મશીન, જરૂરિયાત અથવા અંગ શોધો...",
    "top.callUs": "સહાયતા માટે કૉલ કરો",
    "top.bookDemo": "ડેમો બુક કરો",

    // Navigation & Header
    "nav.home": "હોમ",
    "nav.about": "અમારા વિશે",
    "nav.services": "કેટલોગ",
    "nav.products": "ઉત્પાદનો અને સેવાઓ",
    "nav.allProducts": "બધા ઉત્પાદનો અને સેવાઓ",
    "nav.categories": "શ્રેણીઓ",
    "nav.gallery": "ગેલેરી",
    "nav.reviews": "અભિપ્રાયો",
    "nav.journal": "સ્વાસ્થ્ય પત્રિકા",
    "nav.blog": "બ્લોગ",
    "nav.faq": "પ્રશ્નોત્તરી (FAQ)",
    "nav.bmi": "BMI કેલ્ક્યુલેટર",
    "nav.offers": "ઑફર્સ",
    "nav.contact": "સંપર્ક",
    "nav.support": "સહાયતા",
    "nav.profile": "ડિજિટલ પ્રોફાઇલ",
    "nav.book": "એપોઇન્ટમેન્ટ બુક કરો",
    "nav.admin": "એડમિન સાઇટ",
    "nav.adminTitle": "એડમિન પોર્ટલ પર જાઓ",

    // Global Search Modal
    "search.modalTitle": "ઉકેલ શોધો",
    "search.placeholder": "જરૂરિયાત, અંગ અથવા મશીન દ્વારા શોધો...",
    "search.submit": "શોધો",
    "search.popular": "લોકપ્રિય શોધો:",

    // Hero Section
    "hero.badge": "તમારી સ્વાસ્થ્ય યાત્રા અહીંથી શરૂ થાય છે",
    "hero.title": "આધુનિક થેરાપી અને કુદરતી ઉપચારનું સંગમ",
    "hero.subtitle": "પરંપરાગત વેલનેસ અને આધુનિક થેરાપી સાધનોનો અદભુત સમન્વય. રુદ્ર મસાજ અને વેલનેસ સાથે સ્વસ્થ રહો, પીડામુક્ત જીવો.",
    "hero.exploreCta": "સેવાઓ જુઓ →",
    "hero.bookCta": "એપોઇન્ટમેન્ટ બુક કરો",
    "hero.pill1": "શુદ્ધ આયુર્વેદિક કારીગરી",
    "hero.pill2": "ક્લિનિકલ અર્ગોનોમિક્સ",
    "hero.pill3": "ઘરબેઠા ડેમો સુવિધા",
    "hero.slide1Tag": "સર્વાંગી થેરાપી",
    "hero.slide1Title": "સંપૂર્ણ શરીરનો ઊંડો આરામ",
    "hero.slide1Sub": "મર્મ બિંદુઓની હળવી માલિશ અને માનસિક તણાવમાંથી મુક્તિ.",
    "hero.slide2Tag": "વૈદિક ધાતુ વિજ્ઞાન",
    "hero.slide2Title": "૧૦૦% શુદ્ધ કાંસા ધાતુ",
    "hero.slide2Sub": "પગ અને ચહેરાની કુદરતી ડિટોક્સિફિકેશન થેરાપી.",
    "hero.slide3Tag": "ઓર્થોપેડિક ચોકસાઈ",
    "hero.slide3Title": "કરોડરજ્જુ ડીકોમ્પ્રેશન સારવાર",
    "hero.slide3Sub": "દવા વિના ન્યુમેટિક એર પ્રેશર દ્વારા કમરનો દુખાવો દૂર કરો.",
    "hero.bookNow": "બુક કરો →",
    "hero.explore": "વિગત જુઓ →",
    "hero.bookDemo": "ડેમો બુક કરો →",

    // Feature / Trust Cards
    "trust.card1Tag": "કુદરતી",
    "trust.card1Title": "વેલનેસ પદ્ધતિ",
    "trust.card1Opt1": "આયુર્વેદિક સિદ્ધાંતો",
    "trust.card1Opt2": "ઔષધીય થેરાપી રીતો",
    "trust.card1Opt3": "સર્વાંગી શારીરિક સંભાળ",
    "trust.card2Tag": "આધુનિક",
    "trust.card2Title": "થેરાપી સાધનો",
    "trust.card2Opt1": "ક્લિનિકલ ગુણવત્તાવાળા ઉપકરણો",
    "trust.card2Opt2": "અદ્યતન મસાજ સાધનો",
    "trust.card2Opt3": "દુખાવા નિવારણ માટે સ્માર્ટ ટેક",
    "trust.card3Tag": "તજજ્ઞ માર્ગદર્શન",
    "trust.card3Title": "અને સહાયતા",
    "trust.card3Opt1": "તાલીમબદ્ધ વેલનેસ સ્ટાફ",
    "trust.card3Opt2": "વ્યક્તિગત સલાહ",
    "trust.card3Opt3": "સારવાર પછીની સંભાળ",
    "trust.card4Tag": "ઘર અને સેન્ટર",
    "trust.card4Title": "ઉપયોગ વિકલ્પો",
    "trust.card4Opt1": "ઘરેલુ ઉપયોગના ઉપકરણો",
    "trust.card4Opt2": "સેન્ટર પર થેરાપી સત્રો",
    "trust.card4Opt3": "ઘરબેઠા ડિલિવરી સુવિધા",

    // Explore by Need Section
    "need.badge": "સર્વાંગી ઉપચાર",
    "need.title": "તમારી જરૂરિયાત પ્રમાણે શોધો",
    "need.subtitle": "તમારા દુખાવા અને જરૂરિયાત મુજબ ખાસ તૈયાર કરાયેલા યોગ્ય ઉપાયો શોધો",
    "need.backPain": "કમરનો દુખાવો",
    "need.kneePain": "ઘૂંટણનો દુખાવો",
    "need.neckShoulder": "ગરદન અને ખભાનો દુખાવો",
    "need.eyeCare": "આંખની સંભાળ",
    "need.weightMgmt": "વજન નિયંત્રણ",
    "need.stressSleep": "તણાવ અને ઊંઘ",
    "need.footLeg": "પગ અને પિંડીનો થાક",
    "need.circulation": "રક્ત પરિભ્રમણ સુધારણા",

    // Featured Products & Services
    "feat.title": "પસંદગીના ઉત્પાદનો અને સેવાઓ",
    "feat.subtitle": "તમારા સ્વાસ્થ્ય પ્રવાસ માટે પસંદ કરાયેલા ઉત્કૃષ્ટ ઉપકરણો",
    "feat.viewDetails": "વિગતો જુઓ →",
    "feat.bookAppointment": "એપોઇન્ટમેન્ટ બુક કરો",
    "feat.empty": "સંપૂર્ણ સાધનો જોવા માટે સર્વિસ કેટલોગ તપાસો.",
    "feat.featured": "પસંદગીના",

    // About Section (Homepage)
    "about.badge": "અમારો વારસો",
    "about.title": "રુદ્ર મસાજ અને વેલનેસ વિશે",
    "about.desc": "અમે પરંપરાગત આયુર્વેદિક જ્ઞાન અને આધુનિક થેરાપી ટેકનોલોજીનો સમન્વય કરીને તમને સ્વસ્થ અને પીડામુક્ત જીવન આપવા માટે કટિબદ્ધ છીએ. અમારું લક્ષ્ય કુદરતી, સલામત અને અસરકારક ઉપાયો પ્રદાન કરવાનું છે.",
    "about.learnMore": "વધુ જાણો →",
    "about.feat1": "સર્વાંગી વેલનેસ પદ્ધતિ",
    "about.feat2": "વિશ્વાસપાત્ર ગુણવત્તાના સાધનો",
    "about.feat3": "નિષ્ણાત સહાય અને માર્ગદર્શન",

    // How It Works
    "how.badge": "સરળ પ્રક્રિયા",
    "how.title": "આ કેવી રીતે કાર્ય કરે છે",
    "how.subtitle": "૩ સરળ પગલાંમાં શરૂ કરો.",
    "how.step1Title": "ઉત્પાદનો અને સેવાઓ જુઓ",
    "how.step1Desc": "અમારા વેલનેસ સાધનોની શ્રેણી જુઓ અને તમારા માટે શ્રેષ્ઠ પસંદ કરો.",
    "how.step2Title": "યોગ્ય વિકલ્પ પસંદ કરો",
    "how.step2Desc": "તમારી જરૂરિયાત મુજબ સાધન અથવા થેરાપી નક્કી કરો.",
    "how.step3Title": "બુકિંગ અથવા પૂછપરછ કરો",
    "how.step3Desc": "ફોર્મ ભરો અથવા એપોઇન્ટમેન્ટ બુક કરો. અમારી ટીમ ટૂંક સમયમાં સંપર્ક કરશે.",

    // Testimonials
    "test.title": "અમારા ગ્રાહકો શું કહે છે",
    "test.subtitle": "વાસ્તવિક અનુભવો. ઉત્તમ પરિણામો.",
    "test.verified": "ચકાસાયેલ ગ્રાહક",

    // Blog / Journal Section
    "blog.title": "હેલ્થ અને વેલનેસ જર્નલ",
    "blog.subtitle": "તમારા સારા સ્વાસ્થ્ય માટે ઉપયોગી ટિપ્સ અને માર્ગદર્શિકા.",
    "blog.viewAll": "બધા લેખો જુઓ →",
    "blog.readArticle": "લેખ વાંચો →",
    "blog.wellness": "વેલનેસ",
    "blog.lifestyle": "લાઇફસ્ટાઇલ",
    "blog.nutrition": "પોષણ",

    // CTA Banner
    "cta.title": "સારા સ્વાસ્થ્યનો અનુભવ કરવા તૈયાર છો?",
    "cta.lead": "આજે જ અમારા વેલનેસ નિષ્ણાતો સાથે કન્સલ્ટેશન બુક કરો અથવા સંપર્ક કરો.",
    "cta.bookBtn": "એપોઇન્ટમેન્ટ બુક કરો →",
    "cta.exploreBtn": "સેવાઓ જુઓ",
    "cta.point1": "વ્યક્તિગત યોગ્ય ઉપાયો",
    "cta.point2": "નિષ્ણાત માર્ગદર્શન",
    "cta.point3": "સરળ સમય વ્યવસ્થા",

    // Catalogue / Services Page
    "cat.breadcrumbHome": "હોમ",
    "cat.breadcrumbCatalogue": "કેટલોગ",
    "cat.pageTitle": "થેરાપી અને વેલનેસ કેટલોગ",
    "cat.pageSubtitle": "પ્રમાણિત થેરાપી મશીન, વૈદિક કાંસા સાધનો અને ફિઝિયોથેરાપી ઉપકરણો જુઓ અને ફિલ્ટર કરો.",
    "cat.solutionCount": "ઉકેલો ઉપલબ્ધ છે",
    "cat.mobileFilterBtn": "ફિલ્ટર્સ અને શ્રેણીઓ",
    "cat.clearAll": "બધા દૂર કરો",
    "cat.filterBy": "ફિલ્ટર કરો",
    "cat.group1": "૧. જરૂરિયાત / દુખાવો",
    "cat.group2": "૨. શરીરનું અંગ",
    "cat.group3": "૩. ઉત્પાદન અને સેવા પ્રકાર",
    "cat.group4": "૪. ઉપયોગ માટેનું સ્થળ",
    "cat.searchPlaceholder": "નામ, વિગત અથવા શ્રેણી દ્વારા શોધો...",
    "cat.searchBtn": "શોધો",
    "cat.sortBy": "ક્રમ પસંદ કરો:",
    "cat.sortFeatured": "પસંદગીના સાધનો",
    "cat.sortNameAsc": "નામ: A થી Z",
    "cat.sortNameDesc": "નામ: Z થી A",
    "cat.sortNewest": "નવીનતમ પહેલાં",
    "cat.activeFilters": "સક્રિય ફિલ્ટર્સ:",
    "cat.noMatchTitle": "કોઈ પરિણામ મળ્યું નથી",
    "cat.noMatchDesc": "તમે પસંદ કરેલા ફિલ્ટર્સ મુજબ કોઈ સાધન મળ્યું નથી. કૃપા કરીને ફિલ્ટર્સ સાફ કરો અથવા અન્ય શબ્દ શોધો.",
    "cat.clearFiltersBtn": "બધા ફિલ્ટર્સ સાફ કરો",
    "cat.prev": "અગાઉનું",
    "cat.next": "આગળનું",
    "cat.filterCatalogue": "કેટલોગ ફિલ્ટર કરો",
    "cat.reset": "રીસેટ કરો",
    "cat.apply": "લાગુ કરો",

    // Service Detail Page
    "sd.featured": "પસંદગીનું",
    "sd.signature": "સિગ્નેચર વેલનેસ થેરાપી",
    "sd.scopeHeading": "થેરાપીનો વ્યાપ અને યોગ્યતા:",
    "sd.bookAppointment": "એપોઇન્ટમેન્ટ બુક કરો",
    "sd.enquireNow": "પૂછપરછ કરો",
    "sd.trust1": "પ્રમાણિત થેરાપિસ્ટ",
    "sd.trust2": "શુદ્ધ હર્બલ ફોર્મ્યુલેશન",
    "sd.trust3": "વ્યક્તિગત સલાહ",
    "sd.tabDescription": "વિગતો",
    "sd.tabBenefits": "લાભો અને ફાયદા",
    "sd.tabUsage": "ઉપયોગ કરવાની રીત",
    "sd.tabPrecautions": "સાવચેતીઓ",
    "sd.relatedTitle": "સંબંધિત થેરાપી સાધનો",
    "sd.relatedSubtitle": "આ વિભાગના અન્ય પૂરક વેલનેસ સાધનો જુઓ.",

    // Appointment Form
    "apt.title": "તમારી એપોઇન્ટમેન્ટ બુક કરો",
    "apt.subtitle": "સેવા અને તમારી પસંદગીનો સમય પસંદ કરો. અમારી ટીમ પુષ્ટિ માટે તમારો સંપર્ક કરશે.",
    "apt.formTitle": "વેલનેસ કન્સલ્ટેશન અથવા ડેમો વિનંતી",
    "apt.formDesc": "તારીખ, સમય અને સેવા પસંદ કરો. અમારી ટીમ દરેક સત્ર વ્યક્તિગત ધ્યાનપૂર્વક સુનિશ્ચિત કરે છે.",
    "apt.personalInfo": "૧. અંગત વિગતો",
    "apt.scheduleInfo": "૨. સેવા અને સમય પસંદ કરો",
    "apt.chooseSolution": "-- સાધન અથવા સેવા પસંદ કરો * --",
    "apt.demoFormat": "ડેમોનો પ્રકાર",
    "apt.formatCentre": "સેન્ટર મુલાકાત (અમદાવાદ ફેસિલિટી)",
    "apt.formatHome": "ઘરબેઠા ડેમો (પસંદગીના શહેરોમાં)",
    "apt.formatVideo": "ઓનલાઇન વિડીયો કન્સલ્ટેશન",
    "apt.notes": "સરનામું (ઘરબેઠા ડેમો માટે) / ખાસ વિગત",
    "apt.notesPlaceholder": "સરનામું અથવા ખાસ જરૂરિયાત અહીં લખો...",
    "apt.requestBtn": "એપોઇન્ટમેન્ટ વિનંતી મોકલો",
    "apt.privacy": "તમારી વિગતો સુરક્ષિત છે. ડેમો વિનંતી માટે કોઈ અગાઉ ચૂકવણી જરૂરી નથી.",

    // Enquiry Form
    "enq.title": "ઉત્પાદન અને સાધન પૂછપરછ",
    "enq.subtitle": "કિંમત, ક્લિનિક સેટઅપ અને લાઇવ સાધન ડેમો માટે અમારા નિષ્ણાતો સાથે સંપર્ક કરો.",
    "enq.formTitle": "તમારી વિગતો કાળજીપૂર્વક સાચવવામાં આવે છે",
    "enq.formDesc": "અમે તમારી પૂછપરછનો જવાબ આપવા અને ફોલો-અપ કરવા માટે તમારી વિગતોનો ઉપયોગ કરીએ છીએ.",
    "enq.enquiryType": "તમારે કઈ બાબતમાં મદદ જોઈએ છે?",
    "enq.contactMethod": "સંપર્ક માટે પસંદગીની રીત",
    "enq.serviceMachine": "થેરાપી મશીન / સાધન (વૈકલ્પિક)",
    "enq.selectService": "-- સાધન / સેવા પસંદ કરો (વૈકલ્પિક) --",
    "enq.message": "સંદેશ / ખાસ જરૂરિયાતો",
    "enq.messagePlaceholder": "ક્લિનિક સેટઅપ, ઉત્પાદન પ્રશ્નો અથવા ડેમો વિનંતી વિશે અહીં લખો...",
    "enq.sendBtn": "પૂછપરછ મોકલો",

    // Contact Us Page
    "contact.title": "અમારા વેલનેસ સલાહકારો સાથે સંપર્ક કરો",
    "contact.subtitle": "થેરાપી સાધનો, ઓલ-ઇન્ડિયા શિપિંગ અથવા ક્લિનિક ટ્રાયલ વિશે પ્રશ્નો છે? સીધો સંપર્ક કરો.",
    "contact.visitUs": "પ્રદર્શન અને અનુભવ કેન્દ્ર",
    "contact.callUs": "ફોન હેલ્પલાઇન",
    "contact.emailUs": "ઈમેલ પૂછપરછ",
    "contact.hours": "મુલાકાત અને કન્સલ્ટેશન સમય",
    "contact.sendMessage": "અમને સીધો સંદેશ મોકલો",
    "contact.sendBtn": "સંદેશ મોકલો",
    "contact.subject": "વિષય",
    "contact.subjectPlaceholder": "દા.ત. હર્નિયા સપોર્ટ બેલ્ટ પૂછપરછ",

    // About Us Page
    "aboutPage.title": "વિજ્ઞાન અને વૈદિક ધાતુશાસ્ત્ર દ્વારા સર્વાંગી વેલનેસનો નવો વિચાર",
    "aboutPage.subtitle": "ત્રણ હજાર વર્ષ જૂની આયુર્વેદિક પાદઅભ્યંગ પરંપરા અને પ્રમાણિત ઓર્થોપેડિક ડીકોમ્પ્રેશન ટેકનોલોજીનું સંગમ.",
    "aboutPage.ourStory": "અમારો ઇતિહાસ અને યાત્રા",
    "aboutPage.vision": "અમારો દ્રષ્ટિકોણ (Vision)",
    "aboutPage.mission": "અમારું ધ્યેય (Mission)",

    // Generic Common Form Fields & Labels
    "form.fullName": "પૂરું નામ",
    "form.namePlaceholder": "નામ દાખલ કરો",
    "form.email": "ઈમેલ એડ્રેસ",
    "form.emailPlaceholder": "ઈમેલ દાખલ કરો",
    "form.phone": "મોબાઇલ નંબર (+91)",
    "form.phonePlaceholder": "મોબાઇલ નંબર દાખલ કરો",
    "form.city": "શહેર",
    "form.cityPlaceholder": "શહેર દાખલ કરો",
    "form.service": "સાધન અથવા સેવા પસંદ કરો",
    "form.date": "પસંદગીની તારીખ",
    "form.time": "પસંદગીનો સમય",
    "form.message": "સંદેશની વિગત",
    "form.optional": "(વૈકલ્પિક)",
    "form.required": "*",
    "form.submit": "સબમિટ કરો",

    // Buttons
    "btn.viewDetails": "વિગતો જુઓ",
    "btn.enquireNow": "પૂછપરછ કરો",
    "btn.bookAppointment": "એપોઇન્ટમેન્ટ બુક કરો",
    "btn.requestAppointment": "એપોઇન્ટમેન્ટ વિનંતી મોકલો",
    "btn.submitEnquiry": "પૂછપરછ મોકલો",
    "btn.calculateBmi": "મારું BMI ગણો",
    "btn.clearFilters": "બધા ફિલ્ટર્સ સાફ કરો",
    "btn.exploreServices": "સેવાઓ જુઓ",
    "btn.close": "બંધ કરો",
    "btn.apply": "લાગુ કરો",
    "btn.reset": "રીસેટ કરો",

    // Footer
    "footer.desc": "કુદરતી સારવાર અને આધુનિક વેલનેસ ઉકેલોમાં તમારા વિશ્વસનીય ભાગીદાર.",
    "footer.quickLinks": "ઝડપી લિંક્સ",
    "footer.servicesTitle": "અમારી સેવાઓ",
    "footer.contactTitle": "સંપર્ક કરો",
    "footer.viewAll": "બધા જુઓ",
    "footer.rights": "સર્વાધિકાર સુરક્ષિત.",
    "footer.privacy": "ગોપનીયતા નીતિ",
    "footer.terms": "નિયમો અને શરતો",
    "footer.whatsappTitle": "WhatsApp પર સંપર્ક કરો"
  }
};

// Comprehensive bidirectional phrase map for un-annotated elements & taxonomy
const PHRASE_MAP = {
  // Navigation & Core Labels
  "Home": "હોમ",
  "About Us": "અમારા વિશે",
  "Catalogue": "કેટલોગ",
  "Services": "સેવાઓ",
  "All Products & Services": "બધા ઉત્પાદનો અને સેવાઓ",
  "Products & Services": "ઉત્પાદનો અને સેવાઓ",
  "Categories": "શ્રેણીઓ",
  "Gallery": "ગેલેરી",
  "Blog": "બ્લોગ",
  "Contact": "સંપર્ક",
  "Contact Us": "સંપર્ક કરો",
  "Support": "સહાયતા",
  "Admin Site": "એડમિન સાઇટ",
  "Offers": "ઑફર્સ",
  "Digital Profile": "ડિજિટલ પ્રોફાઇલ",
  "BMI Calculator": "BMI કેલ્ક્યુલેટર",
  "FAQ": "પ્રશ્નોત્તરી (FAQ)",
  "Certificates": "પ્રમાણપત્રો",
  "Reviews": "અભિપ્રાયો",
  "Testimonials": "અભિપ્રાયો",

  // Action Buttons
  "Explore Services": "સેવાઓ જુઓ",
  "Explore Services →": "સેવાઓ જુઓ →",
  "Explore Services &rarr;": "સેવાઓ જુઓ →",
  "Book Appointment": "એપોઇન્ટમેન્ટ બુક કરો",
  "Book Appointment →": "એપોઇન્ટમેન્ટ બુક કરો →",
  "Book Appointment &rarr;": "એપોઇન્ટમેન્ટ બુક કરો →",
  "Book Now": "બુક કરો",
  "Book Now →": "બુક કરો →",
  "Book Now &rarr;": "બુક કરો →",
  "Book Demo →": "ડેમો બુક કરો →",
  "Book Demo &rarr;": "ડેમો બુક કરો →",
  "Explore →": "વિગત જુઓ →",
  "Explore &rarr;": "વિગત જુઓ →",
  "View Details": "વિગતો જુઓ",
  "View Details →": "વિગતો જુઓ →",
  "View Details &rarr;": "વિગતો જુઓ →",
  "Learn More →": "વધુ જાણો →",
  "Learn More &rarr;": "વધુ જાણો →",
  "Read Article →": "લેખ વાંચો →",
  "Read Article &rarr;": "લેખ વાંચો →",
  "View All Articles →": "બધા લેખો જુઓ →",
  "View All Articles &rarr;": "બધા લેખો જુઓ →",
  "Shop Now →": "હમણાં ખરીદો →",
  "Shop Now &rarr;": "હમણાં ખરીદો →",
  "Enquire Now": "પૂછપરછ કરો",
  "Enquire Now →": "પૂછપરછ કરો →",
  "Enquire Now &rarr;": "પૂછપરછ કરો →",
  "Send Enquiry": "પૂછપરછ મોકલો",
  "Send Message": "સંદેશ મોકલો",
  "Request Appointment": "એપોઇન્ટમેન્ટ વિનંતી મોકલો",
  "Calculate My BMI": "મારું BMI ગણો",
  "Clear All": "બધા દૂર કરો",
  "Clear All Filters": "બધા ફિલ્ટર્સ સાફ કરો",
  "Search": "શોધો",
  "Sort By:": "ક્રમ પસંદ કરો:",
  "Previous": "અગાઉનું",
  "Next": "આગળનું",
  "Apply": "લાગુ કરો",
  "Reset": "રીસેટ",

  // Sections & Headings
  "Explore by Need": "તમારી જરૂરિયાત પ્રમાણે શોધો",
  "Find the right solution for your wellness needs": "તમારા સ્વાસ્થ્ય માટે યોગ્ય ઉપાય પસંદ કરો",
  "Featured Products & Services": "પસંદગીના ઉત્પાદનો અને સેવાઓ",
  "Handpicked solutions for your wellness journey": "તમારા સ્વાસ્થ્ય પ્રવાસ માટે પસંદ કરાયેલા ઉત્કૃષ્ટ ઉપકરણો",
  "About Rudra Massage & Wellness": "રુદ્ર મસાજ અને વેલનેસ વિશે",
  "How It Works": "આ કેવી રીતે કાર્ય કરે છે",
  "Get started in 3 simple steps.": "૩ સરળ પગલાંમાં શરૂ કરો.",
  "What Our Customers Say": "અમારા ગ્રાહકો શું કહે છે",
  "Real experiences. Better lives.": "વાસ્તવિક અનુભવો. ઉત્તમ પરિણામો.",
  "Health & Wellness Journal": "હેલ્થ અને વેલનેસ જર્નલ",
  "Tips, guides and insights for a healthier you.": "તમારા સારા સ્વાસ્થ્ય માટે ઉપયોગી ટિપ્સ અને માર્ગદર્શિકા.",
  "Ready to Experience Better Well-being?": "સારા સ્વાસ્થ્યનો અનુભવ કરવા તૈયાર છો?",
  "Book a consultation or get in touch with our wellness experts today.": "આજે જ અમારા વેલનેસ નિષ્ણાતો સાથે કન્સલ્ટેશન બુક કરો અથવા સંપર્ક કરો.",
  "Quick Links": "ઝડપી લિંક્સ",
  "Our Services": "અમારી સેવાઓ",
  "Privacy Policy": "ગોપનીયતા નીતિ",
  "Terms & Conditions": "નિયમો અને શરતો",
  "All rights reserved.": "સર્વાધિકાર સુરક્ષિત.",
  "Verified Client": "ચકાસાયેલ ગ્રાહક",

  // Customer Needs
  "Back Pain": "કમરનો દુખાવો",
  "Knee Pain": "ઘૂંટણનો દુખાવો",
  "Neck & Shoulder": "ગરદન અને ખભાનો દુખાવો",
  "Neck Pain": "ગરદનનો દુખાવો",
  "Eye Care": "આંખની સંભાળ",
  "Eye Strain": "આંખનો થાક",
  "Weight Management": "વજન નિયંત્રણ",
  "Stress & Sleep": "તણાવ અને ઊંઘ",
  "Sleep & Stress": "ઊંઘ અને માનસિક તણાવ",
  "Foot & Leg Fatigue": "પગ અને પિંડીનો થાક",
  "Foot Care": "પગની સંભાળ",
  "Circulation Support": "રક્ત પરિભ્રમણ સુધારણા",
  "Hair Care": "વાળની સંભાળ",

  // Categories & Service Types
  "Therapy Machines": "થેરાપી મશીન્સ",
  "Massagers": "મસાજર્સ",
  "Exercise Equipment": "કસરત સાધનો",
  "Kansa Therapy": "કાંસા થેરાપી",
  "Surgical & Support": "સર્જિકલ અને સપોર્ટ",
  "Surgical & Support Products": "સર્જિકલ અને સપોર્ટ પ્રોડક્ટ્સ",
  "Back Massage & Therapy Equipment": "કમર મસાજ અને થેરાપી સાધનો",
  "Body Composition & BMI Equipment": "શરીર બંધારણ અને BMI સાધનો",
  "EMS & Muscle Stimulation Equipment": "EMS અને સ્નાયુ ઉત્તેજના સાધનો",
  "Electrical Massage Equipment": "ઇલેક્ટ્રિકલ મસાજ સાધનો",
  "Eye & Head Wellness Equipment": "આંખ અને માથાના વેલનેસ સાધનો",
  "Kansa/Kashya Therapy Equipment": "કાંસા થેરાપી સાધનો",
  "Hand & Foot Massagers": "હાથ અને પગના મસાજર",
  "Traditional Wellness Equipment": "પરંપરાગત વેલનેસ સાધનો",
  "Knee & Leg Massagers": "ઘૂંટણ અને પગના મસાજર",
  "Leg & Foot Massagers": "પિંડી અને પગના મસાજર",
  "Massage Chairs": "મસાજ ચેર",
  "Percussion Massagers": "પર્કશન મસાજર",

  // Body Parts
  "Back": "કમર / પીઠ",
  "Knees": "ઘૂંટણ",
  "Neck": "ગરદન",
  "Shoulders": "ખભા",
  "Feet": "પગના તળિયા",
  "Legs": "પગ / પિંડી",
  "Eyes": "આંખો",
  "Head": "માથું",
  "Hands": "હાથ",
  "Full Body": "સંપૂર્ણ શરીર",

  // Usage Settings
  "Home Use": "ઘરેલુ ઉપયોગ",
  "Clinic/Centre": "ક્લિનિક / સેન્ટર",
  "Elderly-Friendly": "વરિષ્ઠ નાગરિકો માટે અનુકૂળ",
  "Elderly-Friendly Products": "વરિષ્ઠ નાગરિકો માટે અનુકૂળ સાધનો",

  // Form Labels & Prompts
  "Full Name": "પૂરું નામ",
  "Your Name": "તમારું નામ",
  "Your Full Name": "તમારું પૂરું નામ",
  "Email Address": "ઈમેલ એડ્રેસ",
  "Mobile Number (+91)": "મોબાઇલ નંબર (+91)",
  "City": "શહેર",
  "Preferred Date": "પસંદગીની તારીખ",
  "Preferred Time": "પસંદગીનો સમય",
  "Subject": "વિષય",
  "Demo Format": "ડેમોનો પ્રકાર",
  "Select Service / Machine": "સાધન અથવા સેવા પસંદ કરો",
  "Your Message / Specific Concerns": "તમારો સંદેશ અથવા ચોક્કસ વિગત",
  "Message Details": "સંદેશની વિગત",
  "Address (if Home Demo) / Special Requests": "સરનામું (ઘરબેઠા ડેમો માટે) / ખાસ વિગત",
  "Health Concerns / Specific Notes": "આરોગ્ય સંબંધી તકલીફ / ખાસ નોંધ",
  "What do you need help with?": "તમારે કઈ બાબતમાં મદદ જોઈએ છે?",
  "Preferred Contact Method": "સંપર્ક માટે પસંદગીની રીત",
  "Therapy machine / wellness product": "થેરાપી મશીન / વેલનેસ સાધન",
  "Home wellness setup": "ઘર માટે વેલનેસ સેટઅપ",
  "Clinic / professional setup": "ક્લિનિક / પ્રોફેશનલ સેટઅપ",
  "Bulk or business enquiry": "જથ્થાબંધ અથવા બિઝનેસ પૂછપરછ",
  "Existing product support": "ખરીદેલ સાધન માટે સહાયતા",
  "Not sure — I need guidance": "ખાતરી નથી — માર્ગદર્શન જોઈએ છે",
  "Phone": "ફોન",
  "WhatsApp": "વોટ્સએપ",
  "Email": "ઈમેલ",

  // Time Slots & Demo Formats
  "-- Choose Solution * --": "-- સાધન અથવા સેવા પસંદ કરો * --",
  "-- Choose Slot * --": "-- સમય પસંદ કરો * --",
  "-- Choose Subject --": "-- વિષય પસંદ કરો --",
  "Morning (10:00 AM - 1:00 PM)": "સવાર (૧૦:૦૦ AM - ૧:૦૦ PM)",
  "Midday (1:00 PM - 3:00 PM)": "બપોર (૧:૦૦ PM - ૩:૦૦ PM)",
  "Afternoon (3:00 PM - 5:00 PM)": "બપોર પછી (૩:૦૦ PM - ૫:૦૦ PM)",
  "Evening (5:00 PM - 7:30 PM)": "સાંજ (૫:૦૦ PM - ૭:૩૦ PM)",
  "Centre Visit (Ahmedabad Facility)": "સેન્ટર મુલાકાત (અમદાવાદ ફેસિલિટી)",
  "Centre Visit (Ahmedabad Demonstration Facility)": "સેન્ટર મુલાકાત (અમદાવાદ પ્રદર્શન કેન્દ્ર)",
  "Home Doorstep Demo (Selected Cities)": "ઘરબેઠા ડેમો (પસંદગીના શહેરોમાં)",
  "Virtual Guided Video Consultation": "ઓનલાઇન વિડીયો કન્સલ્ટેશન",

  // Filter Group Headers
  "1. Customer Need / Pain": "૧. જરૂરિયાત / દુખાવો",
  "2. Body Part": "૨. શરીરનું અંગ",
  "3. Product & Service Type": "૩. ઉત્પાદન અને સેવા પ્રકાર",
  "4. Intended Usage Setting": "૪. ઉપયોગ માટેનું સ્થળ",
  "Featured Relevance": "પસંદગીના ઉપકરણો",
  "Name: A to Z": "નામ: A થી Z",
  "Name: Z to A": "નામ: Z થી A",
  "Newest First": "નવીનતમ પહેલાં",

  // Trust Card Points
  "Ayurvedic principles": "આયુર્વેદિક સિદ્ધાંતો",
  "Herbal therapy methods": "ઔષધીય થેરાપી રીતો",
  "Holistic body care": "સર્વાંગી શારીરિક સંભાળ",
  "Clinical-grade devices": "ક્લિનિકલ ગુણવત્તાવાળા ઉપકરણો",
  "Advanced massage tools": "અદ્યતન મસાજ સાધનો",
  "Smart pain relief tech": "દુખાવા નિવારણ માટે સ્માર્ટ ટેક",
  "Trained wellness staff": "તાલીમબદ્ધ વેલનેસ સ્ટાફ",
  "Personalised advice": "વ્યક્તિગત સલાહ",
  "Post-treatment care": "સારવાર પછીની સંભાળ",
  "Home-use devices": "ઘરેલુ ઉપયોગના ઉપકરણો",
  "Centre sessions": "સેન્ટર પર થેરાપી સત્રો",
  "Doorstep delivery": "ઘરબેઠા ડિલિવરી સુવિધા",

  // How it works items
  "Explore Products & Services": "ઉત્પાદનો અને સેવાઓ જુઓ",
  "Browse our wide range of wellness solutions and find what suits you.": "અમારા વેલનેસ સાધનોની શ્રેણી જુઓ અને તમારા માટે શ્રેષ્ઠ પસંદ કરો.",
  "Choose a Relevant Option": "યોગ્ય વિકલ્પ પસંદ કરો",
  "Select your preferred product, service or therapy.": "તમારી જરૂરિયાત મુજબ સાધન અથવા થેરાપી નક્કી કરો.",
  "Book or Enquire": "બુકિંગ અથવા પૂછપરછ કરો",
  "Fill in the form or book an appointment. We'll get back to you soon.": "ફોર્મ ભરો અથવા એપોઇન્ટમેન્ટ બુક કરો. અમે ટૂંક સમયમાં સંપર્ક કરીશું.",

  // Hero carousel slides
  "Holistic Therapy": "સર્વાંગી થેરાપી",
  "Full Body Deep Relaxation": "સંપૂર્ણ શરીરનો ઊંડો આરામ",
  "Gentle pressure marma point recovery & stress release.": "મર્મ બિંદુઓની હળવી માલિશ અને માનસિક તણાવમાંથી મુક્તિ.",
  "Vedic Metallurgy": "વૈદિક ધાતુ વિજ્ઞાન",
  "100% Pure Kansa Bronze": "૧૦૦% શુદ્ધ કાંસા ધાતુ",
  "Bio-metallic detoxification for foot & facial vitality.": "પગ અને ચહેરાની કુદરતી ડિટોક્સિફિકેશન થેરાપી.",
  "Orthopedic Precision": "ઓર્થોપેડિક ચોકસાઈ",
  "Spinal Curvature Decompression": "કરોડરજ્જુ ડીકોમ્પ્રેશન સારવાર",
  "Drug-free pneumatic air bladder lumbar traction.": "દવા વિના ન્યુમેટિક એર પ્રેશર દ્વારા કમરનો દુખાવો દૂર કરો.",

  // Value items
  "Personalized Solutions": "વ્યક્તિગત યોગ્ય ઉપાયો",
  "Expert Guidance": "નિષ્ણાત માર્ગદર્શન",
  "Flexible Scheduling": "સરળ સમય વ્યવસ્થા",
  "Holistic Wellness Approach": "સર્વાંગી વેલનેસ પદ્ધતિ",
  "Trusted Quality Products": "વિશ્વાસપાત્ર ગુણવત્તાના સાધનો",
  "Expert Support & Guidance": "નિષ્ણાત સહાય અને માર્ગદર્શન",

  // Gallery filters & tags
  "All Showcase": "બધા પ્રદર્શન",
  "Vedic Kansa Metal": "વૈદિક કાંસા ધાતુ",
  "Demonstration Centre": "પ્રદર્શન કેન્દ્ર",
  "Live Sessions": "લાઇવ સત્રો",
  "Flagship Centre": "મુખ્ય કેન્દ્ર",
  "Heritage Craft": "વારસાગત કારીગરી",
  "Clinical Therapy": "ક્લિનિકલ થેરાપી",

  // Testimonials filters & badges
  "All Reviews": "બધા અભિપ્રાયો",
  "Back Pain Relief": "કમરના દુખાવામાં રાહત",
  "Knee Pain Relief": "ઘૂંટણના દુખાવામાં રાહત",
  "Stress & Relaxation": "માનસિક તણાવ અને આરામ",

  // Enquiry Usage & Callback
  "Personal / Family Home Use": "વ્યક્તિગત / પારિવારિક ઘરેલુ ઉપયોગ",
  "Physiotherapy / Wellness Clinic": "ફિઝિયોથેરાપી / વેલનેસ ક્લિનિક",
  "Specialized Senior Citizen Care": "વરિષ્ઠ નાગરિકો માટે વિશેષ સંભાળ",
  "Bulk Dealership / Reselling": "જથ્થાબંધ ડીલરશીપ / પુનઃવેચાણ",
  "Usage Intention": "ઉપયોગનો હેતુ",
  "Preferred Callback Time": "કૉલબેક માટે પસંદગીનો સમય",
  "Anytime": "ગમે ત્યારે",
  "Afternoon (2:00 PM - 5:00 PM)": "બપોર (૨:૦૦ PM - ૫:૦૦ PM)",
  "Evening (5:00 PM - 8:00 PM)": "સાંજ (૫:૦૦ PM - ૮:૦૦ PM)",

  // FAQ categories
  "General Wellness": "સામાન્ય વેલનેસ",
  "Equipment & Orders": "સાધન અને ઓર્ડર",
  "Appointments & Trials": "એપોઇન્ટમેન્ટ અને ટ્રાયલ",
  "Warranty & Maintenance": "વોરંટી અને જાળવણી",

  // BMI Calculator
  "Height": "ઊંચાઈ",
  "Weight": "વજન",
  "Age": "ઉંમર",
  "Gender": "જાતિ",
  "Male": "પુરુષ",
  "Female": "સ્ત્રી",
  "Sedentary": "બેઠાડુ",
  "Moderate": "મધ્યમ",
  "Active": "સક્રિય",

  // Support
  "Submit a Support Request Ticket": "સહાયતા વિનંતી ટિકિટ સબમિટ કરો",
  "Your Support Request": "તમારી સહાયતા વિનંતી",
  "Customer Care & Support Hub": "ગ્રાહક સેવા અને સહાયતા કેન્દ્ર",
  "Track Support Ticket": "ટિકિટ સ્થિતિ જાણો",
  "Contact Support": "સહાયતા માટે સંપર્ક કરો"
};

// Inverse phrase mapping for Gujarati -> English
const REVERSE_PHRASE_MAP = {};
for (const [enKey, guVal] of Object.entries(PHRASE_MAP)) {
  REVERSE_PHRASE_MAP[guVal] = enKey;
}

class LanguageManager {
  constructor() {
    this.currentLang = this.getStoredLanguage();
    this.init();
  }

  getStoredLanguage() {
    // Check localStorage first
    try {
      const local = localStorage.getItem("preferred_lang");
      if (local && (local === "en" || local === "gu")) return local;
    } catch (e) {}

    // Check cookie fallback
    const match = document.cookie.match(/(?:^|;\s*)(?:django_language|preferred_lang)=([^;]+)/);
    if (match && (match[1] === "en" || match[1] === "gu")) {
      return match[1];
    }

    return "en";
  }

  saveLanguage(lang) {
    try {
      localStorage.setItem("preferred_lang", lang);
    } catch (e) {}
    // Save to cookies for server-side persistence with Django LocaleMiddleware
    const expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1);
    const cookieOpts = `;path=/;expires=${expires.toUTCString()};SameSite=Lax`;
    document.cookie = `preferred_lang=${lang}${cookieOpts}`;
    document.cookie = `django_language=${lang}${cookieOpts}`;
  }

  init() {
    this.applyTranslations(this.currentLang);
    this.setupListeners();
    this.observeDOM();
  }

  setLanguage(lang) {
    if (!TRANSLATIONS[lang]) return;
    this.currentLang = lang;
    this.saveLanguage(lang);
    this.applyTranslations(lang);
    this.updateActiveButtonState();

    // Notify any components listening for language change
    try {
      window.dispatchEvent(new CustomEvent("languageChanged", { detail: { language: lang } }));
    } catch (e) {}
  }

  applyTranslations(lang) {
    const dict = TRANSLATIONS[lang];
    if (!dict) return;

    // Set document lang attribute
    document.documentElement.setAttribute("lang", lang);

    // 1. Update elements marked with [data-i18n]
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      const targetText = dict[key];
      if (!targetText) return;

      const textSpan = el.querySelector(".i18n-text");
      if (textSpan) {
        textSpan.textContent = targetText;
      } else if (el.children.length === 0) {
        el.textContent = targetText;
      } else {
        // Preserve nested elements (icons, badges, arrows)
        let replaced = false;
        for (let node of el.childNodes) {
          if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0) {
            const hasLeading = node.textContent.startsWith(" ");
            const hasTrailing = node.textContent.endsWith(" ");
            node.textContent = (hasLeading ? " " : "") + targetText + (hasTrailing ? " " : "");
            replaced = true;
            break;
          }
        }
        if (!replaced) {
          el.textContent = targetText;
        }
      }
    });

    // 2. Update placeholders marked with [data-i18n-placeholder]
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (dict[key]) {
        el.setAttribute("placeholder", dict[key]);
      }
    });

    // 3. Update titles marked with [data-i18n-title]
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      const key = el.getAttribute("data-i18n-title");
      if (dict[key]) {
        el.setAttribute("title", dict[key]);
        if (el.hasAttribute("aria-label")) {
          el.setAttribute("aria-label", dict[key]);
        }
      }
    });

    // 4. Update HTML marked with [data-i18n-html]
    document.querySelectorAll("[data-i18n-html]").forEach(el => {
      const key = el.getAttribute("data-i18n-html");
      if (dict[key]) {
        el.innerHTML = dict[key];
      }
    });

    // 5. Automatic Phrase Translation Fallback for common UI text, cards, and taxonomy
    this.translateCommonPhrases(lang);
  }

  translateCommonPhrases(lang) {
    const isGu = (lang === "gu");
    const activeMap = isGu ? PHRASE_MAP : REVERSE_PHRASE_MAP;

    // Target clickable buttons, labels, headings, badges, and list items without [data-i18n]
    const candidates = document.querySelectorAll(
      "a, button, span, label, h1, h2, h3, h4, h5, h6, option, small, p, li"
    );

    candidates.forEach(el => {
      // Do not touch admin panel or inputs/scripts
      if (el.closest("#customAdminNav") || el.closest(".site-admin") || el.tagName === "SCRIPT" || el.tagName === "STYLE") {
        return;
      }

      // Never translate specific database product model names (protect verified brand names)
      if (el.classList.contains("product-card-title") || el.classList.contains("product-title") || el.classList.contains("brand-name")) {
        return;
      }

      // Check text-only content
      if (el.children.length === 0) {
        const raw = el.textContent.trim();
        // Replace &rarr; or -> normalization
        const clean = raw.replace(/\s*→\s*$/, "").replace(/\s*&rarr;\s*$/, "");
        if (activeMap[raw]) {
          el.textContent = activeMap[raw];
        } else if (activeMap[clean]) {
          const suffix = (raw.includes("→") || raw.includes("&rarr;")) ? " →" : "";
          el.textContent = activeMap[clean] + suffix;
        }
      } else {
        // Walk direct text nodes
        for (let node of el.childNodes) {
          if (node.nodeType === Node.TEXT_NODE) {
            const raw = node.textContent.trim();
            if (!raw) continue;
            const clean = raw.replace(/\s*→\s*$/, "").replace(/\s*&rarr;\s*$/, "");
            if (activeMap[raw]) {
              const hasLeading = node.textContent.startsWith(" ");
              const hasTrailing = node.textContent.endsWith(" ");
              node.textContent = (hasLeading ? " " : "") + activeMap[raw] + (hasTrailing ? " " : "");
            } else if (activeMap[clean]) {
              const suffix = (raw.includes("→") || raw.includes("&rarr;")) ? " →" : "";
              const hasLeading = node.textContent.startsWith(" ");
              const hasTrailing = node.textContent.endsWith(" ");
              node.textContent = (hasLeading ? " " : "") + activeMap[clean] + suffix + (hasTrailing ? " " : "");
            }
          }
        }
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
      const btnLang = btn.getAttribute("data-lang");
      if (btnLang === this.currentLang) {
        btn.classList.add("active");
        btn.setAttribute("aria-pressed", "true");
      } else {
        btn.classList.remove("active");
        btn.setAttribute("aria-pressed", "false");
      }
    });
  }

  observeDOM() {
    // Automatically apply translations if modals, offcanvas, or dynamic content changes
    const observer = new MutationObserver((mutations) => {
      let shouldTranslate = false;
      for (const m of mutations) {
        if (m.addedNodes && m.addedNodes.length > 0) {
          shouldTranslate = true;
          break;
        }
      }
      if (shouldTranslate && this.currentLang === "gu") {
        clearTimeout(this._debounceTimer);
        this._debounceTimer = setTimeout(() => {
          this.applyTranslations(this.currentLang);
        }, 100);
      }
    });

    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }
}

// Global initialization
let langManager;
document.addEventListener("DOMContentLoaded", () => {
  langManager = new LanguageManager();
  window.langManager = langManager;
});
