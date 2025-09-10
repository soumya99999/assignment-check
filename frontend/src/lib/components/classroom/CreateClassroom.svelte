<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import ClassroomForm from './ClassroomForm.svelte';
	import SuccessNotification from './SuccessNotification.svelte';
	import type { Classroom } from '$lib/types/classroom';
	import { getAccessToken } from '$lib/stores/auth';

	const dispatch = createEventDispatcher<{ classroomCreated: Classroom }>();

	let showForm = false;
	let showSuccess = false;
	let successClassroom: Classroom | null = null;
	let creating = false;

	function handleCreateClick() {
		showForm = true;
	}

	function handleCancel() {
		showForm = false;
	}

	async function handleClassroomSubmit(event: CustomEvent<{ name: string; description: string }>) {
		try {
			creating = true;
			const token = getAccessToken();
			if (!token) {
				throw new Error('Authentication token not found. Please log in again.');
			}

			const response = await fetch('/api/classrooms/', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(event.detail)
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Failed to create classroom');
			}

			const newClassroom: Classroom = await response.json();
			successClassroom = newClassroom;
			showSuccess = true;
			showForm = false;

			// Dispatch event to parent component
			dispatch('classroomCreated', newClassroom);
		} catch (error) {
			console.error('Error creating classroom:', error);
			alert(error instanceof Error ? error.message : 'Failed to create classroom');
		} finally {
			creating = false;
		}
	}

	function handleSuccessClose() {
		showSuccess = false;
		successClassroom = null;
	}
</script>

<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
	{#if !showForm}
		<div class="text-center">
			<button
				on:click={handleCreateClick}
				class="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 cursor-pointer"
			>
				<svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 6v6m0 0v6m0-6h6m-6 0H6"
					/>
				</svg>
				Create New Classroom
			</button>
			<p class="mt-2 text-sm text-gray-600">Set up a new classroom for your students</p>
		</div>
	{:else}
		<div>
			<div class="mb-6 flex items-center justify-between">
				<h2 class="text-xl font-semibold text-gray-900">Create New Classroom</h2>
				<button
					on:click={handleCancel}
					class="text-gray-400 hover:text-gray-600 cursor-pointer"
					aria-label="Cancel creating classroom"
				>
					<svg
						class="h-6 w-6"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>
			<ClassroomForm on:submit={handleClassroomSubmit} on:cancel={handleCancel} {creating} />
		</div>
	{/if}
</div>

{#if showSuccess && successClassroom}
	<SuccessNotification classroom={successClassroom} on:close={handleSuccessClose} />
{/if}
