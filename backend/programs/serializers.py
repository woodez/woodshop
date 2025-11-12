from rest_framework import serializers
from .models import Program, ProgramWeek, ProgramDay, ProgramExercise, UserProgram
from workouts.serializers import ExerciseListSerializer


class ProgramExerciseSerializer(serializers.ModelSerializer):
    """Serializer for program exercises with exercise details"""
    exercise_detail = ExerciseListSerializer(source='exercise', read_only=True)

    class Meta:
        model = ProgramExercise
        fields = [
            'id',
            'program_day',
            'exercise',
            'exercise_detail',
            'order',
            'sets',
            'reps',
            'rest_period',
            'notes',
        ]
        read_only_fields = ['id']


class ProgramDaySerializer(serializers.ModelSerializer):
    """Serializer for program days with exercises"""
    exercises = ProgramExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramDay
        fields = [
            'id',
            'program_week',
            'day_number',
            'name',
            'description',
            'exercises',
        ]
        read_only_fields = ['id']


class ProgramWeekSerializer(serializers.ModelSerializer):
    """Serializer for program weeks with days"""
    days = ProgramDaySerializer(many=True, read_only=True)

    class Meta:
        model = ProgramWeek
        fields = [
            'id',
            'program',
            'week_number',
            'description',
            'days',
        ]
        read_only_fields = ['id']


class ProgramSerializer(serializers.ModelSerializer):
    """Detailed serializer for programs with full structure"""
    weeks = ProgramWeekSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    total_days = serializers.SerializerMethodField()
    subscription_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            'id',
            'name',
            'description',
            'created_by',
            'created_by_username',
            'is_public',
            'duration_weeks',
            'difficulty_level',
            'tags',
            'total_days',
            'subscription_count',
            'weeks',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_total_days(self, obj):
        return sum(week.days.count() for week in obj.weeks.all())

    def get_subscription_count(self, obj):
        return obj.subscriptions.filter(is_active=True).count()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProgramListSerializer(serializers.ModelSerializer):
    """Lighter serializer for program lists"""
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    week_count = serializers.SerializerMethodField()
    day_count = serializers.SerializerMethodField()
    subscription_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            'id',
            'name',
            'description',
            'created_by_username',
            'is_public',
            'duration_weeks',
            'difficulty_level',
            'tags',
            'week_count',
            'day_count',
            'subscription_count',
        ]

    def get_week_count(self, obj):
        return obj.weeks.count()

    def get_day_count(self, obj):
        return sum(week.days.count() for week in obj.weeks.all())

    def get_subscription_count(self, obj):
        return obj.subscriptions.filter(is_active=True).count()


class UserProgramSerializer(serializers.ModelSerializer):
    """Serializer for user program subscriptions"""
    program_detail = ProgramListSerializer(source='program', read_only=True)

    class Meta:
        model = UserProgram
        fields = [
            'id',
            'user',
            'program',
            'program_detail',
            'start_date',
            'current_week',
            'current_day',
            'is_active',
            'completed',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
