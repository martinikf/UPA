<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Word, Language } from '$lib/components/models/Word';
	export let model : Model;
	export let data : Word[];

	let selectedLanguageSet : Language = Language.CzechFingerOneHand;
	let userInput = '';
	let sentence : string = '';

	let copyData = [...data.filter((item: Word) => item.learned)];

	//for each Language create dictionary enty with filtered items by that language
	let languageSets = {
		[Language.CzechFingerOneHand]: copyData.filter((item: Word) => item.language === Language.CzechFingerOneHand),
		[Language.CzechFingerTwoHand]: copyData.filter((item: Word) => item.language === Language.CzechFingerTwoHand),
		[Language.Czech]: copyData.filter((item: Word) => item.language === Language.Czech),
	}

	function Check() {
		if (userInput.trim().toLowerCase() === sentence.trim().toLowerCase()) {
			alert('Správně!');
			userInput = '';
		} else {
			alert('Špatně!');
		}
	}

	function createNewSentence(){
		if(languageSets[selectedLanguageSet].length === 0) {
			alert('Nemáte žádné slova k procvičení');
			return;
		}

		let randomIndex = Math.floor(Math.random() * languageSets[selectedLanguageSet].length);
		sentence = languageSets[selectedLanguageSet][randomIndex].str;

		model.playAnimationForText(sentence, selectedLanguageSet);
	}

	function onLanguageChange(){

	}

</script>

<h2>Procvičovat</h2>
<p>
	Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko zkontrolovat.
</p>

<div class="language">
	<label for="language" class="select_label">Jazyk:</label>
	<select id="language" bind:value={selectedLanguageSet} on:change={onLanguageChange}>
		<option value="{Language.CzechFingerOneHand}">Česká prstová abeceda jednoruční</option>
		<option value="{Language.CzechFingerTwoHand}">Česká prstová abeceda obouruční</option>
		<option value="{Language.Czech}">Česká znakový jazyk</option>
		<!-- <option value="cz">ASL</option> -->
	</select>
</div>

<div class="group_control">
	<button on:click={createNewSentence}>Spustit novou větu</button>
	<button on:click={() => {model.playAnimationForText(sentence, selectedLanguageSet)}}>Přehrát znovu</button>
</div>

<div class="group_input">
	<input id="text" class="text_input" type="text" bind:value={userInput} placeholder="Zde napište znakované slovo">
	<button class="smaller_button" on:click={Check}>Zkontrolovat</button>
</div>



<style>
    h2{
        margin-top: 0;
    }

		.select_label{
				text-align: right;
		}

		button, input, select{
				padding: 5px;
		}

		.language{
				margin-bottom: 0.5rem;
		}

		.group_control{
				display: grid;
				grid-template-columns: 1fr 1fr;
				margin-bottom: 0.5rem;
		}

		.group_input{
				display: grid;
				grid-template-columns: 2fr 1fr;
    }

    @media (max-width: 768px) {
        .group_control, .group_input {
            display: flex;
            flex-direction: column;
						gap: 0.5rem;
        }
    }

</style>