<script lang="ts">

import Model from '$lib/components/AnimatedModel.svelte';
import Scene from '$lib/components/Scene.svelte';

import ControlRow from '$lib/components/ControlRow.svelte';


import Review from './Review.svelte'
import Practice from './Practice.svelte'
import Learn from './Learn.svelte'


let currentMode = 'practice';
let scene : Scene;
let model : Model;

$: showString = currentMode != 'practice'

//Fetch all signs
//Fetch user signs

let data = [{str : 'a', learned : true}, {str : 'b', learned : false}, {str : 'c', learned : false}, {str : 'd', learned : false}, {str : 'e', learned : false}, {str : 'f', learned : false}, {str : 'g', learned : false}, {str : 'h', learned : false}, {str : 'ch', learned : false}, {str : 'i', learned : false}, {str : 'j', learned : false}, {str : 'k', learned : false}, {str : 'l', learned : false}, {str : 'm', learned : false}, {str : 'n', learned : false}, {str : 'o', learned : false}, {str : 'p', learned : false}, {str : 'r', learned : false}, {str : 's', learned : false}, {str : 't', learned : false}, {str : 'u', learned : false}, {str : 'v', learned : false}, {str : 'y', learned : false}, {str : 'z', learned : false}, {str : 'zebra', learned : true}, {str : 'auto', learned : false}]


</script>

<div class="learn">

	<p>Tento režim slouží k postupnému učení prostové abecedy a poté základních znaků.</p>

	<div class="tabs">
		<ul>
			<li class:highlight={currentMode === 'practice'}>
				<button on:click={() => {currentMode = 'practice'}}>Procvičovat</button>
			</li>
			<li>
				<button on:click={()=>{currentMode = 'learn'}}>Učit</button>
			</li>
			<li>
				<button on:click={()=>{currentMode = 'review'}}>Znaky</button>
			</li>
		</ul>
	</div>

	<div class="content">

		<div class="animation">
			<div class="animation_canvas">
				<Scene bind:model={model} bind:this={scene} bind:showLetter={showString}/>
			</div>
			<ControlRow model={model}/>
		</div>

		<div class="control">
			{#if currentMode === 'practice'}
				<Practice model={model} data={data}/>
			{:else if currentMode === 'learn'}
				<Learn model={model} data={data}/>
			{:else if currentMode === 'review'}
				<Review model={model} data={data}/>
			{/if}
		</div>

	</div>
</div>

<style>

	.learn{
			width: 80%;
			max-width: 1600px;
			margin: auto auto 2rem;
	}

	.content{
			width: 80%;
			margin: auto;
			display: grid;
			grid-template-columns: 1fr 1fr;
	}

  .animation{
      width: 100%;
      max-width: 400px;
  }

  .animation_canvas{
      border: solid 2px black;
      position: relative;
      background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
      height: 300px;
      width: 400px;
  }
</style>