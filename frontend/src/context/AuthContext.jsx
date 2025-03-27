import React, { createContext, useState, useEffect, useContext } from 'react';
import { customerService } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is logged in on app load
  useEffect(() => {
    const checkLoggedIn = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          // Get user profile
          const response = await customerService.getProfile();
          setCurrentUser(response.data);
        } catch (err) {
          // If error, clear token
          localStorage.removeItem('token');
          setError('Session expired. Please login again.');
        }
      }
      
      setLoading(false);
    };
    
    checkLoggedIn();
  }, []);

  // Login function
  const login = async (credentials) => {
    try {
      const response = await customerService.login(credentials);
      localStorage.setItem('token', response.data.token);
      setCurrentUser(response.data);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
  };

  // Register function
  const register = async (userData) => {
    try {
      const response = await customerService.register(userData);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const value = {
    currentUser,
    loading,
    error,
    login,
    logout,
    register
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook for using the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};