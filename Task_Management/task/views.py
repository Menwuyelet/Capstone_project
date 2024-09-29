from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import CategoryViewSerializer,CategoryCreateSerializer, TaskCreateSerializer, TaskListSerializer,TaskDetailSerializer, TaskUpdateSerializer
from rest_framework.response import Response

## Task views
class TaskListView(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        category_name = self.request.query_params.get('category_name')
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        due_date = self.request.query_params.get('due_date')

        # filter options
        if category_name:
            queryset = queryset.filter(category__name = category_name)
        if status:
            queryset = queryset.filter(status = status)
        if priority:
            queryset = queryset.filter(priority = priority)
        if due_date:
            queryset = queryset.filter(due_date = due_date)

        # sorting option
        sort_by = self.request.query_params.get('sort_by', 'due_date')  # Default to due_date if not provided
        sort_order = self.request.query_params.get('sort_order', 'asc')  # Default to ascending

        # Validate sort_by to ensure it's a valid field (optional but recommended)
        valid_sort_fields = ['due_date', 'priority', 'status']
        if sort_by not in valid_sort_fields:
            sort_by = 'due_date'  # Fallback to default if invalid

        # Apply sorting
        if sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_by}')  # Descending order
        else:
            queryset = queryset.order_by(sort_by)  # Ascending order

        return queryset

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated] 
    lookup_field = 'title'

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    
class TaskDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'title'

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    
class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'title'
    
    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)

## Category Views
class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user = self.request.user)
    
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryUpdateView(generics.UpdateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategoryViewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
