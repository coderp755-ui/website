from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'page_type', 'country', 'branch', 'is_active']
    list_filter = ['page_type', 'country', 'branch', 'is_active']
    search_fields = ['slug']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country':
            return qs.filter(country=request.user.country)
        if request.user.role == 'branch':
            return qs.filter(branch=request.user.branch)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            if not request.user.is_superuser and request.user.role == 'country':
                from apps.locations.models import Country
                kwargs["queryset"] = Country.objects.filter(id=request.user.country.id)
        if db_field.name == "branch":
            if not request.user.is_superuser:
                from apps.locations.models import Branch
                if request.user.role == 'country':
                    kwargs["queryset"] = Branch.objects.filter(country=request.user.country)
                elif request.user.role == 'branch':
                    kwargs["queryset"] = Branch.objects.filter(id=request.user.branch.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'country':
            return obj.country == request.user.country
        if request.user.role == 'branch':
            return obj.branch == request.user.branch
        return False
    
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # Country and branch admins can add pages
        return request.user.role in ['country', 'branch']
    
    def save_model(self, request, obj, form, change):
        # Auto-assign country/branch for non-superusers
        if not request.user.is_superuser:
            if request.user.role == 'country':
                obj.country = request.user.country
            elif request.user.role == 'branch':
                obj.branch = request.user.branch
                obj.country = request.user.branch.country
        super().save_model(request, obj, form, change)
