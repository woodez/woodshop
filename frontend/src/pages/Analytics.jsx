import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analyticsService, personalRecordService } from '../services/analyticsService';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Analytics.css';

function Analytics() {
  const [workoutStats, setWorkoutStats] = useState(null);
  const [volumeTrend, setVolumeTrend] = useState([]);
  const [muscleGroupFrequency, setMuscleGroupFrequency] = useState([]);
  const [personalRecords, setPersonalRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658'];

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    setLoading(true);
    try {
      // Load all analytics data in parallel
      const [statsRes, volumeRes, muscleGroupRes, prsRes] = await Promise.all([
        analyticsService.getWorkoutStats(),
        analyticsService.getVolumeTrend(),
        analyticsService.getFrequencyByMuscleGroup(),
        personalRecordService.getAll({ ordering: '-date_achieved' }),
      ]);

      setWorkoutStats(statsRes.data);
      setVolumeTrend(volumeRes.data);
      setMuscleGroupFrequency(muscleGroupRes.data);
      setPersonalRecords(prsRes.data.results || prsRes.data);
    } catch (err) {
      console.error('Error loading analytics:', err);
      setError('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const formatVolumeTrendData = (data) => {
    return data.map(item => ({
      date: formatDate(item.week_start),
      volume: parseFloat(item.volume),
      workouts: item.workouts,
    }));
  };

  if (loading) {
    return <div className="analytics-page"><p>Loading analytics...</p></div>;
  }

  if (error) {
    return <div className="analytics-page"><p className="error">{error}</p></div>;
  }

  return (
    <div className="analytics-page">
      <header className="analytics-header">
        <h1>Analytics & Progress</h1>
        <div className="analytics-actions">
          <Link to="/analytics/progress-snapshots/new" className="btn btn-primary">
            Log Progress Snapshot
          </Link>
        </div>
      </header>

      {/* Stats Overview */}
      <section className="stats-overview">
        <div className="stat-card">
          <h3>Total Workouts</h3>
          <p className="stat-value">{workoutStats?.total_workouts || 0}</p>
        </div>
        <div className="stat-card">
          <h3>This Week</h3>
          <p className="stat-value">{workoutStats?.workouts_this_week || 0}</p>
        </div>
        <div className="stat-card">
          <h3>This Month</h3>
          <p className="stat-value">{workoutStats?.workouts_this_month || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Current Streak</h3>
          <p className="stat-value">{workoutStats?.current_streak || 0} days</p>
        </div>
        <div className="stat-card">
          <h3>Total Volume</h3>
          <p className="stat-value">{parseFloat(workoutStats?.total_volume || 0).toLocaleString()} lbs</p>
        </div>
        <div className="stat-card">
          <h3>Total Sets</h3>
          <p className="stat-value">{workoutStats?.total_sets || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Total Reps</h3>
          <p className="stat-value">{workoutStats?.total_reps || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Favorite Exercise</h3>
          <p className="stat-value small">{workoutStats?.most_frequent_exercise || 'N/A'}</p>
        </div>
      </section>

      {/* Charts */}
      <div className="charts-grid">
        {/* Volume Trend Chart */}
        <div className="chart-card">
          <h2>Volume Trend (12 Weeks)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={formatVolumeTrendData(volumeTrend)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="volume" stroke="#8884d8" name="Total Volume (lbs)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Muscle Group Frequency Chart */}
        <div className="chart-card">
          <h2>Muscle Group Frequency (30 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={muscleGroupFrequency}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="muscle_group" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#82ca9d" name="Exercise Count" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Muscle Group Distribution Pie Chart */}
        {muscleGroupFrequency.length > 0 && (
          <div className="chart-card">
            <h2>Muscle Group Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={muscleGroupFrequency}
                  dataKey="count"
                  nameKey="muscle_group"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {muscleGroupFrequency.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Personal Records */}
      <section className="personal-records">
        <div className="section-header">
          <h2>Recent Personal Records</h2>
          <Link to="/analytics/personal-records" className="btn btn-secondary">
            View All PRs
          </Link>
        </div>
        {personalRecords.length > 0 ? (
          <div className="pr-grid">
            {personalRecords.slice(0, 6).map((pr) => (
              <div key={pr.id} className="pr-card">
                <h3>{pr.exercise_name}</h3>
                <p className="pr-type">{pr.record_type_display}</p>
                <p className="pr-value">{pr.value}</p>
                <p className="pr-date">{new Date(pr.date_achieved).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>No personal records yet. Start tracking your progress!</p>
        )}
      </section>

      {/* Quick Links */}
      <section className="quick-links">
        <Link to="/analytics/exercise-progress" className="quick-link-card">
          <h3>Exercise Progress</h3>
          <p>Track progress for specific exercises over time</p>
        </Link>
        <Link to="/analytics/body-metrics" className="quick-link-card">
          <h3>Body Metrics</h3>
          <p>View weight, body fat, and measurements history</p>
        </Link>
      </section>
    </div>
  );
}

export default Analytics;
