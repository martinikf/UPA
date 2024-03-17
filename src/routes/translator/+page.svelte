<script lang="ts">
  import Translator from '$lib/components/Translator.svelte'
	import Model from '$lib/components/AnimatedModel.svelte';
	import Scene from '$lib/components/Scene.svelte';

	let scene : Scene;
	let model : Model;
	let displayLetter : boolean = false;

</script>

<h2>Překladač z textu do prstové abecedy</h2>

<Translator bind:model={model}/>

<div class="animation_canvas">
	<Scene bind:model={model} bind:this={scene} bind:showLetter={displayLetter}/>
</div>

<style>
  :global(body) {
    margin: 0;
  }

  .animation_canvas{
      width: 400px;
      height: 500px;
      position: relative;
      background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
  }

</style>
