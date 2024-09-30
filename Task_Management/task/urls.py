from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('list/', TaskListView.as_view(), name = 'Task-list'),
    path('create/', TaskCreateView.as_view(), name = 'Task-create'),
    path('detail/<str:title>/', TaskDetailView.as_view(), name = 'Task-detail'),
    path('update/<str:title>', TaskUpdateView.as_view(), name = 'Task-update'),
    path('delete/<str:title>', TaskDeleteView.as_view(), name = 'Task-delete'),
    path('category/', CategoryListView.as_view(), name = 'Category-list'),
    path('category/create/', CategoryCreateView.as_view(), name = 'Category-create'),
    path('category/update/<str:name>', CategoryUpdateView.as_view(), name = 'Category-update'),
    path('category/delete/<str:name>', CategoryDeleteView.as_view(), name = 'Category-delete'),
]


