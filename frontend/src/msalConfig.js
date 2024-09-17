// src/msalConfig.js
const msalConfig = {
  auth: {
    clientId: process.env.REACT_APP_CLIENT_ID,
    redirectUri: process.env.REACT_APP_REDIRECT_URI,
  },
};

export default msalConfig;
