<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Language } from '$lib/components/models/Word';
	export let model : Model;
	export let data : any;


	let userInput = '';
	let includeFingerAlphabet = true;

	let sentence : string = '';

	let copyData = [...data.filter((item: any) => item.learned)];


	function Check() {
		if (userInput.trim().toLowerCase() === sentence.trim().toLowerCase()) {
			alert('Správně!');
		} else {
			alert('Špatně!');
		}
	}

	//TODO: remake this, doesn't work as intended
	function createNewSentence(){
		if(includeFingerAlphabet){
			let i = Math.random();
			if(i < 0.5 || !copyData.some((item: any) => item.str.length > 2)){


				sentence = copyData.filter((item: any) => item.str.length == 1)[Math.floor(Math.random() * copyData.length)].str;
				model.playAnimationForText(sentence, Language.Czech);

				return
			}
		}

		//Words
		sentence = copyData[Math.floor(Math.random() * copyData.length)].str;
		model.playAnimationForText(sentence, Language.Czech);
	}


</script>

<h2>Procvičovat</h2>
<p>
	Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko zkontrolovat.


</p>
<h3>Ovládání</h3>
<div class="control_block">
	<button on:click={createNewSentence}>Spustit novou větu</button>
	<button on:click={() => {model.playAnimationForText(sentence, Language.Czech)}}>Přehrát znovu</button>

	<input id="text" class="text_input" type="text" bind:value={userInput} placeholder="Zde napište znakované slovo">
	<button class="smaller_button" on:click={Check}>Zkontrolovat</button>
</div>

<style>
    .control_block {
        display: grid;
				grid-template-columns: 1fr 1fr;
				gap: 0.5rem;

    }

    .control_block button {
    		padding: 5px;
				margin-bottom: 0.5rem;
    }

		.control_block .text_input{
				border-radius: 3px;
		}

		.control_block .smaller_button {
        margin-top: 4px;
    }

    @media (max-width: 768px) {
        .control_block{
            display: flex;
            flex-direction: column;
        }

        .control_block .text_input{
						width: 90%;
						margin: auto;
            font-size: 1.15rem;
        }

        .control_block .smaller_button{
            width: 80%;
            margin: 0 auto;
        }
    }
</style>