<script lang="ts">

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import { time } from '@tensorflow/tfjs';

	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	// References
	let landmarkDetection: LandmarkDetection;

	let lastMsg : GestureProbability[]= [];

	let letterFrequency : {[letter: string] : number} = createDict();

	let str: string = "";
	let parsed : string = "";

	let modelName : string = "llama3.1";
	let requestUrl : string = "http://localhost:11434/api/generate";

	/**
	 * Routes landmark detection messages to appropriate components based on current mode
	 * @param msg - Custom event containing gesture probability data
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		lastMsg = msg.detail;

		for(let i = 0; i < msg.detail.length; i++){
			const letter = msg.detail[i].letter;
			if(letter == 'None') return;
			if(i == 0){
				str += letter;
				parsed = convertToFrequencyFormat(str)
			}

			letterFrequency[letter]++;
		}
	}

	function createDict() : {[letter: string] : number}{
		let lettersCz = 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split('');
		//Add letter 'ch' after 'h'
		lettersCz.splice(8, 0, 'Ch');

		let frequency : {[letter: string] : number} = {}
		lettersCz.forEach((letter) => {
			frequency[letter] = 0;
		});

		return  frequency;
	}

	function reset(){
		letterFrequency = createDict();
		str = "";
	}

	async function send(){
		parsed = convertToFrequencyFormat(str);

		console.log("RAW: " + str);
		console.log("Parsed: " + parsed)

		await sendPrompt(parsed.trim().toLowerCase());
		str = "";
	}


	async function sendPrompt(txt : string) {
		let data = {
			'model' : modelName,
			"stream" : false,
			"prompt" : txt
		}

		const res = await fetch(requestUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const resp = await res.json();
		console.log("Response: " + resp.response)
		model.playAnimationForText(resp.response, Language.CzechFingerOneHand)
	}

	function convertToFrequencyFormat(input: string): string {
		// Configuration constants
		const MIN_GROUP_LENGTH = 6;
		const SPACE_INSERT_THRESHOLD = 20;
		const MULTI_CHAR_TOKENS = ['Ch'];
		const ERROR_CONTEXT_SIZE = 1; // Characters to check around mismatches

		// Tokenize input with multi-character support
		const tokens: string[] = [];
		let i = 0;
		while (i < input.length) {
			let matched = false;
			for (const token of MULTI_CHAR_TOKENS) {
				if (input.substr(i, token.length) === token) {
					tokens.push(token);
					i += token.length;
					matched = true;
					break;
				}
			}
			if (!matched) {
				tokens.push(input[i]);
				i++;
			}
		}

		let result = '';
		let currentToken = tokens[0];
		let count = 1;

		for (let i = 1; i <= tokens.length; i++) {
			const isValidExtension = i < tokens.length && (
				tokens[i] === currentToken ||
				(i > ERROR_CONTEXT_SIZE &&
					i < tokens.length - ERROR_CONTEXT_SIZE &&
					tokens[i - ERROR_CONTEXT_SIZE] === currentToken &&
					tokens[i + ERROR_CONTEXT_SIZE] === currentToken)
			);

			if (isValidExtension) {
				count++;
			} else {
				if (count >= MIN_GROUP_LENGTH) {
					result += currentToken;
					if (count >= SPACE_INSERT_THRESHOLD) {
						result += ' ';
					}
				}

				if (i < tokens.length) {
					currentToken = tokens[i];
					count = 1;
				}
			}
		}

		return result;
	}
</script>

<p class="text_input_display">
	{parsed}
</p>

<!-- Layout -->
<div class="layout">

	<!-- Controls -->
	<div class="controls">
		<div class="controls__flow column">
		<button on:click={send}>Send message</button>
		<button on:click={reset}>Delete current message</button>
		</div>

		<hr/>
		<!-- AI API settings -->
		<div class="controls__api column">
			<label for="model_name">Model name</label>
			<input id="model_name" type="text" bind:value={modelName} />
			<label for="request_url">Request url</label>
			<input id="request_url" type="text" bind:value={requestUrl} />
		</div>
	</div>

	<!-- Animation -->
	<div class="animation">
		<div class="animation_canvas">
			<Scene bind:model bind:this={scene} />
		</div>
		<ControlRow bind:this={controlRow} {model} />
	</div>

	<!-- WEBCAM -->
	<div class="webcam_container">
		<div class="webcam">
			<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
		</div>
	</div>
</div>

<style>
	.text_input_display{
		text-align: center;
	}

	.layout{
		display: grid;
		grid-template-columns: 1fr 3fr 1fr;
	}

	.controls{
		margin: auto;
		width: 80%;
	}

	.column{
		display: flex;
		flex-direction: column;
	}

	.column *{
    margin: 0.25rem;
	}

	.controls__flow button{
		padding: 10px;
	}

  .animation {
    width: 100%;
    max-width: 80%;
		margin: auto;
  }

  .animation_canvas {
    border: solid 2px black;
    position: relative;
    background: linear-gradient(
        0deg,
        rgb(255, 115, 0) 0%,
        rgb(255, 216, 0) 35%,
        rgb(0, 86, 184) 100%
    );
		height: 63vh;
  }

	.webcam_container{
		margin: auto;
	}


</style>