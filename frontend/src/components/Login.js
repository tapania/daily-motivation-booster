// src/components/Login.js
import React from 'react';

function Login() {
  const handleLogin = () => {
    window.location.href = `${process.env.REACT_APP_BACKEND_URL}/login`;
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