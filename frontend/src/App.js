// src/App.js
import React from 'react';
import { useIsAuthenticated } from "@azure/msal-react";
import Login from './components/Login';
import PreferencesForm from './components/PreferencesForm';
import PublicSpeeches from './components/PublicSpeeches';
import ErrorBoundary from './components/ErrorBoundary';
import Footer from './components/Footer';

function App() {
  const isAuthenticated = useIsAuthenticated();

  return (
    <ErrorBoundary>
      <div className="flex flex-col min-h-screen">
        <div className="container mx-auto px-4 flex-grow">
          <div className="my-8 text-center">
            <h1 className="text-4xl font-bold">Welcome to the Motivational Speech App</h1>
            <p className="mt-4 text-lg">
              Generate personalized motivational speeches to inspire you every day.
            </p>
          </div>

          {isAuthenticated ? (
            <PreferencesForm />
          ) : (
            <>
              <div className="flex justify-center my-4">
                <Login />
              </div>
              <PublicSpeeches />
            </>
          )}
        </div>
        <Footer />
      </div>
    </ErrorBoundary>
  );
}

export default App;
