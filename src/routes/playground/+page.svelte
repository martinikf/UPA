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
	let webcamMode : string = "";

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
<div class="mode_container">
	<ul class="mode_list">
		<li><button on:click={() => {mode = "translator"}}>Překladač</button></li>
		<li><button on:click={() => {mode = "practice"}}>Procvičení odezírání</button></li>
		{#if webcam}
			<li><button on:click={() => {webcamMode = "practice"}}>Procvičení znakování</button></li>
			<li><button on:click={() => {webcamMode = "transcript"}}>Přepis</button></li>
			<li><button on:click={() => {webcamMode = "interactive"; mode = "interactive";}}>Interaktivní režim</button></li>
		{/if}
	</ul>
</div>



<div class="content_container">
	<div class="animation_canvas">
		<Scene bind:model={model} bind:this={scene} bind:showLetter={displayLetter}/>
	</div>

	<div>
		{#if mode === 'translator'}
			<Translator bind:model={model} />
		{:else if mode === 'practice'}
			<Practice bind:model={model} />
		{/if}
		{#if mode === 'interactive'}
			<Interactive bind:model={model} bind:landmarkDetection={landmarkDetection} bind:this={interactive} />
		{/if}
		{#if webcam && webcamMode === 'practice'}
			<SpellActivity bind:this={spellActivity} bind:landmarkDetection={landmarkDetection} />
		{:else if webcam && webcamMode === 'transcript'}
			<Transcript bind:this={transcript} bind:landmarkDetection={landmarkDetection} />
		{/if}
	</div>

	<div class="webcam_container">
		{#if webcam}
			<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
		{:else}
			<button on:click={() => {webcam = !webcam}}>Zapnout kameru</button>
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
				width: 80%;
				margin: auto;
				grid-template-columns: 1fr 1fr 1fr;
		}

		.animation_canvas{
        width: 440px;
        height: 480px;
        border: solid 2px black;

        position: relative;
        background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
		}

		.webcam_container{
			position: relative;
				height: 480px;
				width: 640px;
			border: solid 2px black;
		}

		.mode_container{
				margin-left: 10%;
				margin-bottom: 50px;
		}
		.mode_list{
				margin: 0;
				padding: 0;
				list-style: none;
		}

		.mode_list li{
				display: inline;
		}
</style>
