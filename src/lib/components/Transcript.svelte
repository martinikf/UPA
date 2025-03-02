<script lang="ts">
	import Model from './AnimatedModel.svelte';
	import { Button, P } from 'flowbite-svelte';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import { convertToFrequencyFormat } from '$lib/helpers/CSLR';

	export let model: Model;

	let str: string = "";
	let parsedStr :string = "";
	let winner: GestureProbability | null = null;
	let automaticMode = true;

	const WINNER_BUFFER_SIZE = 5;
	const TIME_BUFFER_WINDOW = 1000;
	let winnerBuffer: { letter: string, timestamp: number }[] = [];

	export function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		const result = msg.detail;
		winner = findKeyWithMaxValue(result);

		removeOldRecords();

		if(!winner || winner.letter === 'None'){ return;}

		if (automaticMode) {
			str += winner.letter;
			parsedStr = convertToFrequencyFormat(str);
		}
		if(!automaticMode) {
			const currentTime = Date.now();
			winnerBuffer.push({ letter: winner.letter, timestamp: currentTime });
			if (winnerBuffer.length > WINNER_BUFFER_SIZE) {
				winnerBuffer.shift();
			}
			console.log(winnerBuffer);
		}
	}

	function findKeyWithMaxValue(data: GestureProbability[]): GestureProbability | null {
		if (data.length === 0) return null;
		return data.reduce((max, current) => (current.probability > max.probability ? current : max));
	}

	function confirm() {
		if(winnerBuffer.length < 1) return;

		// Find the most appearing letter in the buffer
		let mostFrequentLetter = winnerBuffer.reduce<Record<string, number>>((prev, current) => {
			prev[current.letter] = (prev[current.letter] || 0) + 1;
			return prev;
		}, {});
		let maxLetter = Object.keys(mostFrequentLetter).reduce((a, b) => mostFrequentLetter[a] > mostFrequentLetter[b] ? a : b);

		if(mostFrequentLetter[maxLetter] > 2)
		str += maxLetter;
		winnerBuffer = [];
	}

	function playText() {
		if (model) {
			if(automaticMode)
				model.playAnimationForText(parsedStr, Language.CzechFingerOneHand);
			else
				model.playAnimationForText(str, Language.CzechFingerOneHand);
		}
	}

	function deleteText() {
		str = '';
		parsedStr = "";
	}

	function automatic(){
		automaticMode = true;
		resetState();
	}

	function manual(){
		automaticMode = false;
		resetState();
	}

	function resetState(){
		winnerBuffer = []
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

	function removeOldRecords() {
		const currentTime = Date.now();
		winnerBuffer = winnerBuffer.filter(record => currentTime - record.timestamp <= TIME_BUFFER_WINDOW);
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

	<div class="flex gap-2">
		<Button color="red" class="flex-1" on:click={deleteText}>
			Smazat text
		</Button>
		<Button color="blue" class="flex-1" on:click={playText}>
			Přehrát text
		</Button>
	</div>

	{#if !automaticMode}
		<div class="space-y-3">
			<Button color="primary" class="w-full" on:click={confirm}>
				Potvrdit aktuální znak
			</Button>
		</div>
	{/if}
</div>

<div class="border-b border-gray-200 dark:border-gray-700 my-2"></div>

<div class="space-y-3">
	<P class="text-gray-700 dark:text-gray-300 break-words">
		Text: <br> <strong class="font-semibold text-gray-900 dark:text-white">{automaticMode ? parsedStr : str}</strong>
	</P>
</div>