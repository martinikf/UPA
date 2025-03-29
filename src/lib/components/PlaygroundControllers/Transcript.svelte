<script lang="ts">
	/**
	 * Svelte component controlling the "Přepis" (Transcription) mode in the Playground.
	 *
	 * Allows users to transcribe finger-spelled input detected via webcam into text.
	 * Offers two modes:
	 * - Automatic: Uses the CSLR helper to continuously parse the recognized sign sequence.
	 * - Manual: Requires the user to manually confirm each recognized sign before it's added to the text.
	 * Provides options to play back the transcribed text as an animation and clear the text.
	 *
	 * @prop {Model} model - Instance of the AnimatedModel component for playing back animations.
	 */
	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import { Button, P } from 'flowbite-svelte';
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import { convertToFrequencyFormat } from '$lib/helpers/CSLR';

	/** Instance of the AnimatedModel component, passed as a prop. */
	export let model: Model;

	// Internal state
	let str: string = "";
	let parsedStr :string = "";
	let winner: GestureProbability | null = null;
	let automaticMode = true;

	// Constants for manual confirmation logic
	const WINNER_BUFFER_SIZE = 5;
	const TIME_BUFFER_WINDOW = 1000;

	/** Buffer storing recent gesture recognitions (letter and timestamp) for manual confirmation logic. */
	let winnerBuffer: { letter: string, timestamp: number }[] = [];

	/**
	 * Handles incoming gesture recognition messages from LandmarkDetection.
	 * Updates the winner state. In Automatic mode, updates the raw and parsed strings.
	 * In Manual mode, adds the recognized gesture to a time-limited buffer for later confirmation.
	 * @param msg - Custom event containing gesture probability data.
	 */
	export function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		const result = msg.detail;
		// Find the most probable gesture in the current frame
		winner = findKeyWithMaxValue(result);

		// Clean up old records in the buffer (relevant for Manual mode)
		removeOldRecords();

		// Ignore if no significant gesture is detected
		if(!winner || winner.letter === 'None'){ return;}

		if (automaticMode) {
			// In Automatic mode, append directly and parse using CSLR
			str += winner.letter;
			parsedStr = convertToFrequencyFormat(str);
		}
		if(!automaticMode) {
			// In Manual mode, add the potential winner to a buffer
			const currentTime = Date.now();
			winnerBuffer.push({ letter: winner.letter, timestamp: currentTime });

			// Keep buffer size limited
			if (winnerBuffer.length > WINNER_BUFFER_SIZE) {
				winnerBuffer.shift();
			}
		}
	}

	/**
	 * Finds the GestureProbability object with the highest probability within an array.
	 * @param data - Array of GestureProbability objects.
	 * @returns The GestureProbability object with the maximum probability, or null if the input array is empty.
	 */
	function findKeyWithMaxValue(data: GestureProbability[]): GestureProbability | null {
		if (data.length === 0) return null;
		return data.reduce((max, current) => (current.probability > max.probability ? current : max));
	}

	/**
	 * Confirms the most frequent character in the recent recognition buffer (Manual mode).
	 * If a character appears frequently enough within the buffer, it's appended to the `str`.
	 * The buffer is then cleared.
	 */
	function confirm() {
		// Only applicable in Manual mode and if buffer has entries
		if(automaticMode || winnerBuffer.length < 1) return;

		// Find the most appearing letter in the buffer
		let mostFrequentLetter = winnerBuffer.reduce<Record<string, number>>((prev, current) => {
			prev[current.letter] = (prev[current.letter] || 0) + 1;
			return prev;
		}, {});
		let maxLetter = Object.keys(mostFrequentLetter).reduce((a, b) => mostFrequentLetter[a] > mostFrequentLetter[b] ? a : b);

		// Confirm only if the most frequent letter appeared more than twice (simple stability check)
		if(mostFrequentLetter[maxLetter] > 2)
		str += maxLetter;
		winnerBuffer = []; // Clear the buffer after confirmation attempt
	}

	/**
	 * Triggers the animation playback of the transcribed text using the AnimatedModel component.
	 * Plays either the raw string (Manual mode) or the CSLR-parsed string (Automatic mode).
	 */
	function playText() {
		if (model) {
			if(automaticMode)
				model.playAnimationForText(parsedStr, Language.CzechFingerOneHand);
			else
				model.playAnimationForText(str, Language.CzechFingerOneHand);
		}
	}

	/**
	 * Clears the currently transcribed text (both raw and parsed strings).
	 */
	function deleteText() {
		str = '';
		parsedStr = "";
	}

	/**
	 * Switches the component to Automatic transcription mode and resets the state.
	 */
	function automatic(){
		automaticMode = true;
		resetState();
	}

	/**
	 * Switches the component to Manual transcription mode and resets the state.
	 */
	function manual(){
		automaticMode = false;
		resetState();
	}

	/**
	 * Resets the internal state, clearing the winner buffer and transcribed text.
	 * Called when switching modes or explicitly deleting text.
	 */
	function resetState(){
		winnerBuffer = []
		deleteText();
	}

	/**
	 * Handles keyboard shortcuts for the transcription mode.
	 * Enter: Confirms the current sign in Manual mode.
	 * Backspace: Deletes the last character from the raw string `str` (simple deletion).
	 * @param event - The keyboard event object.
	 */
	function handleKeyPress(event: KeyboardEvent){
		if(event.code === "Enter"){
			confirm();
		}
		else if(event.code === "Backspace"){
			str = str.slice(0, -1);

			// Update parsed string immediately if in automatic mode
			if (automaticMode) {
				parsedStr = convertToFrequencyFormat(str);
			}
		}
	}

	/**
	 * Removes records from the `winnerBuffer` that are older than the defined `TIME_BUFFER_WINDOW`.
	 * Used in Manual mode to keep the confirmation buffer relevant to recent gestures.
	 */
	function removeOldRecords() {
		const currentTime = Date.now();
		winnerBuffer = winnerBuffer.filter(record => currentTime - record.timestamp <= TIME_BUFFER_WINDOW);
	}

</script>

<svelte:window on:keydown={handleKeyPress} />

<div class="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm space-y-4">
	<P class="text-gray-700 dark:text-gray-300">Režim rozpoznávání</P>
	<div class="flex gap-2">
		<Button
			color={automaticMode ? 'blue' : 'none'}
			on:click={automatic}
			class="flex-1"
		>
			Automatický
		</Button>
		<Button
			color={!automaticMode ? 'blue' : 'none'}
			on:click={manual}
			class="flex-1"
		>
			Manuální
		</Button>
	</div>

	<div class="border-b border-gray-200 dark:border-gray-700 my-2"></div>

	<div class="flex gap-2">
		<Button color="red" class="flex-1" on:click={deleteText}>
			Smazat text
		</Button>
		<Button color="blue" class="flex-1" on:click={playText}>
			Přehrát text
		</Button>
	</div>

	{#if !automaticMode}
		<div class="space-y-3">
			<Button color="primary" class="w-full" on:click={confirm}>
				Potvrdit aktuální znak
			</Button>
		</div>
	{/if}
</div>

<div class="border-b border-gray-200 dark:border-gray-700 my-2"></div>

<div class="space-y-3">
	<P class="text-gray-700 dark:text-gray-300 break-words">
		Text: <br> <strong class="font-semibold text-gray-900 dark:text-white">{automaticMode ? parsedStr : str}</strong>
	</P>
</div>