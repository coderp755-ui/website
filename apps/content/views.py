from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.pages.models import Page
from .serializers import SectionSerializer
from apps.common.utils import resolve_country_branch

@api_view(['GET'])
def page_content(request, slug):
    country, branch = resolve_country_branch(request)

    page = (
        Page.objects.filter(branch=branch, slug=slug, is_active=True).first()
        or
        Page.objects.filter(country=country, slug=slug, is_active=True).first()
    )

    if not page:
        return Response({"detail": "Page not found"}, status=404)

    sections = page.section_set.order_by('order')
    data = SectionSerializer(sections, many=True, context={'request': request}).data

    return Response({
        "page": slug,
        "sections": data
    })
