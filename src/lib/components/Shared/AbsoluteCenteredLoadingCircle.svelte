<script>
	/**
	 * A simple Svelte component that displays a centered loading spinner.
	 * Uses the Spinner component from Flowbite Svelte.
	 * Intended to be used as a visual indicator while content is loading.
	 */
	import { Spinner } from 'flowbite-svelte';
</script>

<div role="status" class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
	<Spinner color="primary" size="16" />
</div>