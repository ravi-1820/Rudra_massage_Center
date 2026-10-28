from django.utils import translation


class AdminLocaleMiddleware:
    """
    Ensures that admin portal routes (/admin/ and /custom-admin/)
    always remain in English, preserving their original behavior,
    while public-facing routes follow the user's selected language.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path.startswith('/admin/') or path.startswith('/custom-admin/'):
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        response = self.get_response(request)
        return response
