from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'follows', views.FollowViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.UserDetailView.as_view(), name='user-detail'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify-email'),
    path('verify-email-page/<uuid:token>/', views.verify_email_page, name='verify-email-page'),
    path('resend-verification/', views.resend_verification, name='resend-verification'),
    path('', include(router.urls)),
]

