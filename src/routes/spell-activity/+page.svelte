<script lang="ts">
	import SpellActivity from '$lib/components/SpellActivity.svelte'

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	let landmarkDetection: LandmarkDetection;
	let spellActivity: SpellActivity;

	function handleMessage(msg : any) {
		spellActivity.handleMessage(msg);
	}

</script>

<h2>Procvičení znakování</h2>

<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
<SpellActivity bind:landmarkDetection={landmarkDetection} bind:this={spellActivity}/>

<style>
    :global(body) {
        margin: 0;
    }

</style>
