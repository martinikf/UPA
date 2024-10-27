<script lang="ts">
	/**
	 * Component for practicing learned signs
	 *
	 * Requires model and data
	 */

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Word, Language } from '$lib/components/models/Word';

	// Component props
	export let model: Model;
	export let data: Word[];

	// State variables
	let sentence: string = '';
	let copyData = [...data.filter((item: Word) => item.learned)];

	/**
	 * Organizes words by language type for easier filtering and access
	 * Creates a dictionary with language types as keys and filtered word arrays as values
	 */
	const languageSets = {
		[Language.CzechFingerOneHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerOneHand
		),
		[Language.CzechFingerTwoHand]: copyData.filter(
			(item: Word) => item.language === Language.CzechFingerTwoHand
		),
		[Language.Czech]: copyData.filter((item: Word) => item.language === Language.Czech)
	};

	// User input
	let selectedLanguageSet: Language = Language.CzechFingerOneHand;
	let userInput: string = '';

	/**
	 * Validates user input against the current sentence
	 * Shows success/failure message and clears input on success
	 */
	function checkAnswer() {
		const normalizedInput = userInput.trim().toLowerCase();
		const normalizedSentence = sentence.trim().toLowerCase();

		if (normalizedInput === normalizedSentence) {
			alert('Správně!');
			userInput = '';
		} else {
			alert('Špatně!');
		}
	}

	/**
	 * Generates a new random sentence from the selected language set
	 * Plays the corresponding animation
	 */
	function createNewSentence() {
		if (languageSets[selectedLanguageSet].length === 0) {
			alert('Nemáte žádné slova pro tento jazyk');
			return;
		}

		let randomIndex = Math.floor(Math.random() * languageSets[selectedLanguageSet].length);
		sentence = languageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	/**
	 * Replays the current sentence animation
	 */
	function replayAnimation(): void {
		model.playAnimationForText(sentence, selectedLanguageSet);
	}
</script>

<h2>Procvičovat</h2>
<p>
	Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko
	zkontrolovat.
</p>

<div class="language">
	<label for="language" class="select_label">Jazyk:</label>
	<select id="language" bind:value={selectedLanguageSet}>
		<option value={Language.CzechFingerOneHand}>Česká prstová abeceda jednoruční</option>
		<option value={Language.CzechFingerTwoHand}>Česká prstová abeceda obouruční</option>
		<option value={Language.Czech}>Český znakový jazyk</option>
	</select>
</div>

<div class="group_control">
	<button disabled={languageSets[selectedLanguageSet].length === 0} on:click={createNewSentence}>
		Spustit novou větu
	</button>

	<button on:click={replayAnimation}>Přehrát znovu </button>
</div>

<div class="group_input">
	<input
		id="text"
		class="text_input"
		type="text"
		bind:value={userInput}
		placeholder="Zde napište znakované slovo"
	/>
	<button class="smaller_button" on:click={checkAnswer}>Zkontrolovat</button>
</div>

<style>
	h2 {
		margin-top: 0;
	}

	.select_label {
		text-align: right;
	}

	button,
	input,
	select {
		padding: 5px;
	}

	.language {
		margin-bottom: 0.5rem;
	}

	.group_control {
		display: grid;
		grid-template-columns: 1fr 1fr;
		margin-bottom: 0.5rem;
	}

	.group_input {
		display: grid;
		grid-template-columns: 2fr 1fr;
	}

	@media (max-width: 768px) {
		.group_control,
		.group_input {
			display: flex;
			flex-direction: column;
			gap: 0.5rem;
		}
	}
</style>
