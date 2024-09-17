// src/components/AuthCallback.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

function AuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const error = urlParams.get('error');

      if (error) {
        console.error('Authentication error:', error);
        navigate('/login');
        return;
      }

      if (code) {
        try {
          const verifier = localStorage.getItem('pkce_verifier');
          if (!verifier) {
            throw new Error('PKCE verifier not found');
          }

          const response = await API.post('/process_token', { code, code_verifier: verifier });
          console.log('Authentication successful:', response.data);
          localStorage.removeItem('pkce_verifier'); // Clean up
          navigate('/');
        } catch (error) {
          console.error('Authentication error:', error);
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