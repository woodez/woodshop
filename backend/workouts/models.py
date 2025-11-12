from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class MuscleGroup(models.Model):
    """
    Muscle groups for exercises (e.g., Chest, Back, Legs)
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Exercise(models.Model):
    """
    Exercise library - both default exercises and user-created custom exercises
    """
    CATEGORY_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='strength')
    muscle_groups = models.ManyToManyField(MuscleGroup, related_name='exercises', blank=True)
    equipment_needed = models.CharField(max_length=200, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    # User ownership - null for default exercises, set for custom exercises
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_exercises',
        null=True,
        blank=True
    )
    is_public = models.BooleanField(default=False)  # Custom exercises can be shared

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['created_by']),
        ]


class Workout(models.Model):
    """
    A workout session
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    program = models.ForeignKey(
        'programs.Program',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workouts'
    )

    date = models.DateField()
    name = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        workout_name = self.name or f"Workout on {self.date}"
        return f"{self.user.username} - {workout_name}"

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['completed']),
        ]


class WorkoutExercise(models.Model):
    """
    Junction table linking workouts to exercises with ordering
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workout_exercises')
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout} - {self.exercise.name}"

    class Meta:
        ordering = ['order', 'id']
        unique_together = ['workout', 'exercise', 'order']


class Set(models.Model):
    """
    Individual set within a workout exercise
    """
    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.CASCADE,
        related_name='sets'
    )
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Weight in user's preferred unit (kg or lb)"
    )
    rpe = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Rate of Perceived Exertion (1-10)"
    )
    completed = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Set {self.set_number}: {self.reps} reps @ {self.weight}"

    class Meta:
        ordering = ['set_number']
        unique_together = ['workout_exercise', 'set_number']
