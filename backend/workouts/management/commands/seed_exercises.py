from django.core.management.base import BaseCommand
from workouts.models import MuscleGroup, Exercise


class Command(BaseCommand):
    help = 'Seeds the database with default exercises and muscle groups'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding muscle groups...')

        # Create muscle groups
        muscle_groups = {
            'Chest': MuscleGroup.objects.get_or_create(name='Chest')[0],
            'Back': MuscleGroup.objects.get_or_create(name='Back')[0],
            'Shoulders': MuscleGroup.objects.get_or_create(name='Shoulders')[0],
            'Biceps': MuscleGroup.objects.get_or_create(name='Biceps')[0],
            'Triceps': MuscleGroup.objects.get_or_create(name='Triceps')[0],
            'Legs': MuscleGroup.objects.get_or_create(name='Legs')[0],
            'Quadriceps': MuscleGroup.objects.get_or_create(name='Quadriceps')[0],
            'Hamstrings': MuscleGroup.objects.get_or_create(name='Hamstrings')[0],
            'Glutes': MuscleGroup.objects.get_or_create(name='Glutes')[0],
            'Calves': MuscleGroup.objects.get_or_create(name='Calves')[0],
            'Abs': MuscleGroup.objects.get_or_create(name='Abs')[0],
            'Core': MuscleGroup.objects.get_or_create(name='Core')[0],
            'Forearms': MuscleGroup.objects.get_or_create(name='Forearms')[0],
        }

        self.stdout.write(self.style.SUCCESS(f'Created {len(muscle_groups)} muscle groups'))

        # Default exercises with their muscle groups
        exercises_data = [
            # Chest Exercises
            ('Bench Press', 'strength', ['Chest', 'Triceps', 'Shoulders'], 'Barbell'),
            ('Incline Bench Press', 'strength', ['Chest', 'Shoulders', 'Triceps'], 'Barbell'),
            ('Dumbbell Press', 'strength', ['Chest', 'Triceps', 'Shoulders'], 'Dumbbells'),
            ('Push-ups', 'strength', ['Chest', 'Triceps', 'Shoulders'], 'Bodyweight'),
            ('Dips', 'strength', ['Chest', 'Triceps'], 'Bodyweight'),
            ('Cable Flyes', 'strength', ['Chest'], 'Cable'),

            # Back Exercises
            ('Deadlift', 'strength', ['Back', 'Hamstrings', 'Glutes'], 'Barbell'),
            ('Pull-ups', 'strength', ['Back', 'Biceps'], 'Bodyweight'),
            ('Barbell Row', 'strength', ['Back', 'Biceps'], 'Barbell'),
            ('Lat Pulldown', 'strength', ['Back', 'Biceps'], 'Cable'),
            ('Dumbbell Row', 'strength', ['Back', 'Biceps'], 'Dumbbells'),
            ('T-Bar Row', 'strength', ['Back'], 'Barbell'),

            # Shoulder Exercises
            ('Overhead Press', 'strength', ['Shoulders', 'Triceps'], 'Barbell'),
            ('Lateral Raise', 'strength', ['Shoulders'], 'Dumbbells'),
            ('Front Raise', 'strength', ['Shoulders'], 'Dumbbells'),
            ('Rear Delt Flyes', 'strength', ['Shoulders'], 'Dumbbells'),
            ('Arnold Press', 'strength', ['Shoulders'], 'Dumbbells'),

            # Arm Exercises
            ('Barbell Curl', 'strength', ['Biceps'], 'Barbell'),
            ('Hammer Curl', 'strength', ['Biceps', 'Forearms'], 'Dumbbells'),
            ('Tricep Extension', 'strength', ['Triceps'], 'Dumbbells'),
            ('Tricep Pushdown', 'strength', ['Triceps'], 'Cable'),
            ('Close-Grip Bench Press', 'strength', ['Triceps', 'Chest'], 'Barbell'),

            # Leg Exercises
            ('Squat', 'strength', ['Quadriceps', 'Glutes', 'Hamstrings'], 'Barbell'),
            ('Front Squat', 'strength', ['Quadriceps', 'Core'], 'Barbell'),
            ('Leg Press', 'strength', ['Quadriceps', 'Glutes'], 'Machine'),
            ('Lunges', 'strength', ['Quadriceps', 'Glutes'], 'Dumbbells'),
            ('Leg Extension', 'strength', ['Quadriceps'], 'Machine'),
            ('Leg Curl', 'strength', ['Hamstrings'], 'Machine'),
            ('Romanian Deadlift', 'strength', ['Hamstrings', 'Glutes'], 'Barbell'),
            ('Calf Raise', 'strength', ['Calves'], 'Machine'),

            # Core/Abs Exercises
            ('Plank', 'strength', ['Core', 'Abs'], 'Bodyweight'),
            ('Crunches', 'strength', ['Abs'], 'Bodyweight'),
            ('Russian Twists', 'strength', ['Abs', 'Core'], 'Bodyweight'),
            ('Hanging Leg Raise', 'strength', ['Abs'], 'Bodyweight'),
            ('Cable Crunches', 'strength', ['Abs'], 'Cable'),

            # Cardio
            ('Running', 'cardio', [], 'Cardio Equipment'),
            ('Cycling', 'cardio', [], 'Cardio Equipment'),
            ('Rowing', 'cardio', ['Back', 'Legs'], 'Cardio Equipment'),
        ]

        created_count = 0
        for exercise_name, category, muscle_group_names, equipment in exercises_data:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_name,
                defaults={
                    'category': category,
                    'equipment_needed': equipment,
                    'created_by': None,  # Default exercises have no creator
                    'is_public': True,
                }
            )

            if created:
                # Add muscle groups
                for mg_name in muscle_group_names:
                    if mg_name in muscle_groups:
                        exercise.muscle_groups.add(muscle_groups[mg_name])
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new exercises'))
        self.stdout.write(self.style.SUCCESS(f'Total exercises in database: {Exercise.objects.count()}'))
