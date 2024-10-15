<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';

	export let data : any;

	export let model : Model;

	function animate(txt : string){
		model.playAnimationForText(txt);
	}

	function firstUnlearned(){
		let j = 0;
		while(data[j].learned){
			j++;
		}
		console.log("First unlearned: ", j);
		return j;
	}

	let i = -1;
	let playCount = 0;

	function play(){
		if (i == -1)
			i = firstUnlearned();

		animate(data[i].str);
		playCount++;
	}

	function learned(){
		if (i == -1 || playCount < 1) return;

		//TODO send to server update
		data[i].learned = true;
		playCount = 0;
		i = i+1;
	}

	play();

</script>

<h2>Učit</h2>
<p>
	Bude vám zobrazeno písmeno/znak, zkuste si jej co nejlépe zapomatovat. <br/>
	Po stisknutí tlačítka "Už umím" jej budete vídat v oblasti procvičování.
</p>

<h3>Učíte se: {data[i].str}</h3>

<div class="control_buttons">
	<button on:click={play}>Přehrát znovu</button>

	<button on:click={learned}>Už umím!</button>
</div>

<style>
	.control_buttons button{
			display: block;
			padding: 5px;
			margin-bottom: 0.5rem;
	}

  @media (max-width: 768px) {
			.control_buttons{
				display: flex;
				flex-direction: column;
			}
	}
</style>
