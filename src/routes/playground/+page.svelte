<script lang="ts">
	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte'
	import Scene from '$lib/components/Scene.svelte'
	import Model from '$lib/components/AnimatedModel.svelte';

	import Translator from '$lib/components/Translator.svelte'
	import Practice from '$lib/components/Practice.svelte'

	import SpellActivity from '$lib/components/SpellActivity.svelte';
	import Transcript from '$lib/components/Transcript.svelte';

	import Interactive from '$lib/components/Interactive.svelte';


	let mode : string = 'translator';
	let webcam : boolean = false;
	let webcamMode : string = "practice";

	let scene : Scene;
	let model : Model;
	let displayLetter : boolean = false;

	let transcript : Transcript;
	let spellActivity : SpellActivity;
	let interactive : Interactive;

	let landmarkDetection: LandmarkDetection;

	function handleMessage(msg : any) {
		//let result = msg.detail;
		if(webcam && webcamMode === 'practice') {
			spellActivity.handleMessage(msg);
		} else if(webcam && webcamMode === 'transcript') {
			transcript.handleMessage(msg);
		}
		else if(webcam && webcamMode === 'interactive') {
			interactive.handleMessage(msg);
		}

	}

</script>

<h2>Učitel prstové abecedy</h2>
<ul>
	<li><button on:click={() => {mode = "translator"}}>Překladač</button></li>
	<li><button on:click={() => {mode = "practice"}}>Procvičení odezírání</button></li>
	<li><button on:click={() => {webcam = !webcam}}>Kamera</button></li>
	{#if webcam}
		<li><button on:click={() => {webcamMode = "practice"}}>Procvičení znakování</button></li>
		<li><button on:click={() => {webcamMode = "transcript"}}>Přepis</button></li>
		<li><button on:click={() => {webcamMode = "interactive"; mode = "interactive";}}>Interaktivní režim</button></li>
	{/if}
</ul>


<div class="content_container">
	<div class="animation_container">
		{#if mode === 'translator'}
			<Translator bind:model={model} />
		{:else if mode === 'practice'}
			<Practice bind:model={model} />
		{/if}
		{#if mode === 'interactive'}
			<Interactive bind:model={model} bind:landmarkDetection={landmarkDetection} bind:this={interactive} />
		{/if}


		<div class="animation_canvas">
			<Scene bind:model={model} bind:this={scene} bind:showLetter={displayLetter}/>
		</div>
	</div>

	<div class="webcam_container">
		{#if webcam && webcamMode === 'practice'}
			<SpellActivity bind:this={spellActivity} bind:landmarkDetection={landmarkDetection} />
		{:else if webcam && webcamMode === 'transcript'}
			<Transcript bind:this={transcript} bind:landmarkDetection={landmarkDetection} />
		{/if}

		{#if webcam}
			<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
		{/if}
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
				grid-template-columns: 1fr 1fr;
		}

		.animation_canvas{
        width: 400px;
        height: 500px;
        position: relative;
        background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
		}
</style>
