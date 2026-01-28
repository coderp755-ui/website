from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'country', 'branch')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Import here to avoid circular imports
        from apps.locations.models import Country, Branch
        
        if self.request and not self.request.user.is_superuser:
            # Country admin can only create branch admins in their country
            if self.request.user.role == 'country' and self.request.user.country:
                self.fields['role'].choices = [('branch', 'Branch Admin')]
                
                # Set country field
                if 'country' in self.fields:
                    self.fields['country'].queryset = Country.objects.filter(
                        id=self.request.user.country.id
                    )
                    self.fields['country'].initial = self.request.user.country
                    self.fields['country'].widget.attrs['readonly'] = True
                
                # Only branches in their country
                if 'branch' in self.fields:
                    self.fields['branch'].queryset = Branch.objects.filter(
                        country=self.request.user.country
                    )
            
            # Branch admin cannot create users
            elif self.request.user.role == 'branch':
                self.fields['role'].choices = []
                self.fields['role'].widget.attrs['disabled'] = True

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ['username', 'email', 'role', 'country', 'branch', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['role', 'is_staff', 'is_active', 'country', 'branch']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Location', {'fields': ('role', 'country', 'branch')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'country', 'branch'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # Adding new user
            kwargs['form'] = self.add_form
            form = super().get_form(request, obj, **kwargs)
            form.request = request
            return form
        return super().get_form(request, obj, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'country' and request.user.country:
            return qs.filter(country=request.user.country)
        if request.user.role == 'branch' and request.user.branch:
            return qs.filter(branch=request.user.branch)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            from apps.locations.models import Country
            if not request.user.is_superuser and request.user.role == 'country' and request.user.country:
                kwargs["queryset"] = Country.objects.filter(id=request.user.country.id)
            elif "queryset" not in kwargs:
                kwargs["queryset"] = Country.objects.all()
        
        if db_field.name == "branch":
            from apps.locations.models import Branch
            if not request.user.is_superuser:
                if request.user.role == 'country' and request.user.country:
                    kwargs["queryset"] = Branch.objects.filter(country=request.user.country)
                elif request.user.role == 'branch' and request.user.branch:
                    kwargs["queryset"] = Branch.objects.filter(id=request.user.branch.id)
            elif "queryset" not in kwargs:
                kwargs["queryset"] = Branch.objects.all()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "role":
            if not request.user.is_superuser:
                if request.user.role == 'country':
                    # Country admin can only create branch admins
                    kwargs['choices'] = [('branch', 'Branch Admin')]
                elif request.user.role == 'branch':
                    # Branch admin cannot create users
                    kwargs['choices'] = []
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.role == 'country' and request.user.country:
            return True  # Country admin can add branch admins
        return False  # Branch admin cannot add users
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if request.user.role == 'country' and request.user.country:
            return obj.country == request.user.country
        if request.user.role == 'branch' and request.user.branch:
            return obj.branch == request.user.branch
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.role == 'country' and obj and request.user.country:
            return obj.country == request.user.country and obj.role == 'branch'
        return False
