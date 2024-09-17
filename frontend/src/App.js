// src/App.js
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { msalInstance } from './msalConfig';
import Login from './components/Login';
import PreferencesForm from './components/PreferencesForm';
import PublicSpeeches from './components/PublicSpeeches';
import ErrorBoundary from './components/ErrorBoundary';
import Footer from './components/Footer';
import API from './api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const handleRedirect = async () => {
      try {
        await msalInstance.handleRedirectPromise();
        const account = msalInstance.getActiveAccount();
        if (account) {
          setIsAuthenticated(true);
          // You might want to call your backend here to exchange the token
          // const response = await API.post('/process_token', { idToken: account.idToken });
          // console.log('Authentication successful:', response.data);
        }
      } catch (error) {
        console.error("Error during redirect handling:", error);
      }
    };

    handleRedirect();
  }, []);

  const handleLogout = async () => {
    await msalInstance.logoutRedirect();
  };

  return (
    <Router>
      <ErrorBoundary>
        <div className="flex flex-col min-h-screen">
          <div className="container mx-auto px-4 flex-grow">
            <div className="my-8 text-center">
              <h1 className="text-4xl font-bold">Welcome to the Motivational Speech App</h1>
              <p className="mt-4 text-lg">
                Generate personalized motivational speeches to inspire you every day.
              </p>
            </div>

            <Routes>
              <Route path="/" element={
                isAuthenticated ? (
                  <>
                    <div className="flex justify-end mb-4">
                      <button 
                        onClick={handleLogout}
                        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                      >
                        Logout
                      </button>
                    </div>
                    <PreferencesForm />
                  </>
                ) : (
                  <>
                    <div className="flex justify-center my-4">
                      <Login />
                    </div>
                    <PublicSpeeches />
                  </>
                )
              } />
            </Routes>
          </div>
          <Footer />
        </div>
      </ErrorBoundary>
    </Router>
  );
}

export default App;