import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // Load env variables
  const env = loadEnv(mode, process.cwd(), '');
  const backendUrl = env.PUBLIC_BACKEND_URL || 'http://localhost:8000';
  
  return {
		plugins: [tailwindcss(), sveltekit()],
		server: {
			proxy: {
				'/api': {
					target: backendUrl,
					changeOrigin: true,
					secure: false
				}
			}
		}
  };
});
