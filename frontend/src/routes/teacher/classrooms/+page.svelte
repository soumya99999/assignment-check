<script lang="ts">
  import { onMount } from 'svelte';
  import Sidebar from '$lib/components/sidebar/Sidebar.svelte';
  import { isExpanded } from '$lib/stores/sidebar';
  import ClassroomList from '$lib/components/classroom/ClassroomList.svelte';
  import CreateClassroom from '$lib/components/classroom/CreateClassroom.svelte';
  import type { Classroom } from '$lib/types/classroom';
  import { getAccessToken } from '$lib/stores/auth';

  let classrooms: Classroom[] = [];
  let loading = true;
  let error: string | null = null;
  let retryCount = 0;
  const MAX_RETRIES = 3;

  async function fetchClassrooms(retry = false) {
    try {
      loading = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch('/api/classrooms/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache'
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication failed. Please log in again.');
        } else if (response.status === 403) {
          throw new Error('You do not have permission to access this resource.');
        } else if (response.status >= 500) {
          throw new Error('Server error. Please try again later.');
        } else {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
      }

      const data = await response.json();

      // Validate response structure
      if (!Array.isArray(data)) {
        throw new Error('Invalid response format from server');
      }

      classrooms = data;
      retryCount = 0; // Reset retry count on success

    } catch (err) {
      console.error('Error fetching classrooms:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';

      // Auto-retry for network errors
      if (retry && retryCount < MAX_RETRIES && (
        err instanceof TypeError || // Network errors
        (err instanceof Error && err.message.includes('fetch'))
      )) {
        retryCount++;
        console.log(`Retrying... Attempt ${retryCount}/${MAX_RETRIES}`);
        setTimeout(() => fetchClassrooms(true), 1000 * retryCount); // Exponential backoff
        return;
      }
    } finally {
      loading = false;
    }
  }

  function handleClassroomCreated(event: CustomEvent<Classroom>) {
    // Optimistically update the UI
    classrooms = [event.detail, ...classrooms];
    error = null; // Clear any previous errors
  }

  function handleRetry() {
    fetchClassrooms(true);
  }

  onMount(() => {
    fetchClassrooms();
  });
</script>

<div class="flex min-h-screen bg-gray-50 transition-all duration-300">
  <!-- Sidebar -->
  <Sidebar />

  <!-- Main Content -->
  <main
    class={`flex-1 p-6 transition-all duration-300 ml-10 ${
      $isExpanded ? 'ml-64' : 'ml-20'
    }`}
  >
    <div class="max-w-7xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-indigo-800 mb-2">Classrooms</h1>
        <p class="text-gray-600">Manage your classrooms and create new ones for your students.</p>
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      {/if}

      <!-- Create Classroom Section -->
      <div class="mb-8">
        <CreateClassroom on:classroomCreated={handleClassroomCreated} />
      </div>

      <!-- Classrooms List Section -->
      <div>
        {#if loading}
          <div class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        {:else}
          <ClassroomList {classrooms} basePath="/teacher/classrooms" />
        {/if}
      </div>
    </div>
  </main>
</div>
