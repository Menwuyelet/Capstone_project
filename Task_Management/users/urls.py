from django.urls import path
from .views import RegisterView, LogoutView, DeleteUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
    )


urlpatterns = [ 
    path('login/', TokenObtainPairView.as_view(), name = 'login'),
    path('refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('register/', RegisterView.as_view(), name = 'signup'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('delete/', DeleteUserView.as_view(), name = 'delete_user'),
    
]