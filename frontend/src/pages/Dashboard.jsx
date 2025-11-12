import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Woodshop Dashboard</h1>
        <button onClick={handleLogout} style={styles.logoutButton}>
          Logout
        </button>
      </div>

      <div style={styles.content}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Welcome, {user?.first_name || user?.username}!</h2>
          <p style={styles.cardText}>
            Email: {user?.email}
          </p>
          <p style={styles.cardText}>
            Username: {user?.username}
          </p>
        </div>

        <div style={styles.grid}>
          <div
            style={styles.featureCard}
            onClick={() => navigate('/workouts')}
            role="button"
            tabIndex={0}
          >
            <h3 style={styles.featureTitle}>Workouts</h3>
            <p style={styles.featureText}>Log your exercises, sets, and reps</p>
            <button style={styles.featureButtonActive}>View Workouts</button>
          </div>

          <div
            style={styles.featureCard}
            onClick={() => navigate('/workouts/new')}
            role="button"
            tabIndex={0}
          >
            <h3 style={styles.featureTitle}>Start Workout</h3>
            <p style={styles.featureText}>Begin logging a new workout session</p>
            <button style={styles.featureButtonActive}>Start Now</button>
          </div>

          <div style={styles.featureCard}>
            <h3 style={styles.featureTitle}>Programs</h3>
            <p style={styles.featureText}>Subscribe to workout programs</p>
            <button style={styles.featureButton}>Coming Soon</button>
          </div>

          <div style={styles.featureCard}>
            <h3 style={styles.featureTitle}>Analytics</h3>
            <p style={styles.featureText}>Track your progress with charts</p>
            <button style={styles.featureButton}>Coming Soon</button>
          </div>

          <div
            style={styles.featureCard}
            onClick={() => navigate('/profile')}
            role="button"
            tabIndex={0}
          >
            <h3 style={styles.featureTitle}>Profile</h3>
            <p style={styles.featureText}>View and edit your profile</p>
            <button style={styles.featureButtonActive}>View Profile</button>
          </div>
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
    alignItems: 'center',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    cursor: 'pointer',
    fontWeight: '500',
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
    marginBottom: '30px',
  },
  cardTitle: {
    fontSize: '28px',
    color: '#333',
    marginBottom: '15px',
  },
  cardText: {
    fontSize: '16px',
    color: '#666',
    marginBottom: '8px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
  },
  featureCard: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  featureTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '10px',
  },
  featureText: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '20px',
  },
  featureButton: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#e0e0e0',
    color: '#999',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    cursor: 'not-allowed',
  },
  featureButtonActive: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    cursor: 'pointer',
    fontWeight: '500',
  },
};

export default Dashboard;
