<script lang="ts">

	/**
	 * Hand Gesture Recognition Component
	 *
	 * Svelte component that implements real-time hand gesture recognition using
	 * MediaPipe for landmark detection and TensorFlow.js for gesture classification.
	 * Supports recognition of Czech finger alphabet letters A-Z
	 *
	 * API:
	 * - dispatches 'gestureRecognized' event with GestureProbability containing gesture probabilities
	 * 							this event is dispatched on every gesture recognition
	 * - provides 'toggleShowVideo()' function to toggle video feed visibility
	 * - provides 'disableCam()' function to stop webcam stream
	 * - provides 'gestureConfidenceThreshold' prop to set gesture recognition threshold
	 * - provides 'msToNextPredict' prop to set minimum time between predictions
	 */
	// based on: https://codepen.io/mediapipe-preview/pen/gOKBGPN
	import {
		HandLandmarker,
		FilesetResolver,
		GestureRecognizer,
		DrawingUtils,
		type HandLandmarkerResult
	} from '@mediapipe/tasks-vision';
	import { createEventDispatcher, onMount } from 'svelte';
	import '$lib/handlers/ImageProcessor'

	// Local type imports
	import type { GestureProbability } from '$lib/models/GestureProbability';
	import type {Classificator} from '$lib/handlers/Classificator'
	import { processLandmarks } from '$lib/handlers/ImageProcessor';
	import { ClassificatorNN } from '$lib/handlers/ClassificatorNN';
	import { ClassificatorDF } from '$lib/handlers/ClassificatorDF';
	import AbsoluteCenteredLoadingCircle from '$lib/components/shared/AbsoluteCenteredLoadingCircle.svelte';

	// Component state variables
	/** MediaPipe hand landmark detection model */
	let handLandmarker: HandLandmarker | undefined;
	/** Classificator */
	// const classificator : Classificator = new ClassificatorNN();
	let classificator : Classificator;

	/** Minimum time between predictions in milliseconds for performance optimization */
	export const msToNextPredict = 80;

	// DOM elements
	let canvasElement: HTMLCanvasElement;
	let canvasCtx: CanvasRenderingContext2D;
	let video: HTMLVideoElement;

	/** Flag indicating if webcam is currently active */
	let webcamRunning: boolean = false;
	/** Flag controlling video feed visibility */
	let showVideo: boolean = true;
	/** Timestamp of last prediction for frame rate control */
	let lastTimeMs: number = 0; // used for measuring time between frames
	/** Threshold for gesture recognition [0, 1]*/
	export let gestureConfidenceThreshold: number = 0.8;

	let loaded : boolean = false;

	/**
	 * Component initialization logic.
	 * Sets up DOM elements, checks browser compatibility,
	 * and initializes video stream and models.
	 */
	onMount(() => {
		// Initialize DOM elements
		let _video = document.getElementById('webcam') as HTMLVideoElement | null;
		let _canvasElement = document.getElementById('output_canvas') as HTMLCanvasElement | null;
		let _canvasCtx = _canvasElement?.getContext('2d') as CanvasRenderingContext2D | null;

		if (_video == null || _canvasElement == null || _canvasCtx == null) {
			return;
		}

		video = _video;
		canvasElement = _canvasElement;
		canvasCtx = _canvasCtx;

		classificator = new ClassificatorDF();

		// Check if browser supports getUserMedia <=> is compatible
		if (!navigator.mediaDevices?.getUserMedia) {
			console.error('getUserMedia() is not supported by your browser');
			return;
		}

		enableCamAndStartPredict();
		createHandLandmarker();
		loadTF();
	});

	// Event handling setup
	// https://stackoverflow.com/questions/50702662/passing-parent-method-to-child-in-svelte
	const dispatch = createEventDispatcher();

	/**
	 * Dispatches recognized gesture events to parent component
	 * @param event Object containing probabilities for each recognized gesture
	 */
	function gestureRecognized(event: GestureProbability[]) {
		dispatch('gestureRecognized', event);
	}

	/**
	 * Initializes MediaPipe HandLandmarker with GPU acceleration
	 * Must be called before any hand detection can occur
	 */
	async function createHandLandmarker() {
		const vision = await FilesetResolver.forVisionTasks('wasm-taskvision');
		handLandmarker = await HandLandmarker.createFromOptions(vision, {
			baseOptions: {
				modelAssetPath: `models/hand_landmarker.task`,
				delegate: 'GPU'
			},
			runningMode: 'VIDEO',
			numHands: 1
		});
	}

	/**
	 * Initializes webcam stream and starts prediction pipeline
	 * Requests user permission for camera access
	 */
	function enableCamAndStartPredict() {
		webcamRunning = true;

		// Activate the webcam stream, ask for permission
		navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
			video.srcObject = stream;
			video.addEventListener('loadeddata', () => {
				loaded = true;
				predictWebcam();
			});
		});
	}

	/**
	 * Stops webcam stream
	 */
	export function disableCam() {
		if (video && video.srcObject) {
			webcamRunning = false;
			loaded = false;
			if (video.srcObject instanceof MediaStream) {
				let tracks = video.srcObject.getTracks();
				tracks.forEach(track => track.stop());
			}
		}
	}

	/**
	 * Main prediction loop for hand gesture recognition
	 * Runs continuously while webcam is active
	 * Controls frame rate and coordinates model inference
	 */
	async function predictWebcam() {
		// Delay prediction if models aren't ready
		if (!handLandmarker || !classificator.ready())
			return setTimeout(() => {
				predictWebcam();
			}, 100);

		let startTimeMs = performance.now();
		// Performance monitoring
		// console.log(startTimeMs - lastTimeMs + ' ms'); // time to render one frame
		lastTimeMs = startTimeMs;

		// Run hand detection
		let results: HandLandmarkerResult = handLandmarker.detectForVideo(video, startTimeMs);

		// Clear previous frame (drawing)
		canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

		const drawingUtils = new DrawingUtils(canvasCtx);

		if (results && results.landmarks && results.landmarks.length > 0) {
			// Visualize landmarks
			drawLandmarks(drawingUtils, results);


			// Process landmark data through classification pipeline
			const processedLandmarks = processLandmarks(results.landmarks[0], video.videoWidth, video.videoHeight);
			const gestureProbabilities = await handGestureClassifier(processedLandmarks);

			// Filter and report high-confidence predictions
			let result: GestureProbability[] = [];
			for (let i = 0; i < gestureProbabilities.length; i++) {
				if (gestureProbabilities[i].probability > gestureConfidenceThreshold)
				{
					result.push(gestureProbabilities[i])
				}
			}

			gestureRecognized(result);
		}

		// Schedule next frame (prediction) with time limiting
		if (webcamRunning) {
			let delay = msToNextPredict - (performance.now() - startTimeMs);
			if (delay < 0) delay = 0;
			return setTimeout(() => {
				predictWebcam();
			}, delay);
		}
	}

	/**
	 * Renders hand landmarks and connections on canvas
	 * @param drawingUtils MediaPipe drawing utilities
	 * @param results  HandLandmarkerResult object containing landmark data
	 */
	function drawLandmarks(drawingUtils: DrawingUtils, results: HandLandmarkerResult) {
		for (const landmark of results.landmarks) {
			// Draw connections between landmarks
			drawingUtils.drawConnectors(landmark, GestureRecognizer.HAND_CONNECTIONS, {
				color: '#00FF00',
				lineWidth: 5
			});
			// Draw landmark points
			drawingUtils.drawLandmarks(landmark, {
				color: '#0000FF',
				lineWidth: 2
			});
		}
	}

	/**
	 * Loads the classification method
	 */
	async function loadTF() {
		await classificator.load();
	}

	/**
	 * Classifies hand gestures using classification method
	 * @param landmarks Flattened, normalized landmark coordinates
	 * @returns Array of probabilities for each supported gesture
	 */
	async function handGestureClassifier(landmarks: number[]): Promise<GestureProbability[]> {
		return await classificator.predict(landmarks);
	}

	/**
	 * Toggles visibility of video feed
	 * Note: Recognition continues even when video is hidden
	 */
	export function toggleShowVideo() {
		showVideo = !showVideo;
	}
</script>


<!-- Component Template -->
<div class="webcam_container relative">
	<div id="webcam_mirror">
		<!-- Video feed with mirroring -->
		<video id="webcam" autoplay playsinline><track kind="captions" src="" /></video>
		{#if !showVideo}
			<div class="video_block"></div>
		{/if}
		<!-- Overlay canvas for landmark visualization -->
		<canvas class="output_canvas" id="output_canvas" width="2000" height="1500"></canvas>
	</div>
	<button
		id="toggle_show_video"
		on:click={() => {
						toggleShowVideo();
					}}
	></button>

	<!-- Loading circle -->
	{#if !loaded}
		<AbsoluteCenteredLoadingCircle />
	{/if}
</div>

<style>
	.webcam_container {
		display: flex;
		justify-content: left;
    position: relative;
	}

	.video_block {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: #444444;
	}

	#webcam_mirror {
		transform: scaleX(-1);
		position: relative;
	}

	#webcam {
		width: 100%;
		height: 100%;
	}

	#output_canvas {
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
	}

  #toggle_show_video {
    background-color: transparent;
    border: none;
    padding: 0;
    margin: 0;
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
  }
</style>
