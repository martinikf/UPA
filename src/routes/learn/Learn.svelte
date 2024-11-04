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

<h2>Učit</h2>
<p>
	Bude vám zobrazeno písmeno/znak, zkuste si jej co nejlépe zapomatovat. <br />
	Po stisknutí tlačítka "Už umím" jej budete vídat v oblasti procvičování.
</p>

<div class="language_selection">
	<label for="language">Jazyk:</label>
	<select id="language" bind:value={selectedLanguageSet} on:change={onLanguageChange}>
		<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
		<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda obouruční</option>
		<option value={Language.Czech}>Český znakový jazyk</option>
	</select>
</div>

{#if everythingLearned}
	<h3>Všechno jste se naučili!</h3>
{/if}

{#if !everythingLearned}
	<h3>Učíte se: {languageSet[currentIndex].str}</h3>
{/if}

<div class="control_buttons">
	<button on:click={play} disabled={everythingLearned}>Přehrát znovu</button>

	<button on:click={markAsLearned} disabled={everythingLearned}>Už umím!</button>
</div>

<style>
	h2 {
		margin-top: 0;
	}

	.control_buttons button {
		display: block;
		padding: 5px;
		margin-bottom: 0.5rem;
	}

	.language_selection select {
		padding: 5px;
	}

	@media (max-width: 768px) {
		.control_buttons {
			display: flex;
			flex-direction: column;
		}
	}
</style>
