<script lang="ts">
  import { goto } from '$lib/stores/navigation';
  import type { Classroom } from '$lib/types/classroom';

  export let classrooms: Classroom[] = [];

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  export let basePath: string = '/teacher/classrooms';

  function navigateToClassroom(classroomId: number) {
    goto(`${basePath}/${classroomId}`);
  }
</script>

<div class="space-y-6">
  {#if classrooms.length === 0}
    <div class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No classrooms yet</h3>
      <p class="text-gray-500">Create your first classroom to get started.</p>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each classrooms as classroom (classroom.id)}
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200 cursor-pointer" on:click={() => navigateToClassroom(classroom.id)}>
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 mb-1">{classroom.name}</h3>
              <p class="text-sm text-gray-500">Code: <span class="font-mono font-medium text-indigo-600">{classroom.code}</span></p>
            </div>
            <div class="flex flex-col space-y-2">
              <div class="flex items-center text-sm text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
                {classroom.student_count} students
              </div>
              <div class="flex items-center text-sm text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {classroom.assignment_count} assignments
              </div>
            </div>
          </div>

          {#if classroom.description}
            <p class="text-gray-600 text-sm mb-4 line-clamp-2">{classroom.description}</p>
          {/if}

          <div class="flex items-center justify-between text-xs text-gray-500">
            <span>Created {formatDate(classroom.created_at)}</span>
            <button class="text-indigo-600 hover:text-indigo-800 font-medium cursor-pointer">
              View Details
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box; /* Fallback for WebKit browsers */
    -webkit-line-clamp: 2; /* Limit to 2 lines in WebKit browsers */
    -webkit-box-orient: vertical; /* Vertical stacking in WebKit */
    overflow: hidden; /* Hide overflow content */

    /* Standard property (no prefix) for modern browsers */
    line-clamp: 2; /* Limit to 2 lines */
    box-orient: vertical; /* Vertical stacking (future-proofing) */
    overflow: hidden; /* Hide overflow content */
  }
</style>