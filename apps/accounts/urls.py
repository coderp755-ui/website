from django.urls import path
from .views import (
    create_user, login_user, list_users, 
    current_user, update_user, delete_user
)

urlpatterns = [
    path('register/', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
    path('list/', list_users, name='list_users'),
    path('me/', current_user, name='current_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
]
