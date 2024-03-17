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


<input bind:value={textInput} placeholder="Text..." />
<input type="range" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model.changeSpeed(speed)}} />
<button on:click={() => {newWordOnClick()}}>Nové slovo</button>
<button on:click={() => {model.resetAnimation(); setTimeout(()=>{model.playAnimationForText(randomWord)}, 500)}}>Přehrát znovu</button>
<button on:click={() => {checkAnswer()}}>Zkontrolovat</button>

<style>
    :global(body) {
        margin: 0;
    }

</style>
