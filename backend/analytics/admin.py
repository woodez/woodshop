from django.contrib import admin
from .models import PersonalRecord, ProgressSnapshot


@admin.register(PersonalRecord)
class PersonalRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'record_type', 'value', 'date_achieved']
    list_filter = ['record_type', 'date_achieved']
    search_fields = ['user__username', 'user__email', 'exercise__name']
    raw_id_fields = ['user', 'exercise', 'workout']
    date_hierarchy = 'date_achieved'
    ordering = ['-date_achieved']


@admin.register(ProgressSnapshot)
class ProgressSnapshotAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'body_weight', 'body_fat_percentage']
    list_filter = ['date']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'date')
        }),
        ('Body Metrics', {
            'fields': ('body_weight', 'body_fat_percentage')
        }),
        ('Measurements', {
            'fields': ('neck', 'chest', 'waist', 'hips', 'biceps', 'thighs', 'calves')
        }),
        ('Additional Info', {
            'fields': ('notes', 'photo')
        }),
    )
