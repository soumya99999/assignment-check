<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import type { Classroom } from '$lib/types/classroom';

  const dispatch = createEventDispatcher<{ close: void }>();

  export let classroom: Classroom;

  function handleClose() {
    dispatch('close');
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Copied to clipboard:', text);
    });
  }

  // Handle keyboard events for both Escape and Enter/Space
  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') {
      handleClose();
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });
</script>

<!-- Backdrop -->
<button
  type="button"
  aria-label="Close modal"
  on:click={handleClose}
  on:keydown={handleKeydown} 
  class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-40"
></button>

<!-- Modal -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  tabindex="0" 
  class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white z-50"
  on:click|stopPropagation
>
  <div class="mt-3">
    <!-- Success Icon -->
    <div class="flex items-center justify-center mb-4">
      <div class="flex items-center justify-center w-12 h-12 bg-green-100 rounded-full">
        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
    </div>

    <!-- Title -->
    <h3 id="modal-title" class="text-lg font-medium text-gray-900 text-center mb-2">
      Classroom Created Successfully!
    </h3>

    <!-- Classroom Info -->
    <div class="mb-4">
      <p class="text-sm text-gray-600 text-center mb-4">
        Your classroom <strong>{classroom.name}</strong> has been created.
      </p>

      <!-- Join Code Section -->
      <div class="bg-gray-50 rounded-lg p-4 mb-4">
        <p class="text-sm text-gray-700 mb-2">Share this join code with your students:</p>
        <div class="flex items-center justify-between bg-white rounded border p-3">
          <span class="text-lg font-mono font-bold text-indigo-600">{classroom.code}</span>
          <button
            type="button"
            aria-label="Copy join code to clipboard"
            on:click={() => copyToClipboard(classroom.code)}
            class="ml-3 text-indigo-600 hover:text-indigo-800 p-1"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-center">
      <button
        type="button"
        on:click={handleClose}
        class="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200"
      >
        Got it!
      </button>
    </div>
  </div>
</div>