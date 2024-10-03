from django.urls import path
from .views import RegisterView, LogoutView, DeleteUserView, UpdateProfileAndPasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
    )


urlpatterns = [ 
    path('login/', TokenObtainPairView.as_view(), name = 'login'), # for loging in the user to get access and refresh tokens
    path('refresh/', TokenRefreshView.as_view(), name = 'token_refresh'), # to refresh the access token when expired
    path('register/', RegisterView.as_view(), name = 'signup'), # to register a new user
    path('logout/', LogoutView.as_view(), name = 'logout'), # to logout teh user by black listing its refresh token
    path('delete/', DeleteUserView.as_view(), name = 'delete_user'), # to delete a users account 
    path('update/', UpdateProfileAndPasswordView.as_view(), name = 'update-profile'), # to update a users account by changing its user name, email and password 
]