<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import StudentAssignmentList from '$lib/components/assignment/StudentAssignmentList.svelte';
  import type { Classroom } from '$lib/types/classroom';
  import { getAccessToken } from '$lib/stores/auth';

  let loading = true;
  let error: string | null = null;
  let classroom: Classroom | null = null;
  let classroomId: number | null = null;
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
        throw new Error('Failed to fetch classroom details');
      }

      classroom = await response.json();
    } catch (err) {
      console.error('Error fetching classroom:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';
    } finally {
      loading = false;
    }
  }

  onMount(fetchClassroom);
</script>

<div class="space-y-6">
  <!-- Navbar is already provided via student layout; omit here if duplicated -->
  {#if loading}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
      {error}
    </div>
  {:else if classroom}
    <!-- Classroom Header for students -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{classroom.name}</h1>
          {#if classroom.description}
            <p class="text-gray-600 mb-3">{classroom.description}</p>
          {/if}
          <div class="flex items-center space-x-6 text-sm text-gray-500">
            <span>Code: <span class="font-mono font-medium text-indigo-600">{classroom.code}</span></span>
            <span>{classroom.assignment_count} assignments</span>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
            <!-- Fallback avatar with teacher initials -->
            <span class="text-sm font-medium">
              {classroom.teacher.first_name?.[0]}{classroom.teacher.last_name?.[0]}
            </span>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500">Teacher</p>
            <p class="font-medium text-gray-900">{classroom.teacher.first_name} {classroom.teacher.last_name}</p>
            <p class="text-xs text-gray-500">@{classroom.teacher.username}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Assignment list for student -->
    <StudentAssignmentList {classroomId} />
  {/if}
</div>


