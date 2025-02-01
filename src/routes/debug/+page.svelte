<script lang="ts">

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';


	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	// References
	let landmarkDetection: LandmarkDetection;

	let lastMsg : GestureProbability[]= [];

	let letterFrequency : {[letter: string] : number} = createDict();
	$: sorted = Object.keys(letterFrequency).sort();

	let str: string = "";

	/**
	 * Routes landmark detection messages to appropriate components based on current mode
	 * @param msg - Custom event containing gesture probability data
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		lastMsg = msg.detail;

		for(let i = 0; i < msg.detail.length; i++){
			const letter = msg.detail[i].letter;
			if(letter == 'None') return;
			if(i == 0){
				str += letter;
			}

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

		return  frequency;
	}

	function reset(){
		letterFrequency = createDict();
	}

	async function guess(){
		let parsed = convertToFrequencyFormat(str);
		console.log("RAW: " + str);
		console.log("Parsed: " + parsed)

		await sendPrompt(parsed);

		str = "";
	}


	async function sendPrompt(txt : string) {
		let data = {
			'model' : "llama3.1",
			"stream" : false,
			"prompt" : txt
		}

		const res = await fetch('http://localhost:11434/api/generate', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const resp = await res.json();
		console.log("Response: " + resp.response)
		model.playAnimationForText(resp.response, Language.CzechFingerOneHand)
	}


	function convertToFrequencyFormat(input: string): string {
		// Initialize the result string and a counter
		let result = "";
		let count = 1;

		// Iterate through the string
		for (let i = 1; i <= input.length; i++)
		{
			if (input[i] === input[i - 1] || (i > 2 && i+1 < input.length && input[i] == input[i-2] && input[i] == input[i+1]))
			{
				// Increment the count if the current character is the same as the previous
				// or if there is different char between two same: aba -> assume that b is recognition fail
				count++;
			}
			else
			{
				// Append the count and the character to the result
				if(count > 5)
				{
					//result += `${count}${input[i - 1]}`;
					result += `${input[i - 1]}`;
				}
				if(count > 20)
				{
					result += ' ';
					count = 0;
				}

				// Reset the count for the next character
				count = 1;
			}


		}

		return result;
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
	<button on:click={guess}>Guess</button>
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