// frontend/src/api.js
import axios from 'axios';

// Create an Axios instance
const API = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL, // e.g., "https://your-backend-domain.com"
  withCredentials: true, // Include cookies in requests
});

// Function to set the logout handler
let logoutFunction = () => {};

export const setLogoutFunction = (fn) => {
  logoutFunction = fn;
};

// Add a response interceptor
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Unauthorized, trigger logout
      logoutFunction();
    }
    return Promise.reject(error);
  }
);

export default API;