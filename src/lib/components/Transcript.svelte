<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import Model from './AnimatedModel.svelte';

	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { Button } from 'svelte-tweakpane-ui';

	export let model: Model;
	export let landmarkDetection: LandmarkDetection;

	let wordDisplay : HTMLElement | null = null;
	let winner : string | null = "-";


	export function handleMessage(msg : any) {
		let result = msg.detail;
		winner = findKeyWithMaxValue(result);
	}

	function findKeyWithMaxValue(dict: { [key: string]: number }): string | null {
		let maxKey: string | null = null;
		let maxValue: number | null = null;

		for (const key in dict) {
			if (dict.hasOwnProperty(key)) {
				const value = dict[key];

				if (maxValue === null || value > maxValue) {
					maxValue = value;
					maxKey = key;
				}
			}
		}

		return maxKey;
	}

	function confirm() {
		if(wordDisplay && winner != null && winner != "-"){
			wordDisplay.innerHTML += winner;
		}
	}

	function playText(){
		if(wordDisplay && model && wordDisplay.innerHTML.length > 0 )
			model.playAnimationForText(wordDisplay.innerHTML);
		else
			alert("Není co přehrát.");
	}

	if(browser){
		onMount(() => {
			wordDisplay = document.getElementById("word");
		});
	}

</script>

<div class="controls">
	<button on:click={confirm}>Potvrdit</button>
	<p>Přepis znakování: <strong id="word"> </strong></p>
	<button on:click={playText}>Přehrát zadaný text</button>
</div>

<style>
	.controls{
		padding: 5px;
	}

	button{
		width: 100%;
		padding: 5px;
	}

</style>