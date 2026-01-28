from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)   # NP, AU
    domain = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    slug = models.SlugField()
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city} ({self.country.code})"
