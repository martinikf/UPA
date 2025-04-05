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

	import GestureRecognition from '$lib/components/Recognition/GestureRecognition.svelte';

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
	let gestureRecognition: GestureRecognition;

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
			gestureRecognition.disableCam();
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
		if(gestureRecognition){
			gestureRecognition.disableCam();
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
						<GestureRecognition bind:this={gestureRecognition} on:gestureRecognized={handleMessage} />
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
		<Heading tag="h3" class="mt-6 mb-4">Tipy pro režim Konverzace</Heading>
		<List class="space-y-3">
			<Li>
				<strong>Kvalita modelu ovlivňuje odpovědi:</strong> Pamatujte, že srozumitelnost, relevance a celková kvalita odpovědí virtuálního asistenta přímo závisí na tom, jaký jazykový model (LLM) máte v nastavení zvolený. Větší modely (např. od OpenAI) mohou poskytovat zajímavější a přesnější odpovědi.
			</Li>
			<Li>
				<strong>Nebojte se chyb v přepisu:</strong> Velkou výhodou LLM je, že si často poradí i s textem, který obsahuje drobné chyby nebo překlepy vzniklé při automatickém rozpoznávání vašeho znakování. Nemusíte se tedy stresovat tím, že přepis není dokonalý. Zaměřte se na plynulé znakování a LLM pravděpodobně pochopí, co máte na mysli.
			</Li>
			<Li>
				<strong>Technika znakování pro přepis:</strong> Pro správné vkládání mezer mezi slovy – podržte znak spoledního písmena slova déle a pro zadávání stejných písmen za sebou - krátce změňte gesto mezi znaky.
			</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">Klávesové zkratky v režimu Konverzace</Heading>
		<List class="space-y-2">
			<Li><strong>Enter:</strong> Odešle aktuálně rozpoznaný text (zobrazený nad 3D modelem) jako vaši zprávu jazykovému modelu.</Li>
			<Li><strong>Mezerník:</strong> Manuálně vloží mezeru do rozpoznávaného textu.</Li>
			<Li><strong>Backspace:</strong> Smaže poslední rozpoznaný znak z aktuálně sestavované zprávy.</Li>
		</List>

		<Heading tag="h3" class="mt-6 mb-4">Propojení s jazykovým modelem (API)</Heading>
		<P>Aby režim "Konverzace" fungoval, potřebuje aplikace komunikovat s nějakým velkým jazykovým modelem (LLM), který bude generovat odpovědi. Můžete si vybrat jednu ze dvou možností:</P>

		<Heading tag="h4" class="mb-3">Možnost 1: Ollama (Spouštění modelů na vašem počítači)</Heading>
		<P class="mb-3">Ollama je bezplatný nástroj, který vám umožní stahovat a spouštět různé open-source jazykové modely přímo na vašem vlastním počítači. Výhodou je soukromí (data neopouštějí váš PC) a nulové náklady na použití modelů. Nevýhodou může být náročnost na výkon počítače a nutnost technického nastavení.</P>
		<List tag="ol" class="space-y-3">
			<Li>
				<strong>Instalace Ollama:</strong> Stáhněte a nainstalujte Ollama pro váš operační systém z oficiální stránky: <A href="https://ollama.com/download" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:underline">https://ollama.com/download</A>.
			</Li>
			<Li>
				<strong>Nastavení CORS (Povolení komunikace pro prohlížeč):</strong>
				<ul class="list-disc list-inside pl-5 space-y-1 mt-1">
					<li>Prohlížeč z bezpečnostních důvodů potřebuje explicitní povolení, aby mohl komunikovat s programem Ollama běžící na vašem počítači. To se nastavuje pomocí systémové proměnné OLLAMA_ORIGINS.</li>
					<li>Hodnota této proměnné musí být adresa, na které běží tato webová aplikace.
					</li>
					<li>Jak nastavit proměnnou (PŘED spuštěním programu Ollama):
						<ul class="list-circle list-inside pl-5 space-y-1 mt-1">
							<li>Windows – v příkazové řádce: Zadejte set OLLAMA_ORIGINS=adresa_webové_aplikace (např. set "OLLAMA_ORIGINS=https://158.194.92.104").</li>
						</ul>
					</li>
					<li>Po nastavení proměnné (a restartu služby Ollama, pokud běžela) spusťte model.</li>
				</ul>
			</Li>
			<Li>
				<strong>Stažení a spuštění modelu:</strong>
				<ul class="list-disc list-inside pl-5 space-y-1 mt-1">
					<li>Otevřete si příkazovou řádku vašeho systému.</li>
					<li>Vyberte si model, který chcete použít (seznam najdete na <A href="https://ollama.com/library" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:underline">ollama.com/library</A>).</li>
					<li>Stáhněte a spusťte model zadáním příkazu: <code class="text-sm bg-gray-100 dark:bg-gray-700 p-1 rounded">ollama run název_modelu</code> (např. <code class="text-sm bg-gray-100 dark:bg-gray-700 p-1 rounded">ollama run llama3.1</code>). Při prvním spuštění se model stáhne, což může chvíli trvat.</li>
				</ul>
			</Li>

			<Li>
				<strong>Nastavení v Aplikaci:</strong>
				<ul class="list-disc list-inside pl-5 space-y-1 mt-1">
					<li>V nastavení režimu Konverzace se ujistěte, že nemáte přepínač v poloze "OpenAI API".</li>
					<li>Do pole "Model name" zadejte přesně ten název modelu, který jste spustili příkazem ollama run (např. llama3.1).</li>
					<li>Pole "Request URL" by mělo být nastaveno na výchozí http://localhost:11434/api/chat, což je standardní adresa pro lokálně běžící program Ollama.</li>
				</ul>
			</Li>
			<Li>
				<strong>Ukončení modelu:</strong> Až skončíte s používáním konverzace, můžete model zastavit napsáním příkazu /bye do příkazové řádky. Tím se uvolní systémové prostředky.
			</Li>
		</List>

		<Heading tag="h4" class="mt-4 mb-3">Možnost 2: OpenAI API</Heading>
		<P class="mb-3">Tato možnost využívá modely provozované společností OpenAI (např. GPT-4o). Výhodou je přístup k velmi výkonným modelům bez nároků na váš počítač a jednodušší nastavení. Nevýhodou je nutnost mít účet u OpenAI a fakt, že používání API je placené.</P>
		<List tag="ol" class="space-y-3">
			<Li>
				<strong>Získání API klíče:</strong>
				<ul class="list-disc list-inside pl-5 space-y-1 mt-1">
					<li>Vytvořte si účet (nebo se přihlaste) na <A href="https://platform.openai.com/" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:underline">platform.openai.com</A>.</li>
					<li>V nastavení účtu najděte sekci "API keys".</li>
					<li>Vygenerujte si nový tajný klíč ("secret key"). Tento klíč si ihned bezpečně zkopírujte a uložte, protože ho nelze zobrazit znovu. Nikdy ho nesdílejte veřejně.</li>
				</ul>
			</Li>
			<Li>
				<strong>Výběr modelu:</strong> Zjistěte si názvy dostupných modelů ve vašem účtu (např. gpt-4o-mini, gpt-4o, gpt-3.5-turbo). Informace najdete v dokumentaci OpenAI.
			</Li>
			<Li>
				<strong>Nastavení v Aplikaci:</strong>
				<ul class="list-disc list-inside pl-5 space-y-1 mt-1">
					<li>V nastavení režimu Konverzace zaškrtněte volbu "OpenAI API".</li>
					<li>Do pole "API Key" vložte váš zkopírovaný tajný klíč.</li>
					<li>Do pole "Model name" napište přesný název modelu, který chcete používat.</li>
					<li>Pole "Request URL" by mělo být nastaveno na výchozí https://api.openai.com/v1/chat/completions.</li>
				</ul>
			</Li>
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