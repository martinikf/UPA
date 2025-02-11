<script lang="ts">
	import Model from './AnimatedModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import { Button } from 'flowbite-svelte';

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

<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-4">
	<div class="space-y-3">
		<Button color="primary" class="w-full" on:click={confirm}>
			Potvrdit
		</Button>

		<p class="text-gray-700 dark:text-gray-300">
			Přepis znakování: <strong class="font-semibold text-gray-900 dark:text-white" id="word"></strong>
		</p>

		<Button color="blue" class="w-full" on:click={playText}>
			Přehrát zadaný text
		</Button>
	</div>
</div>