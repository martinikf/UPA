<script lang="ts">
	/**
	 * Svelte component for rendering a 3D animated model on a canvas with
	 * Orbit controls, a perspective camera, and ambient light. This component
	 * is built using Threlte (a Svelte wrapper for Three.js).
	 *
	 * The component includes:
	 * - A 'model' reference to an instance of AnimatedModel.
	 * - A 'showLetter' boolean to control the visibility of the currently
	 *   displayed letter in the animation.
	 *
	 * The displayed letter updates dynamically in the top-right corner of the
	 * screen based on the letter being played by the model.
	 */

	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';

	import Model from './AnimatedModel.svelte';
	import AbsoluteCenteredLoadingCircle from '$lib/components/shared/AbsoluteCenteredLoadingCircle.svelte';
	import { onMount } from 'svelte';

	export let model: Model;
	export let showLetter = true;

	/** Bound variable for displaying the currently played letter */
	let letterDisplay: string = '';

	let initDelay = true;

	onMount(() => {
		setTimeout(() => {
			initDelay = false;
		}, 500)});

</script>

{#if !model || initDelay}
	<AbsoluteCenteredLoadingCircle />
{/if}

<Canvas>
	<T.PerspectiveCamera makeDefault position={[0, 0, 0.8]} fov={60}>
		<OrbitControls autoRotate={false} enableZoom={true} enableDamping={false} />
	</T.PerspectiveCamera>

	<T.AmbientLight intensity={5} />

	<Model bind:this={model} bind:letterDisplay />
</Canvas>

{#if showLetter && model}
	<div class="text" id="text">{letterDisplay}</div>
{/if}

<style>
	.text {
		position: absolute;
		top: 5%;
		left: 80%;
		font-size: 48px;
		font-family: Arial, Helvetica, sans-serif;
		font-weight: bold;
	}
</style>
