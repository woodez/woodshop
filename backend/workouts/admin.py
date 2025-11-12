from django.contrib import admin
from .models import MuscleGroup, Exercise, Workout, WorkoutExercise, Set


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0
    raw_id_fields = ['exercise']


class SetInline(admin.TabularInline):
    model = Set
    extra = 0


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_by', 'is_public', 'created_at']
    list_filter = ['category', 'is_public', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['muscle_groups']
    raw_id_fields = ['created_by']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date', 'completed', 'duration_minutes', 'created_at']
    list_filter = ['completed', 'date', 'created_at']
    search_fields = ['user__username', 'user__email', 'name']
    date_hierarchy = 'date'
    raw_id_fields = ['user', 'program']
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['workout', 'exercise', 'order']
    list_filter = ['workout__date']
    search_fields = ['workout__name', 'exercise__name']
    raw_id_fields = ['workout', 'exercise']
    inlines = [SetInline]


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['workout_exercise', 'set_number', 'reps', 'weight', 'rpe', 'completed']
    list_filter = ['completed', 'created_at']
    raw_id_fields = ['workout_exercise']
