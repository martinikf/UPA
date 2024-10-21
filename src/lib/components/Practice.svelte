<!-- Controller for translator logic -->
<script lang="ts">

	  import Model from './AnimatedModel.svelte';
		import { Language } from '$lib/components/models/Word';

    let words : string[] = [];

    export let model : Model;

    let textInput = "";
    let randomWord : string;
		let selectedLanguageSet : Language;

    function newWordOnClick(){
        if (words.length < 1){
            console.log("Loading words")
            return loadWords();
        }
        
        randomWord = words[Math.floor(Math.random() * words.length)].trim();
        console.log(randomWord);
        model.playAnimationForText(randomWord, selectedLanguageSet);
    }

    function checkAnswer(){
			if(textInput.length < 1){
				alert("Napište slovo, které jste viděli.");
				return;
			}

        if(textInput.trim().toUpperCase() === randomWord.toUpperCase()){
            alert("Správně!");
        } else {
            alert("Špatně!");
        }
    }

		function replay(){
			if(randomWord === undefined || randomWord.length < 1){
				alert("Nejdříve vytvořte slovo.");
				return;
			}
			model.resetAnimation();
			setTimeout(()=>{model.playAnimationForText(randomWord, selectedLanguageSet)}, 500);
		}

    function loadWords(){
        // Load words from file
        fetch("/CzechWords.txt")
            .then((res) => res.text())
            .then((text) => {
                words = text.split("\n");
                newWordOnClick();
            })
            .catch((e) => console.error(e));
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

	<button on:click={() => {newWordOnClick()}}>Vytvořit nové náhodné slovo</button>
	<input bind:value={textInput} placeholder="Zde napište zobrazené slovo..." />
	<button on:click={() => {checkAnswer()}}>Zkontrolovat</button>
	<button on:click={() => {replay()}}>Přehrát slovo znovu</button>
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
