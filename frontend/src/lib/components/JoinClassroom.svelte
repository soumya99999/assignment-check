<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { getAccessToken } from '$lib/stores/auth';
  import { onMount } from 'svelte';

  const dispatch = createEventDispatcher();

  let code = '';
  let error: string | null = null;
  let loading = false;

  async function joinClassroom() {
    error = null;
    if (!code.trim()) {
      error = 'Classroom code is required';
      return;
    }

    loading = true;
    try {
      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch('/api/join-classroom', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code.trim() })
      });

      const data = await response.json();

      if (!response.ok) {
        error = data.error || 'Failed to join classroom';
      } else {
        dispatch('joined', { classroom: data.classroom });
        code = '';
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Unexpected error occurred';
    } finally {
      loading = false;
    }
  }
</script>

<div class="p-4">
  <label for="code" class="block text-sm font-medium text-gray-700 mb-1">Classroom Code</label>
  <input
    id="code"
    type="text"
    bind:value={code}
    placeholder="Enter classroom code"
    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
  />
  {#if error}
    <p class="text-red-600 text-sm mt-1">{error}</p>
  {/if}
  <button
    on:click={joinClassroom}
    disabled={loading}
    class="mt-3 w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
  >
    {#if loading}
      Joining...
    {:else}
      Join Classroom
    {/if}
  </button>
</div>
