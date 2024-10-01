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

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
            model = Category
            fields = ['name']

    def validate_name(self, value):
        """Ensure the name is unique, excluding the current category."""
        request = self.context.get('request')
        if request:
            current_category_name = request.parser_context['kwargs']['name']  # Fetch the current category's name from the URL
            if Category.objects.exclude(name=current_category_name).filter(name=value).exists():
                raise serializers.ValidationError("The provided name is already in use. Please use another one.")
        return value

    def update(self, instance, validated_data):
        """Update the category instance."""
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class TaskListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['title', 'short_description', 'due_date', 'priority', 'status']

    def get_short_description(self, obj):
        # Truncate the description to 30 characters, and add "..." if it's longer
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

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
        category_name = validated_data.pop('category', None)
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
            current_task_title = request.parser_context['kwargs']['title']  # Fetch the current task's title
            if Task.objects.exclude(title=current_task_title).filter(title=value).exists():
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