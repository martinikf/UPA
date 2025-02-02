<script lang="ts">

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';


	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	// References
	let landmarkDetection: LandmarkDetection;

	let lastMsg : GestureProbability[]= [];

	let letterFrequency : {[letter: string] : number} = createDict();
	$: sorted = Object.keys(letterFrequency).sort();

	/**
	 * Routes landmark detection messages to appropriate components based on current mode
	 * @param msg - Custom event containing gesture probability data
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		lastMsg = msg.detail;

		for(let i = 0; i < msg.detail.length; i++){
			const letter = msg.detail[i].letter;
			letterFrequency[letter]++;
		}
	}

	function createDict() : {[letter: string] : number}{
		let lettersCz = 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split('');
		//Add letter 'ch' after 'h'
		lettersCz.splice(8, 0, 'Ch');

		let frequency : {[letter: string] : number} = {}
		lettersCz.forEach((letter) => {
			frequency[letter] = 0;
		});
		frequency["None"] = 0;

		return  frequency;
	}

	function reset(){
		letterFrequency = createDict();
	}

</script>


<div style="display: flex;">
	<!-- WEBCAM -->
	<div class="webcam_container">
		<div class="webcam">
			<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
		</div>
	</div>

	<button on:click={reset}>Reset</button>
	<ul>
		{#each sorted as key}
			<li>{key}: {letterFrequency[key]}</li>
		{/each}
	</ul>

	<ul>
	{#each lastMsg as value}
		<li>{value.letter} : {value.probability}</li>
	{/each}
	</ul>

</div>

<div class="animation">
	<div class="animation_canvas">
		<Scene bind:model bind:this={scene} />
	</div>
	<ControlRow bind:this={controlRow} {model} />
</div>

<style>

  .animation {
    width: 100%;
    max-width: 400px;
  }
</style>