<script lang="ts">
	import Model from './AnimatedModel.svelte';

	export let model : Model;
	let speed : number = 1;

</script>

<div class="control_row">
	<input type="range" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model.changeSpeed(speed)}} />
	<button on:click={() => {model.resetAnimation()}}>Reset</button>
	<button on:click={() => {model.pauseResumeAnimation()}}>Zastavit/Pokračovat</button>
</div>

<style>
    .control_row{
        grid-gap: 10px;
        padding: 0 5px 5px;
        display: grid;
        grid-template-columns: 2fr 1fr 2fr;
    }

		.control_row button{
        padding: 5px;
		}
</style>