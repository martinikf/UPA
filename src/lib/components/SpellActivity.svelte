<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import { browser } from '$app/environment';

	let landmarkDetection: LandmarkDetection;

	let currentState = 0;

	let currentWordDisplay : HTMLElement | null = null;
	let wordDisplay : HTMLElement | null = null;

	function handleMessage(msg) {
		if(randomWord.length < 1 || currentWordDisplay == null) return;

		let result = msg.detail;
		if (currentState >= randomWord.length) {
			alert("Word recognized!");
			currentState = 0;
		}

		let currentLetter = randomWord[currentState].toUpperCase();
		if(currentLetter === 'C' && currentState < randomWord.length - 1 && randomWord[currentState + 1].toUpperCase() === 'H'){
			currentLetter = "CH";
		}

		if (result[currentLetter]) {
			if(currentLetter === "CH")
				currentState++;
			currentState++;
			currentWordDisplay.innerHTML = randomWord.substring(0, currentState);
		}
	}

	let words : string[] = [];
	let randomWord : string;

	function newWordOnClick(){
		randomWord = "";
		currentState = 0;
		if(currentWordDisplay)
			currentWordDisplay.innerHTML = "";

		if (words.length < 1){
			console.log("Loading words")
			return loadWords();
		}

		randomWord = words[Math.floor(Math.random() * words.length)].trim();
		console.log(randomWord);

		if(wordDisplay)
			wordDisplay.innerHTML = randomWord;
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
		currentWordDisplay = document.getElementById("currentWord");
		wordDisplay = document.getElementById("word");

		newWordOnClick();
	}

</script>

<div id="word"> </div>

<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>

<button on:click={newWordOnClick}>Nové slovo</button>

<div id="currentWord"> </div>


<style> </style>