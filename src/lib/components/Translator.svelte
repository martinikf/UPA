<script lang="ts">
	/**
	 * Svelte component for controlling the animation for the purpose of translation
	 * Plays animation for given text and selected language set
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Language } from '$lib/models/Word';
	import { Button, Input, Label, Select } from 'flowbite-svelte';

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
<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm space-y-6">
	<div class="space-y-4">
		<!-- Language Selection -->
		<div>
			<Label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Jazyk:</Label>

			<Select id="language"
							bind:value={selectedLanguageSet}
							placeholder="Prosím zvolte jeden jazyk">
				<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
				<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda dvouruční</option>
				<option value={Language.Czech}>Český znakový jazyk</option>
			</Select>
		</div>

		<!-- Text Input -->
		<Input
			bind:value={textInput}
			placeholder="Zde napište text k přehrání"
			class="w-full"
		/>

		<!-- Translate Button -->
		<Button
			color="blue"
			class="w-full"
			on:click={translate}
		>
			Přeložit
		</Button>
	</div>
</div>