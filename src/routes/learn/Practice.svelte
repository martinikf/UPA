<script lang="ts">
	/**
	 * Component for practicing learned signs
	 *
	 * Requires model and data
	 */

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Word, Language } from '$lib/models/Word';
	import { Alert, Button, Checkbox, Heading, Input, P } from 'flowbite-svelte';
	import { replaceCzechDiacriticsAndNormalize } from '$lib/helpers/TextHelper';
	import LanguageSelector from '$lib/components/shared/LanguageSelector.svelte';

	// Component props
	export let model: Model;
	export let data: Word[];

	// State variables
	let sentence: string = '';
	let copyData = [...data.filter((item: Word) => item.learned)];

	let practiceAllSigns: boolean = false;

	let messageVisible : boolean = false;
	let messageString : string = '';

	/**
	 * Organizes words by language type for easier filtering and access
	 * Creates a dictionary with language types as keys and filtered word arrays as values
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

	const allLanguageSets = {
		[Language.CzechFingerOneHand]: data.filter(
			(item: Word) => item.language === Language.CzechFingerOneHand
		),
		[Language.CzechFingerTwoHand]: data.filter(
			(item: Word) => item.language === Language.CzechFingerTwoHand
		),
		[Language.Czech]: data.filter((item: Word) => item.language === Language.Czech)
	};

	// User input
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;
	let userInput: string = '';

	/**
	 * Validates user input against the current sentence
	 * Shows success/failure message and clears input on success
	 */
	function checkAnswer() {
		const normalizedInput = replaceCzechDiacriticsAndNormalize(userInput);
		const normalizedSentence = replaceCzechDiacriticsAndNormalize(sentence);

		if (normalizedInput === normalizedSentence) {
			displayMessage("Správně");
			userInput = '';
		} else {
			displayMessage("Špatně");
		}
	}

	function displayMessage(str: string){
		messageString = str;

		messageVisible = true;
		setTimeout(() => {
			messageVisible = false;
		}, 3000);
	}


	function createNewSentence(){
		if (practiceAllSigns) {
			createNewAllSignsSentence();
		} else {
			createNewLearnedSentence();
		}
	}

	function createNewAllSignsSentence() {
		let randomIndex = Math.floor(Math.random() * allLanguageSets[selectedLanguageSet].length);
		sentence = allLanguageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	/**
	 * Generates a new random sentence from the selected language set
	 * Plays the corresponding animation
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
	 * Replays the current sentence animation
	 */
	function replayAnimation(): void {
		model.playAnimationForText(sentence, selectedLanguageSet);
	}
</script>

<div class="max-w-7xl mx-auto px-4 pb-8 space-y-6 relative">
	<Heading tag="h2" class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Procvičovat</Heading>

	<P class="text-gray-600 dark:text-gray-400 mb-6">
		Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko
		zkontrolovat.
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
			<Alert color="green" class="shadow-lg text-xl" >
				{messageString}
			</Alert>
		</div>
	{/if}
</div>


