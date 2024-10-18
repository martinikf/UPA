<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';
	import { Language, Word } from '$lib/components/models/Word';

	export let data : Word[];

	let languageSet : Word[] = []; //Used for subset of data for specific language
	let selectedLanguageSet : Language = Language.CzechFingerOneHand;

	export let model : Model;

	let i = -1;
	let playCount = 0;
	let everythingLearned = false;

	//Plays animation for given word
	function animate(word : Word | null){
		if(word == null) return;

		model.playAnimationForText(word.str, word.language);
	}

	//Auxiliary function to find first unlearned word in languageSet
	function firstUnlearned(){
		let j = 0;
		while(languageSet.length > j && languageSet[j].learned){
			j++;
		}

		return j;
	}

	//Updates language set based on selected language, triggered in play() if languageSet is empty
	function updateLanguageSet() {
		languageSet = data.filter((word) => word.language == selectedLanguageSet);
	}

	//Main function for learning, starts animation of current word
	function play(){
		if(languageSet.length == 0)
			updateLanguageSet();

		if (i == -1)
			i = firstUnlearned();

		if(languageSet.length == i) {
			everythingLearned = true;
			return;
		}

		animate(languageSet[i]);
		playCount++;
	}

	//Event handler for learned button, marks current word as learned and moves to next
	function learned(){
		if (i == -1 || playCount < 1) return;

		languageSet[i].learned = true;
		playCount = 0;
		i = i+1;

		//If word is learned, play animation for the next word
		play();
	}

	//Event handler for language change, resets state to default
	function onLanguageChange(){
		i = -1;
		playCount = 0;
		languageSet = [];
		everythingLearned = false;
		play()
	}

	//On load start playing
	play();

</script>

<h2>Učit</h2>
<p>
	Bude vám zobrazeno písmeno/znak, zkuste si jej co nejlépe zapomatovat. <br/>
	Po stisknutí tlačítka "Už umím" jej budete vídat v oblasti procvičování.
</p>

<div class="language_selection">
	<label for="language">Jazyk:</label>
	<select id="language" bind:value={selectedLanguageSet} on:change={onLanguageChange}>
		<option value="{Language.CzechFingerOneHand}">Česká prstová abeceda jednoruční</option>
		<option value="{Language.CzechFingerTwoHand}">Česká prstová abeceda obouruční</option>
		<option value="{Language.Czech}">Česká znakový jazyk</option>
		<!-- <option value="cz">ASL</option> -->
	</select>
</div>


{#if everythingLearned}
	<h3>Všechno jste se naučili!</h3>
{/if}

{#if !everythingLearned}
	<h3>Učíte se: {languageSet[i].str}</h3>
{/if}

<div class="control_buttons">
	<button on:click={play} disabled={everythingLearned}>Přehrát znovu</button>

	<button on:click={learned} disabled={everythingLearned}>Už umím!</button>
</div>

<style>
	h2{
			margin-top: 0;
	}

	.control_buttons button{
			display: block;
			padding: 5px;
			margin-bottom: 0.5rem;
	}

  .language_selection select{
      padding: 5px;
  }

  @media (max-width: 768px) {
			.control_buttons{
				display: flex;
				flex-direction: column;
			}
	}
</style>
