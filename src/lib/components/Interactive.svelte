<script lang="ts">
	/**
	 * Svelte component for controlling animation and recognition
	 *
	 * Given sentence is played by each character, after the character is shown user has to repeat it.
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Language } from '$lib/models/Word';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Alert, Button, Input } from 'flowbite-svelte';
	import { keepOnlyLetters } from '$lib/helpers/TextHelper';

	// Component props
	export let model: Model;

	// Constants
	const DEFAULT_STRING = 'Ukázkový text';
	const RECOGNITION_DELAY = 1500; // ms
	const NEXT_CHAR_DELAY = 2000; // ms
	const WAITING_EMOJI = '🕒';
	const SUCCESS_EMOJI = '👍';

	let customString: string = '';
	let text: string;
	let speed = 1;
	let timeout = 0;

	let messageVisible: boolean = false;
	const SUCCESS_MESSAGE_DURATION = 3000;
	let alertMessage : string = "";

	/**
	 * Handles gesture recognition events from webcam
	 * @param msg CustomEvent containing gesture probability data
	 */
	export function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		if (performance.now() < timeout) return;

		displayChar = currentChar || WAITING_EMOJI;

		const currentCharSanitized = removeDiacritics(currentChar)
		const result = msg.detail;

		if (currentChar && result.filter(x=> x.letter === currentCharSanitized).length > 0) {
			handleSuccessfulRecognition();
		}

		timeout = performance.now() + RECOGNITION_DELAY / speed;
	}

	/**
	 * Handles successful gesture recognition
	 */
	function handleSuccessfulRecognition() {
		displayChar = SUCCESS_EMOJI;
		currentChar = '';
		setTimeout(() => nextChar(), NEXT_CHAR_DELAY / speed);
	}

	/**
	 * Removes diacritical marks from input string
	 * @param inputString String to process
	 * @returns String without diacritical marks
	 */
	function removeDiacritics(inputString: string): string {
		return inputString.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
	}

	let currentChar: string = '';
	let displayChar: string = WAITING_EMOJI;

	/**
	 * Starts the recognition process with either default or custom text
	 */
	function start() {
		customString = keepOnlyLetters(customString);
		text = customString.length > 0 ? customString.replace(' ', '') : DEFAULT_STRING;

		nextChar();
	}

	/**
	 * Replays the animation for current character
	 */
	function replay() {
		model.playAnimationForText(currentChar, Language.CzechFingerOneHand);
	}

	/**
	 * Processes and displays/plays the next character in the sequence
	 * Handles special cases like 'Ch' digraph and non-letter characters
	 */
	function nextChar() {
		if (text.length == 0) {
			displayMessage("Správně!");
			return;
		}

		displayChar = WAITING_EMOJI;

		timeout = performance.now() + NEXT_CHAR_DELAY / speed;

		// Process next character
		let nextChar = getNextValidChar();

		// Handle 'Ch'
		if (nextChar == 'C' && text.length > 1 && text[1].toUpperCase() == 'H') {
			currentChar = 'Ch';
			text = text.slice(1);
		}

		currentChar = nextChar;
		text = text.slice(1);

		model.playAnimationForText(currentChar, Language.CzechFingerOneHand);
	}

	/**
	 * Gets the next valid character from the text
	 * Skips non-letter characters
	 */
	function getNextValidChar(): string {
		let char = text[0].toUpperCase();

		// Skip non-letter characters
		while (char.toLowerCase() === char.toUpperCase() && text.length > 1) {
			text = text.slice(1);
			char = text[0].toUpperCase();
		}

		return char;
	}

	function displayMessage(msg : string) {
		alertMessage = msg;
		messageVisible = true;
		setTimeout(() => {
			messageVisible = false;
		}, SUCCESS_MESSAGE_DURATION);
	}
</script>

<div class="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm space-y-4 relative">
	<!-- Controls -->
	<div class="space-y-3">
		<p class="text-sm text-gray-600 dark:text-gray-400">
			Pro správnou funkčnost držte stále zobrazenou dlaň na kameře.
		</p>

		<Input
			type="text"
			bind:value={customString}
			placeholder={DEFAULT_STRING}
			class="w-full"
		/>

		<div class="grid grid-cols-2 gap-3">
			<Button color="primary" class="w-full" on:click={start}>
				Spustit
			</Button>
			<Button color="blue" class="w-full" on:click={replay}>
				Přehrát znovu
			</Button>
		</div>
	</div>

	<!-- Character Display -->
	<p class="text-center">
		<strong class="text-6xl font-bold text-gray-900 dark:text-white block mt-4">
			{displayChar}
		</strong>
	</p>

	<!-- Success Message -->
	{#if messageVisible}
		<div class="absolute top-0 left-0 m-auto w-fit">
			<Alert color="green" class="shadow-lg text-xl" >
				{alertMessage}
			</Alert>
		</div>
	{/if}
</div>