<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	export let model : Model;
	export let data : any;

	let wordsToShow = [...data];



	function animate(txt : string){
			model.playAnimationForText(txt);
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

</script>

<p>
	Zde vidíte všechny znaky, nezašedlé položky již umíte.
	Pro přehrání daného znaku klikněte myší.
</p>
<h3>Česká jednoruční prstová abeceda</h3>

<div class="letters">
	{#each data as letter}
		{#if letter.str.length === 1 || letter.str === "ch"}
			<span class="letter" class:learned={letter.learned} on:click={() => {animate(letter.str)}}>{letter.str}</span>
		{/if}
	{/each}
</div>


<h3>Česká obouruční prstová abeceda</h3>
<div class="letters">
	todo
</div>

<hr>
<h3>Základní znaky ČZJ</h3>
<input type="text" placeholder="Vyhledávač..." on:keyup={SearchInputOnChange} bind:value={searchInput}>

<div class="words">


{#each wordsToShow as word}
	{#if word.str.length > 1 && word.str !== "ch"}
		<div class="word" class:learned={word.learned} on:click={() => {animate(word.str)}}>{word.str}</div>
	{/if}

{/each}

</div>

<style>
		.letters{
				margin-left: 1rem;
		}
	.letter{
			margin-right: 10px;
      padding: 2px;
	}

	.words{
			display: flex;
			flex-wrap: wrap;
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


</style>