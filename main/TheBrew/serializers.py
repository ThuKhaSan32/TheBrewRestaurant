from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,Log

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        username = validated_data.get('username')
        if username:
            instance.username = username
        email = validated_data.get('email')
        if email:
            instance.email = email
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = []

    def create(self,validated_data):
        user = self.context.get('user')
        return Profile.objects.create(name=user)
    
    def update(self, instance, validated_data):
        profile=instance.name
        username = validated_data.get('username')
        if username:
            profile.username = username
        email = validated_data.get('email')
        if email:
            profile.email = email
        password = validated_data.get('password')
        if password:
            profile.set_password(password)        

        profile.save()
        return instance
    
class LoginSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model=Log
        fields = ['account','action']
