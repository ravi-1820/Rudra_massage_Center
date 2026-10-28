"""
Rudra Massage & Wellness - Central Translation Catalogue & Taxonomy Mappings
Provides verified Gujarati <-> English translations for taxonomy, UI labels,
and dynamic database content while ensuring safe fallbacks.
"""

TAXONOMY_GU = {
    # Categories
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
    "Verification Required – Therapy Equipment": "થેરાપી સાધનો (ચકાસણી હેઠળ)",
    "Massagers – exact type to verify": "મસાજર (ચકાસણી હેઠળ)",
    "Surgical & Support Products": "સર્જિકલ અને સપોર્ટ પ્રોડક્ટ્સ",
    "Therapy Machines": "થેરાપી મશીન્સ",
    "Massagers": "મસાજર્સ",
    "Exercise Equipment": "કસરત સાધનો",
    "Kansa Therapy": "કાંસા થેરાપી",

    # Customer Needs
    "Back Pain": "કમરનો દુખાવો",
    "Knee Pain": "ઘૂંટણનો દુખાવો",
    "Neck Pain": "ગરદનનો દુખાવો",
    "Neck & Shoulder Pain": "ગરદન અને ખભાનો દુખાવો",
    "Eye Care": "આંખની સંભાળ",
    "Eye Strain": "આંખનો થાક",
    "Sleep & Stress": "ઊંઘ અને માનસિક તણાવ",
    "Sleep & Stress Management": "ઊંઘ અને માનસિક તણાવ નિવારણ",
    "Weight Management": "વજન નિયંત્રણ",
    "Weight Management & Fitness": "વજન નિયંત્રણ અને ફિટનેસ",
    "Foot Care": "પગની સંભાળ",
    "Foot & Leg Fatigue": "પગ અને પિંડીનો થાક",
    "Circulation Support": "રક્ત પરિભ્રમણ સુધારણા",
    "Hair Care": "વાળની સંભાળ",

    # Body Parts
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
    "Kansa Foot Massage": "કાંસા પાદઅભ્યંગ",

    # Service Types
    "Surgical and Support Products": "સર્જિકલ અને સપોર્ટ સાધનો",

    # Intended Uses
    "Home Use": "ઘરેલુ ઉપયોગ",
    "Clinic/Centre": "ક્લિનિક / સેન્ટર",
    "Elderly-Friendly": "વરિષ્ઠ નાગરિકો માટે અનુકૂળ",
    "Elderly-Friendly Products": "વરિષ્ઠ નાગરિકો માટે અનુકૂળ સાધનો",

    # Common announcement badges & links
    "Special Offer": "વિશેષ ઑફર",
    "Shop Now →": "હમણાં ખરીદો →",
    "View Offers": "ઑફર્સ જુઓ",
}


def translate_taxonomy_term(term, lang="gu"):
    """
    Translates a taxonomy name or returns the original term as fallback.
    """
    if not term:
        return ""
    if lang == "gu":
        return TAXONOMY_GU.get(term.strip(), term)
    return term
