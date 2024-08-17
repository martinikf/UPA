<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
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
				model.playAnimationForText(sentence);

				return
			}
		}

		//Words
		sentence = copyData[Math.floor(Math.random() * copyData.length)].str;
		model.playAnimationForText(sentence);
	}


</script>

<h2>Procvičovat</h2>
<p>
	Zapište do pole postupně všechny znaky, které vám byly zobrazeny. Poté stiskněte tlačítko zkontrolovat.


</p>
<h3>Ovládání</h3>
<button on:click={createNewSentence}>Spustit novou větu</button>

<label for="includeFingerAlph">Zahrnout prstovou abecedu</label>
<input type="checkbox" name="includeFingerAlph" bind:checked={includeFingerAlphabet}/>

<button on:click={() => {model.playAnimationForText(sentence)}}>Přehrát znovu</button>
<input type="text" bind:value={userInput}>

<button on:click={Check}>Zkontrolovat</button>