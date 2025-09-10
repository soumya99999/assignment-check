<script lang="ts">
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faAngleRight, faAngleLeft } from '@fortawesome/free-solid-svg-icons';
  import { isExpanded } from '$lib/stores/sidebar';

  function toggle() {
    isExpanded.update((v) => !v);
  }
</script>

<div class="h-20 flex items-center justify-end px-4 border-gray-300">
  <button
    on:click={toggle}
    class="flex items-center justify-center w-10 h-10 rounded-full
           bg-[#f4f6f8] shadow-[4px_4px_8px_#c9c9c9,-4px_-4px_8px_#ffffff]
           hover:shadow-[inset_4px_4px_8px_#c9c9c9,inset_-4px_-4px_8px_#ffffff]
           transition cursor-pointer"
  >
    {#if $isExpanded}
      <FontAwesomeIcon icon={faAngleLeft} class="w-5 h-5 text-indigo-800" />
    {:else}
      <FontAwesomeIcon icon={faAngleRight} class="w-5 h-5 text-indigo-800" />
    {/if}
  </button>
</div>
