// Auth helper utilities
'use client';

import { useState, useEffect } from 'react';
import type { User } from './types';
import { getStoredUser, clearAuthStorage } from './api';

// Client-side auth state management
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Listen for auth state changes from other components
    const handleAuthChange = (event: CustomEvent) => {
      setUser(event.detail);
      setLoading(false);
    };

    window.addEventListener('authStateChanged', handleAuthChange as EventListener);

    // Hydrate from localStorage for immediate UX
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
    }
    setLoading(false);

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
      clearAuthStorage();
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
