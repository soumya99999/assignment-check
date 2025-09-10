<script lang="ts">
  import StudentAssignmentList from '$lib/components/assignment/StudentAssignmentList.svelte';
  import type { Classroom } from '$lib/types/classroom';
  import { createEventDispatcher } from 'svelte';

  export let classroom: Classroom;

  const dispatch = createEventDispatcher();

  function handleBack() {
    dispatch('back');
  }
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 bg-gray-50 min-h-screen">
  <button
    on:click={handleBack}
    class="inline-flex items-center text-indigo-600 hover:text-indigo-800 font-medium mb-6"
  >
    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
    </svg>
    Back to Classrooms
  </button>

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
      <div class="text-right flex items-center space-x-4">
        <!-- Teacher Profile Picture Placeholder -->
        <div class="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center">
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div>
          <p class="text-sm text-gray-500">Teacher</p>
          <p class="font-medium text-gray-900">{classroom.teacher.first_name} {classroom.teacher.last_name}</p>
        </div>
      </div>
    </div>
  </div>

  <StudentAssignmentList classroomId={classroom.id} />
</div>
