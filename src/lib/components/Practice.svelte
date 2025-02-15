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
	import { Alert, Button, Input } from 'flowbite-svelte';
	import { replaceCzechDiacriticsAndNormalize } from '$lib/helpers/TextHelper';
	import LanguageSelector from '$lib/components/shared/LanguageSelector.svelte';

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

	let messageVisible: boolean = false;
	const SUCCESS_MESSAGE_DURATION = 3000;
	let alertMessage : string = "";

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
			displayMessage("Napište slovo, které jste viděli");
			return;
		}

		if(replaceCzechDiacriticsAndNormalize(textInput) === replaceCzechDiacriticsAndNormalize(randomWord)) {
			displayMessage("Správně!");
			textInput = '';
			randomWord = '';
		} else {
			displayMessage("Chyba, zkuste to znovu.")
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

	function giveUp(){
		displayMessage(`Správné slovo bylo: ${randomWord}`);
	}

	/**
	 * Displays a success message for a few seconds
	 */
	function displayMessage(msg : string) {
		alertMessage = msg;
		messageVisible = true;
		setTimeout(() => {
			messageVisible = false;
		}, SUCCESS_MESSAGE_DURATION);
	}
</script>

<div class="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm space-y-4 relative">

	<LanguageSelector bind:selectedLanguageSet={selectedLanguageSet}/>

	<!-- Control Buttons -->
	<div class="space-y-3">
		<Button
			color="green"
			class="w-full"
			on:click={newWordOnClick}
		>
			Vytvořit nové náhodné slovo
		</Button>

		<Input
			bind:value={textInput}
			placeholder="Zde napište zobrazené slovo"
			class="w-full"
		/>

		<div class="grid grid-cols-2 gap-3">
			<Button
				color="primary"
				class="w-full col-span-2"
				on:click={checkAnswer}
				disabled={randomWord.length < 1}
			>
				Zkontrolovat
			</Button>

			<Button
				color="blue"
				class="w-full"
				on:click={replay}
				disabled={randomWord.length < 1}
			>
				Přehrát znovu
			</Button>

			<Button
				color="red"
				class="w-full"
				on:click={giveUp}
				disabled={randomWord.length < 1}
			>
				Prozradit
			</Button>
		</div>
	</div>

	<!-- Success Message -->
	{#if messageVisible}
		<div class="absolute top-0 left-0 m-auto w-fit">
			<Alert color="green" class="shadow-lg text-xl" >
				{alertMessage}
			</Alert>
		</div>
	{/if}
</div>