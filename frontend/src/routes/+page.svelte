<script lang="ts">
  import { getAccessToken } from '$lib/stores/auth';
  import { goto } from '$lib/stores/navigation';

  function handleDashboard() {
    if (getAccessToken()) {
      goto('/dashboard');
    } else {
      goto('/login');
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-blue-200">
  <div class="card w-full max-w-md bg-white shadow-lg rounded-lg p-8 text-center">
    <h1 class="text-3xl font-bold mb-6">Welcome to the App</h1>
    <p class="mb-4">Please log in or register to continue.</p>
    <div class="space-y-4">
      <a href="/login" class="btn btn-primary w-full rounded-md">Login</a>
      <a href="/register" class="btn btn-secondary w-full rounded-md">Register</a>
      <button on:click={handleDashboard} class="btn btn-outline w-full rounded-md">
        Go to Dashboard
      </button>
    </div>
  </div>
</div>