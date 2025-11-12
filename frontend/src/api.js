import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
});
export const getSchedule = () => api.get('/api/schedule');
export const sendMessage = (message) => api.post('/api/chat', { message });