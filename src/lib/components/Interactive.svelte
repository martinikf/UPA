<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import Model from './AnimatedModel.svelte';

	export let model : Model;
	export let landmarkDetection: LandmarkDetection;

	let speed = 1;

	const DEFAULT_STRING = "Testovací text bla bla";
	let customString : string = "";

	let text : string;

	let running : boolean = false;

	let timeout = 0;

	export function handleMessage(msg : any) {
		console.log(model.transitioning)
		if(performance.now() < timeout || model.transitioning) return;

		display_char = char == "" ? "🕒" : char;

		let result = msg.detail;
		if (char)
			if(result[removeDiacritics(char)]){
				display_char = "👍"
				char = ""
				setTimeout(() => {nextChar();}, 2_000 / speed)
			}

		timeout = performance.now() + 1_500 / speed;
	}

	function removeDiacritics(inputString : string) : string {
		return inputString.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
	}

	let char : string = "";
	let display_char : string = "🕒";

	function start(){
		if(running){
			return;
		}
		running = true;

		text = DEFAULT_STRING;

		if(customString.length > 0){
			text = customString;
		}

		timeout = performance.now() + 2_000 / speed;

		char = text[0].toUpperCase();
		text = text.slice(1);
		model.playAnimationForText(char);

	}

	function replay(){
		model.playAnimationForText(char);
	}

	function nextChar(){
		if(text.length == 0){
			alert("Konec")
			running = false;
			return;
		}

		//clock icon
		display_char = "🕒"

		timeout = performance.now() + 2_000 / speed;

		char = text[0].toUpperCase();
		if (char =="C" && text.length > 1 && text[1].toUpperCase() == "H"){
			char = "Ch";
			text = text.slice(1);
		}
		text = text.slice(1);

		model.playAnimationForText(char);
	}


</script>

<div class="controls">
	<p>Pro správnou funkčnost držte stále zobrazenou dlaň na kameře.</p>
	<input type="text" bind:value={customString} placeholder="{DEFAULT_STRING}">
	<button on:click={start}>Spustit</button>
	<button on:click={replay}>Přehrát znovu</button>
</div>

<p class="text">
	<strong class="char_to_show">
		{display_char}
	</strong>
</p>

<style>

		.controls{
				margin-top: 50px;
				padding: 5px;
				display: grid;
				grid-template-columns: 1fr;
		}

		.controls > *{
				padding: 5px;
				margin-bottom: 10px;
		}

		.text{
				text-align: center;
		}

		.char_to_show{
			font-size: 3em;
			font-weight: bold;
		}

</style>
