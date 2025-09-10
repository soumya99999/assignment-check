<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher<{
    submit: { name: string; description: string };
    cancel: void;
  }>();

  export let creating = false;

  let name = '';
  let description = '';
  let nameError = '';
  let descriptionError = '';

  function validateForm(): boolean {
    nameError = '';
    descriptionError = '';

    if (!name.trim()) {
      nameError = 'Classroom name is required';
      return false;
    }

    if (name.trim().length < 3) {
      nameError = 'Classroom name must be at least 3 characters';
      return false;
    }

    if (description.trim().length > 500) {
      descriptionError = 'Description must be less than 500 characters';
      return false;
    }

    return true;
  }

  function handleSubmit(event: Event) {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    dispatch('submit', {
      name: name.trim(),
      description: description.trim()
    });
  }

  function handleCancel() {
    dispatch('cancel');
  }
</script>

<form on:submit={handleSubmit} class="space-y-6">
  <div>
    <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
      Classroom Name *
    </label>
    <input
      id="name"
      type="text"
      bind:value={name}
      placeholder="Enter classroom name"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      disabled={creating}
      required
    />
    {#if nameError}
      <p class="mt-1 text-sm text-red-600">{nameError}</p>
    {/if}
  </div>

  <div>
    <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
      Description
    </label>
    <textarea
      id="description"
      bind:value={description}
      placeholder="Enter classroom description (optional)"
      rows="4"
      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 resize-none"
      disabled={creating}
    ></textarea>
    {#if descriptionError}
      <p class="mt-1 text-sm text-red-600">{descriptionError}</p>
    {/if}
    <p class="mt-1 text-sm text-gray-500">
      {description.length}/500 characters
    </p>
  </div>

  <div class="flex justify-end space-x-3">
    <button
      type="button"
      on:click={handleCancel}
      class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
      disabled={creating}
    >
      Cancel
    </button>
    <button
      type="submit"
      disabled={creating}
      class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
    >
      {#if creating}
        <div class="flex items-center">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          Creating...
        </div>
      {:else}
        Create Classroom
      {/if}
    </button>
  </div>
</form>
