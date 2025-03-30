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

	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import { Language, Word } from '$lib/models/Word';
	import { Heading, Hr, Input, P } from 'flowbite-svelte';

	export let model: Model;
	export let data: Word[];


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
		model.playAnimationForText(txt, language);
	}

	/**
	 * Filters words based on search input
	 * Is fired on change of search input
	 */
	function SearchInputOnChange() {
		let sanitizedSearchInput = searchInput.toLowerCase().trim();
		if (sanitizedSearchInput.length > 0) {
			wordsToShow = data.filter((word) => {
				return word.str.toLowerCase().includes(sanitizedSearchInput);
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

<div class="max-w-7xl mx-auto px-4 pb-8 space-y-6">
	<Heading tag="h2" class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Přehled</Heading>

	<P class="text-gray-600 dark:text-gray-400 mb-6">
		Zde vidíte všechny znaky, nezašedlé položky již umíte.<br>
		Pro přehrání daného znaku klikněte na&nbsp;něj.<br>
		Pokud jste již v&nbsp;minulosti tento režim použili, dvojklikem na&nbsp;znak se daný znak označí jako již naučený.
	</P>

	<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-6">
		{#key rerender}
			<!-- Czech One-Handed Alphabet -->
			<div class="space-y-4">
				<Heading tag="h3" class="text-xl font-semibold text-gray-800 dark:text-gray-200">
					Česká jednoruční prstová abeceda
				</Heading>
				<div class="flex flex-wrap gap-2">
					{#each data as letter}
						{#if letter.language === Language.CzechFingerOneHand}
							<button
								class="px-4 py-2 rounded-lg font-semibold transition-colors
                                    {letter.learned
                                        ? 'bg-green-600 text-white'
                                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'}
                                    hover:bg-green-500 dark:hover:bg-gray-600"
								on:dblclick={() => markAsLearned(letter)}
								on:click={() => animate(letter.str, letter.language)}
							>
								{letter.str}
							</button>
						{/if}
					{/each}
				</div>
			</div>

			<!-- Czech Two-Handed Alphabet -->
			<div class="space-y-4">
				<Heading tag="h3" class="text-xl font-semibold text-gray-800 dark:text-gray-200">
					Česká dvouruční prstová abeceda
				</Heading>
				<div class="flex flex-wrap gap-2">
					{#each data as letter}
						{#if letter.language === Language.CzechFingerTwoHand}
							<button
								class="px-4 py-2 rounded-lg font-semibold transition-colors
                                    {letter.learned
                                        ? 'bg-green-600 text-white'
                                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'}
                                    hover:bg-green-500 dark:hover:bg-gray-600"
								on:dblclick={() => markAsLearned(letter)}
								on:click={() => animate(letter.str, letter.language)}
							>
								{letter.str}
							</button>
						{/if}
					{/each}
				</div>
			</div>

			<Hr class="my-6" />

			<!-- Basic CZJ Signs -->
			<div class="space-y-4">
				<Heading tag="h3" class="text-xl font-semibold text-gray-800 dark:text-gray-200">
					Základní znaky ČZJ
				</Heading>
				<Input
					type="text"
					placeholder="Vyhledávač..."
					bind:value={searchInput}
					on:keyup={SearchInputOnChange}
					class="w-full mb-4"
				/>

				<div class="flex flex-wrap gap-2">
					{#each wordsToShow as word}
						{#if word.language == Language.Czech}
							<button
								class="px-4 py-2 rounded-lg transition-colors
                                    {word.learned
                                        ? 'bg-green-600 text-white'
                                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'}
                                    hover:bg-green-500 dark:hover:bg-gray-600"
								on:dblclick={() => markAsLearned(word)}
								on:click={() => animate(word.str, word.language)}
							>
								{word.str}
							</button>
						{/if}
					{/each}
				</div>
			</div>
		{/key}
	</div>
</div>
