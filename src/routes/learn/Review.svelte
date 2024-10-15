<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	export let model : Model;
	export let data : any;

	let wordsToShow = [...data];

	import { Language, Word } from '$lib/components/models/word';

	//TODO: play the sign two times
	function animate(txt : string, language : Language){
			model.playAnimationForText(txt, language);
	}

	let searchInput : string = "";

	function SearchInputOnChange(){
		if(searchInput.length > 0){
			wordsToShow = data.filter((word) => {
				return word.str.includes(searchInput);
			})
		}
		else{
			wordsToShow = [...data];
		}
	}

	console.log(data)

</script>

<h2>Přehled</h2>
<p>
	Zde vidíte všechny znaky, nezašedlé položky již umíte.
	Pro přehrání daného znaku klikněte na něj.
</p>

<h3>Česká jednoruční prstová abeceda</h3>
<div class="letters">
	{#each data as letter}
		{#if letter.language == Language.CzechFingerOneHand}
			<span class="letter" class:learned={letter.learned} on:click={() => {animate(letter.str, letter.language)}}>{letter.str}</span>
		{/if}
	{/each}
</div>


<h3>Česká obouruční prstová abeceda</h3>
<div class="letters">
	{#each data as letter}
		{#if letter.language == Language.CzechFingerTwoHand}
			<span class="letter" class:learned={letter.learned} on:click={() => {animate(letter.str, letter.language)}}>{letter.str}</span>
		{/if}
	{/each}
</div>

<hr>
<div>
	<h3>Základní znaky ČZJ</h3>
	<input type="text" class="text_input" placeholder="Vyhledávač..." on:keyup={SearchInputOnChange} bind:value={searchInput}>

	<div class="words">
		{#each wordsToShow as word}
			{#if word.language == Language.Czech}
				<div class="word" class:learned={word.learned} on:click={() => {animate(word.str, word.language)}}>{word.str}</div>
			{/if}
		{/each}
	</div>
</div>


<style>
	.letters{
			display: flex;
			flex-wrap: wrap;
			padding-left: 0.5rem;
			padding-right: 0.5rem;
	}

	.letter{
			margin-right: 10px;
      padding: 2px;
	}

	.words{
			display: flex;
			flex-wrap: wrap;
      padding-left: 0.5rem;
      padding-right: 0.5rem;
	}

	.word{
			margin-right: 10px;
      padding: 2px;
	}
	.learned{
		color: green;
	}

	.word:hover, .letter:hover{
		cursor: pointer;
	}

	.text_input{
			display: block;
			width: 95%;
			margin: auto;
	}

  @media (max-width: 768px) {
      .text_input {
          margin-bottom: 1rem;
      }

			.word, .letter {
          padding: 5px;
      }
  }

</style>