<script lang="ts">
	/**
	 * Svelte component for controlling the animation
	 *
	 * Provides controls for changing the speed of the animation, pausing, resuming it and resetting it.
	 *
	 * Requires the AnimatedModel component to be passed as a prop
	 */
	import Model from './AnimatedModel.svelte';
	import { Button, ButtonGroup, Label, Range } from 'flowbite-svelte';
	import { PauseOutline, PlayOutline, RefreshOutline } from 'flowbite-svelte-icons';


	export let model: Model | undefined = undefined;
	let speed: number = 1;
	let paused : boolean = false;

	/**
	 * Resets the animation
	 */
	function resetOnClick() {
		if (model === undefined) return;

		model.resetAnimation();
		paused = false;
	}

	/**
	 * Pauses or resumes the animation
	 */
	function pauseResumeOnClick() {
		if (model === undefined) return;

		model.pauseResumeAnimation();
		paused = !paused;
	}
</script>

<!-- Control row with speed slider, reset and pause/resume buttons -->
<div class="flex flex-row justify-between gap-4 mt-2">
	<!-- Speed slider -->
	<div>
		<Label for="animation_speed_slider" class="md:text-base text-xs">Rychlost</Label>
		<Range id = "animation_speed_slider"
					min = "0"
					max = "4"
					step = "0.2"
					bind:value = {speed}
					on:change = { () => {model?.changeSpeed(speed);} }
					size="md"
					class="mt-2 ml-2"/>
	</div>

	<!-- Reset and pause/resume buttons-->
	<div>
		<ButtonGroup>
			<Button size="xs" on:click={() => {	resetOnClick(); }}>
				<RefreshOutline />
			</Button>

			<Button size="xs" on:click={() => { pauseResumeOnClick();	}} >
				{#if paused}
					<PlayOutline />
				{:else}
					<PauseOutline />
				{/if}
			</Button>
		</ButtonGroup>
	</div>
</div>