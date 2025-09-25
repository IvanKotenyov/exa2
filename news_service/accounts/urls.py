from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    # Регистрация и активация
    path('register/', views.register, name='register'),
    path('activate/', views.activate, name='activate'),
    
    # Авторизация
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Профиль
    path('profile/', views.profile, name='profile'),
]