from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Program(models.Model):
    """
    Workout Program - A structured workout plan with weeks and days
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_programs',
        null=True,
        blank=True
    )
    is_public = models.BooleanField(default=False)
    duration_weeks = models.PositiveIntegerField(default=4)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_public', 'difficulty_level']),
        ]


class ProgramWeek(models.Model):
    """
    A week within a program
    """
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.program.name} - Week {self.week_number}"

    class Meta:
        ordering = ['week_number']
        unique_together = ['program', 'week_number']


class ProgramDay(models.Model):
    """
    A day within a program week
    """
    program_week = models.ForeignKey(ProgramWeek, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    name = models.CharField(max_length=200, help_text="e.g., 'Push Day', 'Leg Day'")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.program_week.program.name} - Week {self.program_week.week_number} - Day {self.day_number}: {self.name}"

    class Meta:
        ordering = ['day_number']
        unique_together = ['program_week', 'day_number']


class ProgramExercise(models.Model):
    """
    An exercise within a program day with suggested sets/reps
    """
    program_day = models.ForeignKey(ProgramDay, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey('workouts.Exercise', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(help_text="Suggested number of sets")
    reps = models.CharField(max_length=50, help_text="Suggested reps (e.g., '8-12', '10', '5x5')")
    rest_period = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Rest period in seconds"
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.program_day.name} - {self.exercise.name}"

    class Meta:
        ordering = ['order']


class UserProgram(models.Model):
    """
    User's subscription to a program with progress tracking
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_programs')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    current_week = models.PositiveIntegerField(default=1)
    current_day = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.program.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'program']
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
