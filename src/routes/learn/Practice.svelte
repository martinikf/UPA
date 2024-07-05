<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Checkbox } from 'svelte-tweakpane-ui';
	import { onMount } from 'svelte';
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

	let words : string[] = [];

	function loadWords(){
		// Load words from file
		fetch("/CzechWords.txt")
			.then((res) => res.text())
			.then((text) => {
				words = text.split("\n");
			})
			.catch((e) => console.error(e));
	}

	function createNewSentence(){
		if(includeFingerAlphabet){
			let i = Math.random();
			if(i < 0.5 || !copyData.some((item: any) => item.str.length > 2)){
				if(!words){
					loadWords();
				}

				sentence = words[Math.floor(Math.random() * words.length)].trim();
				model.playAnimationForText(sentence);

				return
			}
		}

		//Words
		sentence = copyData[Math.floor(Math.random() * copyData.length)].str;
		model.playAnimationForText(sentence);
	}
	onMount(() => {
		loadWords();
	});

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