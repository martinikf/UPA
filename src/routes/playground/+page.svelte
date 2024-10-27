<script lang="ts">
	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';
	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	import Translator from '$lib/components/Translator.svelte';
	import Practice from '$lib/components/Practice.svelte';

	import SpellActivity from '$lib/components/SpellActivity.svelte';
	import Transcript from '$lib/components/Transcript.svelte';
	import Interactive from '$lib/components/Interactive.svelte';

	import type { GestureProbability } from '$lib/components/models/GestureProbability';
	import { PlaygroundModes } from '$lib/components/models/PlaygroundModes';

	let mode: PlaygroundModes = PlaygroundModes.Translator;
	let webcam: boolean = false;

	let scene: Scene;
	let model: Model;
	let displayLetter: boolean = true;

	let transcript: Transcript;
	let spellActivity: SpellActivity;
	let interactive: Interactive;

	let landmarkDetection: LandmarkDetection;

	let controlRow: ControlRow;

	//Landmark message forwarder to the correct component
	function handleMessage(msg: CustomEvent<GestureProbability>) {
		//let result = msg.detail;
		if (webcam && mode === PlaygroundModes.Spelling) {
			spellActivity.handleMessage(msg);
		} else if (webcam && mode === PlaygroundModes.Transcript) {
			transcript.handleMessage(msg);
		} else if (webcam && mode === PlaygroundModes.Interactive) {
			interactive.handleMessage(msg);
		}
	}

	function displayLetterHandler() {
		if (mode == PlaygroundModes.Practice) {
			displayLetter = false;
		} else {
			displayLetter = true;
		}
	}

	function modeButtonOnClick() {
		model.resetAnimation();
		displayLetterHandler();
	}

	function toggleWebcam() {
		if (webcam && landmarkDetection) {
			landmarkDetection.disableCam();
			mode = PlaygroundModes.Translator;
			modeButtonOnClick();
		}

		webcam = !webcam;
	}
</script>

<!-- MODE SELECTION -->
<div class="mode_container">
	<h3>Režimy UPA pro českou prstovou abecedu</h3>
	<div class="mode_flex">
		<ul class="mode_list left">
			<li>
				<button
					on:click={() => {
						mode = PlaygroundModes.Translator;
						modeButtonOnClick();
					}}
				>
					Překladač
				</button>
			</li>
			<li>
				<button
					on:click={() => {
						mode = PlaygroundModes.Practice;
						modeButtonOnClick();
					}}
				>
					Procvičení odezírání
				</button>
			</li>
		</ul>
		<ul class="mode_list middle">
			<li>
				<button class="webcam_button" on:click={toggleWebcam}>
					{webcam ? 'Vypnout kameru' : 'Zapnout kameru'}
				</button>
			</li>
		</ul>
		<ul class="mode_list right">
			{#if webcam}
				<li>
					<button
						on:click={() => {
							mode = PlaygroundModes.Spelling;
							modeButtonOnClick();
						}}
					>
						Procvičení znakování
					</button>
				</li>
				<li>
					<button
						on:click={() => {
							mode = PlaygroundModes.Transcript;
							modeButtonOnClick();
						}}
					>
						Přepis
					</button>
				</li>
				<li>
					<button
						on:click={() => {
							mode = PlaygroundModes.Interactive;
							modeButtonOnClick();
						}}
						>
						Interaktivní režim
					</button>
				</li>
			{/if}
		</ul>
	</div>
</div>

<!-- ANIMATION and ControlRow -->
<div class="content_container">
	<div class="animation">
		<div class="animation_canvas">
			<Scene bind:model bind:this={scene} showLetter={displayLetter} />
		</div>
		<ControlRow bind:this={controlRow} {model} />
	</div>

	<!-- CONTROLS -->
	<div class="control_container">
		{#if mode === PlaygroundModes.Translator}
			<Translator {model} />
		{:else if mode === PlaygroundModes.Practice}
			<Practice {model} />
		{:else if mode === PlaygroundModes.Interactive}
			<Interactive {model} bind:this={interactive} />
		{:else if webcam && mode === PlaygroundModes.Spelling}
			<SpellActivity bind:this={spellActivity} {model} />
		{:else if webcam && mode === PlaygroundModes.Transcript}
			<Transcript bind:this={transcript} {model} />
		{/if}
	</div>

	<!-- WEBCAM -->
	<div class="webcam_container">
		{#if webcam}
			<div class="webcam">
				<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
				<button
					id="toggle_show_video"
					on:click={() => {
						landmarkDetection.toggleShowVideo();
					}}
				></button>
			</div>
		{/if}
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
	}

	.mode_container {
		width: 80%;
		max-width: 1600px;
		margin: auto auto 2rem;
	}

	.mode_flex {
		display: grid;
		grid-template-columns: 4fr 1fr 4fr;
	}

	.right {
		justify-self: right;
	}

	.mode_list {
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.middle {
		justify-self: center;
	}

	.mode_list li {
		display: inline-block;
	}

	.mode_list li button {
		padding: 5px;
	}

	.content_container {
		display: flex;
		justify-content: space-between;
		width: 80%;
		max-width: 1600px;
		margin: auto;
	}

	.animation {
		width: 100%;
		max-width: 400px;
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
		height: 300px;
		width: 400px;
	}

	.control_container {
		min-width: 400px;
		margin-left: 2rem;
		margin-right: 2rem;
		margin-top: 50px;
	}

	.webcam_container {
		width: 400px;
	}

	.webcam {
		position: relative;
		margin-top: 5px;
		border: solid 2px black;
	}

	#toggle_show_video {
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
		.mode_container {
			width: 90%;
		}

		.mode_flex {
			grid-template-columns: 1fr;
		}
		.mode_flex > * {
			margin-bottom: 5px;
		}
		.right {
			justify-self: left;
		}

		.control_container {
			min-width: 200px;
			margin-right: 0;
			margin-top: 0;
		}

		.content_container {
			width: 90%;
			display: grid;
			grid-template-columns: 1fr 1fr;
		}

		.middle {
			justify-self: left;
		}
	}

	@media (max-width: 768px) {
		.content_container {
			display: grid;
			grid-template-columns: 1fr;
			width: 95%;
		}

		.content_container > * {
			margin: auto;
		}

		.control_container {
			width: 100%;
			margin-top: 15px;
		}

		.mode_flex > * {
			justify-self: right;
		}
	}

	@media (max-width: 480px) {
		.content_container {
			position: relative;
		}

		.webcam_container {
			width: 100px;
			position: absolute;
			left: 3%;
			top: -3%;
		}

		.animation {
			width: 300px;
			margin: auto;
		}

		.animation_canvas {
			width: 300px;
			height: 300px;
		}
	}
</style>
