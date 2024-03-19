<script lang="ts">
	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte'
	import Scene from '$lib/components/Scene.svelte'
	import Model from '$lib/components/AnimatedModel.svelte';

	import Translator from '$lib/components/Translator.svelte'
	import Practice from '$lib/components/Practice.svelte'

	import SpellActivity from '$lib/components/SpellActivity.svelte';
	import Transcript from '$lib/components/Transcript.svelte';

	import Interactive from '$lib/components/Interactive.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	let mode : string = 'translator';
	let webcam : boolean = false;

	let scene : Scene;
	let model : Model;
	let displayLetter : boolean = false;

	let transcript : Transcript;
	let spellActivity : SpellActivity;
	let interactive : Interactive;

	let landmarkDetection: LandmarkDetection;

	function handleMessage(msg : any) {
		//let result = msg.detail;
		if(webcam && mode === 'practiceWebcam') {
			spellActivity.handleMessage(msg);
		} else if(webcam && mode === 'transcript') {
			transcript.handleMessage(msg);
		}
		else if(webcam && mode === 'interactive') {
			interactive.handleMessage(msg);
		}
	}

</script>


<div class="mode_container">
	<h3>Režimy UPA</h3>
	<ul class="mode_list">
		<li><button on:click={() => {mode = "translator"}}>Překladač</button></li>
		<li><button on:click={() => {mode = "practice"}}>Procvičení odezírání</button></li>
		{#if webcam}
			<li><button on:click={() => {mode = "practiceWebcam"}}>Procvičení znakování</button></li>
			<li><button on:click={() => {mode = "transcript"}}>Přepis</button></li>
			<li><button on:click={() => {mode = "interactive"; mode = "interactive";}}>Interaktivní režim</button></li>
		{/if}
	</ul>
</div>


<div class="content_container">
	<div class="animation">
		<ControlRow bind:model={model}/>

		<div class="animation_canvas">
			<Scene bind:model={model} bind:this={scene} bind:showLetter={displayLetter}/>
		</div>
	</div>

	<div>
		{#if mode === 'translator'}
			<Translator bind:model={model} />
		{:else if mode === 'practice'}
			<Practice bind:model={model} />
		{:else if mode === 'interactive'}
			<Interactive bind:model={model} bind:landmarkDetection={landmarkDetection} bind:this={interactive} />
		{:else if webcam && mode === 'practiceWebcam'}
			<SpellActivity bind:this={spellActivity} bind:landmarkDetection={landmarkDetection} />
		{:else if webcam && mode === 'transcript'}
			<Transcript bind:this={transcript} bind:landmarkDetection={landmarkDetection} />
		{/if}
	</div>

	<div class="webcam_container">
		<button class="webcam_button" on:click={() => {webcam = !webcam}}>{webcam ? "Vypnout kameru" : "Zapnnout kameru"}</button>
		<div class="webcam">
			{#if webcam}
				<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
			{/if}
		</div>
	</div>
</div>

<svelte:head>
	<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-core"></script>
	<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-cpu"></script>
	<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite/dist/tf-tflite.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-webgpu/dist/tf-backend-webgpu.js"></script>
</svelte:head>

<style>
	:global(body) {
		margin: 0;
	}

	.content_container{
		display: grid;
		width: 80%;
		margin: auto;
		grid-template-columns: 1fr 1fr 1fr;
	}

	.animation_canvas{
		border: solid 2px black;
		position: relative;
		background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
	}

	.webcam{
		position: relative;
		border: solid 2px black;
		margin-top: 5px;
	}

	.mode_container{
		margin-bottom: 50px;
		margin-top: 15px;
		margin-left: 10%;
	}

	.mode_list{
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.mode_list li{
		display: inline-block;
	}
	.mode_list li button{
		padding: 5px;
	}

	.webcam_button{
		padding: 5px;
		width: 100%;
	}

	/* Desktops */
	@media screen and (max-width: 1200px) {
	}

	/* Laptops */
	@media screen and (max-width: 1024px) {
	}

	/* Tablets */
	@media sceen and (max-width: 768px) {
  }

	/* Phones */
  @media (max-width: 480px) {
      .content_container{
          grid-template-columns: 1fr;
          width: 98%;
      }

			.webcam{
					width: 400px;
					height: 300px;
			}
  }
</style>
