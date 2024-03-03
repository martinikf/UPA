<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import Model from './AnimatedModel.svelte';
	import Scene from './Scene.svelte';

	let scene : Scene;
	let model : Model;
	let landmarkDetection: LandmarkDetection;

	let speed = 1;

	const alphabet = "aábcčdďeéěfghchiíjklmnňoópqrřsštťuúůvwxyýzž";

	let text : string;

	let running : boolean = false;

	let timeout = 0;

	function handleMessage(msg : any) {
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

		text = alphabet;

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

<div class="flex">
	<div class="animation">
		<Scene bind:model={model} bind:this={scene}/>
	</div>

	<div id="charToShow">
		{display_char}
	</div>

	<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
</div>


<button on:click={start}>Zapnout</button>
<button on:click={replay}>Přehrát znovu</button>

<input type="range" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model.changeSpeed(speed)}} />

<style>
    .animation{
        width: 400px;
        height: 400px;
        position: relative;
        background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
    }

		.flex{
				display: flex;
				flex-direction: row;
				justify-content: space-around;
		}

		#charToShow{
			font-size: 3em;
			font-weight: bold;

				width: 100px;
		}
</style>
