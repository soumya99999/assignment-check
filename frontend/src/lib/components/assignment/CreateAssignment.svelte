<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { Assignment, AssignmentFormData } from '$lib/types/assignment';
  import { getAccessToken } from '$lib/stores/auth';

  export let classroomId: number | null = null;

  const dispatch = createEventDispatcher<{ assignmentCreated: Assignment }>();

  let showForm = false;
  let creating = false;
  let error: string | null = null;

  // Form data
  let title = '';
  let description = '';
  let totalMarks = 100;
  let questionFile: File | null = null;
  let answerFile: File | null = null;

  function handleCreateClick() {
    showForm = true;
    error = null;
  }

  function handleCancel() {
    showForm = false;
    resetForm();
  }

  function resetForm() {
    title = '';
    description = '';
    totalMarks = 100;
    questionFile = null;
    answerFile = null;
    error = null;
  }

  function handleQuestionFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      questionFile = target.files[0];
    }
  }

  function handleAnswerFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      answerFile = target.files[0];
    }
  }

  async function handleSubmit() {
    if (!classroomId) {
      error = 'Invalid classroom ID';
      return;
    }

    if (!title.trim()) {
      error = 'Assignment title is required';
      return;
    }

    if (totalMarks <= 0) {
      error = 'Total marks must be greater than 0';
      return;
    }

    try {
      creating = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      // Create FormData for file uploads
      const formData = new FormData();
      formData.append('title', title.trim());
      formData.append('description', description.trim());
      formData.append('classroom', classroomId.toString());
      formData.append('total_marks', totalMarks.toString());

      if (questionFile) {
        formData.append('question_file', questionFile);
      }

      if (answerFile) {
        formData.append('correct_answer_file', answerFile);
      }

      const response = await fetch('/api/assignments/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // Don't set Content-Type for FormData, let browser set it with boundary
        },
        body: formData
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication failed. Please log in again.');
        } else if (response.status === 403) {
          throw new Error('You do not have permission to create assignments.');
        } else {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
      }

      const newAssignment: Assignment = await response.json();

      // Dispatch event to parent component
      dispatch('assignmentCreated', newAssignment);

      // Reset form and hide
      resetForm();
      showForm = false;

      // Show success message
      alert('Assignment created successfully!');

    } catch (err) {
      console.error('Error creating assignment:', err);
      error = err instanceof Error ? err.message : 'Failed to create assignment';
    } finally {
      creating = false;
    }
  }
</script>

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  {#if !showForm}
    <div class="text-center">
      <button
        on:click={handleCreateClick}
        class="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 cursor-pointer"
      >
        <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Create New Assignment
      </button>
      <p class="mt-2 text-sm text-gray-600">Add a new assignment for your students</p>
    </div>
  {:else}
    <div>
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-gray-900">Create New Assignment</h2>
        <button
          on:click={handleCancel}
          class="text-gray-400 hover:text-gray-600"
          aria-label="Cancel creating assignment"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      {/if}

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <!-- Title -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
            Assignment Title *
          </label>
          <input
            type="text"
            id="title"
            bind:value={title}
            required
            placeholder="Enter assignment title"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            id="description"
            bind:value={description}
            rows="4"
            placeholder="Enter assignment description"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          ></textarea>
        </div>

        <!-- Total Marks -->
        <div>
          <label for="totalMarks" class="block text-sm font-medium text-gray-700 mb-2">
            Total Marks *
          </label>
          <input
            type="number"
            id="totalMarks"
            bind:value={totalMarks}
            min="1"
            required
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <!-- Question File -->
        <div>
          <label for="questionFile" class="block text-sm font-medium text-gray-700 mb-2">
            Question File (PDF, DOC, DOCX)
          </label>
          <input
            type="file"
            id="questionFile"
            accept=".pdf,.doc,.docx"
            on:change={handleQuestionFileChange}
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
          />
          {#if questionFile}
            <p class="mt-1 text-sm text-gray-600">Selected: {questionFile.name}</p>
          {/if}
        </div>

        <!-- Answer File -->
        <div>
          <label for="answerFile" class="block text-sm font-medium text-gray-700 mb-2">
            Correct Answer File (PDF, DOC, DOCX)
          </label>
          <input
            type="file"
            id="answerFile"
            accept=".pdf,.doc,.docx"
            on:change={handleAnswerFileChange}
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
          />
          {#if answerFile}
            <p class="mt-1 text-sm text-gray-600">Selected: {answerFile.name}</p>
          {/if}
        </div>

        <!-- Submit Buttons -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            on:click={handleCancel}
            disabled={creating}
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={creating}
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {#if creating}
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating...
            {:else}
              Create Assignment
            {/if}
          </button>
        </div>
      </form>
    </div>
  {/if}
</div>
