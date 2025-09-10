<script lang="ts">
	// Simple loading spinner instead of Lottie animation
</script>

<div
	class="fixed inset-0 z-50 flex h-full w-full items-center justify-center bg-white/20 backdrop-blur-md"
>
	<div class="loading-spinner-container">
		<div class="loading-spinner"></div>

		<div class="mt-4 font-bold text-black">Loading...</div>
	</div>
</div>

<style>
	.loading-spinner-container {
		display: flex;
		flex-direction: column;

		align-items: center;

		justify-content: center;
	}

	.loading-spinner {
		width: 50px;

		height: 50px;

		border: 5px solid rgba(0, 0, 0, 0.1);

		border-radius: 50%;

		border-top-color: #000;

		animation: spin 1s ease-in-out infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
