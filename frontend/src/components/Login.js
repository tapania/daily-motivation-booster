// src/components/Login.js
import React, { useEffect } from 'react';
import pkceChallenge from 'pkce-challenge';

function Login() {
  useEffect(() => {
    const { code_verifier, code_challenge } = pkceChallenge();
    localStorage.setItem('pkce_verifier', code_verifier);
    localStorage.setItem('pkce_challenge', code_challenge);
  }, []);

  const handleLogin = () => {
    const challenge = localStorage.getItem('pkce_challenge');
    const clientId = process.env.REACT_APP_CLIENT_ID;
    const redirectUri = encodeURIComponent(`${window.location.origin}/auth/callback`);
    const scope = encodeURIComponent('openid profile email');
    const responseType = 'code';
    const responseMode = 'query';
    const challengeMethod = 'S256';

    const url = `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=${clientId}&response_type=${responseType}&redirect_uri=${redirectUri}&response_mode=${responseMode}&scope=${scope}&code_challenge=${challenge}&code_challenge_method=${challengeMethod}`;

    window.location.href = url;
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