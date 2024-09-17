// src/components/AuthCallback.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

function AuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      const hash = window.location.hash.substring(1);
      const params = new URLSearchParams(hash);
      const code = params.get('code');

      if (code) {
        try {
          const response = await API.post('/process_token', { code });
          // Assuming the backend returns a success message or user data
          console.log('Authentication successful:', response.data);
          // Redirect to the main page or dashboard
          navigate('/');
        } catch (error) {
          console.error('Authentication error:', error);
          // Redirect to login page or show an error message
          navigate('/login');
        }
      } else {
        console.error('No code found in URL');
        navigate('/login');
      }
    };

    handleCallback();
  }, [navigate]);

  return <div>Processing authentication...</div>;
}

export default AuthCallback;