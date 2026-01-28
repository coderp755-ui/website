from django.contrib import admin
from .models import Section, SectionItem

class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 1
    fields = ['title', 'subtitle', 'description', 'image', 'icon', 'button_text', 'button_link', 'order']
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.role in ['country', 'branch']
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.role in ['country', 'branch']
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.role in ['country', 'branch']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['section_type', 'page', 'order']
    list_filter = ['section_type', 'page__country', 'page__branch']
    search_fields = ['section_type', 'page__slug']
    inlines = [SectionItemInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country':
            return qs.filter(page__country=request.user.country)
        if request.user.role == 'branch':
            return qs.filter(page__branch=request.user.branch)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "page":
            if not request.user.is_superuser:
                from apps.pages.models import Page
                if request.user.role == 'country':
                    kwargs["queryset"] = Page.objects.filter(country=request.user.country)
                elif request.user.role == 'branch':
                    kwargs["queryset"] = Page.objects.filter(branch=request.user.branch)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'country':
            return obj.page.country == request.user.country
        if request.user.role == 'branch':
            return obj.page.branch == request.user.branch
        return False
    
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # Country and branch admins can add sections
        return request.user.role in ['country', 'branch']
    
    def save_model(self, request, obj, form, change):
        # Ensure the page belongs to the user's scope
        if not request.user.is_superuser and not change:
            # For new sections, validate the page assignment
            if request.user.role == 'country' and obj.page.country != request.user.country:
                raise PermissionError("You can only create sections for pages in your country")
            elif request.user.role == 'branch' and obj.page.branch != request.user.branch:
                raise PermissionError("You can only create sections for pages in your branch")
        super().save_model(request, obj, form, change)

@admin.register(SectionItem)
class SectionItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section__page__country', 'section__page__branch']
    search_fields = ['title', 'subtitle', 'description']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country':
            return qs.filter(section__page__country=request.user.country)
        if request.user.role == 'branch':
            return qs.filter(section__page__branch=request.user.branch)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "section":
            if not request.user.is_superuser:
                from apps.content.models import Section
                if request.user.role == 'country':
                    kwargs["queryset"] = Section.objects.filter(page__country=request.user.country)
                elif request.user.role == 'branch':
                    kwargs["queryset"] = Section.objects.filter(page__branch=request.user.branch)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'country':
            return obj.section.page.country == request.user.country
        if request.user.role == 'branch':
            return obj.section.page.branch == request.user.branch
        return False
    
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # Country and branch admins can add section items
        return request.user.role in ['country', 'branch']
    
    def save_model(self, request, obj, form, change):
        # Ensure the section belongs to the user's scope
        if not request.user.is_superuser and not change:
            # For new section items, validate the section assignment
            if request.user.role == 'country' and obj.section.page.country != request.user.country:
                raise PermissionError("You can only create section items for sections in your country")
            elif request.user.role == 'branch' and obj.section.page.branch != request.user.branch:
                raise PermissionError("You can only create section items for sections in your branch")
        super().save_model(request, obj, form, change)
