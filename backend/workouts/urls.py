from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MuscleGroupViewSet,
    ExerciseViewSet,
    WorkoutViewSet,
    WorkoutExerciseViewSet,
    SetViewSet,
)

router = DefaultRouter()
router.register(r'muscle-groups', MuscleGroupViewSet, basename='muscle-group')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'workout-exercises', WorkoutExerciseViewSet, basename='workout-exercise')
router.register(r'sets', SetViewSet, basename='set')

urlpatterns = [
    path('', include(router.urls)),
]
