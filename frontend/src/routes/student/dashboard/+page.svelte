<script lang="ts">
  import StudentClassroomList from '$lib/components/classroom/StudentClassroomList.svelte';
  import StudentClassroomView from '$lib/components/classroom/StudentClassroomView.svelte';
  import type { Classroom } from '$lib/types/classroom';

  import { onMount } from 'svelte';
  import { getUser, getAccessToken } from '$lib/stores/auth';
  import { writable } from 'svelte/store';

  let user = null;
  let classrooms: Classroom[] = [];
  let selectedClassroom: Classroom | null = null;

  const loading = writable(true);
  const error = writable<string | null>(null);

  async function fetchClassrooms() {
    loading.set(true);
    error.set(null);
    try {
      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }
      const response = await fetch('/api/classrooms/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        throw new Error('Failed to fetch classrooms');
      }

      classrooms = await response.json();
    } catch (err) {
      error.set(err instanceof Error ? err.message : 'Unexpected error');
    } finally {
      loading.set(false);
    }
  }

  function handleClassroomSelected(event: CustomEvent<Classroom>) {
    // Navigate to student/classrooms/[id] for consistent URL and page logic
    import('$lib/stores/navigation').then(({ goto }) => goto(`/student/classrooms/${event.detail.id}`));
  }

  function handleBack() {
    selectedClassroom = null;
  }

  onMount(() => {
    user = getUser();
    fetchClassrooms();
  });
</script>


{#if selectedClassroom}
  <StudentClassroomView classroom={selectedClassroom} on:back={handleBack} />
{:else}
  <div class="p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold text-indigo-800 mb-6">Student Dashboard</h1>

    {#if $loading}
      <p>Loading classrooms...</p>
    {:else if $error}
      <p class="text-red-600">{$error}</p>
    {:else}
      <StudentClassroomList {classrooms} on:classroomSelected={handleClassroomSelected} />
    {/if}
  </div>
{/if}

