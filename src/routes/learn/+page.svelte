<script lang="ts">
	/**
	 * Teacher Mode page
	 *
	 * A comprehensive learning interface for sign language that provides three modes:
	 * - Review: Browse and review all available signs
	 * - Learn: Progressively learn new signs
	 * - Practice: Test knowledge of learned signs
	 *
	 */

	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import Scene from '$lib/components/Animation/Scene.svelte';
	import ControlRow from '$lib/components/Animation/ControlRow.svelte';
	import { Language, Word } from '$lib/models/Word';
	import { LearnMode } from '$lib/models/LearnMode';

	import Review from '$lib/components/LearnControllers/Review.svelte';
	import Practice from '$lib/components/LearnControllers/Practice.svelte';
	import Learn from '$lib/components/LearnControllers/Learn.svelte';
	import { TabItem, Tabs } from 'flowbite-svelte';

	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	let currentMode: LearnMode = LearnMode.Review;
	// Computed property to determine if string should be shown
	$: showString = currentMode != LearnMode.Practice;

	/**
	 * Builds a list of words and letters for learning
	 * Includes Czech alphabet (including 'ch') and basic words
	 * @returns {Word[]} Array of Word objects
	 */
	function buildList(): Word[] {
		let lettersCz = 'abcdefghijklmnopqrstuvwxyz'.split('');
		//Add letter 'ch' after 'h'
		lettersCz.splice(8, 0, 'ch');

		let words = ['Mama', 'Ahoj']; //TODO, load dynamically from AnimatedModel - duplication!

		let listOfAllWords: Word[] = [];

		// Create Word objects for each letter in both one-hand and two-hand variants
		lettersCz.forEach((letter) => {
			listOfAllWords.push(
				new Word(letter, Language.CzechFingerOneHand, false),
				new Word(letter, Language.CzechFingerTwoHand, false)
			);
		});

		// Create Word objects for basic words
		words.forEach((word) => {
			listOfAllWords.push(new Word(word, Language.Czech, false));
		});

		return listOfAllWords;
	}

	let data = buildList();

	/**
	 * Changes the current learning mode
	 * @param {LearnMode} mode - The mode to switch to
	 */
	function changeMode(mode: LearnMode) {
		currentMode = mode;
	}
</script>

	<div class="md:mt-8 mt-2 max-w-7xl mx-auto px-4 pb-8 dark:bg-gray-900 relative">
		<div class="grid grid-cols-1 md:grid-cols-5 md:gap-6">

			<!-- Animation Column -->
			<div class="col-span-3 md:relative fixed bottom-4 left-1 z-50 md:w-full w-2/4">
				<div class="md:bg-white bg-gray-300 md:dark:bg-gray-800 dark:bg-gray-600 md:p-4 p-2 rounded-lg shadow-sm">
					<div class="bg-gradient-to-b from-blue-400 to-yellow-600 md:h-[454px] h-[250px] rounded-xl border-2 border-gray-200 dark:border-gray-700 shadow-lg relative">
						<Scene bind:model bind:this={scene} bind:showLetter={showString} />
					</div>
					<ControlRow {model} bind:this={controlRow} />
				</div>
			</div>


			<div class="md:mt-0 md:mb-0 mb-[320px] col-span-1 md:col-span-2">
				<Tabs>
					<TabItem
						on:click={() => changeMode(LearnMode.Practice)}	>
						<span slot="title" class="text-xl">Procvičovat</span>
						<Practice {model} {data} />
					</TabItem>

					<TabItem
						on:click={() => changeMode(LearnMode.Learn)}>
						<span slot="title" class="text-xl">Učit</span>
						<Learn {model} {data} />
					</TabItem>

					<TabItem
						on:click={() => changeMode(LearnMode.Review)}	open>
						<span slot="title" class="text-xl">Znaky</span>
						<Review {model} {data} />
					</TabItem>
				</Tabs>
			</div>
		</div>
	</div>