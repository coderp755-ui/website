from django.urls import path
from .views import site_config

urlpatterns = [
    path('site-config/', site_config, name='site-config'),
]
