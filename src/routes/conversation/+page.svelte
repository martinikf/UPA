<script lang="ts">
	/**
	 * Svelte component for the Conversation mode.
	 *
	 * Allows users to interact with an LLM (Ollama or OpenAI) by signing
	 * using the Czech one-handed finger alphabet via webcam. The user's input
	 * is transcribed in real-time, sent to the LLM, and the LLM's response
	 * is displayed as a 3D animation using the AnimatedModel component.
	 * Provides settings for API endpoints and model selection.
	 */

	import { beforeNavigate } from '$app/navigation';

	import LandmarkDetection from '$lib/components/Recognition/LandmarkDetection.svelte';

	// Import required components
	import Scene from '$lib/components/Animation/Scene.svelte';
	import Model from '$lib/components/Animation/AnimatedModel.svelte';
	import ControlRow from '$lib/components/Animation/ControlRow.svelte';

	// Import types and helpers
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

	// Component references
	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;
	let landmarkDetection: LandmarkDetection;

	// Component state
	let webcamOn : boolean = false;
	let disabledToggle = false;


	// LLM Configuration state
	let systemPrompt = `You are a conversation assistant. Follow these rules:
	1. Answer in a language based on language in which was the previous message written.
	2. Your responses must be of maximum length of one sentence (around 6 words).
	3. Focus on clear, simple communication, go straight to the point.
	4. Keep the user engaged, continue in the conversation, bring new ideas, ask questions.
	5. There might be often typing errors, try to ignore them.`
	let useOpenAi : boolean = false;
	let openAiAPIKey : string = "";
	let modelNameOpenAI : string = "gpt-4o-mini";
	let requestUrlOpenAI : string = "https://api.openai.com/v1/chat/completions";
	let modelNameOllama : string = "llama3.1"
	let requestUrlOllama : string = "http://localhost:11434/api/chat"

	// Input and Transcription state
	let str: string = "";
	let parsed : string = "";

	// UI state
	let showChat = false;
	let showLetter = false;

	// Chat history - Stores the conversation messages
	let chatHistory: Array<{ role: string, content: string }> = [
		{
			role: 'system',
			content: systemPrompt
		}
	];

	/**
	 * Handles gesture recognition events from the LandmarkDetection component.
	 * Updates the raw input string, parsed string using CSLR, and letter frequency count.
	 * @param msg - Custom event containing an array of gesture probability data. Only the most probable gesture (index 0) is used.
	 */
	function handleMessage(msg: CustomEvent<GestureProbability[]>) {
		// Ignore if no gesture probabilities are received
		if (!msg.detail || msg.detail.length === 0) return;

		for(let i = 0; i < msg.detail.length; i++){
			const letter = msg.detail[i].letter;
			// Ignore 'None' gesture
			if(letter == 'None') return;

			// Process only the most probable letter (first in the array)
			if(i == 0){
				str += letter; // Append recognized letter to the raw string
				parsed = convertToFrequencyFormat(str) // Update the parsed string using CSLR logic
			}
		}
	}

	/**
	 * Resets the current user input state (raw string, parsed string).
	 */
	function reset(){
		str = "";
		parsed = "";
	}

	/**
	 * Resets the chat history to only contain the initial system prompt.
	 */
	function resetChat(){
		chatHistory = [
			{
				role: 'system',
				content: systemPrompt
			}
		];
	}

	/**
	 * Finalizes the parsed input string and sends it to the LLM.
	 * Clears the input state afterward.
	 */
	async function send(){
		// Ensure the final parsed string is up-to-date before sending
		parsed = convertToFrequencyFormat(str);

		// Trim whitespace and convert to lowercase before sending to LLM
		await sendPrompt(parsed.trim().toLowerCase());

		// Reset input fields after sending
		str = "";
		parsed = "";
	}

	/**
	 * Adds the user's message to the chat history and triggers the appropriate LLM API call.
	 * Scrolls the chat view after the response is processed.
	 * @param txt - The user's message text to send.
	 */
	async function sendPrompt(txt : string) {
		// Add user message to history
		chatHistory = [
			...chatHistory,
			{
				role: 'user',
				content: txt
			}
		];

		// Call the selected LLM API
		if(useOpenAi) {
			await sendOpenAiPrompt();
		}
		else {
			await sendOllamaPrompt();
		}

		// Scroll chat to show the latest messages
		scrollChatToBottom();
	}


	/**
	 * Sends the current chat history to the configured Ollama API endpoint.
	 * Handles the API response, updates chat history with the assistant's reply,
	 * triggers the animation of the reply, and manages potential errors.
	 */
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

			// Animate the assistant's reply
			model.playAnimationForText(assistantReply, Language.CzechFingerOneHand);
		} catch (error) {
			console.error("API Error:", error);
			// Add error message to chat history
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: "Error connecting to AI service"
				}
			];
		}
	}

	/**
	 * Sends the current chat history to the configured OpenAI API endpoint.
	 * Handles the API response, updates chat history with the assistant's reply,
	 * triggers the animation of the reply, and manages potential errors.
	 * Requires a valid API key.
	 */
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
			// Extract assistant's message from the response structure
			const assistantReply = resp.choices[0].message.content || "No response";

			// Add assistant response to history
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: assistantReply
				}
			];

			// Animate the assistant's reply
			model.playAnimationForText(assistantReply, Language.CzechFingerOneHand);
		} catch (error) {
			console.error("API Error:", error);
			// Add error message to chat history
			chatHistory = [
				...chatHistory,
				{
					role: 'assistant',
					content: "Error connecting to AI service"
				}
			];
		}
	}

	/**
	 * Scrolls the chat message container to the bottom to show the latest messages.
	 * Uses a short timeout to ensure rendering is complete before scrolling.
	 */
	function scrollChatToBottom() {
		const container = document.getElementsByClassName('messages')[0];

		setTimeout(() => {
			container.scrollTo({
				top: container.scrollHeight,
			});
		}, 250);
	}

	/**
	 * Handles key press events for keyboard shortcuts.
	 * Space: Adds spaces to the input string for CSLR processing.
	 * Backspace: Removes the last recognized character group from the input string.
	 * Enter: Sends the current message.
	 * @param event - The keyboard event object.
	 */
	function handleKeyPress(event: KeyboardEvent) {
		if (event.code === "Space") {
			// Prevent default space scrolling behavior
			event.preventDefault();

			// Add multiple spaces to simulate holding a pause for CSLR
			str += " ".repeat(MIN_GROUP_LENGTH);
			parsed = convertToFrequencyFormat(str) // Update parsed view

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
			event.preventDefault(); // Prevent default form submission if applicable
			send() // Send the message
		}
	}

	/**
	 * Toggles the webcam stream on or off.
	 * Includes a short delay to prevent rapid toggling.
	 */
	function webcamToggle() {
		if (webcamOn) {
			landmarkDetection.disableCam();
		}

		webcamOn = !webcamOn;

		if (webcamOn) {
			// Briefly disable the toggle button to prevent immediate re-clicks
			// while the camera might be initializing.
			disabledToggle = true;
			setTimeout(() => {
				disabledToggle = false;
			}, 2000)
		}
	}

	/**
	 * Svelte lifecycle function called before navigating away from the page.
	 * Ensures the webcam is disabled to release the resource.
	 */
	beforeNavigate(() => {
		if(landmarkDetection){
			landmarkDetection.disableCam();
		}
	});
