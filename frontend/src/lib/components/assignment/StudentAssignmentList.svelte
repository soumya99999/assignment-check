<script lang="ts">
  import { onMount } from 'svelte';
  import type { Assignment, Submission } from '$lib/types/assignment';
  import { getAccessToken, getUser } from '$lib/stores/auth';

  export let classroomId: number | null = null;

  let assignments: Assignment[] = [];
  let submissions: { [assignmentId: number]: Submission | null } = {};
  let loading = true;
  let error: string | null = null;
  let user = getUser();

  async function fetchAssignments() {
    if (!classroomId) return;

    try {
      loading = true;
      error = null;

      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      // Fetch assignments for this classroom
      const assignmentsResponse = await fetch(`/api/assignments/?classroom=${classroomId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!assignmentsResponse.ok) {
        throw new Error('Failed to fetch assignments');
      }

      assignments = await assignmentsResponse.json();
      // Extra safety: ensure only the selected classroom's assignments are shown
      if (classroomId) {
        assignments = assignments.filter((a) => a.classroom === classroomId);
      }

      // Fetch submissions for current user
      if (user) {
        const submissionsResponse = await fetch(`/api/submissions/?student=${user.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (submissionsResponse.ok) {
          const allSubmissions: Submission[] = await submissionsResponse.json();

          // Map submissions by assignment ID
          submissions = {};
          allSubmissions.forEach(submission => {
            submissions[submission.assignment] = submission;
          });
        }
      }

    } catch (err) {
      console.error('Error fetching data:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';
    } finally {
      loading = false;
    }
  }

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  async function downloadQuestionFile(assignment: Assignment) {
    if (!assignment.question_file) {
      alert('Question file not available');
      return;
    }

    try {
      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found');
      }

      const response = await fetch(assignment.question_file, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to download file');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `question_${assignment.title}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (err) {
      console.error('Error downloading file:', err);
      alert('Failed to download question file');
    }
  }

  function submitAssignment(assignmentId: number) {
    // Create a hidden file input
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.doc,.docx,.txt';
    input.onchange = async (event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (!file) return;

      await uploadSubmission(assignmentId, file);
    };
    input.click();
  }

  async function uploadSubmission(assignmentId: number, file: File) {
    try {
      const token = getAccessToken();
      if (!token) {
        throw new Error('Authentication token not found');
      }

      const formData = new FormData();
      formData.append('assignment', assignmentId.toString());
      formData.append('submission_file', file);

      const response = await fetch('/api/submissions/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit assignment');
      }

      // Refresh data after successful submission
      await fetchAssignments();
      alert('Assignment submitted successfully!');

    } catch (err) {
      console.error('Error submitting assignment:', err);
      alert(err instanceof Error ? err.message : 'Failed to submit assignment');
    }
  }

  onMount(() => {
    if (classroomId) {
      fetchAssignments();
    } else {
      loading = false;
      error = 'Invalid classroom ID';
    }
  });
</script>

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-xl font-semibold text-gray-900">Assignments</h2>
  </div>

  {#if loading}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
      {error}
    </div>
  {:else if assignments.length === 0}
    <div class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No assignments yet</h3>
      <p class="text-gray-500">Assignments will appear here when your teacher creates them.</p>
    </div>
  {:else}
    <div class="space-y-4">
      {#each assignments as assignment (assignment.id)}
        {@const submission = submissions[assignment.id]}
        <div class="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-medium text-gray-900 mb-2">{assignment.title}</h3>
              {#if assignment.description}
                <p class="text-gray-600 text-sm mb-3 line-clamp-2">{assignment.description}</p>
              {/if}

              <div class="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                <span>Created {formatDate(assignment.created_at)}</span>
                <span>Total marks: {assignment.total_marks}</span>
              </div>

              <!-- Submission Status -->
              {#if submission}
                <div class="mb-3">
                  {#if submission.score !== null}
                    <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Scored: {submission.score}/{assignment.total_marks}
                    </div>
                  {:else}
                    <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      Submitted - Awaiting grading
                    </div>
                  {/if}
                  <div class="text-xs text-gray-500 mt-1">
                    Submitted on {formatDate(submission.submission_date)}
                  </div>
                </div>
              {:else}
                <div class="mb-3">
                  <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                    Not submitted
                  </div>
                </div>
              {/if}
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center space-x-2 ml-4">
              {#if assignment.question_file}
                <button
                  on:click={() => downloadQuestionFile(assignment)}
                  class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  Download
                </button>
              {/if}

              {#if !submission}
                <button
                  on:click={() => submitAssignment(assignment.id)}
                  class="inline-flex items-center px-3 py-2 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                  Submit
                </button>
              {:else}
                <button
                  on:click={() => submitAssignment(assignment.id)}
                  class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  Re-submit
                </button>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-clamp: 2;
    box-orient: vertical;
  }
</style>
