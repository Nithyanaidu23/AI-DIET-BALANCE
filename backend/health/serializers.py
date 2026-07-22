"""Health app serializers."""
from rest_framework import serializers
from .models import BMIRecord, WaterTracker


class BMIInputSerializer(serializers.Serializer):
    """Input for BMI + calorie calculation."""
    weight_kg = serializers.FloatField(min_value=10, max_value=500)
    height_cm = serializers.FloatField(min_value=50, max_value=300)
    age = serializers.IntegerField(min_value=1, max_value=120)
    gender = serializers.ChoiceField(choices=['male', 'female', 'other'])
    activity_level = serializers.ChoiceField(
        choices=['sedentary', 'light', 'moderate', 'very', 'extra']
    )
    goal = serializers.ChoiceField(
        choices=['lose_fat', 'build_muscle', 'maintain', 'improve_health', 'increase_endurance']
    )
    save_record = serializers.BooleanField(default=True)


class BMIRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BMIRecord
        exclude = ('user',)
        read_only_fields = ('id', 'recorded_at')


class WaterTrackerSerializer(serializers.ModelSerializer):
    percent_complete = serializers.ReadOnlyField()

    class Meta:
        model = WaterTracker
        exclude = ('user',)
        read_only_fields = ('id',)
