from apps.locations.models import Country, Branch

def resolve_country_branch(request):
    if request.country:
        country = request.country
    else:
        country = Country.objects.filter(
            code=request.geo_country_code
        ).first()

    if not country:
        country = Country.objects.first()

    branch = Branch.objects.filter(
        country=country,
        is_main=True
    ).first()

    return country, branch
