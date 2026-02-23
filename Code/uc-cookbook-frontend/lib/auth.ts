// Auth helper utilities
'use client';

import { useState, useEffect } from 'react';
import type { User } from './types';

// Client-side auth state management
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user data exists in localStorage
    const loadUser = () => {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (error) {
          console.error('Failed to parse user data:', error);
          localStorage.removeItem('user');
        }
      }
      setLoading(false);
    };

    loadUser();

    // Listen for auth state changes from other components
    const handleAuthChange = (event: CustomEvent) => {
      setUser(event.detail);
      setLoading(false);
    };

    window.addEventListener('authStateChanged', handleAuthChange as EventListener);
    
    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange as EventListener);
    };
  }, []);

  const setAuthUser = (userData: User | null) => {
    setUser(userData);
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData));
      // Dispatch custom event to notify all components of auth state change
      window.dispatchEvent(new CustomEvent('authStateChanged', { detail: userData }));
    } else {
      localStorage.removeItem('user');
      window.dispatchEvent(new CustomEvent('authStateChanged', { detail: null }));
    }
  };

  return {
    user,
    setUser: setAuthUser,
    isAuthenticated: !!user,
    loading,
  };
}
