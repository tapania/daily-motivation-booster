// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useIsAuthenticated } from "@azure/msal-react";
import Login from './components/Login';
import AuthCallback from './components/AuthCallback';
import PreferencesForm from './components/PreferencesForm';
import PublicSpeeches from './components/PublicSpeeches';
import ErrorBoundary from './components/ErrorBoundary';
import Footer from './components/Footer';
import API from './api';

function App() {
  const isAuthenticated = useIsAuthenticated();

  const handleLogout = async () => {
    try {
      await API.get('/logout');
      // Redirect to home page or refresh the page to update auth state
      window.location.href = '/';
    } catch (error) {
      console.error("Logout failed", error);
    }
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
              <Route path="/auth/callback" element={<AuthCallback />} />
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