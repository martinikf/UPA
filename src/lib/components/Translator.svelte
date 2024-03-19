<!-- Controller for translator logic -->
<script lang="ts">

    import Model from './AnimatedModel.svelte';

    export let model : Model;

    let textInput = "";

		function translate(){
			if(textInput.trim() != "")
				model.playAnimationForText(textInput.trim());
			else{
				alert("Textové pole je prázdné!");
			}
		}

</script>


<div class="controls">
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
