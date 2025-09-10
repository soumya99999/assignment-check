<script lang="ts">
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import type { IconDefinition } from '@fortawesome/free-solid-svg-icons';
  import type { Readable } from 'svelte/store';
  import { isExpanded } from '$lib/stores/sidebar';

  export let link: { label: string; href?: string; icon: IconDefinition; color: string };
  export let currentPath: Readable<string>;
  export let onClick: (() => void) | undefined = undefined;

  // Map Tailwind classes per color
  const colorClasses: Record<string, { active: string; text: string }> = {
    green: { active: 'bg-green-100 font-bold text-green-700', text: 'text-green-600' },
    yellow: { active: 'bg-yellow-100 font-bold text-yellow-700', text: 'text-yellow-600' },
    purple: { active: 'bg-purple-100 font-bold text-purple-700', text: 'text-purple-600' },
    blue: { active: 'bg-blue-100 font-bold text-blue-700', text: 'text-blue-600' },
    red: { active: 'bg-red-100 font-bold text-red-700', text: 'text-red-600' }
  };

  $: styles = colorClasses[link.color] || colorClasses.blue;
</script>

{#if onClick}
  <button
    type="button"
    class={`w-full text-left flex items-center rounded-xl px-4 py-3 mx-3 gap-4 transition-colors duration-200
           shadow-[inset_2px_2px_4px_#d1d1d1,inset_-2px_-2px_4px_#ffffff]
           hover:shadow-[inset_4px_4px_8px_#c1c1c1,inset_-4px_-4px_8px_#ffffff]
           bg-[#f4f6f8] ${styles.text}`}
    on:click={onClick}
  >
    <FontAwesomeIcon icon={link.icon} class="w-6 h-6" />
    {#if $isExpanded}
      <span class="text-sm">{link.label}</span>
    {/if}
  </button>
{:else}
  <a
    href={link.href}
    class={`flex items-center rounded-xl px-4 py-3 mx-3 gap-4 transition-colors duration-200
           shadow-[inset_2px_2px_4px_#d1d1d1,inset_-2px_-2px_4px_#ffffff]
           hover:shadow-[inset_4px_4px_8px_#c1c1c1,inset_-4px_-4px_8px_#ffffff]
           ${link.href && $currentPath.startsWith(link.href) ? styles.active : 'bg-[#f4f6f8] ' + styles.text}`}
  >
    <FontAwesomeIcon icon={link.icon} class="w-6 h-6" />
    {#if $isExpanded}
      <span class="text-sm">{link.label}</span>
    {/if}
  </a>
{/if}
