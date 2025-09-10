import { writable } from 'svelte/store';

export const currentPath = writable<string>(typeof window !== 'undefined' ? window.location.pathname : '/');

// Update on popstate (browser back/forward)
if (typeof window !== 'undefined') {
  window.addEventListener('popstate', () => {
    currentPath.set(window.location.pathname);
  });
}
