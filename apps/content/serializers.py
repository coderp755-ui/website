from rest_framework import serializers
from .models import Section, SectionItem

class SectionItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = SectionItem
        fields = '__all__'
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class SectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['section_type', 'order', 'items']

    def get_items(self, obj):
        items = obj.sectionitem_set.order_by('order')
        return SectionItemSerializer(items, many=True, context=self.context).data
