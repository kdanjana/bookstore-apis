from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        pwd = self.validated_data['password']
        pwd2 = self.validated_data['password2']
        if pwd != pwd2:
            raise serializers.ValidationError({'error': 'pwd and pwd2 are not same.'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'user already exists'})
        user = User(email=self.validated_data['email'],
                    username=self.validated_data['username'])
        user.set_password(pwd)
        user.save()
        return user