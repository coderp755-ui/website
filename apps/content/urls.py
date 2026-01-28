from django.urls import path
from .views import page_content

urlpatterns = [
    path('<slug:slug>/', page_content, name='page-content'),
]
