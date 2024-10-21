<!-- Controller for translator logic -->
<script lang="ts">

    import Model from './AnimatedModel.svelte';
		import { Language } from '$lib/components/models/Word';

    export let model : Model;

    let textInput = "";
		let selectedLanguageSet : Language;

		function translate(){
			if(textInput.trim() != "")
				model.playAnimationForText(textInput.trim(), selectedLanguageSet);
			else{
				alert("Textové pole je prázdné!");
			}
		}

</script>


<div class="controls">
	<div class="language_selection">
		<label for="language">Jazyk:</label>
		<select id="language" bind:value={selectedLanguageSet}>
			<option value="{Language.CzechFingerOneHand}">Česká prstová abeceda jednoruční</option>
			<option value="{Language.CzechFingerTwoHand}">Česká prstová abeceda obouruční</option>
			<option value="{Language.Czech}">Česká znakový jazyk</option>
		</select>
	</div>

	<input bind:value={textInput} placeholder="Text..." />
	<button on:click={() => {translate()}}>Přeložit</button>
</div>

<style>
    :global(body) {
        margin: 0;
    }

    .controls{
        display: grid;
        grid-template-columns: 1fr;
				padding: 5px;
    }

    .controls > * {
        padding: 5px;
        margin-bottom: 10px;
    }
</style>
