import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { workoutService } from '../services/workoutService';

const Workouts = () => {
  const navigate = useNavigate();
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      setLoading(true);
      const response = await workoutService.getAll({ limit: 50 });
      setWorkouts(response.data.results || []);
    } catch (err) {
      setError('Failed to load workouts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartWorkout = () => {
    navigate('/workouts/new');
  };

  const handleViewWorkout = (id) => {
    navigate(`/workouts/${id}`);
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading workouts...</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>My Workouts</h1>
        <button onClick={handleStartWorkout} style={styles.startButton}>
          + Start New Workout
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.content}>
        {workouts.length === 0 ? (
          <div style={styles.empty}>
            <h2 style={styles.emptyTitle}>No workouts yet!</h2>
            <p style={styles.emptyText}>
              Click "Start New Workout" to log your first workout.
            </p>
          </div>
        ) : (
          <div style={styles.grid}>
            {workouts.map((workout) => (
              <div
                key={workout.id}
                style={styles.card}
                onClick={() => handleViewWorkout(workout.id)}
              >
                <div style={styles.cardHeader}>
                  <span style={styles.cardDate}>
                    {new Date(workout.date).toLocaleDateString()}
                  </span>
                  {workout.completed && (
                    <span style={styles.completedBadge}>✓ Completed</span>
                  )}
                </div>
                <h3 style={styles.cardTitle}>
                  {workout.name || 'Untitled Workout'}
                </h3>
                <div style={styles.cardStats}>
                  <span>{workout.exercise_count} exercises</span>
                  <span>•</span>
                  <span>{workout.total_sets} sets</span>
                  {workout.duration_minutes && (
                    <>
                      <span>•</span>
                      <span>{workout.duration_minutes} min</span>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
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
    alignItems: 'center',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  startButton: {
    padding: '12px 24px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
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
    padding: '12px 40px',
    margin: '20px 40px',
    borderRadius: '4px',
  },
  content: {
    padding: '40px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  empty: {
    textAlign: 'center',
    padding: '60px 20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  emptyTitle: {
    fontSize: '24px',
    color: '#333',
    marginBottom: '10px',
  },
  emptyText: {
    fontSize: '16px',
    color: '#666',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '20px',
  },
  card: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  cardDate: {
    fontSize: '14px',
    color: '#666',
  },
  completedBadge: {
    fontSize: '12px',
    backgroundColor: '#4CAF50',
    color: 'white',
    padding: '4px 8px',
    borderRadius: '4px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '10px',
  },
  cardStats: {
    fontSize: '14px',
    color: '#666',
    display: 'flex',
    gap: '8px',
  },
};

export default Workouts;
