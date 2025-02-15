<script lang="ts">
	import { Language } from '$lib/models/Word.js';
	import { Label, Select } from 'flowbite-svelte';

	export let selectedLanguageSet: Language;
	export let onChange: (event: Event) => void = () => {};
</script>

<div>
	<Label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Jazyk:</Label>

	<Select id="language"
					bind:value={selectedLanguageSet}
					placeholder="Prosím zvolte jeden jazyk"
					on:change={onChange}>
		<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
		<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda dvouruční</option>
		<option value={Language.Czech}>Český znakový jazyk</option>
	</Select>
</div>