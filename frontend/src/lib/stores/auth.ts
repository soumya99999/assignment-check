import { writable } from 'svelte/store';
import type { User } from '$lib/types/auth';
import { goto } from '$lib/stores/navigation';

const accessToken = writable<string | null>(null);
const user = writable<User | null>(null);

// Initialize token and user data from localStorage on app start
if (typeof window !== 'undefined') {
  const storedToken = localStorage.getItem('access_token');
  if (storedToken) {
    accessToken.set(storedToken);
  }

  const storedUser = localStorage.getItem('user_data');
  if (storedUser) {
    try {
      const userData = JSON.parse(storedUser);
      user.set(userData);
    } catch (e) {
      console.error('Failed to parse stored user data:', e);
      localStorage.removeItem('user_data');
    }
  }
}

export function setAccessToken(token: string): void {
  accessToken.set(token);
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
}

export function getAccessToken(): string | null {
  let token: string | null = null;
  accessToken.subscribe((value) => (token = value))();
  return token;
}

export function clearAccessToken(): void {
  accessToken.set(null);
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
}

export function setUser(userData: User): void {
  user.set(userData);
  if (typeof window !== 'undefined') {
    localStorage.setItem('user_data', JSON.stringify(userData));
  }
}

export function getUser(): User | null {
  let userData: User | null = null;
  user.subscribe((value) => (userData = value))();
  return userData;
}

export function clearUser(): void {
  user.set(null);
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user_data');
  }
}

export function logout(): void {
  clearAccessToken();
  clearUser();
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_data');
  goto('/login');
}

export { user };
