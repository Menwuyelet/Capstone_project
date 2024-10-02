from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class UpdateProfileAndPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'current_password', 'new_password']

    def validate(self, data):
        user = self.instance

        # Validate if current password is provided and is correct
        if 'new_password' in data and data['new_password']:
            if not user.check_password(data['current_password']):
                raise serializers.ValidationError({'current_password': 'Current password is incorrect.'})

        return data

    def update(self, instance, validated_data):
        # Update username and email
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # If a new password is provided, update the password
        if 'new_password' in validated_data and validated_data['new_password']:
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance