// src/components/Login.js
import React from 'react';
import { useMsal } from "@azure/msal-react";

function Login() {
  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginRedirect();
  };

  return (
    <button
      onClick={handleLogin}
      className="btn btn-primary"
    >
      Sign in with Microsoft
    </button>
  );
}

export default Login;
