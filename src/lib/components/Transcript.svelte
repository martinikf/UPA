<script lang="ts">

	import LandmarkDetection from './LandmarkDetection.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	export let landmarkDetection: LandmarkDetection;

	let wordDisplay : HTMLElement | null = null;
	let winner : string | null = "-";


	export function handleMessage(msg : any) {
		let result = msg.detail;
		winner = findKeyWithMaxValue(result);
	}

	function findKeyWithMaxValue(dict: { [key: string]: number }): string | null {
		let maxKey: string | null = null;
		let maxValue: number | null = null;

		for (const key in dict) {
			if (dict.hasOwnProperty(key)) {
				const value = dict[key];

				if (maxValue === null || value > maxValue) {
					maxValue = value;
					maxKey = key;
				}
			}
		}

		return maxKey;
	}

	function confirm() {
		if(wordDisplay && winner != null){
			wordDisplay.innerHTML += winner;
		}
	}

	if(browser){
		onMount(() => {
			wordDisplay = document.getElementById("word");
		});
	}

</script>

<div id="word"> </div>

<button on:click={confirm}>Potvrdit</button>

<style> </style>