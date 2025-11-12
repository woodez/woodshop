from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Program(models.Model):
    """
    Workout Program - placeholder for Phase 4
    Will be fully implemented in Phase 4: Workout Programs & Subscriptions
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
