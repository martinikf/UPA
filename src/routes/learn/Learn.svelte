<script lang="ts">
	/**
	 * Component for learning sign language through interactive animations
	 *
	 * Features:
	 * - Progressive learning of signs/words
	 * - Supports multiple sign language variants
	 * - Tracks learning progress
	 * - Interactive replay and marking words as learned
	 *
	 * Learned signs can be practiced and reviewed in other modes
	 *
	 *
	 * Requires Model and Data
	 */

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Language, Word } from '$lib/models/Word';
	import { Button, Heading, Label, P, Select } from 'flowbite-svelte';

	// Component props
	export let model: Model;
	export let data: Word[];

	// Component state
	let languageSet: Word[] = []; // Filtered subset of words for current language
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;
	let currentIndex = -1; // Index of current word being learned
	let playCount = 0; // Number of times current word has been played
	let everythingLearned = false;

	/**
	 * Plays animation for a given word
	 * @param word - Word object containing text and language information
	 */
	function animate(word: Word | null) {
		if (word == null) return;

		model.playAnimationForText(word.str, word.language);
	}

	/**
	 * Finds the index of the first unlearned word in the current language set
	 * @returns {number} Index of first unlearned word, or length of language set if all words are learned
	 */
	function firstUnlearned(): number {
		let j: number = 0;
		while (languageSet.length > j && languageSet[j].learned) {
			j++;
		}

		return j;
	}

	/**
	 * Updates the language set based on the selected language
	 * Filters the main data array to include only words of the selected language
	 */
	function updateLanguageSet() {
		languageSet = data.filter((word) => word.language == selectedLanguageSet);
	}

	/**
	 * Main learning function that manages the learning flow
	 * - Initializes language set if empty
	 * - Finds first unlearned word if needed
	 * - Plays animation for current word
	 * - Updates learning progress
	 */
	function play() {
		if (languageSet.length == 0) updateLanguageSet();

		if (currentIndex == -1) currentIndex = firstUnlearned();

		if (languageSet.length == currentIndex) {
			everythingLearned = true;
			return;
		}

		animate(languageSet[currentIndex]);
		playCount++;
	}

	/**
	 * Handles marking current word as learned
	 * - Validates that a word is currently selected and has been played
	 * - Updates word status and moves to next word
	 * - Automatically plays next word animation
	 */
	function markAsLearned() {
		if (currentIndex == -1 || playCount < 1) return;

		languageSet[currentIndex].learned = true;
		playCount = 0;
		currentIndex = currentIndex + 1;

		//If word is learned, play animation for the next word
		play();
	}

	/**
	 * Handles language selection change
	 * - Resets all learning progress states
	 * - Starts learning process for new language
	 */
	function onLanguageChange() {
		currentIndex = -1;
		playCount = 0;
		languageSet = [];
		everythingLearned = false;
		play();
	}

	play();
</script>
<div class="max-w-7xl mx-auto px-4 pb-8 space-y-6">
	<Heading tag="h2" class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Učit</Heading>

	<P class="text-gray-600 dark:text-gray-400 mb-6">
		Bude vám zobrazeno písmeno/znak, zkuste si jej co nejlépe zapamatovat.<br>
		Po stisknutí tlačítka "Už umím" jej budete vídat v oblasti procvičování.
	</P>

	<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm mb-6">
		<div class="space-y-4">
			<div>
				<Label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Jazyk:</Label>
				<Select id="language"
								bind:value={selectedLanguageSet} on:change={onLanguageChange}
								placeholder="Prosím zvolte jeden jazyk">
					<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
					<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda dvouruční</option>
					<option value={Language.Czech}>Český znakový jazyk</option>
				</Select>
			</div>

			{#if everythingLearned}
				<Heading tag="h3" class="text-lg font-semibold text-green-600 dark:text-green-400 mb-4">
					Všechno jste se naučili!
				</Heading>
			{:else}
				<Heading tag="h3" class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
					Učíte se: {languageSet[currentIndex].str}
				</Heading>
			{/if}

			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<Button
					color="blue"
					on:click={play}
					disabled={everythingLearned}
					class="w-full {everythingLearned ? 'opacity-50 cursor-not-allowed' : ''}"
				>
					Přehrát znovu
				</Button>

				<Button
					color="green"
					on:click={markAsLearned}
					disabled={everythingLearned}
					class="w-full {everythingLearned ? 'opacity-50 cursor-not-allowed' : ''}"
				>
					Už umím!
				</Button>
			</div>
		</div>
	</div>
</div>