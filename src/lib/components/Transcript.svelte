<script lang="ts">
	import Model from './AnimatedModel.svelte';
	import { Button, Heading, P } from 'flowbite-svelte';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';

	export let model: Model;

	let str: string = "";
	let winner: GestureProbability | null = null;
	let automaticMode = true;

	export function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		const result = msg.detail;
		winner = findKeyWithMaxValue(result);

		if (automaticMode && winner && winner.letter != 'None') {
			str += winner.letter;
		}
	}

	function findKeyWithMaxValue(data: GestureProbability[]): GestureProbability | null {
		if (data.length === 0) return null;
		return data.reduce((max, current) => (current.probability > max.probability ? current : max));
	}

	function confirm() {
		if (winner?.letter) {
			str += winner.letter;
		}
	}

	function playText() {
		if (model && str.length > 0) {
			model.playAnimationForText(str, Language.CzechFingerOneHand);
		} else {
			alert('Není co přehrát.');
		}
	}

	function deleteText() {
			str = '';
	}

	function automatic(){
		automaticMode = true;
		deleteText();
	}

	function manual(){
		automaticMode = false;
		deleteText();
	}

	function handleKeyPress(event: KeyboardEvent){
		if(event.code === "Enter"){
			confirm();
		}
		else if(event.code === "Backspace"){
			str = str.slice(0, -1);
		}
	}
</script>

<svelte:window on:keydown={handleKeyPress} />

<div class="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm space-y-4">
	<P class="text-gray-700 dark:text-gray-300">Režim rozpoznávání</P>
	<div class="flex gap-2">
		<Button
			color={automaticMode ? 'blue' : 'none'}
			on:click={automatic}
			class="flex-1"
		>
			Automatický
		</Button>
		<Button
			color={!automaticMode ? 'blue' : 'none'}
			on:click={manual}
			class="flex-1"
		>
			Manuální
		</Button>
	</div>

	<div class="border-b border-gray-200 dark:border-gray-700 my-2"></div>


	{#if !automaticMode}
		<div class="space-y-3">
			<Button color="primary" class="w-full" on:click={confirm}>
				Potvrdit aktuální znak
			</Button>
		</div>
	{/if}

	<div class="space-y-3">
		<P class="text-gray-700 dark:text-gray-300">
			Přepis znakování: <strong class="font-semibold text-gray-900 dark:text-white">{str}</strong>
		</P>

		<div class="border-b border-gray-200 dark:border-gray-700 my-2"></div>

		<div class="flex gap-2">
			<Button color="red" class="flex-1" on:click={deleteText}>
				Smazat text
			</Button>
			<Button color="blue" class="flex-1" on:click={playText}>
				Přehrát text
			</Button>
		</div>
	</div>
</div>