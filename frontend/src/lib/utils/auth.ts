import type { AuthResponse, User } from '$lib/types/auth';
import { setAccessToken, setUser, getAccessToken} from '$lib/stores/auth';


export function storeTokens({ access, refresh }: AuthResponse): void {
  setAccessToken(access);
  localStorage.setItem('refresh_token', refresh);
}

export async function registerUser(formData: FormData): Promise<void> {
  const response = await fetch('/api/register', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  return await response.json();
}

export async function loginUser(formData: FormData): Promise<AuthResponse> {
  const response = await fetch('/api/login', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const data: AuthResponse = await response.json();
  storeTokens(data);

  // Fetch user data after login
  await fetchUserData();

  return data;
}

export async function refreshAccessToken(): Promise<void> {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await fetch('/api/token/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh: refreshToken })
  });

  if (!response.ok) {
    throw new Error('Failed to refresh access token');
  }

  const data: AuthResponse = await response.json();
  setAccessToken(data.access);
}

export async function fetchUserData(): Promise<void> {
  const token = getAccessToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const response = await fetch('/api/user', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user data');
  }

  const userData: User = await response.json();
  // show user data
  console.log(userData);
  setUser(userData);
}
