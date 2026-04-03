from rest_framework import serializers
from . models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

ALLOWED_DOMAIN1 ="student.metrouni.ac.bd"
ALLOWED_DOMAIN2 = "metrouni.edu.bd"
TEST = "gmail.com"

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
        if not value.endswith((f"@{ALLOWED_DOMAIN1}", f"@{ALLOWED_DOMAIN2}",f"@{TEST}")):
            raise serializers.ValidationError("Only university email addresses are allowed")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email address already exists. Please use a different email to continue")
        return value

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


class UserProfileSerializer(serializers.ModelSerializer):
    #this serializer for user profile details
    role = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class UpdateProfileSerializer(serializers.ModelSerializer):
    #Serializer for updating user profile (first name, last name, username)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
    
    def validate_username(self, value):
        #checking the username is already exists or not
        user = self.instance
        if User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
    
    def update(self, instance, validated_data):
        #Updating the peofile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    #This is for password change
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate_old_password(self, value):
        #checking old password valid or not
        user = self.context.get('user')
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, data):
      #Validate that new passwords match and meet requirements
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
        
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError({"new_password": "New password must be different from old password."})
        
        # Validate password strength
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": str(e)})
        
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    #Serializer for requesting password reset via email
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        #Check if user with this email exists
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user account found with this email address.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
   #Serializer for confirming password reset with token
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        #matching password
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        # Validate password strength
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": str(e)})
        
        return data