<script lang="ts">
  import type { RegisterForm } from '$lib/types/auth';
  import FormInput from './FormInput.svelte';
  import NeumorphicSelect from './NeumorphicSelect.svelte';

  export let form: RegisterForm;
  export let handleSubmit: () => void;
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4 relative">
  <FormInput label="Username" type="text" id="username" placeholder="Choose a username" bind:value={form.username} required />
  <FormInput label="Email" type="email" id="email" placeholder="Your email address" bind:value={form.email} required />
  <FormInput label="First Name" type="text" id="first_name" placeholder="Enter first name" bind:value={form.first_name} required />
  <FormInput label="Last Name" type="text" id="last_name" placeholder="Enter last name" bind:value={form.last_name} required />
  <NeumorphicSelect
    id="role"
    bind:selected={form.role}
    required={true}
    options={[
      { value: 'student', label: 'Student' },
      { value: 'teacher', label: 'Teacher' }
    ]}
  />
  {#if form.role === 'student'}
    <FormInput label="Registration Number" type="text" id="regdno" placeholder="Enter registration number" bind:value={form.regdno} required />
  {/if}
  <FormInput label="Password" type="password" id="password" placeholder="Create a password" bind:value={form.password} required />
  <FormInput label="Confirm Password" type="password" id="password2" placeholder="Confirm your password" bind:value={form.password2} required />

  <!-- FAB (Register button) -->
  <div class="flex justify-center mt-6">
    <button
      type="submit"
      class="flex items-center justify-center h-14 w-14 rounded-full cursor-pointer
             bg-[#f4f6f8] text-indigo-800 font-bold text-lg
             shadow-[6px_6px_12px_#c9c9c9,-6px_-6px_12px_#ffffff]
             hover:shadow-[inset_6px_6px_12px_#c9c9c9,inset_-6px_-6px_12px_#ffffff]
             transition"
      aria-label="Register"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </button>
  </div>
</form>
