from django.http import HttpResponseForbidden

class RestrictOriginMiddleware :
    ALLOWED_ORIGINS = ["https://cryptopunch.tech", 'localhost']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        referer = request.META.get('HTTP_REFERER')
        print(referer)
        
        if not any([referer.startswith(origin) for origin in self.ALLOWED_ORIGINS]):
            return HttpResponseForbidden("Forbidden: Invalid origin")

        response = self.get_response(request)
        return response