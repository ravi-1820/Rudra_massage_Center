/**
 * Rudra Massage & Wellness - Central Therapy Dataset
 * Includes comprehensive items across 18 Categories, Needs, Body Parts, and Usages.
 * Formatted for easy future backend API replacement.
 */

const WELLNESS_PRODUCTS = [
  {
    id: "wt-101",
    name: "AyurSpine Deep Shiatsu Lumbar & Back Decompression Belt",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Back Pain",
    needSlug: "back-pain",
    bodyPart: "Back",
    bodyPartSlug: "back",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 4999,
    originalPrice: 7499,
    rating: 4.9,
    reviewsCount: 142,
    badge: "Bestseller",
    shortDesc: "Pneumatic traction belt designed to alleviate spinal compression and soothe chronic lower back stiffness.",
    description: "Engineered with clinical spinal decompression technology, the AyurSpine traction belt gently stretches the lumbar spine to relieve pressure from herniated discs, sciatica, and lower back fatigue. Crafted with skin-friendly breathable cotton and ergonomic hand-pump inflation, it provides immediate targeted relief during work or rest.",
    image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Dynamic Air Traction: Expands up to 2.8x vertically to unload spinal facet joints",
      "Dual Lumbar Support: Magnet therapy integration with 16 therapeutic nodes",
      "Universal Ergonomic Fit: Accommodates waist circumferences from 28 to 48 inches",
      "Lightweight Portability: Can be worn discreetly beneath everyday clothing"
    ],
    specifications: {
      "Material": "Medical-Grade TPU + Breathable Organic Cotton",
      "Pressure Range": "0.15 - 0.28 MPa",
      "Weight": "650g",
      "Warranty": "2 Years Comprehensive Replacement Warranty"
    },
    precautions: "Do not use over unhealed surgical incisions. Consult your physician if diagnosed with severe osteoporosis or spondylolisthesis.",
    tags: ["Lumbar Support", "Air Traction", "Spine Care", "Ayurvedic Alignment"]
  },
  {
    id: "wt-102",
    name: "Pure Vedic Bronze (Kansa) Vataki Foot Therapy Massager",
    category: "Kansa Therapy",
    categorySlug: "kansa-therapy",
    need: "Foot & Leg Fatigue",
    needSlug: "foot-leg-fatigue",
    bodyPart: "Feet",
    bodyPartSlug: "feet",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 3299,
    originalPrice: 4899,
    rating: 4.8,
    reviewsCount: 98,
    badge: "Traditional Ayurvedic",
    shortDesc: "Authentic copper-tin bell metal bowl mechanized with harmonic oscillation for dosha balancing.",
    description: "Rooted in ancient Charaka Samhita traditions, the Kansa Vataki massager utilizes a sacred alloy of copper and tin to draw excess pitta (heat) and toxins from the soles of your feet. Upgraded with smooth dual-direction rotational vibration, it soothes tired feet, stimulates marma reflexology points, and promotes deeply restorative sleep.",
    image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "High Purity Kansa Alloy (78% Copper, 22% Tin) for maximum bio-resonance",
      "Dual Speed Harmonic Vibration with ultra-quiet 35dB copper-wound motor",
      "Includes 100ml Cold-Pressed Sesame & Eranda Foot Elixir",
      "Ergonomic Foot Cradle for comfortable seated self-therapy sessions"
    ],
    specifications: {
      "Bowl Diameter": "120 mm Pure Cast Bronze",
      "Power Input": "12V DC Adapter (Energy efficient 18W)",
      "Vibration Speed": "1200 - 2400 RPM",
      "Origin": "Hand-forged by artisan metalsmiths in Gujarat"
    },
    precautions: "Best paired with authentic botanical oils. Wipe clean with a dry microfiber cloth; avoid synthetic harsh detergents.",
    tags: ["Kansa Bowl", "Padabhyanga", "Sleep Remedy", "Marma Reflexology"]
  },
  {
    id: "wt-103",
    name: "OrthoRelief Infrared Heated Knee & Joint Physiotherapy Guard",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Knee Pain",
    needSlug: "knee-pain",
    bodyPart: "Knees",
    bodyPartSlug: "knees",
    usage: "Elderly-Friendly Products",
    usageSlug: "elderly-friendly",
    price: 3899,
    originalPrice: 5999,
    rating: 4.9,
    reviewsCount: 215,
    badge: "Senior Choice",
    shortDesc: "Triple-action therapy combining far-infrared heat, air compression, and gentle high-frequency vibration.",
    description: "Designed specifically for older adults and individuals battling joint stiffness, the OrthoRelief wrap surrounds the patella with 360-degree thermotherapy. Far-infrared wavelengths penetrate deep into the synovial capsule, increasing local blood flow and reducing morning stiffness without heavy medications.",
    image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Far-Infrared Carbon Fiber Heat: 3 temperature presets (45°C, 55°C, 65°C)",
      "Pulsed Air Pressure Massage mimicking manual physical therapy kneading",
      "Large High-Contrast Touch LED screen with audible prompts for elders",
      "Cordless Rechargeable Battery (3000mAh) offering 120 minutes of runtime"
    ],
    specifications: {
      "Battery Life": "Up to 8 sessions per charge",
      "Adjustable Straps": "Fits leg circumferences up to 60 cm",
      "Auto Timer": "15, 20, and 30-minute safety cut-off",
      "Certifications": "CE, RoHS, Medical Device ISO 13485 compliant"
    },
    precautions: "Begin therapy on lowest temperature level. Do not apply directly over acute inflammation with swelling less than 48 hours old.",
    tags: ["Knee Rehabilitation", "Infrared Heat", "Joint Care", "Elderly Friendly"]
  },
  {
    id: "wt-104",
    name: "CervicalFlex Smart Trapezius & Neck Acupressure Massager",
    category: "Massagers",
    categorySlug: "massagers",
    need: "Neck & Shoulder Pain",
    needSlug: "neck-shoulder-pain",
    bodyPart: "Neck",
    bodyPartSlug: "neck",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 2799,
    originalPrice: 4299,
    rating: 4.7,
    reviewsCount: 167,
    badge: "Popular",
    shortDesc: "3D bionic pinch rollers with soothing thermo-therapy targeting stiff trapezius and suboccipital muscles.",
    description: "Counteract long hours of screen posture and desk slump. CervicalFlex features patented 8-roller nodes that reproduce the thumbs-and-palms technique of a seasoned massage therapist. Positioned comfortably over your neck and shoulders, the hands-free shoulder harness lets you relax or read while releasing tension.",
    image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Dual Bi-Directional Nodes that alternate rotation every 60 seconds",
      "Integrated 42°C Hyper-Warmth function to melt away trigger points",
      "Multi-Position Use: Works wonders on neck, upper back, thighs, and calves",
      "Soft vegan PU leather with hygienic washable mesh lining"
    ],
    specifications: {
      "Motor Torque": "Pure Copper High-Torque 24W Engine",
      "Noise Level": "< 40 dB whisper quiet",
      "Power Source": "Dual use (AC wall adapter & 12V car adapter included)"
    },
    precautions: "Do not apply intense pressure against the carotid sinus. Avoid use during sudden neck trauma or whiplash without clinical clearance.",
    tags: ["Cervical Tension", "Desk Posture", "Deep Kneading", "Heat Therapy"]
  },
  {
    id: "wt-105",
    name: "OcuRest Smart Air-Pressure & Bluetooth Eye Care Massager",
    category: "Massagers",
    categorySlug: "massagers",
    need: "Eye Strain",
    needSlug: "eye-strain",
    bodyPart: "Eyes",
    bodyPartSlug: "eyes",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 2499,
    originalPrice: 3999,
    rating: 4.8,
    reviewsCount: 184,
    badge: "Top Rated",
    shortDesc: "Gentle rhythmic temple compression, warm compress, and ambient soundscapes to relieve digital eye fatigue.",
    description: "Formulated for professionals, students, and night-owls experiencing dry eyes and tension headaches. OcuRest gently massages the periorbital acupoints around the eyes and temples. Heated compresses warm the meibomian glands, encouraging natural eye moisture and relieving screen fatigue.",
    image: "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Gentle Micro-Airbags targeting Jingming and Sizhukong acupressure points",
      "Soothing Constant 40°C Warm Compress to stimulate tear-film lipids",
      "Foldable 180° Clamshell Design with luxurious suede interior",
      "Integrated Bluetooth 5.0 for relaxing ambient binaural audio"
    ],
    specifications: {
      "Battery": "1200mAh Lithium polymer, USB-C fast charging",
      "Weight": "Ultra-light 280g",
      "Folding Angle": "180 degrees with travel pouch included"
    },
    precautions: "Remove contact lenses before use. Not recommended for patients with detached retina, recent eye surgery, or glaucoma.",
    tags: ["Digital Detox", "Dry Eyes", "Temple Relief", "Sleep Aid"]
  },
  {
    id: "wt-106",
    name: "AyurShiro Shirodhara Automated Drip Therapy Console",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Sleep & Stress Management",
    needSlug: "sleep-stress-management",
    bodyPart: "Head",
    bodyPartSlug: "head",
    usage: "Clinic / Centre Use",
    usageSlug: "clinic-centre",
    price: 34999,
    originalPrice: 44999,
    rating: 5.0,
    reviewsCount: 46,
    badge: "Clinical Professional",
    shortDesc: "Automated continuous herbal oil flow console with precise digital temperature control for authentic Shirodhara.",
    description: "The gold standard in Ayurvedic therapy centres and luxury wellness resorts. AyurShiro modernizes the classical Shirodhara ritual by maintaining continuous, uninterrupted herbal oil stream onto the forehead (Ajna Marma) at precise Ayurvedic body temperature without manual pouring.",
    image: "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Micro-Controlled Constant Heating: 36°C to 41°C digital thermostat",
      "Continuous Silent Recirculation with food-grade peristaltic pump",
      "Solid Handcrafted Brass Vessel with drip-control valve",
      "Sturdy 304 Stainless Steel adjustable boom stand on medical caster wheels"
    ],
    specifications: {
      "Vessel Capacity": "3.5 Liters",
      "Power": "220V AC, 350W peak heating",
      "Stand Adjustment": "110 cm to 185 cm height"
    },
    precautions: "Intended for qualified therapists, clinics, and professional wellness practitioners.",
    tags: ["Shirodhara", "Panchakarma", "Stress Reduction", "Ajna Marma"]
  },
  {
    id: "wt-107",
    name: "VedaRoot Scalp Micro-Current & Red Light Therapy Helmet",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Hair & Scalp Care",
    needSlug: "hair-scalp-care",
    bodyPart: "Head",
    bodyPartSlug: "head",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 8999,
    originalPrice: 13999,
    rating: 4.8,
    reviewsCount: 79,
    badge: "Wellness Tech",
    shortDesc: "650nm medical-grade low-level laser diodes combined with botanical oil mist infusion combs.",
    description: "Revitalize weakened hair follicles through dual bio-stimulation. The VedaRoot helmet uses targeted 650nm red light wavelengths to energize mitochondrial ATP production in cellular roots, while integrated micro-current teeth gently stimulate micro-circulation throughout the scalp.",
    image: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "108 Medical Precision 650nm Red Light diodes for full scalp coverage",
      "TENS Micro-Current stimulation to enhance absorption of hair tonics",
      "Built-in 10-minute auto timer with sensor shutoff when removed",
      "Ergonomic weight distribution with adjustable headband cushioning"
    ],
    specifications: {
      "Laser Power": "5mW per diode, Class 3R safe rating",
      "Wavelength": "650nm +/- 10nm",
      "Charging": "Magnetic dock station with USB-C"
    },
    precautions: "Do not stare directly into the active laser diodes. Keep out of reach of children.",
    tags: ["Scalp Rejuvenation", "Red Light Therapy", "Follicle Health", "Ayurvedic Hair"]
  },
  {
    id: "wt-108",
    name: "PranaFlow Sequential Pneumatic Leg & Foot Compression Boots",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Circulation Support",
    needSlug: "circulation-support",
    bodyPart: "Legs",
    bodyPartSlug: "legs",
    usage: "Clinic / Centre Use",
    usageSlug: "clinic-centre",
    price: 11999,
    originalPrice: 17999,
    rating: 4.9,
    reviewsCount: 134,
    badge: "Athletic & Recovery",
    shortDesc: "6-chamber overlapping air sleeves for lymphatic drainage, varicose relief, and athletic metabolic flush.",
    description: "Favored by wellness clinics, marathoners, and individuals dealing with heavy, restless legs. PranaFlow mimics the muscular pump of the calves, directing venous return upward from the ankles to the upper thighs. It rapidly accelerates lactic acid clearance and reduces dependent edema.",
    image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "6 Overlapping Gradient Pressure Chambers for seamless continuous flow",
      "4 Specialized Modes: Lymphatic Flush, Recovery Knead, Target Pulse, Full Pump",
      "Pressure adjustability from 20 to 250 mmHg with digital dial",
      "Heavy-duty ripstop nylon boots with durable air-tight zippers"
    ],
    specifications: {
      "Chambers": "6 Independent pneumatic zones",
      "Pressure Range": "20 - 250 mmHg",
      "Sizes": "Standard (up to 5'10\") and Tall (5'11\" and above)"
    },
    precautions: "Contraindicated in severe active deep vein thrombosis (DVT) or acute skin infections of the lower limbs.",
    tags: ["Lymphatic Drainage", "Leg Compression", "Athletic Recovery", "Circulation"]
  },
  {
    id: "wt-109",
    name: "AgniFit Whole Body Vibration Therapeutic Platform",
    category: "Exercise Equipment",
    categorySlug: "exercise-equipment",
    need: "Weight Management & Fitness",
    needSlug: "weight-management-fitness",
    bodyPart: "Full Body",
    bodyPartSlug: "full-body",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 9499,
    originalPrice: 14999,
    rating: 4.7,
    reviewsCount: 112,
    badge: "Metabolic Boost",
    shortDesc: "Linear and oscillatory dual-motor plate that activates 95% of muscle fibers and accelerates calorie burn.",
    description: "Stimulate systemic circulation, improve bone mineral density, and enhance core stability in just 10 minutes a day. The AgniFit vibration plate triggers rapid involuntary reflex muscle contractions, elevating metabolic rate while placing minimal strain on connective joint tissues.",
    image: "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Dual 500W Silent Drive Motors: Oscillating + Micro-Pulsing vibration",
      "99 Speed Levels & 5 Pre-programmed metabolic training routines",
      "Magnetic Acupressure Foot Surface with non-skid suction base",
      "Includes 2 Resistance Training Straps & Wireless Remote Controller"
    ],
    specifications: {
      "Max User Weight": "150 kg (330 lbs)",
      "Amplitude": "0 - 12 mm",
      "Dimensions": "68 x 38 x 14 cm"
    },
    precautions: "Not suitable for pregnant women, individuals with acute fractures or retinal implants. Consult your doctor first.",
    tags: ["Metabolism", "Bone Density", "Vibration Plate", "Core Tone"]
  },
  {
    id: "wt-110",
    name: "Kansa Shringara Handcrafted Face & Jawline Sculpting Wand",
    category: "Kansa Therapy",
    categorySlug: "kansa-therapy",
    need: "Sleep & Stress Management",
    needSlug: "sleep-stress-management",
    bodyPart: "Head",
    bodyPartSlug: "head",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 1899,
    originalPrice: 2699,
    rating: 4.9,
    reviewsCount: 230,
    badge: "Handcrafted",
    shortDesc: "Vedic beauty ritual wand crafted with carved teak wood and bronze alloy to release facial jaw tension.",
    description: "Centuries of Ayurvedic wisdom captured in an ergonomic personal beauty and stress-release wand. Massaging the face with pure Kansa metal helps neutralize acidity, drains stagnant lymphatic fluid, defines facial contours, and relieves subconscious clenching of the jaw muscles.",
    image: "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Sacred alloy of 78% copper and 22% tin for natural alkaline balancing",
      "Carved Sheesham (Indian Rosewood) handle with satin grip finish",
      "Sculpted dome contours smoothly over jawline, cheekbones, and brow",
      "Includes velvet storage pouch and Kumkumadi face oil miniature"
    ],
    specifications: {
      "Dome Size": "42 mm contoured diameter",
      "Weight": "115g lightweight",
      "Maintenance": "Clean with gentle lemon-salt paste or dry cloth"
    },
    precautions: "Gentle pressure is sufficient. Grayish residue during initial massages is a natural oxidation sign of acid release.",
    tags: ["Facial Marma", "Jaw Tension", "Ayurvedic Glow", "Kansa Wand"]
  },
  {
    id: "wt-111",
    name: "SpinoPosture Orthopedic Clavicle & Upper Spine Corrector",
    category: "Surgical & Support Products",
    categorySlug: "surgical-support",
    need: "Neck & Shoulder Pain",
    needSlug: "neck-shoulder-pain",
    bodyPart: "Shoulders",
    bodyPartSlug: "shoulders",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 1499,
    originalPrice: 2199,
    rating: 4.6,
    reviewsCount: 153,
    badge: "Ergonomic Essential",
    shortDesc: "Breathable posture brace that gently retracts rounded shoulders and retrains spinal memory.",
    description: "Fix forward-head syndrome and slouching shoulders without restrictive rigidity. SpinoPosture utilizes high-tensile cross-back elastic webbing that cues your neuromuscular system to maintain an upright, open chest posture, instantly reducing strain on thoracic spine and clavicle.",
    image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Breathable Honeycomb Neoprene mesh prevents heat and sweat buildup",
      "Dual adjustable velcro shoulder straps for tailored tension",
      "Slim profile fits smoothly under formal shirts or kurtas",
      "Reinforced back support plate to guide spinal centerline"
    ],
    specifications: {
      "Sizes Available": "S (28-34 in), M (34-40 in), L (40-46 in), XL (46-52 in)",
      "Wash Care": "Hand wash with mild soap, air dry"
    },
    precautions: "Wear for 20-30 minutes on day one, gradually increasing up to 2 hours. Do not wear during sleep.",
    tags: ["Posture Correction", "Rounded Shoulders", "Desk Support", "Spine Guard"]
  },
  {
    id: "wt-112",
    name: "DharaSteam Ayurvedic Herbal Steam Sauna Generator & Tent",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Weight Management & Fitness",
    needSlug: "weight-management-fitness",
    bodyPart: "Full Body",
    bodyPartSlug: "full-body",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 6899,
    originalPrice: 9999,
    rating: 4.8,
    reviewsCount: 88,
    badge: "Swedana Therapy",
    shortDesc: "Portable personal herbal steam tent with external herb-infusion kettle for classical Swedana sweat detox.",
    description: "Recreate the purifying Swedana chamber of Ayurvedic wellness retreats in your own home. The DharaSteam system features an external boiler with dedicated herb chambers for Dashamoola, eucalyptus, or neem leaves, directing warm therapeutic steam around the body while keeping your head cool outside.",
    image: "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Quick Pop-up Insulated Tent with waterproof zippered hand openings",
      "2.5 Liter Smart Steamer with 9 heat levels and anti-dry burn safety",
      "Herb & Essential Oil Diffuser Box for fresh botanical decoctions",
      "Includes foldable sturdy therapy chair and floor absorbent mat"
    ],
    specifications: {
      "Boiler Power": "1000W rapid steam generation in 7 minutes",
      "Tent Dimensions": "80 x 80 x 100 cm compact footprint",
      "Safety": "Automatic shut-off upon low water detection"
    },
    precautions: "Limit sessions to 15-20 minutes. Keep well hydrated before and after. Not advised during high fever or acute hypertension.",
    tags: ["Swedana", "Detox Sauna", "Herbal Steam", "Sweat Therapy"]
  },
  {
    id: "wt-113",
    name: "ThermoGrip Heated Carpal Tunnel & Hand Arthritis Massager",
    category: "Massagers",
    categorySlug: "massagers",
    need: "Neck & Shoulder Pain",
    needSlug: "neck-shoulder-pain",
    bodyPart: "Hands",
    bodyPartSlug: "hands",
    usage: "Elderly-Friendly Products",
    usageSlug: "elderly-friendly",
    price: 3199,
    originalPrice: 4799,
    rating: 4.8,
    reviewsCount: 92,
    badge: "Hand Mobility",
    shortDesc: "Air-compression glove with thousands of acupressure dimples and warm palm heating for stiff fingers.",
    description: "Provides welcome relief for typists, artisans, knitters, and seniors with morning knuckle stiffness. ThermoGrip envelopes fingers, palm, and wrist in rhythmic sequential air compression. Acupressure microbeads press gently along hand meridian channels to restore flexibility and finger warmth.",
    image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Multi-Segment Airbag Cushioning from finger joints to wrist",
      "2 Heating Levels (38°C / 43°C) to soothe cold hand numbness",
      "6 Intensity Levels and 6 programmed massage rhythms",
      "Cordless USB rechargeable battery with up to 15 full sessions"
    ],
    specifications: {
      "Weight": "790g portable",
      "Chamber Size": "Spacious opening accommodates small to extra-large hands",
      "Charging Port": "USB Type-C"
    },
    precautions: "Do not use if you have severe open skin lesions on hands or immediate post-fracture recovery without therapist guidance.",
    tags: ["Hand Arthritis", "Carpal Tunnel", "Finger Stiffness", "Acupressure Glove"]
  },
  {
    id: "wt-114",
    name: "VedaSound Harmonic Tibetan Singing Bowl & Gong Frequency Set",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Sleep & Stress Management",
    needSlug: "sleep-stress-management",
    bodyPart: "Full Body",
    bodyPartSlug: "full-body",
    usage: "Clinic / Centre Use",
    usageSlug: "clinic-centre",
    price: 7999,
    originalPrice: 11999,
    rating: 4.9,
    reviewsCount: 64,
    badge: "Sound Therapy",
    shortDesc: "Seven-metal bell bronze singing bowl tuned precisely to 432Hz alpha-wave relaxation resonance.",
    description: "Used by meditation masters, sound healers, and holistic clinics. Hand-hammered with 7 sacred planetary metals (copper, tin, gold, silver, iron, lead, mercury), each bowl emits rich, lingering acoustic frequencies that guide brainwaves from agitated Beta states into calming Theta meditation.",
    image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Authentic Hand-Hammered 7-Metal Composition",
      "Precisely Tuned 432Hz Sound Healing Resonance frequency",
      "Includes dual-ended suede & rosewood striker and brocade ring cushion",
      "Certificate of acoustic frequency tuning included"
    ],
    specifications: {
      "Diameter": "22 cm (approx 8.7 inches)",
      "Weight": "1.35 kg heavy brass/bronze alloy",
      "Tone": "Deep foundational F# tone (Heart & Throat chakra synergy)"
    },
    precautions: "Handle with reverence. Polish occasionally with dry organic cotton; keep away from harsh moisture.",
    tags: ["Sound Healing", "Nada Yoga", "Meditation", "432Hz Frequency"]
  },
  {
    id: "wt-115",
    name: "LumbarArch 3-Tier Multi-Level Spinal Stretcher & Acupressure Pad",
    category: "Exercise Equipment",
    categorySlug: "exercise-equipment",
    need: "Back Pain",
    needSlug: "back-pain",
    bodyPart: "Back",
    bodyPartSlug: "back",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 999,
    originalPrice: 1799,
    rating: 4.6,
    reviewsCount: 290,
    badge: "Budget Hero",
    shortDesc: "Mechanical spinal decompression arch with 88 acupressure nodes and soft silicone spine cushion.",
    description: "A simple, non-electric tool that delivers immense decompression relief. Simply place on the floor or behind your office chair and recline for 5-10 minutes. The adjustable curvature expands the space between vertebrae, alleviating pinched nerves and tight erector spinae muscles.",
    image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "3 Adjustable Arch Slots for beginner, intermediate, and deep stretch angles",
      "88 Acupressure Points stimulating meridian points along the bladder channel",
      "Thickened center silicone strip protects the spinous processes from hard contact",
      "Tough ABS polymer construction supports up to 130 kg"
    ],
    specifications: {
      "Material": "Eco-friendly ABS & NBR foam",
      "Weight": "520g ultra-portable",
      "Dimensions": "38.5 x 25.5 cm"
    },
    precautions: "Start on Level 1 (lowest incline). Roll onto your side to stand up after reclining; do not snap upward abruptly.",
    tags: ["Spine Alignment", "Lumbar Traction", "Office Ergonomics", "Budget Friendly"]
  },
  {
    id: "wt-116",
    name: "Kansa Marma Foot Bath Hydrotherapy Vessel (Vedic Spa Basin)",
    category: "Kansa Therapy",
    categorySlug: "kansa-therapy",
    need: "Foot & Leg Fatigue",
    needSlug: "foot-leg-fatigue",
    bodyPart: "Feet",
    bodyPartSlug: "feet",
    usage: "Clinic / Centre Use",
    usageSlug: "clinic-centre",
    price: 8499,
    originalPrice: 12499,
    rating: 4.9,
    reviewsCount: 51,
    badge: "Heritage Spa",
    shortDesc: "Traditional bronze wash basin with textured bottom for herbal foot soaks and sensory grounding.",
    description: "Designed for premium Ayurvedic wellness centres and serene home foot spas. Hand-turned by ancestral metalsmiths, the natural copper-tin bell metal maintains water warmth and imparts subtle bio-cleansing properties to warm Epsom salt or Dashamoola foot baths.",
    image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Solid Handcrafted Heavy Gauge Bell Metal Alloy",
      "Textured base pebbles for self-guided marma foot acupressure",
      "Wide rim accommodates full adult foot sizes with ample water depth",
      "Naturally anti-microbial and rust-resistant finish"
    ],
    specifications: {
      "Basin Diameter": "40 cm (15.7 inches)",
      "Capacity": "Approx 10 Liters",
      "Weight": "3.8 kg heavy-cast bronze"
    },
    precautions: "Do not expose to aggressive chemical bleaches. Dry with clean towel after each hydrotherapy session.",
    tags: ["Foot Bath", "Hydrotherapy", "Kansa Basin", "Ayurvedic Spa"]
  },
  {
    id: "wt-117",
    name: "VedaStep Smart Walking Insole & Reflexology Pressure Sensors",
    category: "Surgical & Support Products",
    categorySlug: "surgical-support",
    need: "Foot & Leg Fatigue",
    needSlug: "foot-leg-fatigue",
    bodyPart: "Feet",
    bodyPartSlug: "feet",
    usage: "Elderly-Friendly Products",
    usageSlug: "elderly-friendly",
    price: 1999,
    originalPrice: 2999,
    rating: 4.7,
    reviewsCount: 118,
    badge: "Foot Orthotics",
    shortDesc: "Gel arch support insoles with targeted magnet therapy nodes and heel shock dampening.",
    description: "Transform any shoe into an orthopedic haven. VedaStep insoles feature medical-grade silicone shock absorption, deep heel cup stabilization, and strategically embedded neodymium magnets positioned over planetary reflex points to stimulate energy pathways with every step.",
    image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Plantar Fasciitis Relief through contoured anatomical arch support",
      "8 Bio-Magnetic nodes per foot stimulating circulatory flow",
      "Perforated breathable fabric layer reduces moisture and odor",
      "Cut-to-size customizable template fits Indian shoe sizes 6 to 11"
    ],
    specifications: {
      "Material": "Medical TPE Gel + Antimicrobial velvet top",
      "Thickness": "6mm at heel tapering to 3mm at toes"
    },
    precautions: "Trim with clean scissors along provided cut guides. Avoid soaking in hot water.",
    tags: ["Arch Support", "Plantar Fasciitis", "Reflexology", "Comfort Insole"]
  },
  {
    id: "wt-118",
    name: "AyurGlow Infrared & Ionic Herbal Facial Steam Vaporizer",
    category: "Therapy Machines",
    categorySlug: "therapy-machines",
    need: "Eye Strain",
    needSlug: "eye-strain",
    bodyPart: "Eyes",
    bodyPartSlug: "eyes",
    usage: "Home Use",
    usageSlug: "home-use",
    price: 1799,
    originalPrice: 2599,
    rating: 4.8,
    reviewsCount: 176,
    badge: "Skin & Sinus",
    shortDesc: "Nano-ionic warm steam vapor generator with dedicated chamber for tulsi, eucalyptus, and mint leaves.",
    description: "Clear congested airways, relieve dry eye irritations, and purify facial skin pores with ultrafine nano-ionic steam particles that penetrate 10x deeper than regular steam vaporizers. The built-in stainless chamber accepts fresh herbs and essential oils without clogging.",
    image: "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=800&q=80"
    ],
    features: [
      "Nano-Ionic Mist Generator produces vapor in under 30 seconds",
      "Dedicated Botanical Basket for herbal decoctions or essential oils",
      "Adjustable 360-degree nozzle for seated comfort",
      "Smart Auto Shut-off when water reservoir is depleted"
    ],
    specifications: {
      "Water Tank": "150 ml capacity (provides 18 minutes of continuous mist)",
      "Power": "280W quick heating system"
    },
    precautions: "Keep face at least 20cm away from the nozzle. Use filtered or RO water for longevity.",
    tags: ["Herbal Inhalation", "Sinus Comfort", "Nano Steam", "Facial Detox"]
  }
];

