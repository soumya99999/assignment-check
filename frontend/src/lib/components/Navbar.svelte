<script lang="ts">
  import { user, logout } from '$lib/stores/auth';
  import JoinClassroom from './JoinClassroom.svelte';
  import { goto } from '$lib/stores/navigation';

  let showJoinModal = false;

  function toggleJoinModal() {
    showJoinModal = !showJoinModal;
  }

  function handleJoinClassroom() {
    toggleJoinModal();
  }

  function handleJoined(event: CustomEvent) {
    console.log('Joined classroom:', event.detail.classroom);
    showJoinModal = false;
    // Optionally refresh the page or update state
    window.location.reload();
  }

  function goToMyClassrooms() {
    const u = $user;
    if (!u) return;
    if (u.role === 'student') goto('/student/classrooms');
    else if (u.role === 'teacher') goto('/teacher/classrooms');
  }
</script>

<nav class="bg-white shadow-sm border-b border-gray-200">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <!-- Left: Logo + Username -->
      <div class="flex items-center space-x-3">
        {#if $user?.role === 'student'}
          <img src="/assets/reading.svg" alt="Student" class="h-8 w-8" />
        {:else if $user?.role === 'teacher'}
          <img src="/assets/Teacher.svg" alt="Teacher" class="h-8 w-8" />
        {/if}

        {#if $user}
          <span class="text-gray-900 font-medium">
            {$user.first_name} {$user.last_name} ({$user.username})
          </span>
        {/if}
      </div>

      <!-- Center: Primary Nav -->
      <div class="flex items-center">
        <button on:click={goToMyClassrooms} class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
          My Classrooms
        </button>
      </div>

      <!-- Right: Actions -->
      <div class="flex items-center">
        {#if $user?.role === 'student'}
          <button
            on:click={handleJoinClassroom}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer mr-2"
          >
            Join Classroom
          </button>
        {/if}

        <button on:click={logout} class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
          Logout
        </button>
      </div>
    </div>
  </div>
</nav>

<!-- Join Classroom Modal -->
{#if showJoinModal}
  <JoinClassroom on:joined={handleJoined} on:close={toggleJoinModal} />
{/if}
