<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$lib/stores/navigation';
  import Sidebar from '$lib/components/sidebar/Sidebar.svelte';
  import { isExpanded } from '$lib/stores/sidebar';
  import AssignmentList from '$lib/components/assignment/AssignmentList.svelte';
  import CreateAssignment from '$lib/components/assignment/CreateAssignment.svelte';
  import StudentAssignmentList from '$lib/components/assignment/StudentAssignmentList.svelte';
  import type { Classroom } from '$lib/types/classroom';
  import { getAccessToken, user } from '$lib/stores/auth';

  let classroom: Classroom | null = null;
  let loading = true;
  let error: string | null = null;
  let classroomId: number | null = null;
  let assignmentListComponent: AssignmentList | null = null;

  // Subscribe to page store to get the classroom ID
  $: classroomId = $page.params.id ? parseInt($page.params.id) : null;

  async function fetchClassroom() {
    if (!classroomId) return;

    try {
      loading = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const response = await fetch(`/api/classrooms/${classroomId}/`, {
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
          throw new Error('You do not have permission to access this classroom.');
        } else if (response.status === 404) {
          throw new Error('Classroom not found.');
        } else {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
      }

      classroom = await response.json();
    } catch (err) {
      console.error('Error fetching classroom:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';
    } finally {
      loading = false;
    }
  }

  function handleBackToClassrooms() {
    goto('/teacher/classrooms');
  }

  function handleAssignmentCreated(event: CustomEvent) {
    // Refresh the assignment list when a new assignment is created
    if (assignmentListComponent && typeof assignmentListComponent.fetchAssignments === 'function') {
      assignmentListComponent.fetchAssignments();
    }
  }

  onMount(() => {
    if (classroomId) {
      fetchClassroom();
    } else {
      error = 'Invalid classroom ID';
      loading = false;
    }
  });
</script>

<div class="flex min-h-screen bg-gray-50 transition-all duration-300">
  <Sidebar/>

  <!-- Main Content -->
  <main
    class="flex-1 transition-all duration-300 ml-10"
  >
    <div class="max-w-7xl mx-auto">
      <!-- Back Button -->
      <div class="mb-6">
        <button
          on:click={handleBackToClassrooms}
          class="inline-flex items-center text-indigo-600 hover:text-indigo-800 font-medium cursor-pointer"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Classrooms
        </button>
      </div>

      {#if loading}
        <div class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      {:else if error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      {:else if classroom}
        <!-- Classroom Header -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-gray-900 mb-2">{classroom.name}</h1>
              {#if classroom.description}
                <p class="text-gray-600 mb-4">{classroom.description}</p>
              {/if}
              <div class="flex items-center space-x-6 text-sm text-gray-500">
                <span>Code: <span class="font-mono font-medium text-indigo-600">{classroom.code}</span></span>
                <span>{classroom.student_count} students</span>
                <span>{classroom.assignment_count} assignments</span>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-500">Teacher</p>
              <p class="font-medium text-gray-900">{classroom.teacher.first_name} {classroom.teacher.last_name}</p>
            </div>
          </div>
        </div>

        <!-- Create Assignment Section -->
        {#if $user?.role === 'teacher'}
          <div class="mb-8">
            <CreateAssignment {classroomId} on:assignmentCreated={handleAssignmentCreated} />
          </div>

          <!-- Assignments Section -->
          <div>
            <AssignmentList {classroomId} bind:this={assignmentListComponent} />
          </div>
        {/if}
      {/if}
    </div>
  </main>
</div>
