from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('list/', TaskListView.as_view(), name = 'Task-list'), # for listinf all the tasks the user own
    path('create/', TaskCreateView.as_view(), name = 'Task-create'), # for creating a new task
    path('detail/<str:title>/', TaskDetailView.as_view(), name = 'Task-detail'), # for viewing the deatils of a specific task
    path('update/<str:title>', TaskUpdateView.as_view(), name = 'Task-update'), # for updating a specific task
    path('delete/<str:title>', TaskDeleteView.as_view(), name = 'Task-delete'), # for deleting a specifid task
    path('category/', CategoryListView.as_view(), name = 'Category-list'), # for listing all categories the user own
    path('category/create/', CategoryCreateView.as_view(), name = 'Category-create'), # for creating a new category
    path('category/update/<str:name>', CategoryUpdateView.as_view(), name = 'Category-update'), # for updating a specific category 
    path('category/delete/<str:name>', CategoryDeleteView.as_view(), name = 'Category-delete'), # for deleting a specific category
]


