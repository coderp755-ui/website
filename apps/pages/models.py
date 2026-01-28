from django.db import models
from apps.locations.models import Country, Branch

class Page(models.Model):
    PAGE_TYPES = (
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('contact', 'Contact'),
    )

    slug = models.CharField(max_length=50)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES)

    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE
    )
    branch = models.ForeignKey(
        Branch, null=True, blank=True, on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug
