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
	import { Language } from '$lib/models/Word';
	import { Button, Input, Label, Select } from 'flowbite-svelte';

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

<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-4">
	<!-- Language Selection -->
	<div>
		<Label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Jazyk:</Label>

		<Select id="language"
						bind:value={selectedLanguageSet}
						placeholder="Prosím zvolte jeden jazyk">
			<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
			<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda dvouruční</option>
			<option value={Language.Czech}>Český znakový jazyk</option>
		</Select>
	</div>


	<!-- Control Buttons -->
	<div class="space-y-3">
		<Button
			color="primary"
			class="w-full"
			on:click={newWordOnClick}
		>
			Vytvořit nové náhodné slovo
		</Button>

		<Input
			bind:value={textInput}
			placeholder="Zde napište zobrazené slovo..."
			class="w-full"
		/>

		<div class="grid grid-cols-2 gap-3">
			<Button
				color="green"
				class="w-full"
				on:click={checkAnswer}
			>
				Zkontrolovat
			</Button>

			<Button
				color="blue"
				class="w-full"
				on:click={replay}
			>
				Přehrát slovo znovu
			</Button>
		</div>
	</div>
</div>