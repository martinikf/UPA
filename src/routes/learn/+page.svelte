<script lang="ts">

import Model from '$lib/components/AnimatedModel.svelte';
import Scene from '$lib/components/Scene.svelte';
import ControlRow from '$lib/components/ControlRow.svelte';
import { Language, Word } from '$lib/components/models/Word';

import Review from './Review.svelte'
import Practice from './Practice.svelte'
import Learn from './Learn.svelte'


let currentMode = 'review';
let scene : Scene;
let model : Model;
let controlRow : ControlRow;

$: showString = currentMode != 'practice'

function buildList() : Word[]{
	let lettersCz = 'abcdefghijklmnopqrstuvwxyz'.split('');
	//Add letter 'ch'
	lettersCz.splice(8, 0, 'ch');

	let words = ["auto", "autobus"]; //TODO, load dynamically from model

	let listOfAllWords = [];

	//Build a list of czech alphabet
	for(let i = 0; i < lettersCz.length; i++) {
		listOfAllWords.push(new Word(lettersCz[i], Language.CzechFingerOneHand, false));
		listOfAllWords.push(new Word(lettersCz[i], Language.CzechFingerTwoHand, false));
	}

	for(let i = 0; i < words.length; i++) {
		listOfAllWords.push(new Word(words[i], Language.Czech, false));
	}

	return listOfAllWords;
}

let data = buildList();

</script>

<div class="learn">

	<h2>Režim učitel</h2>
	<p>Tento režim slouží k postupnému učení prostové abecedy a základních znaků.</p>

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
			<ControlRow model={model} bind:this={controlRow}/>
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
			margin: auto;
			display: grid;
			grid-template-columns: 1fr 2fr;
	}

  .animation{
      width: 100%;
      max-width: 400px;
			margin-right: 2rem;
  }

  .tabs{
      list-style: none;
			display: flex;

			justify-content: left;
      padding: 0;
      margin: 0 0 2rem;
  }

	.tabs ul{
			padding: 0;
			margin: 0;
			display: flex;
      gap: 0.5rem;
	}

  .tabs li{
      display: inline-block;
  }

	.tabs li button{
      padding: 5px;
  }

  .tabs li button{
      padding: 5px;
			font-size: 1rem;
  }

  .animation_canvas{
      border: solid 2px black;
      position: relative;
      background: linear-gradient(0deg, rgb(255, 115, 0) 0%, rgb(255, 216, 0) 35%, rgb(0, 86, 184) 100%);
      height: 300px;
      width: 400px;
  }

  @media (max-width: 1400px) {

  }

  @media (max-width: 768px) {
			.content{
					grid-template-columns: 1fr;

			}
      .tabs{
          justify-content: right;
      }

			.animation{
					margin: auto;
			}

			.learn{
					width: 90%;
			}

  }

  @media (max-width: 480px) {
      .learn{
          width: 95%;
      }
  }
</style>