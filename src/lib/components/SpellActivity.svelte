<script lang="ts">
	/**
	 * Svelte component for controlling sign language animation and webcam recognition.
	 * Handles word generation, gesture recognition, and animation playback.
	 * This component supports only Czech one hand finger alphabet.
	 *
	 * Used for practicing signing.
	 * User tries to sign the created word and webcam recognition tries to detect it.
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */

	import Model from './AnimatedModel.svelte';
	import type { GestureProbability } from '$lib/components/models/GestureProbability';
	import { Language } from '$lib/components/models/Word';

	// Component props
	export let model: Model;

	// Constants
	const DETECTION_DELAY = 750; // ms
	const WORDS_FILE_PATH = '/CzechWords.txt';
	const SUCCESS_MESSAGE_DURATION = 3000;

	// User input
	let customWord: string = '';

	// State variable to control visibility of success message
	let successMessageVisible: boolean = false;

	// Container for loaded words from external source
	let words: string[] = [];

	// State management
	interface State {
		currentLetterIndex: number;
		guessedLetters: string;
		lastDetectionTime: number;
		wordToGuess: string;
	}

	// Initialize state with default values
	const state: State = {
		currentLetterIndex: 0,
		guessedLetters: '',
		lastDetectionTime: 0,
		wordToGuess: ''
	};

	/**
	 * Displays a success message for a few seconds
	 */
	function displaySuccessMessage() {
		successMessageVisible = true;
		setTimeout(() => {
			successMessageVisible = false;
		}, SUCCESS_MESSAGE_DURATION);
	}

	/**
	 * Handles gesture recognition results from webcam
	 * Validates detected gestures against the current letter being tested
	 * @param msg CustomEvent containing gesture probability data
	 */
	export function handleMessage(msg: CustomEvent<GestureProbability>) {
		if (!state.wordToGuess) return;

		const result = msg.detail;
		if (performance.now() < state.lastDetectionTime + DETECTION_DELAY) return;

		const currentLetter = getCurrentLetter();
		if (!currentLetter) return;

		if (result[removeDiacritics(currentLetter)]) {
			updateProgress(currentLetter);
			checkCompletion();
		}
	}

	/**
	 * Gets the current letter to be recognized, handling special cases like 'Ch'
	 */
	function getCurrentLetter(): string {
		const letter = state.wordToGuess[state.currentLetterIndex]?.toUpperCase();
		if (!letter) return '';

		// Handle special case for 'Ch' digraph
		if (
			letter === 'C' &&
			state.currentLetterIndex < state.wordToGuess.length - 1 &&
			state.wordToGuess[state.currentLetterIndex + 1].toUpperCase() === 'H'
		) {
			return 'Ch';
		}
		return letter;
	}

	/**
	 * Updates progress after successful letter recognition
	 * @param recognizedLetter The letter that was successfully recognized
	 */
	function updateProgress(recognizedLetter: string) {
		if (recognizedLetter === 'Ch') state.currentLetterIndex++;
		state.currentLetterIndex++;
		state.guessedLetters = state.wordToGuess.substring(0, state.currentLetterIndex);
		state.lastDetectionTime = performance.now();
	}

	/**
	 * Checks if the word has been completely recognized
	 */
	function checkCompletion() {
		if (state.currentLetterIndex >= state.wordToGuess.length) {
			resetProgress();
			displaySuccessMessage();
		}
	}

	/**
	 * Resets progress tracking
	 */
	function resetProgress() {
		state.currentLetterIndex = 0;
		state.guessedLetters = '';
	}

	/**
	 * Removes diacritical marks from input string
	 * @param inputString String to process
	 * @returns String without diacritical marks
	 */
	function removeDiacritics(inputString: string): string {
		return inputString.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
	}

	/**
	 * Generates a new random word from the loaded word list
	 */
	async function newWordOnClick() {
		resetWord();
		if (words.length < 1) {
			console.log('Loading words');
			await loadWords();
		}
		state.wordToGuess = words[Math.floor(Math.random() * words.length)]?.trim() ?? '';
	}

	/**
	 * Sets a custom word for practice
	 */
	function customWordOnClick() {
		resetWord();
		state.wordToGuess = customWord;
	}

	/**
	 * Resets the current word state
	 */
	function resetWord() {
		state.wordToGuess = '';
		resetProgress();
	}

	/**
	 * Loads word list from file
	 */
	async function loadWords() {
		// Load words from file
		fetch(WORDS_FILE_PATH)
			.then((res) => res.text())
			.then((text) => {
				words = text.split('\n');
				newWordOnClick();
			})
			.catch((e) => console.error(e));
	}

	/**
	 * Triggers animation playback for current word
	 */
	function showWord() {
		model.playAnimationForText(state.wordToGuess, Language.CzechFingerOneHand);
	}
</script>

<!-- Success message overlay, visible when user guesses correctly -->
<div class="container">
	<div class="controls">
		<p>Aktuální slovo: <strong id="word">{state.wordToGuess}</strong></p>
		<p>Správně znakovaná písmena: <strong id="currentWord">{state.guessedLetters}</strong></p>

		<div class="controls_grid">
			<button on:click={newWordOnClick}>Vytvořit nové náhodné slovo</button>

			<div class="gap"></div>

			<input type="text" placeholder="Vlastní slovo..." bind:value={customWord} />
			<button on:click={customWordOnClick} disabled={customWord.length < 1}>
				Nastavit vlastní slovo
			</button>

			<div class="gap"></div>

			<button on:click={showWord}> Ukázat slovo v animaci </button>
		</div>
	</div>

	<!-- Notification message signaling success -->
	{#if successMessageVisible}
		<div class="success-overlay">
			<p>Slovo bylo správně vyznakováno!</p>
		</div>
	{/if}
</div>

<style>
	.controls {
		padding: 5px;
	}
	.controls_grid {
		display: grid;
		grid-template-columns: 1fr;
	}
	.controls_grid > * {
		padding: 5px;
		margin-bottom: 10px;
	}
	.gap {
		height: 5px;
		border-bottom: solid black 3px;
	}

	.container {
		position: relative;
	}

	.success-overlay {
		position: absolute;
		top: -1rem;
		right: -1rem;
	}

	@media (max-width: 768px) {
		.success-overlay {
			position: absolute;
			top: -1rem;
			right: 0;
		}
	}
</style>
