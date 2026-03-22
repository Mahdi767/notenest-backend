from rest_framework import  serializers
from . models import User

ALLOWED_DOMAIN1 ="student.metrouni.ac.bd"
ALLOWED_DOMAIN2 = "metrouni.edu.bd"



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True, style={'input_type': 'text'})
    first_name = serializers.CharField(max_length=150, required=True, style={'input_type': 'text'})
    last_name = serializers.CharField(max_length=150, required=True, style={'input_type': 'text'})
    email = serializers.EmailField(required=True, style={'input_type': 'email'})
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def validate_email(self,value):
        if not value.endswith((f"@{ALLOWED_DOMAIN1}", f"@{ALLOWED_DOMAIN2}")):
            raise serializers.ValidationError("Only university email addresses are allowed")
        return value
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({
            "An account with this email address already exists. Please use a different email to continue"
        })

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_active=False  # Make user inactive until email is verified
        )
        return user
        

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)