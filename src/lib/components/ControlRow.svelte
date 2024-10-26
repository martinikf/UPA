<script lang="ts">
	/**
	 * Svelte component for controlling the animation
	 *
	 * Provides controls for changing the speed of the animation, pausing, resuming it and resetting it.
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';

	export let model: Model | undefined = undefined;
	let speed: number = 1;
	let pauseButtonText = '⏸';

	/**
	 * Resets the animation
	 */
	function resetOnClick() {
		if (model === undefined) return;

		model.resetAnimation();
		pauseButtonText = '⏸';
	}

	/**
	 * Pauses or resumes the animation
	 */
	function pauseResumeOnClick() {
		if (model === undefined) return;

		model.pauseResumeAnimation();
		pauseButtonText = model.isPaused ? '⏵' : '⏸';
	}
</script>

<!-- Control row with speed slider, reset and pause/resume buttons -->
<div class="control_row">
	<!-- Speed slider -->
	<div>
		<label for="speed_slider">Rychlost</label>
		<input
			type="range"
			id="speed_slider"
			min="0"
			max="3"
			step="0.2"
			bind:value={speed}
			on:change={() => {
				model ? model.changeSpeed(speed) : null;
			}}
		/>
	</div>

	<!-- Reset and pause/resume buttons-->
	<div>
		<button
			on:click={() => {
				resetOnClick();
			}}
		>
			Reset
		</button>

		<button
			on:click={() => {
				pauseResumeOnClick();
			}}
		>
			{pauseButtonText}
		</button>
	</div>
</div>

<style>
	.control_row {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	.control_row > * {
		padding: 5px;
	}

	#speed_slider {
		margin-bottom: -0.4rem;
	}

	@media (max-width: 480px) {
		.control_row {
			display: block;
		}

		.control_row div {
			display: flex;
			flex-direction: row;
			justify-content: end;
		}

		#speed_slider {
			margin-bottom: 0;
			margin-left: 10px;
		}

		button {
			margin-left: 10px;
			padding: 8px;
		}
	}
</style>
