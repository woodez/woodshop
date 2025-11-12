import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  workoutService,
  exerciseService,
  workoutExerciseService,
  setService,
} from '../services/workoutService';

const NewWorkout = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Create workout, 2: Add exercises, 3: Log sets
  const [workout, setWorkout] = useState(null);
  const [workoutName, setWorkoutName] = useState('');
  const [workoutDate, setWorkoutDate] = useState(new Date().toISOString().split('T')[0]);

  // Exercise selection
  const [exercises, setExercises] = useState([]);
  const [selectedExercises, setSelectedExercises] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  // Set logging
  const [workoutExercises, setWorkoutExercises] = useState([]);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [sets, setSets] = useState({});
  const [currentSet, setCurrentSet] = useState({ reps: '', weight: '' });

  useEffect(() => {
    if (step === 2) {
      fetchExercises();
    }
  }, [step]);

  const fetchExercises = async () => {
    try {
      setLoading(true);
      const response = await exerciseService.getAll({ limit: 100 });
      setExercises(response.data.results || []);
    } catch (err) {
      console.error('Failed to load exercises:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkout = async () => {
    try {
      const response = await workoutService.create({
        date: workoutDate,
        name: workoutName || `Workout ${workoutDate}`,
        completed: false,
      });
      setWorkout(response.data);
      setStep(2);
    } catch (err) {
      alert('Failed to create workout');
      console.error(err);
    }
  };

  const handleAddExercise = (exercise) => {
    if (!selectedExercises.find((e) => e.id === exercise.id)) {
      setSelectedExercises([...selectedExercises, exercise]);
    }
  };

  const handleRemoveExercise = (exerciseId) => {
    setSelectedExercises(selectedExercises.filter((e) => e.id !== exerciseId));
  };

  const handleContinueToSets = async () => {
    try {
      // Create workout exercises
      const createdExercises = [];
      for (let i = 0; i < selectedExercises.length; i++) {
        const response = await workoutExerciseService.create({
          workout: workout.id,
          exercise: selectedExercises[i].id,
          order: i,
        });
        createdExercises.push(response.data);
      }
      setWorkoutExercises(createdExercises);
      setStep(3);
    } catch (err) {
      alert('Failed to add exercises');
      console.error(err);
    }
  };

  const handleAddSet = async () => {
    if (!currentSet.reps || !currentSet.weight) {
      alert('Please enter reps and weight');
      return;
    }

    try {
      const workoutExercise = workoutExercises[currentExerciseIndex];
      const currentSets = sets[workoutExercise.id] || [];
      const setNumber = currentSets.length + 1;

      const response = await setService.create({
        workout_exercise: workoutExercise.id,
        set_number: setNumber,
        reps: parseInt(currentSet.reps),
        weight: parseFloat(currentSet.weight),
        completed: true,
      });

      setSets({
        ...sets,
        [workoutExercise.id]: [...currentSets, response.data],
      });
      setCurrentSet({ reps: '', weight: '' });
    } catch (err) {
      alert('Failed to log set');
      console.error(err);
    }
  };

  const handleNextExercise = () => {
    if (currentExerciseIndex < workoutExercises.length - 1) {
      setCurrentExerciseIndex(currentExerciseIndex + 1);
      setCurrentSet({ reps: '', weight: '' });
    }
  };

  const handlePreviousExercise = () => {
    if (currentExerciseIndex > 0) {
      setCurrentExerciseIndex(currentExerciseIndex - 1);
      setCurrentSet({ reps: '', weight: '' });
    }
  };

  const handleFinishWorkout = async () => {
    try {
      await workoutService.complete(workout.id);
      navigate('/workouts');
    } catch (err) {
      alert('Failed to complete workout');
      console.error(err);
    }
  };

  const filteredExercises = exercises.filter((ex) =>
    ex.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Step 1: Create Workout
  if (step === 1) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>New Workout</h1>
        </div>
        <div style={styles.content}>
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Workout Details</h2>
            <div style={styles.formGroup}>
              <label style={styles.label}>Date</label>
              <input
                type="date"
                value={workoutDate}
                onChange={(e) => setWorkoutDate(e.target.value)}
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Workout Name (Optional)</label>
              <input
                type="text"
                value={workoutName}
                onChange={(e) => setWorkoutName(e.target.value)}
                placeholder="e.g., Upper Body, Leg Day"
                style={styles.input}
              />
            </div>
            <button onClick={handleCreateWorkout} style={styles.button}>
              Continue
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Step 2: Select Exercises
  if (step === 2) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Add Exercises</h1>
        </div>
        <div style={styles.content}>
          <div style={styles.columns}>
            <div style={styles.column}>
              <h3>Exercise Library</h3>
              <input
                type="text"
                placeholder="Search exercises..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={styles.searchInput}
              />
              <div style={styles.exerciseList}>
                {loading ? (
                  <div>Loading exercises...</div>
                ) : (
                  filteredExercises.map((exercise) => (
                    <div key={exercise.id} style={styles.exerciseItem}>
                      <div>
                        <div style={styles.exerciseName}>{exercise.name}</div>
                        <div style={styles.exerciseCategory}>{exercise.category}</div>
                      </div>
                      <button
                        onClick={() => handleAddExercise(exercise)}
                        style={styles.addButton}
                      >
                        +
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div style={styles.column}>
              <h3>Selected Exercises ({selectedExercises.length})</h3>
              <div style={styles.selectedList}>
                {selectedExercises.length === 0 ? (
                  <div style={styles.emptyText}>
                    No exercises added yet. Add exercises from the left.
                  </div>
                ) : (
                  selectedExercises.map((exercise) => (
                    <div key={exercise.id} style={styles.selectedItem}>
                      <span>{exercise.name}</span>
                      <button
                        onClick={() => handleRemoveExercise(exercise.id)}
                        style={styles.removeButton}
                      >
                        ×
                      </button>
                    </div>
                  ))
                )}
              </div>
              {selectedExercises.length > 0 && (
                <button onClick={handleContinueToSets} style={styles.button}>
                  Continue to Log Sets
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Step 3: Log Sets
  if (step === 3 && workoutExercises.length > 0) {
    const currentWorkoutExercise = workoutExercises[currentExerciseIndex];
    const currentExercise = selectedExercises[currentExerciseIndex];
    const currentExerciseSets = sets[currentWorkoutExercise.id] || [];

    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>
            {currentExercise.name} ({currentExerciseIndex + 1}/{workoutExercises.length})
          </h1>
        </div>
        <div style={styles.content}>
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Previous Sets</h3>
            {currentExerciseSets.length === 0 ? (
              <div style={styles.emptyText}>No sets logged yet</div>
            ) : (
              <div style={styles.setsList}>
                {currentExerciseSets.map((set) => (
                  <div key={set.id} style={styles.setItem}>
                    Set {set.set_number}: {set.reps} reps @ {set.weight} lbs
                  </div>
                ))}
              </div>
            )}

            <h3 style={styles.cardTitle}>Log New Set</h3>
            <div style={styles.setInputs}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Reps</label>
                <input
                  type="number"
                  value={currentSet.reps}
                  onChange={(e) =>
                    setCurrentSet({ ...currentSet, reps: e.target.value })
                  }
                  placeholder="10"
                  style={styles.input}
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Weight (lbs)</label>
                <input
                  type="number"
                  step="0.5"
                  value={currentSet.weight}
                  onChange={(e) =>
                    setCurrentSet({ ...currentSet, weight: e.target.value })
                  }
                  placeholder="135"
                  style={styles.input}
                />
              </div>
            </div>
            <button onClick={handleAddSet} style={styles.button}>
              Add Set
            </button>

            <div style={styles.navigation}>
              {currentExerciseIndex > 0 && (
                <button onClick={handlePreviousExercise} style={styles.navButton}>
                  ← Previous Exercise
                </button>
              )}
              {currentExerciseIndex < workoutExercises.length - 1 ? (
                <button onClick={handleNextExercise} style={styles.navButton}>
                  Next Exercise →
                </button>
              ) : (
                <button onClick={handleFinishWorkout} style={styles.finishButton}>
                  Finish Workout
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: 'white',
    padding: '20px 40px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  content: {
    padding: '40px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  card: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '20px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#333',
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '12px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
    boxSizing: 'border-box',
  },
  searchInput: {
    width: '100%',
    padding: '12px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '16px',
    marginBottom: '15px',
    boxSizing: 'border-box',
  },
  button: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: '500',
    marginTop: '10px',
  },
  columns: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
  },
  column: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  exerciseList: {
    maxHeight: '500px',
    overflowY: 'auto',
  },
  exerciseItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px',
    borderBottom: '1px solid #eee',
  },
  exerciseName: {
    fontSize: '16px',
    fontWeight: '500',
    color: '#333',
  },
  exerciseCategory: {
    fontSize: '12px',
    color: '#666',
    textTransform: 'capitalize',
  },
  addButton: {
    width: '32px',
    height: '32px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    fontSize: '20px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  selectedList: {
    minHeight: '300px',
    maxHeight: '500px',
    overflowY: 'auto',
    marginBottom: '20px',
  },
  selectedItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px',
    backgroundColor: '#f5f5f5',
    marginBottom: '8px',
    borderRadius: '4px',
  },
  removeButton: {
    width: '24px',
    height: '24px',
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    fontSize: '18px',
    cursor: 'pointer',
    lineHeight: '1',
  },
  emptyText: {
    textAlign: 'center',
    color: '#999',
    padding: '20px',
  },
  setInputs: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
    marginBottom: '20px',
  },
  setsList: {
    marginBottom: '30px',
  },
  setItem: {
    padding: '10px',
    backgroundColor: '#f5f5f5',
    marginBottom: '8px',
    borderRadius: '4px',
  },
  navigation: {
    display: 'flex',
    gap: '10px',
    marginTop: '30px',
  },
  navButton: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#2196F3',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: '500',
  },
  finishButton: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: '500',
  },
};

export default NewWorkout;
