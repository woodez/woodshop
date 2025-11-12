import api from './api';

/**
 * Service for workout-related API calls
 */

// Exercise endpoints
export const exerciseService = {
  getAll: (params = {}) => api.get('/exercises/', { params }),
  getById: (id) => api.get(`/exercises/${id}/`),
  create: (data) => api.post('/exercises/', data),
  update: (id, data) => api.patch(`/exercises/${id}/`, data),
  delete: (id) => api.delete(`/exercises/${id}/`),
  search: (query) => api.get('/exercises/', { params: { search: query } }),
};

// Muscle group endpoints
export const muscleGroupService = {
  getAll: () => api.get('/muscle-groups/'),
  getById: (id) => api.get(`/muscle-groups/${id}/`),
};

// Workout endpoints
export const workoutService = {
  getAll: (params = {}) => api.get('/workouts/', { params }),
  getById: (id) => api.get(`/workouts/${id}/`),
  create: (data) => api.post('/workouts/', data),
  update: (id, data) => api.patch(`/workouts/${id}/`, data),
  delete: (id) => api.delete(`/workouts/${id}/`),
  complete: (id) => api.post(`/workouts/${id}/complete/`),
  getToday: () => api.get('/workouts/today/'),
};

// Workout exercise endpoints
export const workoutExerciseService = {
  getAll: (params = {}) => api.get('/workout-exercises/', { params }),
  getById: (id) => api.get(`/workout-exercises/${id}/`),
  create: (data) => api.post('/workout-exercises/', data),
  update: (id, data) => api.patch(`/workout-exercises/${id}/`, data),
  delete: (id) => api.delete(`/workout-exercises/${id}/`),
};

// Set endpoints
export const setService = {
  getAll: (params = {}) => api.get('/sets/', { params }),
  getById: (id) => api.get(`/sets/${id}/`),
  create: (data) => api.post('/sets/', data),
  update: (id, data) => api.patch(`/sets/${id}/`, data),
  delete: (id) => api.delete(`/sets/${id}/`),
};
