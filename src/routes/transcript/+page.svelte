<script lang="ts">
	import Transcript from '$lib/components/Transcript.svelte';
	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	let landmarkDetection: LandmarkDetection;
	let transcript: Transcript;

	function handleMessage(msg : any) {
		transcript.handleMessage(msg);
	}

</script>

<h1>Přepis videa na text</h1>

<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
<Transcript bind:landmarkDetection={landmarkDetection} bind:this={transcript}/>

<style>
    :global(body) {
        margin: 0;
    }

</style>
