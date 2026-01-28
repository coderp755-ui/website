from django.db import models
from apps.pages.models import Page

class Section(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.section_type


class SectionItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='sections/', blank=True)
    icon = models.CharField(max_length=50, blank=True)

    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)

    order = models.PositiveIntegerField(default=0)
