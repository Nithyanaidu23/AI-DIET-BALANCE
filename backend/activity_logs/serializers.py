from rest_framework import serializers
from .models import ActivityLog, LoginHistory


class ActivityLogSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = ActivityLog
        fields = ('id', 'user_email', 'action', 'description', 'ip_address', 'timestamp')


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__'
