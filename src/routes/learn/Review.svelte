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
<h3>Prstová abeceda</h3>

{#each data as letter}
	{#if letter.str.length === 1 || letter.str === "ch"}
		<span class="letter" class:learned={letter.learned} on:click={() => {animate(letter.str)}}>{letter.str}</span>
	{/if}
{/each}

<hr>
<h3>Základní znaky</h3>
<input type="text" placeholder="Vyhledávač..." on:keyup={SearchInputOnChange} bind:value={searchInput}>

<div class="words">


{#each wordsToShow as word}
	{#if word.str.length > 1 && word.str !== "ch"}
		<div class:learned={word.learned} on:click={() => {animate(word.str)}}>{word.str}</div>
	{/if}

{/each}

</div>

<style>
	.letter{
			margin-right: 10px;
	}

	.words{
			display: flex;
			flex-wrap: wrap;
	}

	.words div{
			margin-right: 10px;
	}
	.learned{
		color: green;
	}


</style>