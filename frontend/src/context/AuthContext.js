// frontend/src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import API from '../api';
import { handleError } from '../utils/errorHandler';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Function to fetch current user
  const fetchCurrentUser = async () => {
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

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  // Logout function
  const logout = async () => {
    try {
      await API.get('/logout');
    } catch (error) {
      console.error("Error during logout:", error);
    } finally {
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
