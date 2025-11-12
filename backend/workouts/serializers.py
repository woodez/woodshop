from rest_framework import serializers
from .models import MuscleGroup, Exercise, Workout, WorkoutExercise, Set


class MuscleGroupSerializer(serializers.ModelSerializer):
    """Serializer for muscle groups"""

    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'description']


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for exercises with muscle group details"""
    muscle_groups = MuscleGroupSerializer(many=True, read_only=True)
    muscle_group_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=MuscleGroup.objects.all(),
        source='muscle_groups',
        required=False
    )
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'description',
            'category',
            'muscle_groups',
            'muscle_group_ids',
            'equipment_needed',
            'instructions',
            'video_url',
            'created_by',
            'created_by_username',
            'is_public',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set created_by to current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ExerciseListSerializer(serializers.ModelSerializer):
    """Lighter serializer for exercise lists"""
    muscle_group_names = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'category',
            'muscle_group_names',
            'equipment_needed',
        ]

    def get_muscle_group_names(self, obj):
        return [mg.name for mg in obj.muscle_groups.all()]


class SetSerializer(serializers.ModelSerializer):
    """Serializer for individual sets"""

    class Meta:
        model = Set
        fields = [
            'id',
            'workout_exercise',
            'set_number',
            'reps',
            'weight',
            'rpe',
            'completed',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """Serializer for workout exercises with sets"""
    sets = SetSerializer(many=True, read_only=True)
    exercise_detail = ExerciseListSerializer(source='exercise', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'workout',
            'exercise',
            'exercise_detail',
            'order',
            'notes',
            'sets',
        ]
        read_only_fields = ['id']


class WorkoutExerciseCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating workout exercises"""

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'workout', 'exercise', 'order', 'notes']
        read_only_fields = ['id']


class WorkoutSerializer(serializers.ModelSerializer):
    """Detailed serializer for workouts with all exercises and sets"""
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id',
            'user',
            'program',
            'date',
            'name',
            'notes',
            'duration_minutes',
            'completed',
            'exercises',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set user to current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WorkoutListSerializer(serializers.ModelSerializer):
    """Lighter serializer for workout lists"""
    exercise_count = serializers.SerializerMethodField()
    total_sets = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            'id',
            'date',
            'name',
            'completed',
            'duration_minutes',
            'exercise_count',
            'total_sets',
        ]

    def get_exercise_count(self, obj):
        return obj.exercises.count()

    def get_total_sets(self, obj):
        return sum(we.sets.count() for we in obj.exercises.all())
