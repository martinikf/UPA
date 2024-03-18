<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	export let landmarkDetection: LandmarkDetection;

	let currentState = 0;

	let currentWordDisplay : HTMLElement | null = null;
	let wordDisplay : HTMLElement | null = null;

	let timeout = 0;

	export function handleMessage(msg : any) {
		if(randomWord.length < 1 || currentWordDisplay == null) return;

		let result = msg.detail;
		if (currentState >= randomWord.length) {
			alert("Word recognized!");
			currentState = 0;
		}

		if(performance.now() < timeout) return;

		let currentLetter = randomWord[currentState].toUpperCase();
		if(currentLetter === 'C' && currentState < randomWord.length - 1 && randomWord[currentState + 1].toUpperCase() === 'H'){
			currentLetter = "CH";
		}

		if (result[removeDiacritics(currentLetter)]) {
			if(currentLetter === "CH")
				currentState++;
			currentState++;
			currentWordDisplay.innerHTML = randomWord.substring(0, currentState);
			timeout = performance.now() + 500;
		}
	}

	function removeDiacritics(inputString : string) : string {
		return inputString.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
	}

	let words : string[] = [];
	let randomWord : string;
	let customWord : string = "";

	function newWordOnClick() {
		randomWord = "";
		currentState = 0;
		if (currentWordDisplay)
			currentWordDisplay.innerHTML = "";

		if (words.length < 1) {
			console.log("Loading words")
			return loadWords();
		}

		randomWord = words[Math.floor(Math.random() * words.length)].trim();
		console.log(randomWord);

		if (wordDisplay) {
			wordDisplay.innerHTML = randomWord;
			console.log("Nastaveno slovo: " + randomWord)
		}
	}

	function customWordOnClick(){
		if(customWord.length < 1) {
			alert("Zadejte prosím slovo.")
			return;
		}

		currentState = 0;
		if (currentWordDisplay)
			currentWordDisplay.innerHTML = "";
		randomWord = customWord;

		if (wordDisplay) {
			wordDisplay.innerHTML = randomWord;
			console.log("Nastaveno slovo: " + randomWord)
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

	if(browser){
		onMount(() => {
			currentWordDisplay = document.getElementById("currentWord");
			wordDisplay = document.getElementById("word");

			newWordOnClick();
		});
	}

</script>



<div class="controls">
	<p>Aktuální slovo: <strong id="word"></strong></p>
	<p>Správně znakovaná písmena: <strong id="currentWord"></strong></p>
	<div class="controls_grid">
		<button on:click={newWordOnClick}>Vytvořit nové náhodné slovo</button>
		<div class="gap"></div>
		<input type="text" placeholder="Vlastní slovo..." bind:value={customWord} />
		<button on:click={customWordOnClick}>Nastavit vlastní slovo</button>
	</div>
</div>

<style>
	.controls{
			margin-top: 50px;
			padding: 5px;
	}
	.controls_grid{
			display: grid;
			grid-template-columns: 1fr;
	}
	.controls_grid > *{
			padding: 5px;
			margin-bottom: 10px;
	}
	.gap {
			height: 5px;
			border-bottom: solid black 3px;
	}

</style>