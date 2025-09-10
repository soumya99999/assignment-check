<script lang="ts">
  import Sidebar from '$lib/components/sidebar/Sidebar.svelte';
  import { isExpanded } from '$lib/stores/sidebar'; // store controlling sidebar
</script>

<div class="flex min-h-screen bg-gray-50 transition-all duration-300">
  <!-- Sidebar -->
  <Sidebar />

  <!-- Main Content -->
  <main
    class={`flex-1 p-6 transition-all duration-300 ${
      $isExpanded ? 'ml-64' : 'ml-20'
    }`}
  >
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-indigo-800 mb-6">Teacher Dashboard</h1>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- Classrooms Card -->
        <a
          href="/teacher/classrooms"
          class="block bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="flex items-center justify-center w-10 h-10 bg-purple-100 rounded-lg">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Classrooms</h3>
              <p class="text-sm text-gray-500">Manage your classrooms</p>
            </div>
          </div>
        </a>

        <!-- Assignments Card -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Assignments</h3>
              <p class="text-sm text-gray-500">Create and manage assignments</p>
            </div>
          </div>
        </div>

        <!-- Reports Card -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">Reports</h3>
              <p class="text-sm text-gray-500">View assignment reports</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
