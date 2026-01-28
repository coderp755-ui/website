from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.utils import resolve_country_branch

@api_view(['GET'])
def site_config(request):
    country, branch = resolve_country_branch(request)

    if not country:
        return Response({
            "error": "No country configuration found"
        }, status=404)

    if not branch:
        return Response({
            "error": "No branch found for this country"
        }, status=404)

    return Response({
        "country": country.name,
        "country_code": country.code,
        "branch": branch.city,
        "branch_slug": branch.slug
    })
