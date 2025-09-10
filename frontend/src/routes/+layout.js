import { browser } from '$app/environment';
import { getAccessToken } from '$lib/stores/auth';
import { refreshAccessToken } from '$lib/utils/auth';
import { redirect } from '@sveltejs/kit';

export async function load({ url }) {
  if (!browser) {
    return {};
  }

  const protectedRoutes = ['/dashboard'];
  const currentPath = url.pathname;

  if (protectedRoutes.includes(currentPath)) {
    const token = getAccessToken();
    if (!token) {
      try {
        await refreshAccessToken();
      } catch {
        throw redirect(302, '/login');
      }
    }
  }

  return {};
}
