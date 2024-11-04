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

	/**
	 * Handles gesture recognition events from webcam
	 * @param msg CustomEvent containing gesture probability data
	 */
	export function handleMessage(msg: CustomEvent<GestureProbability>) {
		if (performance.now() < timeout) return;

		displayChar = currentChar || WAITING_EMOJI;

		const result = msg.detail;
		if (currentChar && result[removeDiacritics(currentChar)]) {
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
			alert('Konec');
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
</script>

<div class="controls">
	<p class="instruction-text">Pro správnou funkčnost držte stále zobrazenou dlaň na kameře.</p>
	<input type="text" bind:value={customString} placeholder={DEFAULT_STRING} />
	<button on:click={start}>Spustit</button>
	<button on:click={replay}>Přehrát znovu</button>
</div>

<p class="text">
	<strong class="char_to_show">
		{displayChar}
	</strong>
</p>

<style>
	.controls {
		padding: 5px;
		display: grid;
		grid-template-columns: 1fr;
	}

	.controls > * {
		padding: 5px;
		margin-bottom: 10px;
	}

	.text {
		text-align: center;
	}

	.char_to_show {
		font-size: 3em;
		font-weight: bold;
	}
</style>
