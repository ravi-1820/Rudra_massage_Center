from django import template
from user.translation_catalog import translate_taxonomy_term

register = template.Library()


@register.filter(name="translate_term")
def translate_term_filter(value, lang_code=""):
    """
    Translates a taxonomy string (Category, Need, Body Part, etc.) into Gujarati
    if the language is 'gu', otherwise preserves the original English value.
    """
    if not value:
        return ""
    code = (str(lang_code) or "en").lower()
    if code.startswith("gu"):
        return translate_taxonomy_term(str(value), lang="gu")
    return str(value)


@register.simple_tag(takes_context=True)
def localized_term(context, value):
    """
    Translates a taxonomy term using request.LANGUAGE_CODE from template context.
    """
    if not value:
        return ""
    request = context.get("request")
    lang = getattr(request, "LANGUAGE_CODE", "en") if request else "en"
    if str(lang).lower().startswith("gu"):
        return translate_taxonomy_term(str(value), lang="gu")
    return str(value)
