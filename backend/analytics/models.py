from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class PersonalRecord(models.Model):
    """
    Track personal records for exercises
    """
    RECORD_TYPE_CHOICES = [
        ('max_weight', 'Max Weight'),
        ('max_reps', 'Max Reps'),
        ('max_volume', 'Max Volume'),
        ('one_rep_max', 'One Rep Max (Estimated)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_records')
    exercise = models.ForeignKey('workouts.Exercise', on_delete=models.CASCADE, related_name='personal_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    date_achieved = models.DateField()
    workout = models.ForeignKey(
        'workouts.Workout',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personal_records'
    )
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}: {self.record_type} = {self.value}"

    class Meta:
        ordering = ['-date_achieved']
        unique_together = ['user', 'exercise', 'record_type']
        indexes = [
            models.Index(fields=['user', 'exercise']),
            models.Index(fields=['date_achieved']),
        ]


class ProgressSnapshot(models.Model):
    """
    Track body measurements and metrics over time
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_snapshots')
    date = models.DateField()

    # Body metrics
    body_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in user's preferred unit"
    )
    body_fat_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Measurements (in inches or cm)
    neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    biceps = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thighs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calves = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='progress_photos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