</script>

<!-- Attach the event listener to the window -->
<svelte:window on:keydown={handleKeyPress} />


<main class="max-w-7xl mx-auto px-4 pb-8 relative">
	<div class="grid grid-cols-1 md:gap-3 md:grid-cols-5">
		<!-- Left Column - Controls -->
		<div class="space-y-6 flex flex-col md:mt-12 mt-0">

			<div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm order-2 md:order-1">

				<div class="flex justify-center">
					<Toggle checked={webcamOn} on:change={webcamToggle} class="mb-2" color="red" disabled={disabledToggle}>
						<span class="text-sm text-gray-600 dark:text-gray-300">
							{webcamOn ? 'Kamera zapnuta' : 'Kamera vypnuta'}
						</span>
					</Toggle>
				</div>

				<div class="aspect-auto mb-4 border-2 border-gray-200 md:dark:border-gray-700 md:w-full rounded-lg overflow-hidden md:relative fixed md:top-0 md:left-0 top-2 left-2 w-1/4 z-40">
					{#if webcamOn}
						<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
					{/if}
				</div>

				<div class="space-y-3 flex flex-col-reverse md:flex-col">
					<div class="space-y-3">
						<Button class="md:w-full md:relative fixed md:bottom-0 bottom-2 md:right-0 right-2 w-1/4 z-40 h-16 md:h-auto" color="primary" on:click={send} disabled={!webcamOn}>Odeslat zprávu</Button>
						<Button class="w-full" color="blue" on:click={reset}>Odstranit aktuální zprávu</Button>
						<Button class="w-full" color="red" on:click={resetChat}>Restartovat historii</Button>
					</div>
					<div class="flex flex-col space-y-3">
						<Checkbox bind:checked={showLetter} class="text-gray-700 dark:text-gray-300 flex flex-row justify-end md:justify-start">Zobrazit přehrávaný znak</Checkbox>
						<Checkbox bind:checked={showChat} class="text-gray-700 dark:text-gray-300 flex-row justify-end md:justify-start">Zobrazit konverzaci</Checkbox>
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
		<div class="col-span-3 md:col-span-3 md:w-full w-11/12 mx-auto">
			<P class="text-center mb-3 mt-3 text-gray-600 dark:text-gray-400">Rozpoznaný vstup: <span class="font-bold">{parsed}</span></P>
			<div class="bg-gradient-to-b from-blue-400 to-yellow-600 md:h-[600px] h-[400px] rounded-xl border-2 border-gray-200 dark:border-gray-700 shadow-lg relative">
				<Scene bind:model bind:this={scene} bind:showLetter={showLetter} />
			</div>
			<ControlRow bind:this={controlRow} {model} />
		</div>

		<!-- Right Column - Chat -->
		<div class="md:mt-12 mt-2">
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
		<Heading tag="h3" class="mb-4">Obecné informace</Heading>
		<List class="space-y-3">
			<Li>Kvalita odpovědí velmi závisí na použitém modelu.</Li>
			<Li>
				V závislosti na zvoleném modelu, lze ignorovat chyby vzniklé nedokonalostí ropoznání textu, nebo chybně zobrazeným znakem v textu Vaší odpovědi a není potřeba takové chyby opravovat.
				Vaše odpověď bude nejspíše modelem pochopena správně. Obecně řečeno, čím kvalitnější/větší model a čím delší text odpovědi a historie chatu, tím méně záleží na bezchybnosti Vaší odpovědi.
			</Li>
			<Li>Pro vytvoření mezery zobrazuje poslední znak slova déle a poté pokračujte prvním znakem dalšího slova.</Li>
			<Li>Chcete-li znakovat stejný znak dvakrát za sebou, zobrazte znak, plynule ukažte jiné gesto a hned poté opět daný znak.</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">Klávesové zkratky</Heading>
		<List class="space-y-2">
			<Li><strong>Enter</strong> - odešle zprávu asistentovi</Li>
			<Li><strong>Space</strong> - vytvoří mezeru</Li>
			<Li><strong>Backspace</strong> - smaže poslední registrovaný znak</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">API</Heading>
		<P>Pro funkčnost režimu je nutné, aby aplikace byla propojena s nějaká LLM modelem. Aplikace nabízí dvě rozhraní:</P>
		<Heading tag="h4" class="mb-3">Ollama API</Heading>
		<List class="space-y-2">
			<Li>Nainstalujte program ollama z: <A href="https://ollama.com/" class="text-blue-600 dark:text-blue-400">https://ollama.com/</A>.</Li>
			<Li>CORS nastavení: SET OLLAMA_ORIGINS='adresa-webové-aplikace' a restartujte aplikaci ollama.</Li>
			<Li>Nainstalujte si libovolný model, seznam modelů lze nalézt na webové stránce programu ollama.</Li>
			<Li>Model spusťte a napište název modelu do pole pro název modelu.</Li>
		</List>

		<Heading tag="h4" class="mb-3">OpenAI API</Heading>
		<List class="space-y-2">
			<Li>Získejte klíč k platformě OpenAI a vložte do pole.</Li>
			<Li>Zadejte název Vámi zvoleného modelu.</Li>
		</List>
	</div>
</main>

<style>
  /* Custom animations */
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

</style>