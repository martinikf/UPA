<script lang="ts">
	/**
	 * Svelte component for controlling the animation for the purpose of translation
	 * Plays animation for given text and selected language set
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import { Language } from '$lib/models/Word';
	import { Button, Input } from 'flowbite-svelte';
	import LanguageSelector from '$lib/components/Shared/LanguageSelector.svelte';
	import { keepOnlyLetters, removeFormating } from '$lib/helpers/TextHelper';

	export let model: Model;

	// User input variables
	let textInput: string = '';
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;

	/**
	 * Plays animation for the given text and selected language set
	 */
	function translate() {
		let sanitizedInput = keepOnlyLetters(removeFormating(textInput));

		if (sanitizedInput.length > 0)
			model.playAnimationForText(sanitizedInput, selectedLanguageSet);
	}

</script>
<div class="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm space-y-6">
	<div class="space-y-4">

		<LanguageSelector bind:selectedLanguageSet={selectedLanguageSet}/>

		<!-- Text Input -->
		<Input
			bind:value={textInput}
			placeholder="Zde napište text k přehrání"
			class="w-full"
		/>

		<!-- Translate Button -->
		<Button
			color="primary"
			class="w-full"
			on:click={translate}
			disabled="{textInput.trim().length < 1}"
		>
			Přeložit
		</Button>
	</div>
</div>