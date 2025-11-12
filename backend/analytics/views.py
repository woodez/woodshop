from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Max, Count, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import PersonalRecord, ProgressSnapshot
from .serializers import (
    PersonalRecordSerializer,
    PersonalRecordListSerializer,
    ProgressSnapshotSerializer,
    ProgressSnapshotListSerializer,
    ExerciseProgressSerializer,
    WorkoutStatsSerializer,
)
from workouts.models import Workout, WorkoutExercise, Set


class PersonalRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing personal records
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['exercise__name', 'record_type']
    ordering_fields = ['date_achieved', 'value']
    ordering = ['-date_achieved']

    def get_queryset(self):
        """Return only user's personal records"""
        queryset = PersonalRecord.objects.filter(user=self.request.user).select_related(
            'exercise', 'workout'
        )

        # Filter by exercise
        exercise_id = self.request.query_params.get('exercise')
        if exercise_id:
            queryset = queryset.filter(exercise_id=exercise_id)

        # Filter by record type
        record_type = self.request.query_params.get('record_type')
        if record_type:
            queryset = queryset.filter(record_type=record_type)

        return queryset

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == 'list':
            return PersonalRecordListSerializer
        return PersonalRecordSerializer

    def perform_create(self, serializer):
        """Set user when creating PR"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_exercise(self, request):
        """
        Get all PRs grouped by exercise
        """
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response(
                {'error': 'exercise_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        records = self.get_queryset().filter(exercise_id=exercise_id)
        serializer = PersonalRecordListSerializer(records, many=True)
        return Response(serializer.data)


class ProgressSnapshotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing progress snapshots
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['-date']

    def get_queryset(self):
        """Return only user's progress snapshots"""
        queryset = ProgressSnapshot.objects.filter(user=self.request.user)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == 'list':
            return ProgressSnapshotListSerializer
        return ProgressSnapshotSerializer

    def perform_create(self, serializer):
        """Set user when creating snapshot"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get most recent progress snapshot"""
        snapshot = self.get_queryset().first()
        if snapshot:
            serializer = self.get_serializer(snapshot)
            return Response(serializer.data)
        return Response(
            {'detail': 'No progress snapshots found'},
            status=status.HTTP_404_NOT_FOUND
        )


