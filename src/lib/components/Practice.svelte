<script lang="ts">
	/**
	 * Svelte component for controlling the animation for the purpose Practicing
	 * Randomly selected word is played in the animation
	 * and user has to correctly guess what the word was
	 *
	 * Language selection, replay capability
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Language } from '$lib/components/models/Word';

	export let model: Model;

	/** Path to the file with words */
	const wordFilePath : string = '/CzechWords.txt';

	// Internal state variables
	/** Variable for storing loaded list of words */
	let words: string[] = [];
	/** Randomly selected word */
	let randomWord: string = '';

	/** User's text input (word guess) */
	let textInput: string = '';
	/** Selected language set */
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;

	/**
	 * Selects random word from words list and plays animation
	 * If the word list is empty, loads words
	 */
	function newWordOnClick() {
		if (words.length < 1) {
			console.log('Loading words');
			return loadWords();
		}

		randomWord = words[Math.floor(Math.random() * words.length)].trim();
		console.log(randomWord);
		model.playAnimationForText(randomWord, selectedLanguageSet);
	}

	/**
	 * Checks if the user's input is correct
	 * Trims the input and ignores case
	 */
	function checkAnswer() {
		if (textInput.length < 1) {
			alert('Napište slovo, které jste viděli.');
			return;
		}

		if (textInput.trim().toUpperCase() === randomWord.toUpperCase()) {
			alert('Správně!');
		} else {
			alert('Špatně!');
		}
	}

	/**
	 * Resets the animation and plays it again
	 */
	function replay() {
		model.resetAnimation();
		setTimeout(() => {
			model.playAnimationForText(randomWord, selectedLanguageSet);
		}, 500);
	}

	/**
	 * Loads words from the file to words variable
	 */
	function loadWords() {
		fetch(wordFilePath)
			.then((res) => res.text())
			.then((text) => {
				words = text.split('\n');
				newWordOnClick();
			})
			.catch((e) => console.error(e));
	}
</script>

<!-- Control block with language selection, text input and buttons -->
<div class="controls">
	<div class="language_selection">
		<label for="language">Jazyk:</label>
		<select id="language" bind:value={selectedLanguageSet}>
			<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
			<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda obouruční</option>
			<option value={Language.Czech}>Český znakový jazyk</option>
		</select>
	</div>

	<button
		on:click={() => {
			newWordOnClick();
		}}
	>
		Vytvořit nové náhodné slovo
	</button>

	<input bind:value={textInput} placeholder="Zde napište zobrazené slovo..." />

	<button
		on:click={() => {
			checkAnswer();
		}}
	>
		Zkontrolovat
	</button>

	<button
		on:click={() => {
			replay();
		}}
	>
		Přehrát slovo znovu
	</button>
</div>

<style>
	:global(body) {
		margin: 0;
	}

	.controls {
		display: grid;
		grid-template-columns: 1fr;
		padding: 5px;
	}

	.controls > * {
		padding: 5px;
		margin-bottom: 10px;
	}

	.language_selection select {
		padding: 5px;
	}
</style>
