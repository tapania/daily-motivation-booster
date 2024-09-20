// frontend/src/App.js
import React, { useContext, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import PreferencesForm from './components/PreferencesForm';
import PublicSpeeches from './components/PublicSpeeches';
import MySpeeches from './components/MySpeeches';
import ErrorBoundary from './components/ErrorBoundary';
import Footer from './components/Footer';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import SpeechDetail from './components/SpeechDetail';
import { AuthContext } from './context/AuthContext';
import { handleError } from './utils/errorHandler';
import API, { setLogoutFunction } from './api';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const { isAuthenticated, user, logout, isLoading } = useContext(AuthContext);

  useEffect(() => {
    // Set the logout handler in API interceptors
    setLogoutFunction(logout);
  }, [logout]);

  if (isLoading) {
    return <div className="text-center mt-10">Loading...</div>;
  }

  return (
    <Router>
      <ErrorBoundary>
        <div className="flex flex-col min-h-screen">
          <Header isAuthenticated={isAuthenticated} handleLogout={logout} />
          <div className="container mx-auto px-4 flex-grow">
            <Routes>
              {/* Root Path: LandingPage for unauthenticated, PublicSpeeches for authenticated */}
              <Route
                path="/"
                element={
                  isAuthenticated ? <PublicSpeeches /> : <LandingPage />
                }
              />
              <Route
                path="/public_speeches"
                element={<PublicSpeeches />}
              />
              <Route
                path="/public_speeches/:id"
                element={<SpeechDetail type="public" />}
              />
              <Route
                path="/my_speeches"
                element={
                  isAuthenticated ? (
                    <MySpeeches />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route
                path="/my_speeches/:id"
                element={
                  isAuthenticated ? (
                    <SpeechDetail type="private" />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route
                path="/settings"
                element={
                  isAuthenticated ? (
                    <PreferencesForm />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
          <Footer />
        </div>
      </ErrorBoundary>
      <ToastContainer />
    </Router>
  );
}

export default App;