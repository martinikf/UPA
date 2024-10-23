<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	export let model : Model;
	export let data : Word[];

	let wordsToShow = [...data];

	import { Language, Word } from '$lib/components/models/Word';

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

	let rerender = 0;

	//When a letter is marked as learned, assume that all the previous letters are learned as well
	//When a word is marked, mark only the word itself
	function markAsLearned(word : Word){
		let language = word.language;

		//Handler for words, not finger alphabets. Just mark the word as learned and return
		if(language == Language.Czech) {
			word.learned = true;
			rerender++;
			return;
		}

		let words = data.filter((w) => {
			return w.language == language;
		});

		//Iterate over filtered words, mark them as learned and break when the word is found
		for(let i = 0; i < words.length; i++){
			words[i].learned = true;
			if(words[i].str == word.str){
				break;
			}
		}
		rerender++;
	}

</script>

<h2>Přehled</h2>
<p>
	Zde vidíte všechny znaky, nezašedlé položky již umíte. <br/>
	Pro přehrání daného znaku klikněte na něj. <br/>
	Pokud jste již v minulosti tento režim použili, dvojklikem na slovo se jej rovnou naučíte.
</p>

{#key rerender}
<h3>Česká jednoruční prstová abeceda</h3>
<div class="letters">
	{#each data as letter}
		{#if letter.language === Language.CzechFingerOneHand}
			<button class="letter" class:learned={letter.learned}
						on:dblclick={() => {markAsLearned(letter)}}
						on:click={() => {animate(letter.str, letter.language)}}>
				{letter.str}
			</button>
		{/if}
	{/each}
</div>


<h3>Česká obouruční prstová abeceda</h3>
<div class="letters">
	{#each data as letter}
		{#if letter.language === Language.CzechFingerTwoHand}
			<button class="letter" class:learned={letter.learned}
						on:dblclick={() => {markAsLearned(letter)}}
						on:click={() => {animate(letter.str, letter.language)}}>
				{letter.str}
			</button>
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
				<button class="word" class:learned={word.learned}
						 on:dblclick={() => {markAsLearned(word)}}
						 on:click={() => {animate(word.str, word.language)}}>
					{word.str}
				</button>
			{/if}
		{/each}
	</div>
</div>
	{/key}

<style>
	h2{
			margin-top: 0;
	}

	.letters{
			display: flex;
			flex-wrap: wrap;
			padding-left: 0.5rem;
			padding-right: 0.5rem;
	}

	.words{
			display: flex;
			flex-wrap: wrap;
      padding-left: 0.5rem;
      padding-right: 0.5rem;
	}

	.word, .letter{
			border: none;
			outline: none;
			margin-right: 0.25rem;
			margin-bottom: 0.25rem;
			padding: 0.5rem;
			min-width: 2rem;
	}

	.letter{
      font-weight: bold;
	}

	.learned{
		background-color: green;
	}

	.word:hover, .letter:hover{
		cursor: pointer;
	}

	.text_input{
			display: block;
			width: 95%;
      margin: auto auto 1rem;
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