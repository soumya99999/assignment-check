<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
</script>

<div class="min-h-screen bg-gray-50">
  <Navbar />
  <main class="px-4 sm:px-6 lg:px-8 py-6">
    <slot />
  </main>
  
</div>


