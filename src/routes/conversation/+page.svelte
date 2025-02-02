<script lang="ts">

	import LandmarkDetection from '$lib/components/LandmarkDetection.svelte';

	import Scene from '$lib/components/Scene.svelte';
	import Model from '$lib/components/AnimatedModel.svelte';
	import ControlRow from '$lib/components/ControlRow.svelte';

	// Import types
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import { Language } from '$lib/models/Word';
	import { fade } from 'svelte/transition';
	let scene: Scene;
	let model: Model;
	let controlRow: ControlRow;

	// References
	let landmarkDetection: LandmarkDetection;

	let systemPrompt = `You are a conversation assistant. Follow these rules:
	1. Answer in a language based on language in which was the previous message written.
	2. Your responses must be of maximum length of one sentence (around 10 words).
	3. Focus on clear, simple communication, go straight to the point.
	4. Keep the user engaged, continue in the conversation, bring new ideas, ask questions.`


	let letterFrequency : {[letter: string] : number} = createDict();

	let str: string = "";
	let parsed : string = "";

	let showChat = false;
	let showLetter = false;

	let modelName : string = "llama3.1";
	let requestUrl : string = "http://localhost:11434/api/chat";
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
	}


	async function sendPrompt(txt : string) {
		chatHistory = [
			...chatHistory,
			{
				role: 'user',
				content: txt
			}
		];

		const data = {
			model: modelName,
			stream: false,
			messages: chatHistory
		};

		try {
			const res = await fetch(requestUrl, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data)
			});

			const resp = await res.json();
			const assistantReply = resp.message?.content || "No response";
			console.log(assistantReply)
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

		scrollChatToBottom();
	}

	function scrollChatToBottom() {
		const container = document.getElementsByClassName('messages')[0];

		setTimeout(() => {
			container.scrollTo({
				top: container.scrollHeight,
			});
		}, 250);
	}

	function convertToFrequencyFormat(input: string): string {
		// Configuration constants
		const MIN_GROUP_LENGTH = 6;
		const SPACE_INSERT_THRESHOLD = 20;
		const MULTI_CHAR_TOKENS = ['Ch'];
		const ERROR_CONTEXT_SIZE = 1; // Characters to check around mismatches

		// Tokenize input with multi-character support
		const tokens: string[] = [];
		let i = 0;
		while (i < input.length) {
			let matched = false;
			for (const token of MULTI_CHAR_TOKENS) {
				if (input.substring(i, token.length) === token) {
					tokens.push(token);
					i += token.length;
					matched = true;
					break;
				}
			}
			if (!matched) {
				tokens.push(input[i]);
				i++;
			}
		}

		let result = '';
		let currentToken = tokens[0];
		let count = 1;

		for (let i = 1; i <= tokens.length; i++) {
			const isValidExtension = i < tokens.length && (
				tokens[i] === currentToken ||
				(i > ERROR_CONTEXT_SIZE &&
					i < tokens.length - ERROR_CONTEXT_SIZE &&
					tokens[i - ERROR_CONTEXT_SIZE] === currentToken &&
					tokens[i + ERROR_CONTEXT_SIZE] === currentToken)
			);

			if (isValidExtension) {
				count++;
			} else {
				if (count >= MIN_GROUP_LENGTH) {
					result += currentToken;
					if (count >= SPACE_INSERT_THRESHOLD) {
						result += ' ';
					}
				}

				if (i < tokens.length) {
					currentToken = tokens[i];
					count = 1;
				}
			}
		}

		return result;
	}
</script>

<p class="text_input_display">
	Rozpoznaný vstup: {parsed}
</p>

