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

	import Model from '$lib/components/AnimatedModel.svelte';
	import Scene from '$lib/components/Scene.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';
	import { Language, Word } from '$lib/components/models/Word';
	import { LearnMode } from '$lib/components/models/LearnMode';

	import Review from './Review.svelte';
	import Practice from './Practice.svelte';
	import Learn from './Learn.svelte';

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

		let words = ['auto', 'autobus']; //TODO, load dynamically from model

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

<div class="learn">
	<h2>Režim učitel</h2>
	<p>Tento režim slouží k postupnému učení prostové abecedy a základních znaků.</p>

	<div class="tabs">
		<ul>
			<li class:highlight={currentMode === LearnMode.Practice}>
				<button
					on:click={() => {
						changeMode(LearnMode.Practice);
					}}
				>
					Procvičovat
				</button>
			</li>
			<li>
				<button
					on:click={() => {
						changeMode(LearnMode.Learn);
					}}
				>
					Učit
				</button>
			</li>
			<li>
				<button
					on:click={() => {
						changeMode(LearnMode.Review);
					}}
				>
					Znaky
				</button>
			</li>
		</ul>
	</div>

	<div class="content">
		<div class="animation">
			<div class="animation_canvas">
				<Scene bind:model bind:this={scene} bind:showLetter={showString} />
			</div>
			<ControlRow {model} bind:this={controlRow} />
		</div>

		<div class="control">
			{#if currentMode === LearnMode.Practice}
				<Practice {model} {data} />
			{:else if currentMode === LearnMode.Learn}
				<Learn {model} {data} />
			{:else if currentMode === LearnMode.Review}
				<Review {model} {data} />
			{/if}
		</div>
	</div>
</div>

<style>
	.learn {
		width: 80%;
		max-width: 1600px;
		margin: auto auto 2rem;
	}

	.content {
		margin: auto;
		display: grid;
		grid-template-columns: 1fr 2fr;
	}

	.animation {
		width: 100%;
		max-width: 400px;
		margin-right: 2rem;
	}

	.tabs {
		list-style: none;
		display: flex;

		justify-content: left;
		padding: 0;
		margin: 0 0 2rem;
	}

	.tabs ul {
		padding: 0;
		margin: 0;
		display: flex;
		gap: 0.5rem;
	}

	.tabs li {
		display: inline-block;
	}

	.tabs li button {
		padding: 5px;
	}

	.tabs li button {
		padding: 5px;
		font-size: 1rem;
	}

	.animation_canvas {
		border: solid 2px black;
		position: relative;
		background: linear-gradient(
			0deg,
			rgb(255, 115, 0) 0%,
			rgb(255, 216, 0) 35%,
			rgb(0, 86, 184) 100%
		);
		height: 300px;
		width: 400px;
	}

	@media (max-width: 1400px) {
	}

	@media (max-width: 768px) {
		.content {
			grid-template-columns: 1fr;
		}
		.tabs {
			justify-content: right;
		}

		.animation {
			margin: auto;
		}

		.learn {
			width: 90%;
		}
	}

	@media (max-width: 480px) {
		.learn {
			width: 95%;
		}
	}
</style>
