from django.core.management.base import BaseCommand
from apps.locations.models import Country, Branch
from apps.pages.models import Page
from apps.content.models import Section, SectionItem


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        # Create Country
        country, _ = Country.objects.get_or_create(
            code='NP',
            defaults={
                'name': 'Nepal',
                'domain': 'localhost',
                'is_active': True
            }
        )
        self.stdout.write(f'✓ Country: {country.name}')

        # Create Branch
        branch, _ = Branch.objects.get_or_create(
            country=country,
            city='Kathmandu',
            defaults={
                'slug': 'kathmandu',
                'address': '123 Main Street, Kathmandu',
                'phone': '+977-1-1234567',
                'email': 'info@grace.com.np',
                'is_main': True
            }
        )
        self.stdout.write(f'✓ Branch: {branch.city}')

        # Create Home Page
        home_page, _ = Page.objects.get_or_create(
            slug='home',
            defaults={
                'page_type': 'home',
                'country': country,
                'branch': None,
                'is_active': True
            }
        )
        self.stdout.write(f'✓ Page: {home_page.slug}')

        # Create Hero Section
        hero_section, _ = Section.objects.get_or_create(
            page=home_page,
            section_type='hero',
            defaults={'order': 1}
        )
        
        # Delete existing hero items to avoid duplicates
        SectionItem.objects.filter(section=hero_section).delete()
        
        SectionItem.objects.create(
            section=hero_section,
            title='Welcome to Grace',
            subtitle='Your Trusted Partner',
            description='We provide excellent services to help you succeed',
            button_text='Get Started',
            button_link='/contact',
            image='sections/Screenshot_2026-01-20_100825.png',
            order=1
        )
        self.stdout.write(f'✓ Hero Section created')

        # Create Features Section
        features_section, _ = Section.objects.get_or_create(
            page=home_page,
            section_type='features',
            defaults={'order': 2}
        )
        
        # Delete existing feature items to avoid duplicates
        SectionItem.objects.filter(section=features_section).delete()
        
        features = [
            {
                'title': 'Quality Service',
                'description': 'We deliver top-notch quality in everything we do',
                'icon': '⭐',
                'order': 1
            },
            {
                'title': 'Expert Team',
                'description': 'Our team consists of experienced professionals',
                'icon': '👥',
                'order': 2
            },
            {
                'title': '24/7 Support',
                'description': 'We are always here to help you',
                'icon': '🕐',
                'order': 3
            }
        ]
        
        for feature in features:
            SectionItem.objects.create(
                section=features_section,
                **feature
            )
        
        self.stdout.write(f'✓ Features Section created')

        # Create About Section
        about_section, _ = Section.objects.get_or_create(
            page=home_page,
            section_type='about',
            defaults={'order': 3}
        )
        
        # Delete existing about items to avoid duplicates
        SectionItem.objects.filter(section=about_section).delete()
        
        SectionItem.objects.create(
            section=about_section,
            title='About Us',
            subtitle='Who We Are',
            description='We are a leading company dedicated to providing exceptional services to our clients. With years of experience and a passionate team, we strive for excellence in everything we do.',
            button_text='Learn More',
            button_link='/about',
            order=1
        )
        self.stdout.write(f'✓ About Section created')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now access http://localhost:5173'))

        # ========================================
        # CREATE ABOUT PAGE
        # ========================================
        
        about_page, _ = Page.objects.get_or_create(
            slug='about',
            defaults={
                'page_type': 'about',
                'country': country,
                'branch': None,
                'is_active': True
            }
        )
        self.stdout.write(f'\n✓ About Page: {about_page.slug}')

        # About Hero Section
        about_hero, _ = Section.objects.get_or_create(
            page=about_page,
            section_type='hero',
            defaults={'order': 1}
        )
        
        # Delete existing about hero items to avoid duplicates
        SectionItem.objects.filter(section=about_hero).delete()
        
        SectionItem.objects.create(
            section=about_hero,
            title='About Us',
            subtitle='Learn more about our company and mission',
            order=1
        )
        self.stdout.write(f'✓ About Hero Section created')

        # About Content Section
        about_content, _ = Section.objects.get_or_create(
            page=about_page,
            section_type='content',
            defaults={'order': 2}
        )
        
        # Delete existing about content items to avoid duplicates
        SectionItem.objects.filter(section=about_content).delete()
        
        SectionItem.objects.create(
            section=about_content,
            title='Our Story',
            description='We are a leading company dedicated to providing exceptional services to our clients. With years of experience and a passionate team, we strive for excellence in everything we do. Our journey began with a simple vision: to make a difference in the lives of our customers through innovative solutions and outstanding service.',
            order=1
        )
        
        SectionItem.objects.create(
            section=about_content,
            title='Our Mission',
            description='To deliver high-quality services that exceed customer expectations while maintaining integrity, innovation, and excellence in all our endeavors. We believe in building long-term relationships based on trust and mutual success.',
            order=2
        )
        self.stdout.write(f'✓ About Content Section created')

        # About Values Section
        about_values, _ = Section.objects.get_or_create(
            page=about_page,
            section_type='values',
            defaults={'order': 3}
        )
        
        # Delete existing about values items to avoid duplicates
        SectionItem.objects.filter(section=about_values).delete()
        
        values = [
            {
                'title': 'Integrity',
                'description': 'We conduct our business with honesty and transparency',
                'icon': '🤝',
                'order': 1
            },
            {
                'title': 'Innovation',
                'description': 'We constantly seek new and better ways to serve our clients',
                'icon': '💡',
                'order': 2
            },
            {
                'title': 'Excellence',
                'description': 'We are committed to delivering the highest quality in everything we do',
                'icon': '⭐',
                'order': 3
            },
            {
                'title': 'Customer Focus',
                'description': 'Our customers are at the heart of everything we do',
                'icon': '❤️',
                'order': 4
            }
        ]
        
        for value in values:
            SectionItem.objects.create(
                section=about_values,
                **value
            )
        
        self.stdout.write(f'✓ About Values Section created')

        # About Team Section
        about_team, _ = Section.objects.get_or_create(
            page=about_page,
            section_type='team',
            defaults={'order': 4}
        )
        
        # Delete existing about team items to avoid duplicates
        SectionItem.objects.filter(section=about_team).delete()
        
        team_members = [
            {
                'title': 'John Doe',
                'subtitle': 'CEO & Founder',
                'description': 'Leading the company with vision and passion',
                'icon': '👨‍💼',
                'order': 1
            },
            {
                'title': 'Jane Smith',
                'subtitle': 'Chief Technology Officer',
                'description': 'Driving innovation and technical excellence',
                'icon': '👩‍💻',
                'order': 2
            },
            {
                'title': 'Mike Johnson',
                'subtitle': 'Head of Operations',
                'description': 'Ensuring smooth and efficient operations',
                'icon': '👨‍💼',
                'order': 3
            }
        ]
        
        for member in team_members:
            SectionItem.objects.create(
                section=about_team,
                **member
            )
        
        self.stdout.write(f'✓ About Team Section created')

        self.stdout.write(self.style.SUCCESS('\n✅ All sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Home page: http://localhost:5173'))
        self.stdout.write(self.style.SUCCESS('About page: http://localhost:5173/about'))
