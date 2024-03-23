<script lang="ts">
	import Model from './AnimatedModel.svelte';

	export let model : Model | undefined = undefined;
	let speed : number = 1;
	let pauseButtonText = "⏸";


	function resetOnClick(){
		if(model === undefined) return;

		model.resetAnimation();
		pauseButtonText = "⏸";
	}

	function pauseResumeOnClick(){
		if(model === undefined) return;

		model.pauseResumeAnimation();
		pauseButtonText = model.isPaused ? "⏵" : "⏸";
	}

</script>

<div class="control_row">
	<div>
		<label for="speed_slider">Rychlost</label>
		<input type="range" id="speed_slider" min="0" max="3" step="0.2" bind:value={speed} on:change={() => {model ? model.changeSpeed(speed) : null}} />
	</div>
	<div>
		<button on:click={() => {resetOnClick()}}>Reset</button>
		<button on:click={() => {pauseResumeOnClick()}}>{pauseButtonText}</button>
	</div>
</div>

<style>
    .control_row{
			display: flex;
			flex-direction: row;
			justify-content: space-between;
    }

		.control_row > *{
			padding: 5px;
		}

		#speed_slider{
			margin-bottom: -.4rem;
		}

		@media (max-width: 400px){
			.control_row{
					display: block;
			}

			.control_row div{
				display: flex;
				flex-direction: row;
				justify-content: end;
			}

        #speed_slider{
            margin-bottom: 0;
						margin-left: 10px;
        }

			button{
          margin-left: 10px;
					padding: 8px;
			}
		}

</style>