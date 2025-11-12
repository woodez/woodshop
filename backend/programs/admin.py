from django.contrib import admin
from .models import Program, ProgramWeek, ProgramDay, ProgramExercise, UserProgram


class ProgramDayInline(admin.TabularInline):
    model = ProgramDay
    extra = 0


class ProgramWeekInline(admin.StackedInline):
    model = ProgramWeek
    extra = 0
    inlines = [ProgramDayInline]


class ProgramExerciseInline(admin.TabularInline):
    model = ProgramExercise
    extra = 0
    raw_id_fields = ['exercise']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty_level', 'duration_weeks', 'is_public', 'created_by', 'created_at']
    list_filter = ['difficulty_level', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'tags']
    raw_id_fields = ['created_by']


@admin.register(ProgramWeek)
class ProgramWeekAdmin(admin.ModelAdmin):
    list_display = ['program', 'week_number', 'description']
    list_filter = ['program']
    inlines = [ProgramDayInline]


@admin.register(ProgramDay)
class ProgramDayAdmin(admin.ModelAdmin):
    list_display = ['program_week', 'day_number', 'name']
    list_filter = ['program_week__program']
    inlines = [ProgramExerciseInline]


@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ['program_day', 'exercise', 'sets', 'reps', 'order']
    raw_id_fields = ['exercise']


@admin.register(UserProgram)
class UserProgramAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'start_date', 'current_week', 'current_day', 'is_active', 'completed']
    list_filter = ['is_active', 'completed', 'start_date']
    search_fields = ['user__username', 'program__name']
    raw_id_fields = ['user', 'program']
