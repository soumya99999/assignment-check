<script lang="ts">
  import { onMount } from 'svelte';
  import type { Classroom } from '$lib/types/classroom';
  import { getAccessToken } from '$lib/stores/auth';
  import { goto } from '$lib/stores/navigation';

  let loading = true;
  let error: string | null = null;
  let classrooms: Classroom[] = [];

  async function fetchClassrooms() {
    try {
      loading = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch(`/api/classrooms/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch classrooms');
      }

      const data = await response.json();
      classrooms = Array.isArray(data) ? data : [];
    } catch (err) {
      console.error('Error fetching classrooms:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';
    } finally {
      loading = false;
    }
  }

  function openClassroom(id: number) {
    goto(`/student/classrooms/${id}`);
  }

  onMount(fetchClassrooms);
</script>

<div class="space-y-6">
  <h1 class="text-2xl font-semibold text-gray-900">My Classrooms</h1>

  {#if loading}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
      {error}
    </div>
  {:else if classrooms.length === 0}
    <div class="text-center text-gray-500 py-12">No classrooms yet.</div>
  {:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each classrooms as c}
        <div class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-sm cursor-pointer" on:click={() => openClassroom(c.id)}>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-lg font-medium text-gray-900">{c.name}</h2>
            <span class="text-xs text-gray-500">{c.student_count} students</span>
          </div>
          {#if c.description}
            <p class="text-sm text-gray-600 line-clamp-2">{c.description}</p>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>


