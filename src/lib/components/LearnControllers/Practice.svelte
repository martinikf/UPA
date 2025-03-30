<script lang="ts">
	/**
	 * Svelte component for the "Procvičovat" (Practice/Review) mode within the Learn section.
	 *
	 * Allows users to practice recognizing signs or words they have previously learned (or all signs).
	 * Displays an animation for a randomly selected word/sign from the chosen language set.
	 * The user types their answer, and the component provides feedback on correctness.
	 *
	 * @prop {Model} model - Instance of the AnimatedModel component for displaying animations.
	 * @prop {Word[]} data - Array containing all available Word objects (signs/vocabulary).
	 */

	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import { Word, Language } from '$lib/models/Word';
	import { Alert, Button, Checkbox, Heading, Input, P } from 'flowbite-svelte';
	import { replaceCzechDiacriticsAndNormalize } from '$lib/helpers/TextHelper';
	import LanguageSelector from '$lib/components/Shared/LanguageSelector.svelte';

	// Component props
	/** Instance of the AnimatedModel component, passed as a prop. */
	export let model: Model;
	/** Array containing all available Word objects, passed as a prop. */
	export let data: Word[];

	// State variables
	let sentence: string = '';
	let copyData = [...data.filter((item: Word) => item.learned)];

	let practiceAllSigns: boolean = false;

	let messageVisible : boolean = false;
	let messageString : string = '';
	let messageColor : string = '';

	/**
	 * Pre-filtered dictionary containing only the learned words, organized by language.
	 * Used for efficient random selection when practicing only learned items.
	 */
	const learnedLanguageSets = {
		[Language.CzechFingerOneHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerOneHand
		),
		[Language.CzechFingerTwoHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerTwoHand
		),
		[Language.Czech]: copyData.filter((item: Word) => item.language === Language.Czech)
	};

	/**
	 * Pre-filtered dictionary containing all words (learned and unlearned), organized by language.
	 * Used for efficient random selection when practicing all items.
	 */
	const allLanguageSets = {
		[Language.CzechFingerOneHand]: data.filter(
			(item: Word) => item.language === Language.CzechFingerOneHand
		),
		[Language.CzechFingerTwoHand]: data.filter(
			(item: Word) => item.language === Language.CzechFingerTwoHand
		),
		[Language.Czech]: data.filter((item: Word) => item.language === Language.Czech)
	};

	// User input state
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;
	let userInput: string = '';

	/**
	 * Validates the user's input against the currently displayed sentence.
	 * Normalizes both strings (removes diacritics, converts to lowercase) before comparison.
	 * Shows a temporary success or failure message. Clears input field on success.
	 */
	function checkAnswer() {
		const normalizedInput = replaceCzechDiacriticsAndNormalize(userInput);
		const normalizedSentence = replaceCzechDiacriticsAndNormalize(sentence);

		if (normalizedInput === normalizedSentence) {
			displayMessage("Správně", "green");
			userInput = '';
		} else {
			displayMessage("Špatně", "red");
		}
	}

	/**
	 * Displays a feedback message (Alert) for a short duration.
	 * @param str - The message string to display.
	 */
	function displayMessage(str: string, color: string){
		messageString = str;
		messageColor = color;

		messageVisible = true;
		setTimeout(() => {
			messageVisible = false;
		}, 3000);
	}

	/**
	 * Selects and displays a new word/sign based on the current settings.
	 * Chooses either from all signs or only learned signs depending on the `practiceAllSigns` flag.
	 */
	function createNewSentence(){
		if (practiceAllSigns) {
			createNewAllSignsSentence();
		} else {
			createNewLearnedSentence();
		}
	}

	/**
	 * Selects a random word/sign from all available items in the selected language set,
	 * updates the `sentence` state, and plays its animation.
	 */
	function createNewAllSignsSentence() {
		let randomIndex = Math.floor(Math.random() * allLanguageSets[selectedLanguageSet].length);
		sentence = allLanguageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	/**
	 * Selects a random word/sign from the learned items in the selected language set,
	 * updates the `sentence` state, and plays its animation.
	 * Handles the case where no items have been learned yet for the selected language.
	 */
	function createNewLearnedSentence() {
		if (learnedLanguageSets[selectedLanguageSet].length === 0) {
			return;
		}

		let randomIndex = Math.floor(Math.random() * learnedLanguageSets[selectedLanguageSet].length);
		sentence = learnedLanguageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	/**
	 * Replays the animation for the currently active sentence.
	 * Does nothing if no sentence is currently active.
	 */
	function replayAnimation(): void {
		model.playAnimationForText(sentence, selectedLanguageSet);
	}
</script>

<div class="max-w-7xl mx-auto px-4 pb-8 space-y-6 relative">
	<Heading tag="h2" class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Procvičovat</Heading>

	<P class="text-gray-600 dark:text-gray-400 mb-6">
		Zapište do&nbsp;pole text, který Vám byl zobrazen. Poté stiskněte tlačítko zkontrolovat.
	</P>

	<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-6">
		<!-- Language Selection -->
		<LanguageSelector bind:selectedLanguageSet={selectedLanguageSet} />

		<!-- Control Buttons -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<Button
				color="primary"
				class="w-full"
				disabled={(learnedLanguageSets[selectedLanguageSet].length === 0 && !practiceAllSigns)}
				on:click={createNewSentence}
			>
				Spustit
			</Button>

			<Button
				color="blue"
				class="w-full"
				on:click={replayAnimation}
				disabled={sentence.length < 1}
			>
				Přehrát znovu
			</Button>
		</div>

		<div>
			<Checkbox bind:checked={practiceAllSigns}>Zahrnout nenaučené znaky</Checkbox>
		</div>

		<!-- Input Group -->
		<div class="grid grid-cols-1 md:grid-cols-5 gap-4">
			<div class="md:col-span-3">
				<Input
					id="text"
					type="text"
					bind:value={userInput}
					placeholder="Zde napište znakované slovo"
					class="w-full"
				/>
			</div>
			<Button
				color="green"
				class="w-full md:col-span-2"
				on:click={checkAnswer}
				disabled={userInput.length < 1 || sentence.length < 1}
			>
				Zkontrolovat
			</Button>
		</div>
	</div>

	{#if messageVisible}
		<div class="m-auto w-fit absolute top-1/4 left-1/4">
			<Alert color="{messageColor}" class="shadow-lg text-xl" >
				{messageString}
			</Alert>
		</div>
	{/if}
</div>


