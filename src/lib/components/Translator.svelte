<!-- Controller for translator logic -->
<script lang="ts">

    import Model from './AnimatedModel.svelte';

    export let model : Model;

    let textInput = "";
    let speed = 1;

</script>


<input bind:value={textInput} placeholder="Text..." />
<input type="range" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model.changeSpeed(speed)}} />
<button on:click={() => {model.playAnimationForText(textInput.trim())}}>Přeložit</button>
<button on:click={() => {model.resetAnimation()}}>Vypnout</button>
<button on:click={() => {model.pauseResumeAnimation()}}>Zastavit/Pokračovat</button>




<style>
    :global(body) {
        margin: 0;
    }
</style>
