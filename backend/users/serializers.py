"""Serializers for user profile."""
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Full read/write serializer for UserProfile."""
    is_complete = serializers.ReadOnlyField()
    allergies_list = serializers.ReadOnlyField()
    medical_conditions_list = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        exclude = ('user',)
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserProfileSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for embedding in dashboard responses."""
    class Meta:
        model = UserProfile
        fields = (
            'age', 'gender', 'height_cm', 'weight_kg',
            'activity_level', 'fitness_goal', 'food_preference',
            'is_complete',
        )
