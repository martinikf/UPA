<!-- Controller for translator logic -->
<script lang="ts">

	import Model from './AnimatedModel.svelte';
    import Scene from './Scene.svelte';

    let scene : Scene;
    let model : Model;

    let textInput = "";
    let speed = 1;

</script>


<input bind:value={textInput} placeholder="Text..." />
<input type="range" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model.changeSpeed(speed)}} />
<button on:click={() => {model.playAnimationForText(textInput.trim())}}>Přeložit</button>
<button on:click={() => {model.resetAnimation()}}>Vypnout</button>
<button on:click={() => {model.pauseResumeAnimation()}}>Zastavit/Pokračovat</button>


<div class="animation">
    <Scene bind:model={model} bind:this={scene}/>
</div>


<style>
    :global(body) {
        margin: 0;
    }

    .animation{
        width: 400px;
        height: 400px;
        position: relative;
        background: linear-gradient(0deg, rgba(2,0,36,1) 0%, rgb(28, 28, 165) 35%, rgba(0,212,255,1) 100%);
    }
</style>
