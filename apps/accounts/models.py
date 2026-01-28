from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('super', 'Super Admin'),
        ('country', 'Country Admin'),
        ('branch', 'Branch Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    country = models.ForeignKey(
        'locations.Country',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    branch = models.ForeignKey(
        'locations.Branch',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
