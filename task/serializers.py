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
        if Category.objects.filter(name=value).exists(): # to check if the name provided is already in use or not
            raise serializers.ValidationError("A category with this name already exists.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
            model = Category
            fields = ['name']

    def validate_name(self, value):
        request = self.context.get('request')
        if request:
            current_category_name = request.parser_context['kwargs']['name']  # Fetch the current category's name from the URL
            if Category.objects.exclude(name=current_category_name).filter(name=value).exists(): # checks if the name is in use excluding the current instance
                raise serializers.ValidationError("The provided name is already in use. Please use another one.")
        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name) # set the name of the instance to the new validated name 
        instance.save()
        return instance

class TaskListSerializer(serializers.ModelSerializer): # used t ojust list the tasks
    short_description = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['title', 'short_description', 'due_date', 'priority', 'status']

    def get_short_description(self, obj):
        # Truncate the description to 30 characters, and add "..." if it's longer
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        return obj.description

class TaskDetailSerializer(serializers.ModelSerializer): # used to give detail of one specific task
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'completed_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']

    def validate_due_date(self, value): # validates if the due date provided for the task is not in the past
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_title(self, value): # validates if the title provided for the task is unique
        if Task.objects.filter(title=value).exists():
            raise serializers.ValidationError("The provided title is already in use. Please use another one.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user # gets the user sending the request
        category_name = validated_data.pop('category', None) # chaeck if the category name is provided in the data sent
        if category_name:
            try:
                category = Category.objects.get(name = category_name) # searchs for category with the provided name in database
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category_name": "Category does not exist."})
        else: 
            category = None # if the category name is not provided it assigns it to none

        return Task.objects.create(user = user, category = category, **validated_data) # creates the task by assigning user and category to it

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']
    
    def validate_due_date(self, value): # checkes if the due date is not in the past
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_title(self, value):
        request = self.context.get('request')
        if request:
            current_task_title = request.parser_context['kwargs']['title']  # Fetch the current task's title
            if Task.objects.exclude(title=current_task_title).filter(title=value).exists(): # checks if the title is not being used by other tasks excluding the current one 
                raise serializers.ValidationError("The provided title is already in use. Please use another one.")
        return value
    
    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == 'Completed': # checkes if the ststus of the task is being updated 
            instance.completed_at = timezone.now() # assignes the time stamp for the task if its status is cheanged to completed

        category_name = validated_data.pop('category', None) # retrive teh category name from the request.
        if category_name is not None:  
            if category_name == '': # if the user have provide an empty entry for category the system assigns it to none
                instance.category = None
            else:
                try:
                    instance.category = Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category_name": "Category does not exist."})
        return super().update(instance, validated_data)