from django.urls import path
from .views import get_page, create_page, update_page, delete_page

urlpatterns = [
    path('<slug:slug>/', get_page, name='get-page'),
    path('admin/create/', create_page, name='create-page'),
    path('admin/update/<int:pk>/', update_page, name='update-page'),
    path('admin/delete/<int:pk>/', delete_page, name='delete-page'),
]
