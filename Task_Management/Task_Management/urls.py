from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls'), name = 'users-management'),
    path('task/', include('task.urls'), name = 'Tasks-managment'),
]
