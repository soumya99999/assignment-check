<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$lib/stores/navigation';
  import type { Assignment } from '$lib/types/assignment';
  import { getAccessToken } from '$lib/stores/auth';

  export let classroomId: number | null = null;

  let assignments: Assignment[] = [];
  let filteredAssignments: Assignment[] = [];
  let loading = true;
  let error: string | null = null;
  let searchQuery = '';
  let retryCount = 0;
  const MAX_RETRIES = 3;

  // Reactive statement to filter assignments based on search query
  $: {
    if (searchQuery.trim() === '') {
      filteredAssignments = assignments;
    } else {
      filteredAssignments = assignments.filter(assignment =>
        assignment.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        assignment.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
  }

  async function fetchAssignments(retry = false) {
    if (!classroomId) return;

    try {
      loading = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch(`/api/assignments/?classroom=${classroomId}`, {
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
          throw new Error('You do not have permission to access these assignments.');
        } else {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
      }

      assignments = await response.json();
      // Extra safety: ensure only the selected classroom's assignments are shown
      if (classroomId) {
        assignments = assignments.filter((a) => a.classroom === classroomId);
      }
      retryCount = 0; // Reset retry count on success

    } catch (err) {
      console.error('Error fetching assignments:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';

      // Auto-retry for network errors
      if (retry && retryCount < MAX_RETRIES && (
        err instanceof TypeError || // Network errors
        (err instanceof Error && err.message.includes('fetch'))
      )) {
        retryCount++;
        console.log(`Retrying... Attempt ${retryCount}/${MAX_RETRIES}`);
        setTimeout(() => fetchAssignments(true), 1000 * retryCount);
        return;
      }
    } finally {
      loading = false;
    }
  }

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  function handleSubmissionClick(assignmentId: number) {
    // Navigate to submissions view for this assignment
    goto(`/assignments/${assignmentId}/submissions`);
  }

  function handleEditAssignment(assignmentId: number) {
    // TODO: Implement edit functionality
    console.log('Edit assignment:', assignmentId);
  }

  async function handleDeleteAssignment(assignmentId: number) {
    if (!confirm('Are you sure you want to delete this assignment? This action cannot be undone.')) {
      return;
    }

    try {
      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch(`/api/assignments/${assignmentId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete assignment');
      }

      // Remove assignment from list
      assignments = assignments.filter(assignment => assignment.id !== assignmentId);
      alert('Assignment deleted successfully');

    } catch (err) {
      console.error('Error deleting assignment:', err);
      alert(err instanceof Error ? err.message : 'Failed to delete assignment');
    }
  }

  function handleRetry() {
    fetchAssignments(true);
  }

  onMount(() => {
    if (classroomId) {
      fetchAssignments();
    } else {
      loading = false;
      error = 'Invalid classroom ID';
    }
  });
</script>

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-xl font-semibold text-gray-900">Assignments</h2>

    <!-- Search Bar -->
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search assignments..."
        class="block w-64 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
      />
    </div>
  </div>

  {#if loading}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6 cursor-pointer">
      {error}
      <button
        on:click={handleRetry}
        class="ml-4 text-red-700 underline hover:text-red-800"
      >
        Retry
      </button>
    </div>
  {:else if filteredAssignments.length === 0}
    {#if searchQuery}
      <div class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-.966-5.618-2.479.032-.211.07-.42.12-.626A3 3 0 0112 9c1.543 0 2.833.973 3.162 2.291.05.206.088.415.12.626C16.29 14.034 14.34 15 12 15z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No assignments found</h3>
        <p class="text-gray-500">Try adjusting your search query.</p>
      </div>
    {:else}
      <div class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No assignments yet</h3>
        <p class="text-gray-500">Create your first assignment to get started.</p>
      </div>
    {/if}
  {:else}
    <div class="space-y-4">
      {#each filteredAssignments as assignment (assignment.id)}
        <div class="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-medium text-gray-900 mb-2">{assignment.title}</h3>
              {#if assignment.description}
                <p class="text-gray-600 text-sm mb-3 line-clamp-2">{assignment.description}</p>
              {/if}

              <div class="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                <span>Created {formatDate(assignment.created_at)}</span>
                <span>Total marks: {assignment.total_marks}</span>
              </div>

              <!-- Clickable Submission Count -->
              <button
                on:click={() => handleSubmissionClick(assignment.id)}
                class="inline-flex items-center text-indigo-600 hover:text-indigo-800 font-medium"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {assignment.submitted_students_count} submissions
              </button>
            </div>

            <!-- Quick Actions -->
            <div class="flex items-center space-x-2 ml-4">
              <button
                on:click={() => handleEditAssignment(assignment.id)}
                class="text-gray-400 hover:text-gray-600 p-1"
                title="Edit assignment"
                aria-label="Edit assignment"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>

              <button
                on:click={() => handleDeleteAssignment(assignment.id)}
                class="text-red-400 hover:text-red-600 p-1"
                title="Delete assignment"
                aria-label="Delete assignment"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
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
    line-clamp: 2;
    box-orient: vertical;
  }
</style>
