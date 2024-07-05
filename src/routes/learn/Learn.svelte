<script lang="ts">

	import Model from '$lib/components/AnimatedModel.svelte';

	export let data : any;

	export let model : Model;

	function animate(txt : string){
		model.playAnimationForText(txt);
	}

	function firstUnlearned(){
		let i = 0;
		while(data[i].learned){
			i++;
		}
		console.log("First unlearned: ", i);
		return i;
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
	Bude vám zobrazeno písmeno a zároveň i jeho zobrazení, zkuste si jej co nejlépe zapomatovat.
	Po stisknutí tlačítka "Už umím" jej budete vídat v oblasti procvičování.
</p>

<h3>Učíte se: {data[i].str}</h3>

<button on:click={play}>Přehrát znovu</button>

<button on:click={learned}>Už umím!</button>