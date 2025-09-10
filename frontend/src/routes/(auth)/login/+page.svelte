<script lang="ts">
  import { goto } from '$lib/stores/navigation';
  import { loginUser } from '$lib/utils/auth';
  import type { LoginForm } from '$lib/types/auth';
  import { getAccessToken } from '$lib/stores/auth';
  import { onMount } from 'svelte';
  import StudentLoader from '$lib/components/ui/StudentLoader.svelte';

  let form: LoginForm = {
    username: '',
    password: ''
  };
  let error: string | null = null;
  let loading = false;

  async function handleSubmit() {
    try {
      const formData = new FormData();
      Object.entries(form).forEach(([key, value]) => {
        formData.append(key, value);
      });

      const data = await loginUser(formData);
      // Redirect based on role
      if (data && data.access) {
        // Decode JWT to get role
        const payload = JSON.parse(atob(data.access.split('.')[1]));
        if (payload.role === 'student') {
          await goto('/student/dashboard');
        } else if (payload.role === 'teacher') {
          await goto('/teacher/dashboard');
        } else {
          await goto('/dashboard');
        }
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Login failed';
    }
  }

  // Optional: redirect if already logged in
  onMount(() => {
    const token = getAccessToken();
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.role === 'student') {
        goto('/student/dashboard');
      } else if (payload.role === 'teacher') {
        goto('/teacher/dashboard');
      }
    }
  });

  async function handleRegisterClick(event: Event) {
    event.preventDefault();
    // No need to set loading state manually as our navigation store handles it
    await goto('/register');
  }
</script>

<div class="grid h-screen md:grid-cols-2 bg-white/80 backdrop-blur-md overflow-hidden w-full">
  <!-- Illustration side -->
  <div class="hidden md:flex items-center justify-center rounded-tl-2xl rounded-bl-2xl overflow-hidden">
    <img src="/assets/reading.svg" alt="Reading" class="object-contain w-full h-full" />
  </div>

  <!-- Form side -->
  <div class="flex flex-col items-center justify-center p-12 rounded-tr-2xl rounded-br-2xl">
    <div
      class="w-full max-w-md rounded-2xl bg-[#f4f6f8] p-12 text-lg
             shadow-[10px_10px_20px_#c9c9c9,-10px_-10px_20px_#ffffff]"
    >
      <h1 class="mb-8 text-center text-3xl font-bold text-indigo-800">Welcome Back 👋</h1>

      {#if error}
        <div
          class="mb-4 rounded-md p-3 text-sm text-red-700 bg-[#fde8e8] shadow-[inset_4px_4px_8px_#d1d1d1,inset_-4px_-4px_8px_#ffffff]"
        >
          {error}
        </div>
      {/if}

      {#if loading}
        <StudentLoader />
      {/if}

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Username</label>
          <input
            type="text"
            id="username"
            placeholder="Enter your username"
            bind:value={form.username}
            required
            class="w-full rounded-xl px-4 py-3 text-sm outline-none border-none bg-[#f4f6f8]
                   shadow-[inset_5px_5px_10px_#d1d1d1,inset_-5px_-5px_10px_#ffffff]
                   focus:shadow-[inset_3px_3px_6px_#c1c1c1,inset_-3px_-3px_6px_#ffffff]"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            bind:value={form.password}
            required
            class="w-full rounded-xl px-4 py-3 text-sm outline-none border-none bg-[#f4f6f8]
                   shadow-[inset_5px_5px_10px_#d1d1d1,inset_-5px_-5px_10px_#ffffff]
                   focus:shadow-[inset_3px_3px_6px_#c1c1c1,inset_-3px_-3px_6px_#ffffff]"
          />
        </div>

        <!-- Circular FAB login button -->
        <div class="flex justify-center">
          <button
            type="submit"
            class="flex h-14 w-14 items-center justify-center rounded-full cursor-pointer
                   bg-[#f4f6f8] text-indigo-800
                   shadow-[6px_6px_12px_#c9c9c9,-6px_-6px_12px_#ffffff]
                   hover:shadow-[inset_6px_6px_12px_#c9c9c9,inset_-6px_-6px_12px_#ffffff]
                   transition"
            aria-label="Login"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </form>

      {#if loading}
        <StudentLoader />
      {:else}
        <p class="mt-6 text-center text-sm text-gray-700">
          New here?  
          <a href="/register" on:click={handleRegisterClick} class="font-medium text-indigo-700 hover:underline">Create an account</a>
        </p>
      {/if}
    </div>
  </div>
</div>
