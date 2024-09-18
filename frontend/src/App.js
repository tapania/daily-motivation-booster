// frontend/src/App.js
import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PreferencesForm from './components/PreferencesForm';
import PublicSpeeches from './components/PublicSpeeches';
import ErrorBoundary from './components/ErrorBoundary';
import Footer from './components/Footer';
import API from './api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication status
    const checkAuth = async () => {
      try {
        const response = await API.get('/me');
        setUser(response.data);
        setIsAuthenticated(true);
      } catch (error) {
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = () => {
    window.location.href = `${process.env.REACT_APP_BACKEND_URL}/login`;
  };

  const handleLogout = async () => {
    try {
      await API.get('/logout');
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

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
                      <button
                        onClick={handleLogin}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                      >
                        Login with Microsoft
                      </button>
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
