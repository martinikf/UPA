<script lang="ts">
	/**
	 * Sign Language Playground page
	 *
	 * Learning and practicing Czech finger alphabet with multiple modes:
	 * - Translator: Convert text to sign language
	 * - Practice: Practice sign reading
	 * - Spelling Practice: Practice signing with webcam
	 * - Transcription: Real-time sign language transcription
	 * - Interactive: Interactive learning with webcam
	 *
	 */

	import GestureRecognition from '$lib/components/Recognition/GestureRecognition.svelte';
	import Scene from '$lib/components/Animation/Scene.svelte';
	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import ControlRow from '$lib/components/Animation/ControlRow.svelte';

	// Import modes
	import Translator from '$lib/components/PlaygroundControllers/Translator.svelte';
	import Practice from '$lib/components/PlaygroundControllers/Practice.svelte';
	import SpellActivity from '$lib/components/PlaygroundControllers/SpellActivity.svelte';
	import Transcript from '$lib/components/PlaygroundControllers/Transcript.svelte';
	import Interactive from '$lib/components/PlaygroundControllers/Interactive.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { PlaygroundMode } from '$lib/models/PlaygroundMode';
	import { Button, Toggle } from 'flowbite-svelte';
	import { beforeNavigate } from '$app/navigation';

	// State
	let mode: PlaygroundMode = PlaygroundMode.Translator;
	let webcam: boolean = false;
	let displayLetter: boolean = true;

	// References
	let scene: Scene;
	let model: Model;
	let transcript: Transcript;
	let spellActivity: SpellActivity;
	let interactive: Interactive;
	let gestureRecognition: GestureRecognition;
	let controlRow: ControlRow;

	let disabledToggle = false;

	/**
	 * Routes landmark detection messages to appropriate components based on current mode
	 * @param msg - Custom event containing gesture probability data
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		if (!webcam) return;

		switch (mode) {
			case PlaygroundMode.Spelling:
				spellActivity.handleMessage(msg);
				break;
			case PlaygroundMode.Transcript:
				transcript.handleMessage(msg);
				break;
			case PlaygroundMode.Interactive:
				interactive.handleMessage(msg);
				break;
		}
	}

	/**
	 * Updates letter display based on current mode
	 * Letters are hidden in practice mode
	 */
	function updateLetterDisplay(): void {
		displayLetter = mode !== PlaygroundMode.Practice;
	}

	/**
	 * Handles mode changes by resetting animation and updating letter display
	 */
	function handleModeChange() {
		model.resetAnimation();
		updateLetterDisplay();
	}


	/**
	 * Toggles webcam state and handles related mode changes
	 */
	function toggleWebcam() {
		if (webcam && gestureRecognition) {
			gestureRecognition.disableCam();

			if(mode != PlaygroundMode.Translator && mode != PlaygroundMode.Practice) {
				mode = PlaygroundMode.Translator;
				handleModeChange();
			}
		}

		webcam = !webcam;

		if(webcam){
			disabledToggle = true;
			setTimeout(() => {
				disabledToggle = false;
			}, 2000);
		}
	}

	/**
	 * Changes playground mode and updates component state
	 * @param newMode - The mode to switch to
	 */
	function changeMode(newMode: PlaygroundMode): void {
		mode = newMode;
		handleModeChange();
	}

	/**
	 * Svelte lifecycle function called before navigating away from the page.
	 * Ensures the webcam is disabled to release the resource.
	 */
	beforeNavigate(() => {
		if(gestureRecognition){
			gestureRecognition.disableCam();
		}
	});
</script>


<div class="max-w-7xl mx-auto px-4 pb-8 dark:bg-gray-900">
	<!-- Mode Selection -->
	<div class="mx-auto mb-8 mt-8">
		<div class="grid md:grid-cols-3 grid-cols-1 gap-4  md:justify-items-stretch justify-items-center">
			<!-- Left Modes -->
			<div class="flex flex-wrap gap-2">
				<Button
					color={mode === PlaygroundMode.Translator ? 'blue' : 'dark'}
					on:click={() => changeMode(PlaygroundMode.Translator)}
				>
					Překladač
				</Button>
				<Button
					color={mode === PlaygroundMode.Practice ? 'blue' : 'dark'}
					on:click={() => changeMode(PlaygroundMode.Practice)}
				>
					Odezírání
				</Button>
			</div>

			<!-- Middle Webcam Toggle -->
			<div class="flex justify-center items-center gap-2">
				<div class="flex flex-col">
					<Toggle
						color="red"
						checked={webcam}
						on:change={toggleWebcam}
						class="mx-auto"
						disabled={disabledToggle}
					/>
					<span class="text-sm text-gray-600 dark:text-gray-300">
						{webcam ? 'Kamera zapnuta' : 'Kamera vypnuta'}
					</span>
				</div>
			</div>

			<!-- Right Modes -->
				<div class="flex flex-nowrap gap-2 justify-end">
					<Button
						color={mode === PlaygroundMode.Spelling ? 'blue' : 'dark'}
						on:click={() => changeMode(PlaygroundMode.Spelling)}
						disabled={!webcam}
					>
						Znakování
					</Button>
					<Button
						color={mode === PlaygroundMode.Transcript ? 'blue' : 'dark'}
						on:click={() => changeMode(PlaygroundMode.Transcript)}
						disabled={!webcam}
					>
						Přepis
					</Button>
					<Button
						color={mode === PlaygroundMode.Interactive ? 'blue' : 'dark'}
						on:click={() => changeMode(PlaygroundMode.Interactive)}
						disabled={!webcam}
					>
						Procvičování
					</Button>
				</div>
		</div>
	</div>

	<!-- Animation + Controls + Webcam -->
	<div class="relative md:grid md:grid-cols-3 md:gap-3">
			<!-- Animation -->
		<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm md:w-full w-11/12 mx-auto">
			<div class="bg-gradient-to-b from-blue-400 to-yellow-600 h-64 rounded-xl border-2 border-gray-200 dark:border-gray-700 relative">
				<Scene bind:model bind:this={scene} showLetter={displayLetter} />
			</div>
			<ControlRow bind:this={controlRow} {model} />
		</div>

		<!-- Controls -->
		<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm md:mt-0 mt-2">
			{#if mode === PlaygroundMode.Translator}
				<Translator {model} />
			{:else if mode === PlaygroundMode.Practice}
				<Practice {model} />
			{:else if mode === PlaygroundMode.Interactive}
				<Interactive {model} bind:this={interactive} />
			{:else if webcam && mode === PlaygroundMode.Spelling}
				<SpellActivity bind:this={spellActivity} {model} />
			{:else if webcam && mode === PlaygroundMode.Transcript}
				<Transcript bind:this={transcript} {model} />
			{/if}
		</div>


		<!-- Webcam -->
		<div class="rounded-lg shadow-sm absolute w-1/4 top-0 left-0 md:relative md:p-4 md:w-full md:bg-white md:dark:bg-gray-800">
			{#if webcam}
				<div class="aspect-auto border-2 border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
					<GestureRecognition bind:this={gestureRecognition} on:gestureRecognized={handleMessage} />
				</div>
			{/if}
		</div>
	</div>
</div>