<!-- Layout -->
<div class="layout">

	<!-- Controls -->
	<div class="left_column">
		<div class="webcam_container">
			<div class="webcam">
				<LandmarkDetection bind:this={landmarkDetection} on:gestureRecognized={handleMessage} />
			</div>
		</div>

		<div class="controls__flow column">
			<button on:click={send}>Odeslat zprávu</button>
			<button on:click={reset}>Odstranit aktuální zprávu</button>
			<button on:click={resetChat}>Restartovat histori konverzace.</button>
			<div>
				<label for="show_chat">Zobrazit přehrávaný znak: </label>
				<input type="checkbox" id="show_chat" bind:checked={showLetter} />
			</div>
			<div>
				<label for="show_chat">Zobrazit konverzaci: </label>
				<input type="checkbox" id="show_chat" bind:checked={showChat} />
			</div>
		</div>

		<hr/>

		<!-- AI API settings -->
		<div class="controls__api column">
			<label for="model_name">Model name</label>
			<input id="model_name" type="text" bind:value={modelName} />
			<label for="request_url">Request url</label>
			<input id="request_url" type="text" bind:value={requestUrl} />
		</div>
	</div>

	<!-- Animation -->
	<div class="animation">
		<div class="animation_canvas">
			<Scene bind:model bind:this={scene} bind:showLetter={showLetter}/>
		</div>
		<ControlRow bind:this={controlRow} {model} />
	</div>

	<!-- WEBCAM with chat log -->
	<div class="column__left">


		<div class="chat_log">
			<div class="messages">
				{#each chatHistory.slice(1) as message}
					<div
						transition:fade
						class="message {message.role}">
						<div class="header">
							<span class="role">{message.role === 'user' ? 'Vy' : 'Asistent'}</span>
						</div>
						<div class="content">
							{#if showChat}
								{message.content}
							{:else}
								{message.content.replace(/\S/g, '*')}
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>

	</div>

</div>

<hr>
<h3>Jak používat tento režim</h3>
<ul>
	<li>Kvalita odpovědí velmi závisí na použitém LLM. Menší/nenáročné modely nemusí rozumět českému jazyku, obzvlášt při nedokonalém vstupu dat.</li>
	<li>Pro vytvoření mezery zobrazuje poslední znak slova po doby jedné sekundy. (Podobně jako 3D animace)</li>
	<li>Chcete-li znakovat stejný znak dvakrát zasebou, ukažte znak, uvolněte ruku do neurčitého stavu a zobrazte znak znovu.</li>
</ul>

<h3>Jak zprovoznit ollama API k funkčnosti tohoto režimu:</h3>


<h3>Jak použít nekompatibilní API:</h3>
<p>
Pro programátory, ve zdrojovém kodu naleznete podobu API dotazů. Poté stačí naprogramovat Adaptér - překládající dotazy pro Vaši API.
<a href="https://github.com/martinikf/UPA/blob/main/src/routes/conversation/%2Bpage.svelte">Zdrojový kod</a>
</p>
<style>
	.text_input_display{
		text-align: center;
	}

	.layout{
		display: grid;
		grid-template-columns: 1fr 3fr 1fr;
	}

	.left_column{
		margin: auto;
		width: 80%;
	}

	.column{
		display: flex;
		flex-direction: column;
	}

	.column *{
    margin: 0.25rem;
	}

	.controls__flow button{
		padding: 10px;
	}

  .animation {
    width: 100%;
    max-width: 80%;
		margin: auto;
  }

  .animation_canvas {
    border: solid 2px black;
    position: relative;
    background: linear-gradient(
        0deg,
        rgb(255, 115, 0) 0%,
        rgb(255, 216, 0) 35%,
        rgb(0, 86, 184) 100%
    );
		height: 63vh;
  }

  .chat_log {
    display: flex;
    flex-direction: column-reverse;

		max-height: 63vh;
  }

  .messages {
    overflow-y: scroll;
    flex-grow: 1;
    padding-right: 5px;
  }

  .message {
    margin-bottom: 1rem;
    padding: 0.8rem;
    border-radius: 6px;
    animation: slideIn 0.2s ease-out;
  }

  .message.user {
    background: #2e2e2e;
    margin-left: 20%;
    border: 1px solid #bbdefb;
  }

  .message.assistant {
    background: #2e2e2e;
    margin-right: 20%;
    border: 1px solid #eee;
  }

  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.8em;
  }

  .role {
    font-weight: 800;
  }

  .content {
    white-space: pre-wrap;
    word-break: break-word;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>