from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date, timedelta

from .models import Program, ProgramWeek, ProgramDay, ProgramExercise, UserProgram
from .serializers import (
    ProgramSerializer,
    ProgramListSerializer,
    ProgramWeekSerializer,
    ProgramDaySerializer,
    ProgramExerciseSerializer,
    UserProgramSerializer,
)


class ProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout programs
    Users can view public programs and their own programs
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['name', 'difficulty_level', 'duration_weeks', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Return public programs and user's created programs"""
        user = self.request.user
        queryset = Program.objects.filter(
            Q(is_public=True) | Q(created_by=user)
        ).prefetch_related('weeks__days__exercises__exercise').distinct()

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by duration
        max_weeks = self.request.query_params.get('max_weeks')
        if max_weeks:
            queryset = queryset.filter(duration_weeks__lte=max_weeks)

        return queryset

    def get_serializer_class(self):
        """Use list serializer for list action, detailed for others"""
        if self.action == 'list':
            return ProgramListSerializer
        return ProgramSerializer

    def perform_create(self, serializer):
        """Set creator when creating program"""
        serializer.save(created_by=self.request.user)


class UserProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user program subscriptions
    """
    serializer_class = UserProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only user's program subscriptions"""
        queryset = UserProgram.objects.filter(user=self.request.user).select_related(
            'program', 'program__created_by'
        ).prefetch_related('program__weeks__days__exercises__exercise')

        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset

    def perform_create(self, serializer):
        """Set user when subscribing to program"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def advance(self, request, pk=None):
        """
        Advance to next day/week in program
        """
        user_program = self.get_object()
        program = user_program.program

        # Get total days in current week
        current_week_obj = program.weeks.filter(week_number=user_program.current_week).first()
        if not current_week_obj:
            return Response(
                {'error': 'Current week not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_days_in_week = current_week_obj.days.count()

        # Advance day
        if user_program.current_day < total_days_in_week:
            user_program.current_day += 1
        else:
            # Advance week
            if user_program.current_week < program.duration_weeks:
                user_program.current_week += 1
                user_program.current_day = 1
            else:
                # Program completed
                user_program.completed = True
                user_program.completed_at = date.today()
                user_program.is_active = False

        user_program.save()
        serializer = self.get_serializer(user_program)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def today_workout(self, request, pk=None):
        """
        Get today's workout from the program
        """
        user_program = self.get_object()
        program = user_program.program

        # Get current week and day
        current_week = program.weeks.filter(week_number=user_program.current_week).first()
        if not current_week:
            return Response(
                {'error': 'Current week not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        current_day = current_week.days.filter(day_number=user_program.current_day).first()
        if not current_day:
            return Response(
                {'error': 'Current day not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProgramDaySerializer(current_day)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get user's active program"""
        active_program = self.get_queryset().filter(is_active=True).first()
        if active_program:
            serializer = self.get_serializer(active_program)
            return Response(serializer.data)
        return Response(
            {'detail': 'No active program'},
            status=status.HTTP_404_NOT_FOUND
        )
