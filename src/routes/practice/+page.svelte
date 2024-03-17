<script lang="ts">
  import Practice from '$lib/components/Practice.svelte'
	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';

	let scene : Scene;
	let model : Model;
	let displayLetter : boolean = false;

</script>

<h2>Procvičení odezírání</h2>

<Practice bind:model={model}/>

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
  