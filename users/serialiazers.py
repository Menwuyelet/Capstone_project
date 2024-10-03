from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): # used for registretion of a new user
    password = serializers.CharField(write_only = True) # ensures that the password is not vissible when it is writn

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user( # calls the Create_user function in usermanager cllass
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
 
class UpdateProfileAndPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False) # ensures that the password is not vissible when it is writn
    new_password = serializers.CharField(write_only=True, required=False) # ensures that the password is not vissible when it is writn

    class Meta:
        model = User
        fields = ['username', 'email', 'current_password', 'new_password'] # additional fields to update password

    def validate(self, data):
        user = self.instance # assignes the current user 

        # if a new password is provided, validate the current password
        if 'new_password' in data and data['new_password']:
            if not user.check_password(data['current_password']): # checks if the current password is valid
                raise serializers.ValidationError({'current_password': 'Current password is incorrect.'})

        return data

    def update(self, instance, validated_data):
        # update username and email
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # if a new password is provided, update the password
        if 'new_password' in validated_data and validated_data['new_password']: # optional to change the password or not 
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance
    