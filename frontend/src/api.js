import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export const login = (username, password) =>
  api.post('/auth/login', { username, password });

export const getMe = () => api.get('/auth/me');

export const getProducts = (page = 1, limit = 10, category) =>
  api.get('/products', { params: { page, limit, category } });

export const getProduct = id => api.get(`/products/${id}`);

export const createProduct = data => api.post('/products', data);

export const deleteProduct = id => api.delete(`/products/${id}`);

export const getSlowReport = () => api.get('/products/report/slow');

export const getHealth = () => api.get('/health');

export default api;