class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for analytics calculations and aggregations
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def exercise_progress(self, request):
        """
        Get progress data for a specific exercise over time
        Returns: date, max_weight, total_reps, total_volume
        """
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response(
                {'error': 'exercise_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get date range (default to last 90 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=90)

        start_param = request.query_params.get('start_date')
        end_param = request.query_params.get('end_date')

        if start_param:
            start_date = datetime.strptime(start_param, '%Y-%m-%d').date()
        if end_param:
            end_date = datetime.strptime(end_param, '%Y-%m-%d').date()

        # Get workout exercises for this exercise
        workout_exercises = WorkoutExercise.objects.filter(
            workout__user=request.user,
            workout__date__gte=start_date,
            workout__date__lte=end_date,
            exercise_id=exercise_id,
            workout__completed=True
        ).select_related('workout').prefetch_related('sets')

        # Aggregate by date
        progress_data = {}
        for we in workout_exercises:
            workout_date = we.workout.date
            sets = we.sets.all()

            if not sets:
                continue

            max_weight = max([s.weight for s in sets])
            total_reps = sum([s.reps for s in sets])
            total_volume = sum([s.weight * s.reps for s in sets])

            if workout_date in progress_data:
                progress_data[workout_date]['max_weight'] = max(
                    progress_data[workout_date]['max_weight'], max_weight
                )
                progress_data[workout_date]['total_reps'] += total_reps
                progress_data[workout_date]['total_volume'] += total_volume
            else:
                progress_data[workout_date] = {
                    'date': workout_date,
                    'max_weight': max_weight,
                    'total_reps': total_reps,
                    'total_volume': total_volume,
                }

        # Convert to list and sort by date
        result = sorted(progress_data.values(), key=lambda x: x['date'])
        serializer = ExerciseProgressSerializer(result, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def workout_stats(self, request):
        """
        Get overall workout statistics for the user
        """
        user = request.user
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        # Total workouts
        total_workouts = Workout.objects.filter(
            user=user, completed=True
        ).count()

        # Workouts this week
        workouts_this_week = Workout.objects.filter(
            user=user, completed=True, date__gte=week_start
        ).count()

        # Workouts this month
        workouts_this_month = Workout.objects.filter(
            user=user, completed=True, date__gte=month_start
        ).count()

        # Total volume (all time)
        total_volume = Set.objects.filter(
            workout_exercise__workout__user=user,
            workout_exercise__workout__completed=True
        ).aggregate(
            volume=Sum(F('weight') * F('reps'))
        )['volume'] or 0

        # Total sets and reps
        set_stats = Set.objects.filter(
            workout_exercise__workout__user=user,
            workout_exercise__workout__completed=True
        ).aggregate(
            total_sets=Count('id'),
            total_reps=Sum('reps')
        )

        # Most frequent exercise
        most_frequent = WorkoutExercise.objects.filter(
            workout__user=user,
            workout__completed=True
        ).values('exercise__name').annotate(
            count=Count('id')
        ).order_by('-count').first()

        # Current streak (consecutive days with workouts)
        current_streak = self._calculate_streak(user)

        data = {
            'total_workouts': total_workouts,
            'workouts_this_week': workouts_this_week,
            'workouts_this_month': workouts_this_month,
            'total_volume': total_volume,
            'total_sets': set_stats['total_sets'] or 0,
            'total_reps': set_stats['total_reps'] or 0,
            'most_frequent_exercise': most_frequent['exercise__name'] if most_frequent else None,
            'current_streak': current_streak,
        }

        serializer = WorkoutStatsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def volume_trend(self, request):
        """
        Get volume trend over time (weekly aggregation)
        """
        # Get date range (default to last 12 weeks)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(weeks=12)

        start_param = request.query_params.get('start_date')
        end_param = request.query_params.get('end_date')

        if start_param:
            start_date = datetime.strptime(start_param, '%Y-%m-%d').date()
        if end_param:
            end_date = datetime.strptime(end_param, '%Y-%m-%d').date()

        # Get all workouts in range
        workouts = Workout.objects.filter(
            user=request.user,
            completed=True,
            date__gte=start_date,
            date__lte=end_date
        ).prefetch_related('workout_exercises__sets')

        # Aggregate by week
        weekly_data = {}
        for workout in workouts:
            # Get start of week for this workout
            week_start = workout.date - timedelta(days=workout.date.weekday())

            # Calculate volume for this workout
            volume = 0
            for we in workout.workout_exercises.all():
                for s in we.sets.all():
                    volume += s.weight * s.reps

            if week_start in weekly_data:
                weekly_data[week_start]['volume'] += volume
                weekly_data[week_start]['workouts'] += 1
            else:
                weekly_data[week_start] = {
                    'week_start': week_start,
                    'volume': volume,
                    'workouts': 1
                }

        # Convert to list and sort
        result = sorted(weekly_data.values(), key=lambda x: x['week_start'])
        return Response(result)

    @action(detail=False, methods=['get'])
    def frequency_by_muscle_group(self, request):
        """
        Get workout frequency by muscle group
        """
        # Get date range (default to last 30 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        start_param = request.query_params.get('start_date')
        if start_param:
            start_date = datetime.strptime(start_param, '%Y-%m-%d').date()

        # Get workout exercises in date range
        muscle_group_counts = WorkoutExercise.objects.filter(
            workout__user=request.user,
            workout__completed=True,
            workout__date__gte=start_date,
            workout__date__lte=end_date
        ).values(
            'exercise__muscle_groups__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        # Format results
        result = [
            {
                'muscle_group': item['exercise__muscle_groups__name'],
                'count': item['count']
            }
            for item in muscle_group_counts if item['exercise__muscle_groups__name']
        ]

        return Response(result)

    def _calculate_streak(self, user):
        """
        Calculate current workout streak (consecutive days)
        """
        today = timezone.now().date()
        workouts = Workout.objects.filter(
            user=user, completed=True
        ).values_list('date', flat=True).distinct().order_by('-date')

        if not workouts:
            return 0

        # Check if there's a workout today or yesterday
        if workouts[0] not in [today, today - timedelta(days=1)]:
            return 0

        streak = 0
        current_date = workouts[0]

        for workout_date in workouts:
            if workout_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif workout_date < current_date:
                # Allow for rest days - check if within reasonable gap
                days_diff = (current_date - workout_date).days
                if days_diff <= 2:  # Allow up to 2 rest days
                    streak += 1
                    current_date = workout_date - timedelta(days=1)
                else:
                    break
            else:
                break

        return streak
