import { goto } from '$lib/stores/navigation';

// Handle client-side navigation and authentication
export async function handleError({ error }: { error: App.Error }) {
  // Log errors in development
  if (import.meta.env.DEV) {
    console.error('Client error:', error);
  }

  // Handle authentication errors
  if (error?.status === 401 || error?.status === 403) {
    // Clear any stored tokens
    localStorage.removeItem('refresh_token');
    // Redirect to login
    await goto('/login');
    return;
  }
}

// Handle session management
export function initAuth() {
  // Check for stored tokens on app start
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    // No token, redirect to login if not already there
    const currentPath = window.location.pathname;
    if (!currentPath.includes('/login') && !currentPath.includes('/register')) {
      goto('/login');
    }
  }
}

// Initialize auth on client start
initAuth();
