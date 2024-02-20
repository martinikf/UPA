<!-- Controller for translator logic -->
<script lang="ts">

	import Model from './AnimatedModel.svelte';
    import Scene from './Scene.svelte';

    let words : string[] = [];

    let scene : Scene;
    let model : Model;

    let textInput = "";
    let speed = 1;

    let displayLetter = false; //Hide letter for practice mode

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


<div class="animation">
    <Scene bind:model={model} bind:this={scene} bind:showLetter={displayLetter}/>
</div>


<style>
    :global(body) {
        margin: 0;
    }

    .animation{
        width: 400px;
        height: 400px;
        background: linear-gradient(0deg, rgba(2,0,36,1) 0%, rgb(165, 28, 81) 35%, rgb(153, 65, 170) 100%);
    }

</style>
