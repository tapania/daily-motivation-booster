// src/components/Login.js
import React from 'react';
import { msalInstance, loginRequest } from '../msalConfig';

function Login() {
  const handleLogin = async () => {
    try {
      await msalInstance.loginRedirect(loginRequest);
    } catch (error) {
      console.error("Error during login", error);
    }
  };

  return (
    <button
      onClick={handleLogin}
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Login with Microsoft
    </button>
  );
}

export default Login;