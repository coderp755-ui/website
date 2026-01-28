from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Country, Branch

@api_view(['GET'])
def country_list(request):
    data = Country.objects.filter(is_active=True).values(
        'id', 'name', 'code'
    )
    return Response(data)

@api_view(['GET'])
def branch_list(request):
    country_code = request.GET.get('country')

    qs = Branch.objects.all()
    if country_code:
        qs = qs.filter(country__code=country_code)

    data = qs.values(
        'id', 'city', 'slug', 'country__code'
    )
    return Response(data)
