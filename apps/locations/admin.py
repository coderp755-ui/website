from django.contrib import admin
from .models import Country, Branch

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'domain', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'domain']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country':
            return qs.filter(id=request.user.country.id)
        return qs.none()
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return False
        if request.user.role == 'country':
            return obj == request.user.country
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['city', 'country', 'slug', 'phone', 'email', 'is_main']
    list_filter = ['country', 'is_main']
    search_fields = ['city', 'address', 'phone', 'email']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country':
            return qs.filter(country=request.user.country)
        if request.user.role == 'branch':
            return qs.filter(id=request.user.branch.id)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            if not request.user.is_superuser and request.user.role == 'country':
                from .models import Country
                kwargs["queryset"] = Country.objects.filter(id=request.user.country.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # Country admins can add branches in their country
        return request.user.role == 'country'
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'country':
            return obj.country == request.user.country
        if request.user.role == 'branch':
            return obj == request.user.branch
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Country admins can delete branches in their country
        if request.user.role == 'country' and obj:
            return obj.country == request.user.country
        return False
    
    def save_model(self, request, obj, form, change):
        # Auto-assign country for country admins
        if not request.user.is_superuser and request.user.role == 'country':
            obj.country = request.user.country
        super().save_model(request, obj, form, change)
