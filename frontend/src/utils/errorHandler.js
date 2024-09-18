// frontend/src/utils/errorHandler.js
import { toast } from 'react-toastify'; // You can use a library like react-toastify for notifications

export function handleError(error) {
  if (error.response) {
    console.error('Server responded with an error:', error.response);
    if (error.response.status === 401) {
      toast.error('Session expired. Please log in again.');
    } else {
      toast.error(`Error: ${error.response.data.detail || 'An error occurred.'}`);
    }
  } else if (error.request) {
    console.error('No response received:', error.request);
    toast.error('No response from server. Please try again later.');
  } else {
    console.error('Error setting up request:', error.message);
    toast.error(`Error: ${error.message}`);
  }
}
