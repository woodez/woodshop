import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { workoutService } from '../services/workoutService';

const WorkoutDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [workout, setWorkout] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchWorkout();
  }, [id]);

  const fetchWorkout = async () => {
    try {
      setLoading(true);
      const response = await workoutService.getById(id);
      setWorkout(response.data);
    } catch (err) {
      setError('Failed to load workout');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this workout?')) {
      try {
        await workoutService.delete(id);
        navigate('/workouts');
      } catch (err) {
        alert('Failed to delete workout');
        console.error(err);
      }
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading workout...</div>
      </div>
    );
  }

  if (error || !workout) {
    return (
      <div style={styles.container}>
        <div style={styles.error}>{error || 'Workout not found'}</div>
        <button onClick={() => navigate('/workouts')} style={styles.button}>
          Back to Workouts
        </button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>{workout.name || 'Workout'}</h1>
          <p style={styles.subtitle}>
            {new Date(workout.date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
        <div style={styles.headerButtons}>
          <button onClick={() => navigate('/workouts')} style={styles.backButton}>
            Back
          </button>
          <button onClick={handleDelete} style={styles.deleteButton}>
            Delete
          </button>
        </div>
      </div>

      <div style={styles.content}>
        <div style={styles.summary}>
          <div style={styles.stat}>
            <div style={styles.statLabel}>Status</div>
            <div style={styles.statValue}>
              {workout.completed ? '✓ Completed' : 'In Progress'}
            </div>
          </div>
          {workout.duration_minutes && (
            <div style={styles.stat}>
              <div style={styles.statLabel}>Duration</div>
              <div style={styles.statValue}>{workout.duration_minutes} min</div>
            </div>
          )}
          <div style={styles.stat}>
            <div style={styles.statLabel}>Exercises</div>
            <div style={styles.statValue}>{workout.exercises?.length || 0}</div>
          </div>
          <div style={styles.stat}>
            <div style={styles.statLabel}>Total Sets</div>
            <div style={styles.statValue}>
              {workout.exercises?.reduce((sum, ex) => sum + (ex.sets?.length || 0), 0) ||
                0}
            </div>
          </div>
        </div>

        {workout.notes && (
          <div style={styles.notesCard}>
            <h3 style={styles.cardTitle}>Notes</h3>
            <p style={styles.notesText}>{workout.notes}</p>
          </div>
        )}

        <div style={styles.exercisesSection}>
          <h2 style={styles.sectionTitle}>Exercises</h2>
          {workout.exercises && workout.exercises.length > 0 ? (
            workout.exercises.map((workoutExercise, index) => (
              <div key={workoutExercise.id} style={styles.exerciseCard}>
                <div style={styles.exerciseHeader}>
                  <h3 style={styles.exerciseName}>
                    {index + 1}. {workoutExercise.exercise_detail?.name || 'Exercise'}
                  </h3>
                </div>

                {workoutExercise.sets && workoutExercise.sets.length > 0 ? (
                  <div style={styles.setsTable}>
                    <div style={styles.tableHeader}>
                      <span style={styles.tableHeaderCell}>Set</span>
                      <span style={styles.tableHeaderCell}>Reps</span>
                      <span style={styles.tableHeaderCell}>Weight</span>
                      {workoutExercise.sets.some((s) => s.rpe) && (
                        <span style={styles.tableHeaderCell}>RPE</span>
                      )}
                    </div>
                    {workoutExercise.sets.map((set) => (
                      <div key={set.id} style={styles.tableRow}>
                        <span style={styles.tableCell}>{set.set_number}</span>
                        <span style={styles.tableCell}>{set.reps}</span>
                        <span style={styles.tableCell}>{set.weight} lbs</span>
                        {workoutExercise.sets.some((s) => s.rpe) && (
                          <span style={styles.tableCell}>{set.rpe || '-'}</span>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={styles.noSets}>No sets logged</div>
                )}

                {workoutExercise.notes && (
                  <div style={styles.exerciseNotes}>
                    <strong>Notes:</strong> {workoutExercise.notes}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div style={styles.noExercises}>No exercises in this workout</div>
          )}
        </div>
      </div>
    </div>
  );
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
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#333',
    margin: '0 0 5px 0',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    margin: 0,
  },
  headerButtons: {
    display: 'flex',
    gap: '10px',
  },
  backButton: {
    padding: '10px 20px',
    backgroundColor: '#2196F3',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    cursor: 'pointer',
    fontWeight: '500',
  },
  deleteButton: {
    padding: '10px 20px',
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    cursor: 'pointer',
    fontWeight: '500',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    fontSize: '18px',
    color: '#666',
  },
  error: {
    backgroundColor: '#fee',
    color: '#c33',
    padding: '12px',
    margin: '20px',
    borderRadius: '4px',
  },
  button: {
    padding: '12px 24px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    margin: '20px',
  },
  content: {
    padding: '40px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  summary: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  stat: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    textAlign: 'center',
  },
  statLabel: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '8px',
  },
  statValue: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
  },
  notesCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '30px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '10px',
  },
  notesText: {
    fontSize: '16px',
    color: '#666',
    lineHeight: '1.6',
  },
  exercisesSection: {
    marginTop: '30px',
  },
  sectionTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '20px',
  },
  exerciseCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '20px',
  },
  exerciseHeader: {
    marginBottom: '15px',
  },
  exerciseName: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  setsTable: {
    marginTop: '10px',
  },
  tableHeader: {
    display: 'grid',
    gridTemplateColumns: '60px 80px 100px 80px',
    gap: '10px',
    padding: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '4px',
    fontWeight: 'bold',
    fontSize: '14px',
    color: '#666',
  },
  tableHeaderCell: {
    textAlign: 'center',
  },
  tableRow: {
    display: 'grid',
    gridTemplateColumns: '60px 80px 100px 80px',
    gap: '10px',
    padding: '10px',
    borderBottom: '1px solid #eee',
  },
  tableCell: {
    textAlign: 'center',
    fontSize: '16px',
    color: '#333',
  },
  noSets: {
    textAlign: 'center',
    color: '#999',
    padding: '20px',
    fontSize: '14px',
  },
  noExercises: {
    textAlign: 'center',
    color: '#999',
    padding: '40px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  exerciseNotes: {
    marginTop: '10px',
    padding: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '4px',
    fontSize: '14px',
    color: '#666',
  },
};

export default WorkoutDetail;
