<!-- Controller for translator logic -->
<script lang="ts">

	  import Model from './AnimatedModel.svelte';

    let words : string[] = [];

    export let model : Model;

    let textInput = "";
    let speed = 1;

    let randomWord : string;

    function newWordOnClick(){
        if (words.length < 1){
            console.log("Loading words")
            return loadWords();
        }
        
        randomWord = words[Math.floor(Math.random() * words.length)].trim();
        console.log(randomWord);
        model.playAnimationForText(randomWord);
    }

    function checkAnswer(){
        if(textInput.trim().toUpperCase() === randomWord.toUpperCase()){
            alert("Správně!");
        } else {
            alert("Špatně!");
        }
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
	<input bind:value={textInput} placeholder="Zde napište zobrazené slovo..." />
	<button on:click={() => {checkAnswer()}}>Zkontrolovat</button>
	<button on:click={() => {model.resetAnimation(); setTimeout(()=>{model.playAnimationForText(randomWord)}, 500)}}>Přehrát slovo znovu</button>
	<button on:click={() => {newWordOnClick()}}>Vytvořit nové náhodné slovo</button>
</div>

<style>
    :global(body) {
        margin: 0;
    }

		.controls{
				display: grid;
				grid-template-columns: 1fr;
				margin-top: 50px;
				padding: 5px;
		}

		.controls > * {
				padding: 5px;
				margin-bottom: 10px;
		}

</style>
