<script lang="ts">
  export let error: string | null;
</script>

{#if error}
  <div class="alert alert-error mb-4 rounded-md">{error}</div>
{/if}