// The 18 Primary Categories of Wellness & Therapy
const WELLNESS_CATEGORIES = [
  { id: 1, name: "Spine & Lumbar Decompression", slug: "spine-lumbar", icon: "bi-shield-check", count: 8, image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=600&q=80", desc: "Clinically engineered traction belts and posture alignment tools." },
  { id: 2, name: "Vedic Kansa Metal Therapy", slug: "kansa-therapy", icon: "bi-flower1", count: 6, image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=600&q=80", desc: "Authentic bronze bowl and wand tools for dosha balancing." },
  { id: 3, name: "Infrared Joint & Knee Care", slug: "joint-knee-care", icon: "bi-heart-pulse", count: 7, image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=600&q=80", desc: "Therapeutic heat, pulsed vibration, and patella protection guards." },
  { id: 4, name: "Cervical & Trapezius Relief", slug: "cervical-trapezius", icon: "bi-person-standing", count: 9, image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=600&q=80", desc: "3D bionic pinch rollers and neck traction supports." },
  { id: 5, name: "Smart Eye & Temple Rejuvenation", slug: "eye-temple", icon: "bi-eye", count: 5, image: "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=600&q=80", desc: "Air-pressure compression and warm compresses for digital strain." },
  { id: 6, name: "Shirodhara & Head Oil Flow", slug: "shirodhara-head", icon: "bi-droplet", count: 4, image: "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80", desc: "Automated temperature-controlled classical oil consoles." },
  { id: 7, name: "Red Light Scalp & Hair Bio-Stimulation", slug: "scalp-hair", icon: "bi-brightness-high", count: 5, image: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80", desc: "Low-level 650nm light therapy and scalp micro-current combs." },
  { id: 8, name: "Pneumatic Compression Boots", slug: "compression-boots", icon: "bi-activity", count: 6, image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=600&q=80", desc: "Multi-chamber gradient pressure for lymphatic and venous return." },
  { id: 9, name: "Metabolic Vibration Platforms", slug: "vibration-platforms", icon: "bi-lightning-charge", count: 4, image: "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80", desc: "Reflexive muscle activation and bone density conditioning." },
  { id: 10, name: "Acupressure & Reflexology Mat Systems", slug: "acupressure-reflexology", icon: "bi-grid-3x3-gap", count: 8, image: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=600&q=80", desc: "Meridian-aligned acupoints for full-body home release." },
  { id: 11, name: "Swedana Herbal Steam Enclosures", slug: "herbal-steam", icon: "bi-cloud-haze", count: 4, image: "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80", desc: "Botanical vapor generation and insulated personal tents." },
  { id: 12, name: "Sound & Frequency Bowls (Nada Yoga)", slug: "sound-therapy", icon: "bi-soundwave", count: 5, image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=600&q=80", desc: "432Hz harmonic Tibetan bell bronze meditation bowls." },
  { id: 13, name: "Orthopedic Supports & Clavicle Braces", slug: "orthopedic-supports", icon: "bi-bandaid", count: 11, image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=600&q=80", desc: "Medical breathable posture aligners and joint splints." },
  { id: 14, name: "Carpal & Hand Mobility Massagers", slug: "hand-mobility", icon: "bi-hand-index", count: 5, image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=600&q=80", desc: "Warm pneumatic gloves for keyboard fatigue and arthritis." },
  { id: 15, name: "Foot Spa & Padabhyanga Hydrotherapy", slug: "foot-spa", icon: "bi-water", count: 6, image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=600&q=80", desc: "Heavy bronze soak vessels and bubbling thermal spas." },
  { id: 16, name: "Facial Marma & Bronze Sculpting Wands", slug: "facial-marma", icon: "bi-gem", count: 7, image: "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=600&q=80", desc: "Ayurvedic beauty wands for lymphatic facial contouring." },
  { id: 17, name: "Elderly-Friendly Mobility & Safety Aids", slug: "senior-care", icon: "bi-person-arms-up", count: 9, image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=600&q=80", desc: "Ergonomic walkers, high-contrast monitors, and gentle wraps." },
  { id: 18, name: "Herbal Inhalation & Vapor Nebulizers", slug: "inhalation-nebulizers", icon: "bi-lungs", count: 6, image: "https://images.unsplash.com/photo-1512290900672-1a4030438ec6?auto=format&fit=crop&w=600&q=80", desc: "Nano-ionic herbal steamers for clear breath and sinus calm." }
];

// Blog Posts Data
const WELLNESS_BLOGS = [
  {
    id: "blog-1",
    title: "Understanding Spinal Decompression: How Daily Air Traction Relieves Lower Back Compression",
    category: "Spine Health",
    date: "October 10, 2026",
    readTime: "5 min read",
    author: "Dr. Alok Verma, BAMS",
    image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
    excerpt: "Modern sedentary desk culture causes progressive disc compression. Discover how gentle pneumatic traction can expand intervertebral space naturally without invasive measures.",
    tags: ["Back Pain", "Ergonomics", "Spine Care"]
  },
  {
    id: "blog-2",
    title: "The Science of Kansa Metal: Why Bronze Has Been Used in Padabhyanga Foot Massage for 3,000 Years",
    category: "Ayurveda & Dosha",
    date: "October 04, 2026",
    readTime: "7 min read",
    author: "Vaidya Meera Joshi",
    image: "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
    excerpt: "Ancient texts extol the copper-tin alloy known as Kansa for its bio-negative ion balance. Learn the exact marma points activated during a 15-minute evening foot session.",
    tags: ["Kansa Therapy", "Sleep", "Ayurvedic Rituals"]
  },
  {
    id: "blog-3",
    title: "Combating Tech Neck & Trapezius Trigger Points: A Physical Therapist's Guide",
    category: "Modern Therapy",
    date: "September 28, 2026",
    readTime: "4 min read",
    author: "Pooja Patel, Senior Physiotherapist",
    image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
    excerpt: "Holding your head forward at 45 degrees places 49 pounds of force on your cervical spine. Explore three targeted stretching techniques and thermal knead routines.",
    tags: ["Posture", "Neck Pain", "Wellness Tech"]
  }
];

// Testimonials Sample Data
const WELLNESS_TESTIMONIALS = [
  {
    id: "test-1",
    name: "Rajesh S. Parekh",
    location: "Ahmedabad, Gujarat",
    rating: 5,
    therapyType: "AyurSpine Decompression Belt",
    comment: "After struggling with L4-L5 lumbar discomfort from long car drives, this belt gave me tangible relief within 2 weeks. The quality of the air pump and stitching feels truly medical-grade.",
    verified: true,
    date: "September 2026"
  },
  {
    id: "test-2",
    name: "Hansaben Patel",
    location: "Vadodara, Gujarat",
    rating: 5,
    therapyType: "Kansa Vataki Foot Massager",
    comment: "My night-time restlessness and burning feet sensation in summers was unbearable. Using the Kansa foot bowl with sesame oil before sleep has become a sacred ritual. Deep sleep is back!",
    verified: true,
    date: "August 2026"
  },
  {
    id: "test-3",
    name: "Dr. K. N. Joshi",
    location: "Surat, Gujarat",
    rating: 5,
    therapyType: "OrthoRelief Infrared Knee Guard",
    comment: "Recommended this for my 68-year-old mother. The large touch controls and gentle warmth allow her to operate it independently twice a day. Her stair-climbing confidence has improved remarkably.",
    verified: true,
    date: "October 2026"
  }
];

// Sample Offers Data
const WELLNESS_OFFERS = [
  {
    id: "off-1",
    title: "Navratri & Diwali Festive Wellness Bundle",
    discount: "Flat 25% OFF",
    code: "FESTIVE25",
    desc: "Valid on all Kansa Metal Therapy & Ayurvedic Steam Chambers. Bring timeless healing home this season.",
    expiry: "Valid till November 15, 2026",
    tag: "Festive Exclusive"
  },
  {
    id: "off-2",
    title: "Senior Citizens Spine & Joint Care Special",
    discount: "Extra ₹1,500 OFF",
    code: "SENIORCARE",
    desc: "Applies on orders including Knee Thermal Wraps, Lumbar Traction Belts, and Supportive Insoles above ₹5,000.",
    expiry: "Ongoing Community Offer",
    tag: "Elders First"
  },
  {
    id: "off-3",
    title: "Centre & Clinic Bulk Trial Demo Package",
    discount: "Free Live Demo & Training",
    code: "CLINICPRO",
    desc: "Book a complimentary in-clinic demo session for Shirodhara consoles and Lymphatic Compression boots.",
    expiry: "Limited to verified practitioners",
    tag: "Practitioner Demo"
  }
];
