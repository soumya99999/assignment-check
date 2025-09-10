<script lang="ts">
  import { goto } from '$lib/stores/navigation';
  import { registerUser } from '$lib/utils/auth';
  import type { RegisterForm as RegisterFormType } from '$lib/types/auth';
  import RegisterForm from '$lib/components/auth/register/RegisterForm.svelte';
  import ErrorAlert from '$lib/components/auth/register/ErrorAlert.svelte';
  import StudentLoader from '$lib/components/ui/StudentLoader.svelte';

  let form: RegisterFormType = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    role: '',
    password: '',
    password2: '',
    regdno: ''
  };
  let error: string | null = null;
  let loading = false;

  async function handleSubmit() {
    try {
      const formData = new FormData();
      Object.entries(form).forEach(([key, value]) => {
        formData.append(key, value);
      });

      await registerUser(formData);
      await goto('/login');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Registration failed';
    }
  }

  function handleTitleClick(event: MouseEvent | KeyboardEvent) {
    if (
      event.type === 'click' ||
      (event instanceof KeyboardEvent && ['Enter', ' '].includes(event.key))
    ) {
      goto('/');
    }
  }

  async function handleLoginClick(event: Event) {
    event.preventDefault();
    // No need to set loading state manually as our navigation store handles it
    await goto('/login');
  }

</script>

<div class="grid h-screen md:grid-cols-2 bg-white/80 backdrop-blur-md overflow-hidden w-full">
  <!-- Left illustration -->
  <div class="hidden md:flex items-center justify-center rounded-tl-2xl rounded-bl-2xl overflow-hidden">
    <img src="/assets/reading.svg" alt="Reading" class="object-contain w-full h-full" />
  </div>

  <!-- Right form -->
  <div class="flex flex-col items-center justify-center p-12 rounded-tr-2xl rounded-br-2xl overflow-hidden hide-scrollbar" style="overflow-y: auto; max-height: 100vh;">
    <div
      class="w-full max-w-lg rounded-2xl bg-[#f4f6f8] p-12 text-lg hide-scrollbar
             shadow-[10px_10px_20px_#c9c9c9,-10px_-10px_20px_#ffffff]"
      style="max-height: 80vh; overflow-y: auto;"
    >
      <button
        type="button"
        class="mb-8 w-full text-center text-3xl font-bold text-indigo-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 rounded-xl px-4 py-3"
        on:click={handleTitleClick}
        on:keydown={handleTitleClick}
      >
        Create Account ✨
      </button>

      <ErrorAlert {error} />

      <RegisterForm {form} {handleSubmit} />

      <p class="mt-6 text-center text-sm text-gray-700">
        Already have an account?
        <a href="/login" on:click={handleLoginClick} class="font-medium text-indigo-700 hover:underline">Login</a>
      </p>

      {#if loading}
        <StudentLoader />
      {/if}
    </div>
  </div>
</div>

<style>
  .hide-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }
  .hide-scrollbar::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
  }
</style>
