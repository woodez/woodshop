from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date

from .models import MuscleGroup, Exercise, Workout, WorkoutExercise, Set
from .serializers import (
    MuscleGroupSerializer,
    ExerciseSerializer,
    ExerciseListSerializer,
    WorkoutSerializer,
    WorkoutListSerializer,
    WorkoutExerciseSerializer,
    WorkoutExerciseCreateSerializer,
    SetSerializer,
)


class MuscleGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing muscle groups
    """
    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSerializer
    permission_classes = [IsAuthenticated]


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exercises
    Users can view default exercises and their own custom exercises
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'equipment_needed']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Return default exercises and user's custom exercises"""
        user = self.request.user
        return Exercise.objects.filter(
            Q(created_by__isnull=True) |  # Default exercises
            Q(created_by=user) |  # User's custom exercises
            Q(is_public=True)  # Public custom exercises
        ).distinct()

    def get_serializer_class(self):
        """Use list serializer for list action, detailed for others"""
        if self.action == 'list':
            return ExerciseListSerializer
        return ExerciseSerializer

    def perform_create(self, serializer):
        """Set the creator when creating custom exercise"""
        serializer.save(created_by=self.request.user)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workouts
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        """Return only user's workouts"""
        queryset = Workout.objects.filter(user=self.request.user)

        # Filter by date range if provided
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        # Filter by completed status
        completed = self.request.query_params.get('completed')
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')

        return queryset.prefetch_related('exercises__exercise', 'exercises__sets')

    def get_serializer_class(self):
        """Use list serializer for list action, detailed for others"""
        if self.action == 'list':
            return WorkoutListSerializer
        return WorkoutSerializer

    def perform_create(self, serializer):
        """Set the user when creating workout"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark workout as completed"""
        workout = self.get_object()
        workout.completed = True
        workout.save()
        serializer = self.get_serializer(workout)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's workout"""
        today_workout = self.get_queryset().filter(date=date.today()).first()
        if today_workout:
            serializer = WorkoutSerializer(today_workout)
            return Response(serializer.data)
        return Response({'detail': 'No workout for today'}, status=status.HTTP_404_NOT_FOUND)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout exercises
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return workout exercises for user's workouts only"""
        return WorkoutExercise.objects.filter(
            workout__user=self.request.user
        ).select_related('exercise', 'workout').prefetch_related('sets')

    def get_serializer_class(self):
        """Use create serializer for create/update, detailed for read"""
        if self.action in ['create', 'update', 'partial_update']:
            return WorkoutExerciseCreateSerializer
        return WorkoutExerciseSerializer


class SetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sets within workout exercises
    """
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return sets for user's workouts only"""
        return Set.objects.filter(
            workout_exercise__workout__user=self.request.user
        ).select_related('workout_exercise__exercise')
