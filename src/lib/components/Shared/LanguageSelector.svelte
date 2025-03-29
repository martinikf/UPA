<script lang="ts">
	/**
	 * A reusable Svelte component for selecting a language or communication system.
	 * Renders a dropdown list populated with options from the Language enum.
	 *
	 * @prop {Language} selectedLanguageSet - The currently selected language value (bindable).
	 * @prop {(event: Event) => void} [onChange=() => {}] - Optional callback function triggered when the selection changes.
	 */
	import { Language } from '$lib/models/Word.js';
	import { Label, Select } from 'flowbite-svelte';

	/** The currently selected language value. Bindable property. */
	export let selectedLanguageSet: Language;
	/** Optional callback function triggered when the selection changes. */
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