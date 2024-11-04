<script lang="ts">
	/**
	 * Component for displaying and managing sign language alphabet and words for teach mode
	 * Features:
	 * - Displays one-handed and two-handed finger alphabets
	 * - Shows basic Czech sign language signs
	 * - Tracks learning progress
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 * Requires data - list of Words
	 */

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Language, Word } from '$lib/models/Word';

	export let model: Model;
	export let data: Word[];

	// Constants
	const MOBILE_BREAKPOINT = 768;
	const MOBILE_DELAY = 500;

	// State
	let wordsToShow = [...data];
	let rerender = 0; // Used only to force rerender of DOM part
	let searchInput: string = '';

	/**
	 * Plays animation for the selected text with delay on smaller screens
	 * @param txt Text to animate
	 * @param language Language enum value
	 */
	function animate(txt: string, language: Language) {
		// delay the animation on mobile size screens
		// assume that users has to scroll
		let delay = 0;
		if (window.innerWidth < MOBILE_BREAKPOINT) delay = MOBILE_DELAY;

		setTimeout(() => {
			model.playAnimationForText(txt, language);
		}, delay);
	}

	/**
	 * Filters words based on search input
	 * Is fired on change of search input
	 */
	function SearchInputOnChange() {
		if (searchInput.length > 0) {
			wordsToShow = data.filter((word) => {
				return word.str.includes(searchInput);
			});
		} else {
			wordsToShow = [...data];
		}
	}

	/**
	 * Marks words or letters as learned
	 * For words: marks only the specific word
	 * For letters: marks all previous letters in sequence as well
	 * @param word Word to mark as learned
	 */
	function markAsLearned(word: Word) {
		if (word.language === Language.Czech) {
			markSingleWord(word);
		} else {
			markLetterSequence(word);
		}
		rerender++;
	}

	/**
	 * Marks a single word as learned
	 * @param word Word to mark
	 */
	function markSingleWord(word: Word): void {
		word.learned = true;
	}

	/**
	 * Marks all letters up to and including the selected letter as learned
	 * @param targetLetter Letter to mark along with previous letters
	 */
	function markLetterSequence(targetLetter: Word): void {
		const sameLanguageWords = data.filter((w) => w.language === targetLetter.language);

		for (const letter of sameLanguageWords) {
			letter.learned = true;
			if (letter.str === targetLetter.str) break;
		}
	}
</script>

<h2>Přehled</h2>
<p>
	Zde vidíte všechny znaky, nezašedlé položky již umíte. <br />
	Pro přehrání daného znaku klikněte na něj. <br />
	Pokud jste již v minulosti tento režim použili, dvojklikem na slovo se jej rovnou naučíte.
</p>

{#key rerender}
	<h3>Česká jednoruční prstová abeceda</h3>
	<div class="letters">
		{#each data as letter}
			{#if letter.language === Language.CzechFingerOneHand}
				<button
					class="letter"
					class:learned={letter.learned}
					on:dblclick={() => {
						markAsLearned(letter);
					}}
					on:click={() => {
						animate(letter.str, letter.language);
					}}
				>
					{letter.str}
				</button>
			{/if}
		{/each}
	</div>

	<h3>Česká obouruční prstová abeceda</h3>
	<div class="letters">
		{#each data as letter}
			{#if letter.language === Language.CzechFingerTwoHand}
				<button
					class="letter"
					class:learned={letter.learned}
					on:dblclick={() => {
						markAsLearned(letter);
					}}
					on:click={() => {
						animate(letter.str, letter.language);
					}}
				>
					{letter.str}
				</button>
			{/if}
		{/each}
	</div>

	<hr />
	<div>
		<h3>Základní znaky ČZJ</h3>
		<input
			type="text"
			class="text_input"
			placeholder="Vyhledávač..."
			on:keyup={SearchInputOnChange}
			bind:value={searchInput}
		/>

		<div class="words">
			{#each wordsToShow as word}
				{#if word.language == Language.Czech}
					<button
						class="word"
						class:learned={word.learned}
						on:dblclick={() => {
							markAsLearned(word);
						}}
						on:click={() => {
							animate(word.str, word.language);
						}}
					>
						{word.str}
					</button>
				{/if}
			{/each}
		</div>
	</div>
{/key}

<style>
	h2 {
		margin-top: 0;
	}

	.letters {
		display: flex;
		flex-wrap: wrap;
		padding-left: 0.5rem;
		padding-right: 0.5rem;
	}

	.words {
		display: flex;
		flex-wrap: wrap;
		padding-left: 0.5rem;
		padding-right: 0.5rem;
	}

	.word,
	.letter {
		border: none;
		outline: none;
		margin-right: 0.25rem;
		margin-bottom: 0.25rem;
		padding: 0.5rem;
		min-width: 2rem;
	}

	.letter {
		font-weight: bold;
	}

	.learned {
		background-color: green;
	}

	.word:hover,
	.letter:hover {
		cursor: pointer;
	}

	.text_input {
		display: block;
		width: 95%;
		margin: auto auto 1rem;
	}

	@media (max-width: 768px) {
		.text_input {
			margin-bottom: 1rem;
		}

		.word,
		.letter {
			padding: 5px;
		}
	}
</style>
