from rest_framework import serializers
from .models import PersonalRecord, ProgressSnapshot
from workouts.serializers import ExerciseSerializer


class PersonalRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for Personal Records
    """
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PersonalRecord
        fields = [
            'id', 'user', 'user_username', 'exercise', 'exercise_detail',
            'record_type', 'value', 'date_achieved', 'workout', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class PersonalRecordListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing personal records
    """
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)

    class Meta:
        model = PersonalRecord
        fields = [
            'id', 'exercise', 'exercise_name', 'record_type',
            'record_type_display', 'value', 'date_achieved'
        ]


class ProgressSnapshotSerializer(serializers.ModelSerializer):
    """
    Serializer for Progress Snapshots (body metrics)
    """
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProgressSnapshot
        fields = [
            'id', 'user', 'user_username', 'date',
            'body_weight', 'body_fat_percentage',
            'neck', 'chest', 'waist', 'hips', 'biceps', 'thighs', 'calves',
            'notes', 'photo',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class ProgressSnapshotListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing progress snapshots
    """
    class Meta:
        model = ProgressSnapshot
        fields = [
            'id', 'date', 'body_weight', 'body_fat_percentage'
        ]


class ExerciseProgressSerializer(serializers.Serializer):
    """
    Serializer for exercise progress over time
    Returns historical data points for charting
    """
    date = serializers.DateField()
    max_weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_reps = serializers.IntegerField()
    total_volume = serializers.DecimalField(max_digits=10, decimal_places=2)
    one_rep_max = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)


class WorkoutStatsSerializer(serializers.Serializer):
    """
    Serializer for workout statistics
    """
    total_workouts = serializers.IntegerField()
    workouts_this_week = serializers.IntegerField()
    workouts_this_month = serializers.IntegerField()
    total_volume = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_sets = serializers.IntegerField()
    total_reps = serializers.IntegerField()
    most_frequent_exercise = serializers.CharField(required=False)
    current_streak = serializers.IntegerField()
