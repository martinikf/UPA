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
	let displayLetter : boolean = true;

	let transcript : Transcript;
	let spellActivity : SpellActivity;
	let interactive : Interactive;

	let landmarkDetection: LandmarkDetection;

	let controlRow : ControlRow;

	//Landmark message forwarder to the correct component
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

	function displayLetterHandler(){
		if(mode == "practice"){
			displayLetter = false;
		}
		else{
			displayLetter = true;
		}
	}

	function toggleLanguagesModeHandler(){
		if(mode == "translator" || mode == "practice"){
			controlRow.enableToggleMode();
		}
		else{
			controlRow.disableToggleMode();
		}
	}

	function modeButtonOnClick(){
		model.resetAnimation();
		displayLetterHandler();
		toggleLanguagesModeHandler();
	}

	function toggleWebcam(){
		if(webcam && landmarkDetection) {
			landmarkDetection.disableCam();
			mode = "translator";
			modeButtonOnClick();
		}

		webcam = !webcam;
	}

</script>

<div class="mode_container">
	<h3>Režimy UPA</h3>
	<div class="mode_flex">
		<ul class="mode_list left">
			<li><button on:click={() => {mode = "translator"; modeButtonOnClick(); }}>Překladač</button></li>
			<li><button on:click={() => {mode = "practice"; modeButtonOnClick(); }}>Procvičení odezírání</button></li>
		</ul>
		<ul class="mode_list middle">
			<li>
				<button class="webcam_button" on:click={toggleWebcam}>
					{webcam ? "Vypnout kameru" : "Zapnnout kameru"}
				</button>
			</li>
		</ul>
			<ul class="mode_list right">
			{#if webcam}
				<li><button on:click={() => {mode = "practiceWebcam"; modeButtonOnClick(); }}>Procvičení znakování</button></li>
				<li><button on:click={() => {mode = "transcript"; modeButtonOnClick(); }}>Přepis</button></li>
				<li><button on:click={() => {mode = "interactive"; modeButtonOnClick(); }}>Interaktivní režim</button></li>
			{/if}
		</ul>
	</div>
</div>


<div class="content_container">
	<div class="animation">
		<div class="animation_canvas">
			<Scene bind:model={model} bind:this={scene} showLetter={displayLetter}/>
		</div>
		<ControlRow bind:this={controlRow} model={model}/>
	</div>

	<div class="control_container">
		{#if mode === 'translator'}
			<Translator model={model} />
		{:else if mode === 'practice'}
			<Practice model={model} />
		{:else if mode === 'interactive'}
			<Interactive model={model} bind:this={interactive} />
		{:else if webcam && mode === 'practiceWebcam'}
			<SpellActivity bind:this={spellActivity} model={model} />
		{:else if webcam && mode === 'transcript'}
			<Transcript bind:this={transcript} model={model}/>
		{/if}
	</div>

	<div class="webcam_container">
		{#if webcam}
				<div class="webcam">
					<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage}/>
					<button id="toggle_show_video" on:click={() => {landmarkDetection.toggleShowVideo();}}></button>
				</div>
		{/if}
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
	}

  .mode_container{
		width: 80%;
		max-width: 1600px;
		margin: auto auto 2rem;
  }

	.mode_flex{
		display: grid;
		grid-template-columns: 4fr 1fr 4fr;
	}

	.right{
		justify-self: right;
	}

  .mode_list{
		margin: 0;
		padding: 0;
		list-style: none;
  }

	.middle{
			justify-self: center;
	}

  .mode_list li{
		display: inline-block;
  }

  .mode_list li button{
		padding: 5px;
  }

	.content_container{
		display: flex;
		justify-content: space-between;
		width: 80%;
		max-width: 1600px;
		margin: auto;
	}

	.animation{
		width: 100%;
		max-width: 400px;
	}

	.animation_canvas{
		border: solid 2px black;
		position: relative;
		background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
		height: 300px;
		width: 400px;
	}

	.control_container{
		min-width: 400px;
		margin-left: 2rem;
		margin-right: 2rem;
		margin-top: 50px;
	}

	.webcam_container{
		width: 400px;
	}

	.webcam{
		position: relative;
		margin-top: 5px;
		border: solid 2px black;
	}

	#toggle_show_video{
		background-color: transparent;
		border: none;
		padding: 0;
		margin: 0;
		position: absolute;
		top: 0;
		right: 0;
		width: 100%;
		height: 100%;
	}

	@media (max-width: 1400px) {
		.mode_container{
			width: 90%;
		}

		.mode_flex{
				grid-template-columns: 1fr;
		}
		.mode_flex > *{
				margin-bottom: 5px;
		}
		.right{
				justify-self: left;
		}

		.control_container{
			min-width: 200px;
			margin-right: 0;
			margin-top: 0;
		}

		.content_container{
			width: 90%;
			display: grid;
			grid-template-columns: 1fr 1fr;
		}

      .middle{
          justify-self: left;
      }
	}

	@media (max-width: 768px) {
		.content_container{
			display: grid;
			grid-template-columns: 1fr;
			width: 95%;
		}

		.content_container > *{
			margin: auto;
		}

		.control_container{
			width: 100%;
			margin-top: 15px;
		}
  }

  @media (max-width: 480px) {

		.mode_flex > *{
			justify-self: right;
		}

		.webcam_container {
			width: 300px;
		}

		.animation{
				width: 300px;
				margin: auto;
		}

		.animation_canvas{
			width: 300px;
			height: 300px;
		}
  }
</style>
