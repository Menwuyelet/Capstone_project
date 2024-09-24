from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, CustomAuthToken

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_login'), 
    path('register/',RegisterView.as_view(), name='register_user'),
]

#the login endpoin is not working 