from django.urls import path
from .views import RegisterView, LoginView, create_superuser
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='pin_list'), name='logout'),
    path('create-superuser/', create_superuser, name='create_superuser'),  # TEMPORARY - REMOVE AFTER USE
]

