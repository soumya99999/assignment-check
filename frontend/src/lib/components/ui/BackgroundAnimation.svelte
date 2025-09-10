<script lang="ts">
  import { onMount } from 'svelte';
  
  let mounted = false;
  
  onMount(() => {
    mounted = true;
  });
</script>

<div class="fixed inset-0 -z-10 overflow-hidden">
  <div class="absolute inset-0 bg-gradient-to-br from-blue-50/30 via-white/60 to-purple-50/30 animate-gradient"></div>
  <div class="absolute inset-0" style="background-image: url('/assets/subtle-pattern.svg'); background-repeat: repeat; background-size: 200px;"></div>
</div>

<style>
  @keyframes gradient {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
  
  .animate-gradient {
    background-size: 200% 200%;
    animation: gradient 15s ease infinite;
  }
</style>