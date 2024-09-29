from rest_framework import serializers
from .models import Category, Task
from django.utils import timezone


class CategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']  

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'status']

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'completed_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_title(self, value):
        if Task.objects.filter(title=value).exists():
            raise serializers.ValidationError("The provided title is already in use. Please use another one.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user 
        category_name = validated_data.pop('category')
        if category_name:
            try:
                category = Category.objects.get(name = category_name)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category_name": "Category does not exist."})
        else: 
            category = None

        return Task.objects.create(user = user, category = category, **validated_data)

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']
    
    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_title(self, value):
        request = self.context.get('request')
        if request:
            task_id = request.parser_context['kwargs']['title']
            if Task.objects.exclude(id=task_id).filter(title=value).exists():
                raise serializers.ValidationError("The provided title is already in use. Please use another one.")
        return value
    
    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == 'Completed':
            instance.completed_at = timezone.now()

        category_name = validated_data.pop('category', None)
        if category_name is not None:  
            if category_name == '':
                instance.category = None
            else:
                try:
                    instance.category = Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category_name": "Category does not exist."})
        return super().update(instance, validated_data)