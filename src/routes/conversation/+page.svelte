<script lang="ts">

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import {
		A,
		Accordion,
		AccordionItem,
		Button,
		Checkbox,
		Heading,
		Hr,
		Input,
		Label,
		Li,
		List,
		P,
		Toggle
	} from 'flowbite-svelte';
	import { convertToFrequencyFormat, MIN_GROUP_LENGTH } from '$lib/helpers/CSLR';
	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	// References
	let landmarkDetection: LandmarkDetection;

	let systemPrompt = `You are a conversation assistant. Follow these rules:
	1. Answer in a language based on language in which was the previous message written.
	2. Your responses must be of maximum length of one sentence (around 6 words).
	3. Focus on clear, simple communication, go straight to the point.
	4. Keep the user engaged, continue in the conversation, bring new ideas, ask questions.
	5. There might be often typing errors, try to ignore them.`


	let letterFrequency : {[letter: string] : number} = createDict();

	let str: string = "";
	let parsed : string = "";

	let showChat = false;
	let showLetter = false;

	let useOpenAi : boolean = false;

	let openAiAPIKey : string = "";
	let modelNameOpenAI : string = "gpt-4o-mini";
	let requestUrlOpenAI : string = "https://api.openai.com/v1/chat/completions";

	let modelNameOllama : string = "llama3.1"
	let requestUrlOllama : string = "http://localhost:11434/api/chat"

	let chatHistory: Array<{ role: string, content: string }> = [
		{
			role: 'system',
			content: systemPrompt
		}
	];

	/**
	 * Routes landmark detection messages to appropriate components based on current mode
	 * @param msg - Custom event containing gesture probability data
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		for(let i = 0; i < msg.detail.length; i++){
			const letter = msg.detail[i].letter;
			if(letter == 'None') return;
			if(i == 0){
				str += letter;
				parsed = convertToFrequencyFormat(str)
			}

			letterFrequency[letter]++;
		}
	}

	function createDict() : {[letter: string] : number}{
		let lettersCz = 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split('');
		//Add letter 'ch' after 'h'
		lettersCz.splice(8, 0, 'Ch');

		let frequency : {[letter: string] : number} = {}
		lettersCz.forEach((letter) => {
			frequency[letter] = 0;
		});

		return  frequency;
	}

	function reset(){
		letterFrequency = createDict();
		str = "";
		parsed = "";
	}

	function resetChat(){
		chatHistory = [
			{
				role: 'system',
				content: systemPrompt
			}
		];
	}

	async function send(){
		parsed = convertToFrequencyFormat(str);

		await sendPrompt(parsed.trim().toLowerCase());
		str = "";
		parsed = "";
	}

	async function sendPrompt(txt : string) {
		chatHistory = [
			...chatHistory,
			{
				role: 'user',
				content: txt
			}
		];

		if(useOpenAi) {
			await sendOpenAiPrompt();
		}
		else {
			await sendOllamaPrompt();
		}

		scrollChatToBottom();
	}

	async function sendOllamaPrompt(){
		const data = {
			model: modelNameOllama,
			stream: false,
			messages: chatHistory
		};

		try {
			const res = await fetch(requestUrlOllama, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data)
			});

			const resp = await res.json();
			const assistantReply = resp.message?.content || "No response";

			// Add assistant response to history
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: assistantReply
				}
			];

			model.playAnimationForText(assistantReply, Language.CzechFingerOneHand);
		} catch (error) {
			console.error("API Error:", error);
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: "Error connecting to AI service"
				}
			];
		}
	}

	async function sendOpenAiPrompt(){
		const data = {
			model: modelNameOpenAI,
			messages: chatHistory
		};

		try {
			const res = await fetch(requestUrlOpenAI, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${openAiAPIKey}`
				},
				body: JSON.stringify(data)
			});

			const resp = await res.json();
			console.log(resp)
			const assistantReply = resp.choices[0].message.content || "No response";

			// Add assistant response to history
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: assistantReply
				}
			];

			model.playAnimationForText(assistantReply, Language.CzechFingerOneHand);
		} catch (error) {
			console.error("API Error:", error);
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: "Error connecting to AI service"
				}
			];
		}
	}

	function scrollChatToBottom() {
		const container = document.getElementsByClassName('messages')[0];

		setTimeout(() => {
			container.scrollTo({
				top: container.scrollHeight,
			});
		}, 250);
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.code === "Space") {
			console.log("space")
			// Prevent default space scrolling behavior
			event.preventDefault();
			str += " ".repeat(MIN_GROUP_LENGTH);
			parsed = convertToFrequencyFormat(str)

		} else if (event.code === "Backspace") {
			// Prevent default backspace behavior
			event.preventDefault();

			while(parsed[parsed.length -1] == " ") parsed = parsed.slice(0, -1);

			const lastParsedChar = parsed[parsed.length - 1];

			const indexOfLast = str.lastIndexOf(lastParsedChar);
			str = str.slice(0, indexOfLast)

			if (str.length > 0) {
				// Remove all trailing characters that match the last one
				while (str.endsWith(lastParsedChar)) {
					str = str.slice(0, str.length - 2);
				}
			}
			parsed = convertToFrequencyFormat(str)
		} else if(event.code === "Enter"){
			send()
		}
	}
</script>

<!-- Attach the event listener to the window -->
<svelte:window on:keydown={handleKeyPress} />

<main class="max-w-7xl mx-auto px-4 pb-8">
	<div class="grid grid-cols-1 md:gap-3 md:grid-cols-5">
		<!-- Left Column - Controls -->
		<div class="space-y-6 flex flex-col md:mt-12 mt-0">

			<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm order-2 md:order-1">
				<div class="aspect-auto mb-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
					<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
				</div>

				<div class="space-y-3">
					<Button class="w-full" color="primary" on:click={send}>Odeslat zprávu</Button>
					<Button class="w-full" color="blue" on:click={reset}>Odstranit aktuální zprávu</Button>
					<Button class="w-full" color="red" on:click={resetChat}>Restartovat historii</Button>

					<div class="flex flex-col space-y-3">
						<Checkbox bind:checked={showLetter} class="text-gray-700 dark:text-gray-300">Zobrazit přehrávaný znak</Checkbox>
						<Checkbox bind:checked={showChat} class="text-gray-700 dark:text-gray-300">Zobrazit konverzaci</Checkbox>
					</div>
				</div>
			</div>

			<!-- API Settings -->
			<Accordion class="bg-white dark:bg-gray-800 p-2 rounded-lg shadow-sm space-y-4 order-1 md:order-2">
				<AccordionItem open>
					<span slot="header">Nastavení modelu</span>
					<Toggle bind:checked={useOpenAi} class="w-full text-sm">OpenAI API</Toggle>
					{#if useOpenAi}
						<div class="space-y-4">
							<Heading class="block text-sm mt-2">OpenAI Nastavení</Heading>
							<div>
								<Label for="model_name_openai">Model name</Label>
								<Input id="model_name_openai" placeholder="Model name" size="sm" bind:value={modelNameOpenAI} />
							</div>
							<div>
								<Label for="request_url_openai">Request URL</Label>
								<Input id="request_url_openai" placeholder="Request url" size="sm" bind:value={requestUrlOpenAI} />
							</div>
							<div>
								<Label for="api_key_openai">API Key</Label>
								<Input id="api_key_openai" placeholder="OpenAI API key" size="sm" bind:value={openAiAPIKey} />
							</div>
						</div>
					{:else}
						<div class="space-y-4">
							<Heading class="block text-sm mt-2">Ollama Nastavení</Heading>
							<div>
								<Label for="model_name_ollama">Model name</Label>
								<Input id="model_name_ollama" placeholder="Model name" size="sm" bind:value={modelNameOllama} />
							</div>
							<div>
								<Label for="request_url_ollama">Request URL</Label>
								<Input id="request_url_ollama" placeholder="Request url" size="sm" bind:value={requestUrlOllama} />
							</div>
						</div>
					{/if}

				</AccordionItem>
			</Accordion>
		</div>

		<!-- Middle Column - Animation -->
		<div class="col-span-3 md:col-span-3">
			<P class="text-center mb-3 mt-3 text-gray-600 dark:text-gray-400">Rozpoznaný vstup: <span class="font-bold">{parsed}</span></P>
			<div class="bg-gradient-to-b from-blue-400 to-yellow-600 h-[600px] rounded-xl border-2 border-gray-200 dark:border-gray-700 shadow-lg">
				<Scene bind:model bind:this={scene} bind:showLetter={showLetter} />
			</div>
			<ControlRow bind:this={controlRow} {model} />
		</div>

		<!-- Right Column - Chat -->
		<div class="md:mt-12 mt-0">
			<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm h-[625px] flex flex-col">
				<div class="overflow-y-auto flex-1 space-y-4">
					{#each chatHistory.slice(1) as message}
						<div class="p-4 rounded-lg {message.role === 'user' ? 'bg-blue-50 dark:bg-gray-700 ml-6' : 'bg-gray-50 dark:bg-gray-700 mr-6'}">
							<Heading tag="h5" class="text-sm font-medium mb-2">{message.role === 'user' ? 'Vy' : 'Asistent'}</Heading>
							<P class="text-gray-700 dark:text-gray-300">
								{#if showChat}
									{message.content}
								{:else}
									{message.content.replace(/\S/g, '*')}
								{/if}
							</P>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>

	<Hr class="my-8" />

	<div class="prose dark:prose-invert max-w-4xl mx-auto">
		<Heading tag="h2" class="mb-6">Jak používat tento režim</Heading>

		<Heading tag="h3" class="mb-4">Obecné informace</Heading>
		<List class="space-y-3">
			<Li>Kvalita odpovědí velmi závisí na použitém LLM...</Li>
			<Li>Pro vytvoření mezery zobrazuje poslední znak...</Li>
			<Li>Chcete-li znakovat stejný znak dvakrát...</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">Klávesové zkratky</Heading>
		<List class="space-y-2">
			<Li><strong>Enter</strong> - odešle zprávu asistentovi</Li>
			<Li><strong>Space</strong> - vytvoří mezeru</Li>
			<Li><strong>Backspace</strong> - smaže poslední registrovaný znak</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">API</Heading>
		<Heading tag="h4" class="mb-3">Ollama API</Heading>
		<List class="space-y-2">
			<Li><A href="https://ollama.com/" class="text-blue-600 dark:text-blue-400">https://ollama.com/</A></Li>
			<Li>Cors nastavení: SET OLLAMA_ORIGINS='*'</Li>
		</List>

		<Heading tag="h4" class="mt-4 mb-3">Nekompatibilní API</Heading>
		<P class="mb-4">
			Pro programátory, ve zdrojovém kodu naleznete podobu API dotazů.<br>
			<A href="https://github.com/martinikf/UPA/blob/main/src/routes/conversation/%2Bpage.svelte" class="text-blue-600 dark:text-blue-400">Zdrojový kód</A>
		</P>
	</div>
</main>

<style>
  /* Custom animations */
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

</style>