from django.urls import path
from .views import country_list, branch_list

urlpatterns = [
    path('countries/', country_list, name='countries'),
    path('branches/', branch_list, name='branches'),
]
