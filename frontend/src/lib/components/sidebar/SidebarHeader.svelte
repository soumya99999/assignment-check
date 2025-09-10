<script lang="ts">
  import { isExpanded } from '$lib/stores/sidebar';
  import { user } from '$lib/stores/auth';

  $: username = $user ? $user.username : '';
</script>

<div
  class="h-20 flex items-center justify-center border-b border-none
         bg-[#f4f6f8] shadow-[inset_3px_3px_6px_#c9c9c9,inset_-3px_-3px_6px_#ffffff]"
>
  {#if $isExpanded}
    <span class="text-lg font-semibold">{$user?.username}</span>
  {:else}
    <span class="text-lg font-bold">
      {#if username}{username.charAt(0).toUpperCase()}{/if}
    </span>
  {/if}
</div>
