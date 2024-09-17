// src/msalConfig.js
import { PublicClientApplication } from "@azure/msal-browser";

const msalConfig = {
  auth: {
    clientId: process.env.REACT_APP_CLIENT_ID,
    authority: "https://login.microsoftonline.com/common",
    redirectUri: process.env.REACT_APP_REDIRECT_URI,
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
};

export const loginRequest = {
  scopes: ["openid", "profile", "email"]
};

export const msalInstance = new PublicClientApplication(msalConfig);

// Call initialize before exporting
msalInstance.initialize().then(() => {
  // Initialize success
  console.log("MSAL initialized successfully");
}).catch((error) => {
  console.error("MSAL initialization fails", error);
});

export default msalConfig;