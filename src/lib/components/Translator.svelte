<script lang="ts">
	/**
	 * Svelte component for controlling the animation for the purpose of translation
	 * Plays animation for given text and selected language set
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Language } from '$lib/components/models/Word';

	export let model: Model;

	// User input variables
	let textInput: string = '';
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;

	/**
	 * Plays animation for the given text and selected language set
	 */
	function translate() {
		if (textInput.trim().length > 0)
			model.playAnimationForText(textInput.trim(), selectedLanguageSet);
	}
</script>

<!-- Control block with language selection, text input and translate button -->
<div class="controls">
	<div class="language_selection">
		<label for="language">Jazyk:</label>
		<select id="language" bind:value={selectedLanguageSet}>
			<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
			<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda obouruční</option>
			<option value={Language.Czech}>Český znakový jazyk</option>
		</select>
	</div>

	<input bind:value={textInput} placeholder="Zde napište text k přehrání" />
	<button
		on:click={() => {
			translate();
		}}
	>
		Přeložit
	</button>
</div>

<style>
	:global(body) {
		margin: 0;
	}

	.controls {
		display: grid;
		grid-template-columns: 1fr;
		padding: 5px;
	}

	.controls > * {
		padding: 5px;
		margin-bottom: 10px;
	}

	.language_selection select {
		padding: 5px;
	}
</style>
