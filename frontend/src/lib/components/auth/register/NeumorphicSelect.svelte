<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';

  export let options: { value: string; label: string }[] = [];
  export let selected: string = '';
  export let id: string = '';
  export const required: boolean = false;

  const dispatch = createEventDispatcher();

  let isOpen = false;
  let container: HTMLElement;

  function toggleDropdown() {
    isOpen = !isOpen;
  }

  function selectOption(value: string) {
    selected = value;
    isOpen = false;
    dispatch('change', { value });
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      isOpen = false;
    }
  }

  onMount(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (container && !container.contains(event.target as Node)) {
        isOpen = false;
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  });
</script>

<div
  bind:this={container}
  class="relative w-full select-none"
  on:keydown={handleKeyDown}
  tabindex="-1"
  role="listbox"
  aria-expanded={isOpen}
  aria-labelledby={id}
>
  <label for={id} class="block text-sm font-medium text-gray-700 mb-2">{id}</label>
  <button
    type="button"
    class="w-full rounded-xl px-4 py-3 text-sm text-left bg-[#f4f6f8]
           shadow-[inset_5px_5px_10px_#d1d1d1,inset_-5px_-5px_10px_#ffffff]
           focus:shadow-[inset_3px_3px_6px_#c1c1c1,inset_-3px_-3px_6px_#ffffff]
           hover:shadow-[inset_6px_6px_12px_#c9c9c9,inset_-6px_-6px_12px_#ffffff]
           transition-shadow duration-200
           flex justify-between items-center cursor-pointer"
    aria-labelledby={id}
    on:click={toggleDropdown}
    aria-haspopup="listbox"
    aria-expanded={isOpen}
  >
    <span>{options.find(o => o.value === selected)?.label || 'Select your role'}</span>
    <svg
      class="w-5 h-5 text-gray-600"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path>
    </svg>
  </button>

  {#if isOpen}
    <ul
      class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-xl bg-[#f4f6f8]
             shadow-[10px_10px_20px_#c9c9c9,-10px_-10px_20px_#ffffff]
             focus:outline-none"
      role="listbox"
      tabindex="-1"
      aria-labelledby={id}
    >
      {#each options as option (option.value)}
        <li
          class="cursor-pointer select-none px-4 py-3 text-sm text-gray-700 hover:bg-indigo-200 rounded-xl"
          role="option"
          aria-selected={option.value === selected}
          on:click={() => selectOption(option.value)}
          on:keydown={(e) => e.key === 'Enter' && selectOption(option.value)}
          tabindex="0"
        >
          {option.label}
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  /* Scrollbar styling for dropdown */
  ul::-webkit-scrollbar {
    width: 8px;
  }
  ul::-webkit-scrollbar-thumb {
    background-color: #c9c9c9;
    border-radius: 4px;
  }
  ul::-webkit-scrollbar-track {
    background: transparent;
  }
</style>
