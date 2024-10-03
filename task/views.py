from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import CategoryViewSerializer, CategoryCreateSerializer, CategoryUpdateSerializer, TaskCreateSerializer, TaskListSerializer,TaskDetailSerializer, TaskUpdateSerializer


## Task views
class TaskListView(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user) # filters the tasks only the user owns 
        category_name = self.request.query_params.get('category_name') # retrive the category name from query 
        status = self.request.query_params.get('status') # retrive the status from query 
        priority = self.request.query_params.get('priority') # retrive the priority from query 
        due_date = self.request.query_params.get('due_date') # retrive the due_date from query 
        title = self.request.query_params.get('title') # retrive the title from query 
        description = self.request.query_params.get('description') # retrive the description from query 

        # filter options
        if category_name: # if categry_name is provided in query it filters the tasks by category_name
            queryset = queryset.filter(category__name = category_name) # 
        if status: # if status is provided in query it filters the tasks by status
            queryset = queryset.filter(status = status)
        if priority: # if priority is provided in query it filters the tasks by priority
            queryset = queryset.filter(priority = priority)
        if due_date: # if due_date is provided in query it filters the tasks by due_date
            queryset = queryset.filter(due_date = due_date)
        if title: # if title is provided in query it searchs for the tasks by title
            queryset = queryset.filter(title__icontains = title)
        if description: # if part of the description of the task is provided in query it searchs for the tasks by the description provided
            queryset = queryset.filter(description__icontains = description)

        # sorting option
        sort_by = self.request.query_params.get('sort_by', 'due_date')  # default to due_date if not provided
        sort_order = self.request.query_params.get('sort_order', 'asc')  # default to ascending if not provided

        # validate sort_by to ensure it's a valid field 
        valid_sort_fields = ['due_date', 'priority', 'status']
        if sort_by not in valid_sort_fields: # cheks if the provided sorting field is valid for sortig if not sort by default due_date ascending
            sort_by = 'due_date'  

        # sort_order assiging
        if sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_by}')  # descending order
        else:
            queryset = queryset.order_by(sort_by)  # ascending order

        return queryset

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated] 
    lookup_field = 'title' # looks up the task with its title not id

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user) # fillter the tasks of the user only
    
class TaskDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'title' # looks up the task with its title not id

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user) # filters the tasks of the user only
    
class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'title' # looks up the task with its title not id
    
    def get_queryset(self):
        return Task.objects.filter(user = self.request.user) # filters the task of the user only

## Category Views
class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user = self.request.user) # filters the category of the user only
    
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # assigns teh user to the current user when creating the caategory

class CategoryUpdateView(generics.UpdateAPIView):
    serializer_class = CategoryUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name' # looks up the category by its name not id
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user) # filters the category of the user only
    
class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategoryViewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name' # looks up the category by its name not id

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user) # filter the category of the user only
