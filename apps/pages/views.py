from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Page
from .serializers import PageSerializer
from apps.common.utils import resolve_country_branch

# PUBLIC: get page metadata
@api_view(['GET'])
@permission_classes([AllowAny])
def get_page(request, slug):
    country, branch = resolve_country_branch(request)

    page = (
        Page.objects.filter(branch=branch, slug=slug, is_active=True).first()
        or Page.objects.filter(country=country, slug=slug, is_active=True).first()
    )

    if not page:
        return Response({"detail": "Page not found"}, status=404)

    serializer = PageSerializer(page)
    return Response(serializer.data)


# ADMIN: Create / Update / Delete Pages
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def create_page(request):
    serializer = PageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_page(request, pk):
    try:
        page = Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        return Response({"detail": "Page not found"}, status=404)
    
    serializer = PageSerializer(page, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_page(request, pk):
    try:
        page = Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        return Response({"detail": "Page not found"}, status=404)
    
    page.delete()
    return Response({"detail": "Page deleted successfully"}, status=204)
