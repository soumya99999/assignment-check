<script lang="ts">
	import '../app.css';
	import BackgroundAnimation from '$lib/components/ui/BackgroundAnimation.svelte';
	import StudentLoader from '$lib/components/ui/StudentLoader.svelte';
	import { isNavigating } from '$lib/stores/navigation';
	
	let { children } = $props();
</script>

<BackgroundAnimation />

{#if $isNavigating}
  <StudentLoader />
{/if}

{@render children?.()}
