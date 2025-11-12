import api from './api';

// Personal Records Service
export const personalRecordService = {
  getAll: (params = {}) => api.get('/personal-records/', { params }),
  getById: (id) => api.get(`/personal-records/${id}/`),
  create: (data) => api.post('/personal-records/', data),
  update: (id, data) => api.put(`/personal-records/${id}/`, data),
  delete: (id) => api.delete(`/personal-records/${id}/`),
  getByExercise: (exerciseId) => api.get(`/personal-records/by_exercise/`, { params: { exercise_id: exerciseId } }),
};

// Progress Snapshots Service
export const progressSnapshotService = {
  getAll: (params = {}) => api.get('/progress-snapshots/', { params }),
  getById: (id) => api.get(`/progress-snapshots/${id}/`),
  create: (data) => api.post('/progress-snapshots/', data),
  update: (id, data) => api.put(`/progress-snapshots/${id}/`, data),
  delete: (id) => api.delete(`/progress-snapshots/${id}/`),
  getLatest: () => api.get('/progress-snapshots/latest/'),
};

// Analytics Service
export const analyticsService = {
  // Get exercise progress over time
  getExerciseProgress: (exerciseId, params = {}) =>
    api.get('/analytics/exercise_progress/', {
      params: { exercise_id: exerciseId, ...params }
    }),

  // Get overall workout statistics
  getWorkoutStats: () => api.get('/analytics/workout_stats/'),

  // Get volume trend (weekly)
  getVolumeTrend: (params = {}) =>
    api.get('/analytics/volume_trend/', { params }),

  // Get frequency by muscle group
  getFrequencyByMuscleGroup: (params = {}) =>
    api.get('/analytics/frequency_by_muscle_group/', { params }),
};

export default {
  personalRecordService,
  progressSnapshotService,
  analyticsService,
};
