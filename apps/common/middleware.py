from apps.locations.models import Country

class DomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        request.country = Country.objects.filter(
            domain=host,
            is_active=True
        ).first()

        request.geo_country_code = request.headers.get('CF-IPCountry')
        return self.get_response(request)
