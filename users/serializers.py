from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Follow
from .validators import PersianPasswordValidator

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'bio', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }

    def validate_username(self, value):
        """
        Check that username is unique and follows the pattern
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('این نام کاربری قبلاً استفاده شده است.')
        return value

    def validate_email(self, value):
        """
        Check that email is unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('این ایمیل قبلاً استفاده شده است.')
        return value

    def validate_password(self, value):
        """
        Validate password using custom validator
        """
        validator = PersianPasswordValidator()
        try:
            validator.validate(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs):
        """
        Check that passwords match
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('رمزهای عبور مطابقت ندارند.')
        return attrs

    def create(self, validated_data):
        """
        Create user with hashed password and set is_active to False initially
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            avatar=validated_data.get('avatar'),
            is_active=False  # User needs to verify email first
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for user details (without password)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'is_email_verified', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_email_verified']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'