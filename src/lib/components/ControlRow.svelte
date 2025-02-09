<script lang="ts">
	/**
	 * Svelte component for controlling the animation
	 *
	 * Provides controls for changing the speed of the animation, pausing, resuming it and resetting it.
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Button, Label, Range } from 'flowbite-svelte';

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
		<Label for="animation_speed_slider">Rychlost</Label>

		<Range  id = "animation_speed_slider"
						min = "0"
						max = "4"
						step = "0.2"
						bind:value = {speed}
						size="md"/>
	</div>

	<!-- Reset and pause/resume buttons-->
	<div>
		<Button on:click={() => {	resetOnClick(); }}>
			Reset
		</Button>

		<Button on:click={() => { pauseResumeOnClick();	}}>
			{pauseButtonText}
		</Button>
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

	@media (max-width: 480px) {
		.control_row {
			display: block;
		}

		.control_row div {
			display: flex;
			flex-direction: row;
			justify-content: end;
		}
	}
</style>
