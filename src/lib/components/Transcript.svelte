<script lang="ts">
	import Model from './AnimatedModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';

	export let model: Model;

	let wordDisplay: HTMLElement | null = null;
	let winner: GestureProbability | null = null;

	export function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		let result = msg.detail;
		winner = findKeyWithMaxValue(result);
	}

	function findKeyWithMaxValue(data: GestureProbability[]): GestureProbability | null {
		if(data.length == 0) return null;

		let best = data[0];
		console.log(data)
		for(let i = 1; i < data.length; i++){
			if(data[i].probability > best.probability){
				best = data[i];
			}
		}

		return best;
	}

	function confirm() {
		if (wordDisplay && winner != null) {
			wordDisplay.innerHTML += winner.letter;
		}
	}

	function playText() {
		if (wordDisplay && model && wordDisplay.innerHTML.length > 0)
			model.playAnimationForText(wordDisplay.innerHTML, Language.CzechFingerOneHand);
		else alert('Není co přehrát.');
	}

	if (browser) {
		onMount(() => {
			wordDisplay = document.getElementById('word');
		});
	}
</script>

<div class="controls">
	<button on:click={confirm}>Potvrdit</button>
	<p>Přepis znakování: <strong id="word"> </strong></p>
	<button on:click={playText}>Přehrát zadaný text</button>
</div>

<style>
	.controls {
		padding: 5px;
	}

	button {
		width: 100%;
		padding: 5px;
	}
</style>
