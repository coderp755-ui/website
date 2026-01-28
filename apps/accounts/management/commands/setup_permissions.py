from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import User
from apps.locations.models import Country, Branch
from apps.pages.models import Page
from apps.content.models import Section, SectionItem

class Command(BaseCommand):
    help = 'Setup role-based permissions for different user types'

    def handle(self, *args, **kwargs):
        self.create_groups_and_permissions()
        self.assign_permissions_to_users()
        self.stdout.write(self.style.SUCCESS('Permissions setup completed!'))

    def create_groups_and_permissions(self):
        """Create groups and assign permissions"""
        
        # Get content types
        user_ct = ContentType.objects.get_for_model(User)
        country_ct = ContentType.objects.get_for_model(Country)
        branch_ct = ContentType.objects.get_for_model(Branch)
        page_ct = ContentType.objects.get_for_model(Page)
        section_ct = ContentType.objects.get_for_model(Section)
        sectionitem_ct = ContentType.objects.get_for_model(SectionItem)

        # Create Groups
        super_admin_group, created = Group.objects.get_or_create(name='Super Admin')
        country_admin_group, created = Group.objects.get_or_create(name='Country Admin')
        branch_admin_group, created = Group.objects.get_or_create(name='Branch Admin')

        if created:
            self.stdout.write(f'Created group: {super_admin_group.name}')

        # Clear existing permissions
        super_admin_group.permissions.clear()
        country_admin_group.permissions.clear()
        branch_admin_group.permissions.clear()

        # Super Admin Permissions (All permissions)
        all_permissions = Permission.objects.all()
        super_admin_group.permissions.set(all_permissions)
        self.stdout.write(f'Super Admin: {all_permissions.count()} permissions assigned')

        # Country Admin Permissions
        country_admin_permissions = [
            # User permissions (limited)
            Permission.objects.get(codename='view_user', content_type=user_ct),
            Permission.objects.get(codename='add_user', content_type=user_ct),
            Permission.objects.get(codename='change_user', content_type=user_ct),
            Permission.objects.get(codename='delete_user', content_type=user_ct),
            
            # Country permissions (view only their country)
            Permission.objects.get(codename='view_country', content_type=country_ct),
            Permission.objects.get(codename='change_country', content_type=country_ct),
            
            # Branch permissions (full access in their country)
            Permission.objects.get(codename='view_branch', content_type=branch_ct),
            Permission.objects.get(codename='add_branch', content_type=branch_ct),
            Permission.objects.get(codename='change_branch', content_type=branch_ct),
            Permission.objects.get(codename='delete_branch', content_type=branch_ct),
            
            # Page permissions (full access in their country)
            Permission.objects.get(codename='view_page', content_type=page_ct),
            Permission.objects.get(codename='add_page', content_type=page_ct),
            Permission.objects.get(codename='change_page', content_type=page_ct),
            Permission.objects.get(codename='delete_page', content_type=page_ct),
            
            # Section permissions (full access in their country)
            Permission.objects.get(codename='view_section', content_type=section_ct),
            Permission.objects.get(codename='add_section', content_type=section_ct),
            Permission.objects.get(codename='change_section', content_type=section_ct),
            Permission.objects.get(codename='delete_section', content_type=section_ct),
            
            # Section Item permissions (full access in their country)
            Permission.objects.get(codename='view_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='add_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='change_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='delete_sectionitem', content_type=sectionitem_ct),
        ]
        
        country_admin_group.permissions.set(country_admin_permissions)
        self.stdout.write(f'Country Admin: {len(country_admin_permissions)} permissions assigned')

        # Branch Admin Permissions
        branch_admin_permissions = [
            # User permissions (view only)
            Permission.objects.get(codename='view_user', content_type=user_ct),
            
            # Country permissions (view only their country)
            Permission.objects.get(codename='view_country', content_type=country_ct),
            
            # Branch permissions (view only their branch)
            Permission.objects.get(codename='view_branch', content_type=branch_ct),
            
            # Page permissions (full access in their branch)
            Permission.objects.get(codename='view_page', content_type=page_ct),
            Permission.objects.get(codename='add_page', content_type=page_ct),
            Permission.objects.get(codename='change_page', content_type=page_ct),
            Permission.objects.get(codename='delete_page', content_type=page_ct),
            
            # Section permissions (full access in their branch)
            Permission.objects.get(codename='view_section', content_type=section_ct),
            Permission.objects.get(codename='add_section', content_type=section_ct),
            Permission.objects.get(codename='change_section', content_type=section_ct),
            Permission.objects.get(codename='delete_section', content_type=section_ct),
            
            # Section Item permissions (full access in their branch)
            Permission.objects.get(codename='view_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='add_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='change_sectionitem', content_type=sectionitem_ct),
            Permission.objects.get(codename='delete_sectionitem', content_type=sectionitem_ct),
        ]
        
        branch_admin_group.permissions.set(branch_admin_permissions)
        self.stdout.write(f'Branch Admin: {len(branch_admin_permissions)} permissions assigned')

    def assign_permissions_to_users(self):
        """Assign users to appropriate groups based on their role"""
        
        # Get groups
        super_admin_group = Group.objects.get(name='Super Admin')
        country_admin_group = Group.objects.get(name='Country Admin')
        branch_admin_group = Group.objects.get(name='Branch Admin')

        # Assign Super Admins
        super_admins = User.objects.filter(role='super')
        for user in super_admins:
            user.groups.clear()
            user.groups.add(super_admin_group)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        self.stdout.write(f'Assigned {super_admins.count()} users to Super Admin group')

        # Assign Country Admins
        country_admins = User.objects.filter(role='country')
        for user in country_admins:
            user.groups.clear()
            user.groups.add(country_admin_group)
            user.is_staff = True
            user.is_superuser = False
            user.save()
        self.stdout.write(f'Assigned {country_admins.count()} users to Country Admin group')

        # Assign Branch Admins
        branch_admins = User.objects.filter(role='branch')
        for user in branch_admins:
            user.groups.clear()
            user.groups.add(branch_admin_group)
            user.is_staff = True
            user.is_superuser = False
            user.save()
        self.stdout.write(f'Assigned {branch_admins.count()} users to Branch Admin group')

        self.stdout.write(
            self.style.SUCCESS(
                '\n=== PERMISSIONS SUMMARY ===\n'
                'Super Admin: Full access to everything\n'
                'Country Admin: Can manage users, branches, and content in their country\n'
                'Branch Admin: Can manage content in their branch only\n'
                '============================'
            )
        )