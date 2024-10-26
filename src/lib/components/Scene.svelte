<script lang="ts">
	/**
	 * Svelte component for creating a canvas with the AnimatedModel inside
	 * based on three.js
	 *
	 * Creates a canvas with Orbit controls, Perspective camera and Ambient light
	 * Text display in right top corner for displaying the currently played letter
	 *
	 * Provides 'model' reference to AnimatedModel
	 * Provides 'showLetter' boolean for controlling the display of a playing letter in the animation
	 */

	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';

	import Model from './AnimatedModel.svelte';

	export let model: Model;
	export let showLetter = true;

	/** Bound variable for displaying the currently played letter */
	let letterDisplay: string = '';
</script>

<Canvas>
	<T.PerspectiveCamera makeDefault position={[0, 0, 0.8]} fov={60}>
		<OrbitControls autoRotate={false} enableZoom={true} enableDamping={false} />
	</T.PerspectiveCamera>

	<T.AmbientLight intensity={4} />

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
