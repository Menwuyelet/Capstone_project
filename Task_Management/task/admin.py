from django.contrib import admin
from .models import Task, Category

@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ['id','title', 'description', 'status', 'priority', 'due_date', 'category', "user"]

@admin.register(Category)
class Catergory(admin.ModelAdmin):
    list_display = ['id', 'name', "user"]