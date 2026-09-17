import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear auth state
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  refresh: (data) => api.post('/auth/refresh', data),
  getProfile: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/me', data),
};

// Commodities API
export const commoditiesAPI = {
  list: (params) => api.get('/commodities/', { params }),
  get: (id) => api.get(`/commodities/${id}`),
  create: (data) => api.post('/commodities/', data),
  update: (id, data) => api.put(`/commodities/${id}`, data),
  delete: (id) => api.delete(`/commodities/${id}`),
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/commodities/upload-csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getPriceHistory: (name, days) =>
    api.get(`/commodities/price-history/${name}`, { params: { days } }),
  getDashboardSummary: () => api.get('/commodities/dashboard/summary'),
};

// Sensors API
export const sensorsAPI = {
  create: (data) => api.post('/sensors/', data),
  list: (params) => api.get('/sensors/', { params }),
  getLatest: (limit) => api.get('/sensors/latest', { params: { limit } }),
  getTruckLocations: () => api.get('/sensors/trucks/locations'),
  getTruckStats: (truckId, days) =>
    api.get(`/sensors/stats/${truckId}`, { params: { days } }),
};

// Alerts API
export const alertsAPI = {
  list: (params) => api.get('/alerts/', { params }),
  getUnreadCount: () => api.get('/alerts/unread-count'),
  update: (id, data) => api.put(`/alerts/${id}`, data),
  markAllRead: () => api.put('/alerts/mark-all-read'),
};

export default api;
