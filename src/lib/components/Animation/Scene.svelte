<script lang="ts">
	/**
	 * Svelte component for rendering the main 3D scene using Threlte.
	 * Sets up the Canvas, PerspectiveCamera, OrbitControls for user interaction,
	 * AmbientLight, and embeds the AnimatedModel component.
	 * Optionally displays the letter currently being animated by the model.
	 * Shows an initial loading indicator.
	 *
	 * @prop {Model | undefined} model - Output binding providing access to the instance of the embedded AnimatedModel component once it's mounted.
	 * @prop {boolean} [showLetter=true] - Controls whether the currently animated letter is displayed in the top-right corner.
	 */

	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';

	import Model from './AnimatedModel.svelte';
	import AbsoluteCenteredLoadingCircle from '$lib/components/Shared/AbsoluteCenteredLoadingCircle.svelte';
	import { onMount } from 'svelte';

	/** Output binding that holds the instance of the child AnimatedModel component. */
	export let model: Model;
	/** Controls the visibility of the letter display overlay. Defaults to true. */
	export let showLetter = true;

	/** Input binding receiving the currently played letter from the AnimatedModel child component. */
	let letterDisplay: string = '';

	/** State variable to manage the initial loading indicator visibility. */
	let initDelay = true;

	/**
	 * Svelte lifecycle function runs after the component mounts.
	 * Used here to hide the initial loading indicator after a short delay,
	 * allowing time for the 3D model to potentially load/initialize.
	 */
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
	<div class="absolute top-4 right-6 text-5xl font-bold" id="text">{letterDisplay}</div>
{/if}

