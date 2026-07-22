"""Serializers for authentication — register, login, user info."""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for new user registration."""
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm password')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        return User.objects.create_user(email=email, password=password, **validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extend JWT payload with user info and role."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_admin
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'is_staff': self.user.is_staff,
            'is_admin': self.user.is_admin,
        }
        # Trigger user_logged_in signal to audit JWT login
        from django.contrib.auth.signals import user_logged_in
        request = self.context.get('request')
        user_logged_in.send(sender=self.user.__class__, request=request, user=self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    """Read/Write serializer for User model."""
    full_name = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name',
                  'role', 'is_admin', 'date_joined', 'is_staff')
        read_only_fields = ('id', 'email', 'date_joined', 'is_admin')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password changes."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        return attrs
