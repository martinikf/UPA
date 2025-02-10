<script lang="ts">
	/**
	 * Component for practicing learned signs
	 *
	 * Requires model and data
	 */

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Word, Language } from '$lib/models/Word';
	import { Button, Heading, Input, Label, P, Select } from 'flowbite-svelte';

	// Component props
	export let model: Model;
	export let data: Word[];

	// State variables
	let sentence: string = '';
	let copyData = [...data.filter((item: Word) => item.learned)];

	/**
	 * Organizes words by language type for easier filtering and access
	 * Creates a dictionary with language types as keys and filtered word arrays as values
	 */
	const languageSets = {
		[Language.CzechFingerOneHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerOneHand
		),
		[Language.CzechFingerTwoHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerTwoHand
		),
		[Language.Czech]: copyData.filter((item: Word) => item.language === Language.Czech)
	};

	// User input
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;
	let userInput: string = '';

	/**
	 * Validates user input against the current sentence
	 * Shows success/failure message and clears input on success
	 */
	function checkAnswer() {
		const normalizedInput = userInput.trim().toLowerCase();
		const normalizedSentence = sentence.trim().toLowerCase();

		if (normalizedInput === normalizedSentence) {
			alert('Správně!');
			userInput = '';
		} else {
			alert('Špatně!');
		}
	}

	/**
	 * Generates a new random sentence from the selected language set
	 * Plays the corresponding animation
	 */
	function createNewSentence() {
		if (languageSets[selectedLanguageSet].length === 0) {
			alert('Nemáte žádné slova pro tento jazyk');
			return;
		}

		let randomIndex = Math.floor(Math.random() * languageSets[selectedLanguageSet].length);
		sentence = languageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	/**
	 * Replays the current sentence animation
	 */
	function replayAnimation(): void {
		model.playAnimationForText(sentence, selectedLanguageSet);
	}
</script>

<div class="max-w-7xl mx-auto px-4 pb-8 space-y-6">
	<Heading tag="h2" class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Procvičovat</Heading>

	<P class="text-gray-600 dark:text-gray-400 mb-6">
		Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko
		zkontrolovat.
	</P>

	<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-6">
		<!-- Language Selection -->
		<div>
			<Label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Jazyk:</Label>
			<Select
				id="language"
				bind:value={selectedLanguageSet}
				class="w-full"
			>
				<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
				<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda dvouruční</option>
				<option value={Language.Czech}>Český znakový jazyk</option>
			</Select>
		</div>

		<!-- Control Buttons -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<Button
				color="primary"
				class="w-full"
				disabled={languageSets[selectedLanguageSet].length === 0}
				on:click={createNewSentence}
			>
				Spustit novou větu
			</Button>

			<Button
				color="blue"
				class="w-full"
				on:click={replayAnimation}
			>
				Přehrát znovu
			</Button>
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
			>
				Zkontrolovat
			</Button>
		</div>
	</div>
</div>
