// src/utils/errorHandler.js
export function handleError(error) {
  if (error.response) {
    console.error('Server responded with an error:', error.response);
  } else if (error.request) {
    console.error('No response received:', error.request);
  } else {
    console.error('Error setting up request:', error.message);
  }
}
