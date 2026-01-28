from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'slug', 'page_type', 'branch', 'country', 'is_active']
