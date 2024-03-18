<!-- Controller for translator logic -->
<script lang="ts">

    import Model from './AnimatedModel.svelte';

    export let model : Model;

    let textInput = "";
    let speed = 1;

</script>


<div class="controls">
	<input bind:value={textInput} placeholder="Text..." />
	<button on:click={() => {model.playAnimationForText(textInput.trim())}}>Přeložit</button>
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
