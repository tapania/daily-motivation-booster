// frontend/src/api.js
import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL, // e.g., "https://your-backend-domain.com"
  withCredentials: true, // Include cookies in requests
});

export default API;
