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

	// Tensorflow imports
	import * as tf from '@tensorflow/tfjs';
	import type { LayersModel } from '@tensorflow/tfjs';

	// Local type imports
	import { Landmark2d, Landmark3d } from '$lib/models/Landmark';
	import type { GestureProbability } from '$lib/models/GestureProbability';

	/** Supported letters for gesture recognition */
	const letters = [
		'A',
		'B',
		'C',
		'D',
		'E',
		'F',
		'G',
		'H',
		'Ch',
		'I',
		'J',
		'K',
		'L',
		'M',
		'N',
		'O',
		'P',
		'Q',
		'R',
		'S',
		'T',
		'U',
		'V',
		'W',
		'X',
		'Y',
		'Z',
		'None'
	];
	/** Minimum time between predictions in milliseconds for performance optimization */
	export const msToNextPredict = 80;

	// Component state variables
	/** MediaPipe hand landmark detection model */
	let handLandmarker: HandLandmarker | undefined;
	/** TensorFlow.js gesture classification model */
	let tfModel: LayersModel | undefined;

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
	export let gestureConfidenceThreshold: number = 0.2;

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
	function gestureRecognized(event: GestureProbability) {
		dispatch('gestureRecognized', event);
	}

	/**
	 * Initializes MediaPipe HandLandmarker with GPU acceleration
	 * Must be called before any hand detection can occur
	 */
	async function createHandLandmarker() {
		const vision = await FilesetResolver.forVisionTasks(
			'./node_modules/@mediapipe/tasks-vision/wasm'
		);
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
			if (video.srcObject instanceof MediaStream) {
				let tracks = video.srcObject.getTracks();
				tracks[0].stop();
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
		if (!handLandmarker || !tfModel)
			return setTimeout(() => {
				predictWebcam();
			}, 100);

		let startTimeMs = performance.now();
		// Performance monitoring
		console.log(startTimeMs - lastTimeMs + ' ms'); // time to render one frame
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
			const probabilities = await handGestureClassifier(
				calcRelativeLandmarks(
					calcAbsolutePositions(results.landmarks[0], video.videoWidth, video.videoHeight)
				)
			);

			// Filter and report high-confidence predictions
			let result: GestureProbability = {};
			for (let i = 0; i < probabilities.length; i++) {
				if (probabilities[i] > gestureConfidenceThreshold) {
					result[letters[i]] = probabilities[i];
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

	// https://github.com/kinivi/hand-gesture-recognition-mediapipe
	/**
	 * Converts landmark coordinates to absolute pixel positions
	 * @param landmarks Array of 3D landmarks
	 * @param imageWidth Video frame width
	 * @param imageHeight Video frame height
	 * @returns Array of 2D landmarks - pixel coordinates
	 */
	function calcAbsolutePositions(
		landmarks: Landmark3d[],
		imageWidth: number,
		imageHeight: number
	): Landmark2d[] {
		let newLandmarks = [];

		for (const landmark of landmarks) {
			let x = Math.min(Math.floor(landmark.x * imageWidth), imageWidth - 1);
			let y = Math.min(Math.floor(landmark.y * imageHeight), imageHeight - 1);
			//let z = landmark.z;
			newLandmarks.push(new Landmark2d(x, y));
		}

		return newLandmarks;
	}

	/**
	 * Normalizes landmarks relative to the base (wrist) position
	 * Makes the model translation-invariant
	 * @param landmarks Array of absolute position landmarks
	 * @returns Flattened array of normalized coordinates
	 */
	function calcRelativeLandmarks(landmarks: Landmark2d[]): number[] {
		const tempLandmarkList = structuredClone(landmarks);

		let baseX: number = 0;
		let baseY: number = 0;

		// Normalize positions relative to wrist
		for (let index = 0; index < tempLandmarkList.length; index++) {
			const landmarkPoint = tempLandmarkList[index];

			if (index === 0) {
				baseX = landmarkPoint.x;
				baseY = landmarkPoint.y;
			}

			tempLandmarkList[index].x = tempLandmarkList[index].x - baseX;
			tempLandmarkList[index].y = tempLandmarkList[index].y - baseY;
		}

		// Flatten to 1D array for model input
		let flattenedLandmarkList = [];
		for (let index = 0; index < tempLandmarkList.length; index++) {
			flattenedLandmarkList.push(tempLandmarkList[index].x);
			flattenedLandmarkList.push(tempLandmarkList[index].y);
		}

		// Normalize
		const absValues = flattenedLandmarkList.map(Math.abs);
		const maxValue: number = Math.max(...absValues);

		return flattenedLandmarkList.map((val) => val / maxValue);
	}

	/**
	 * Loads the TensorFlow.js model for gesture classification
	 */
	async function loadTF() {
		if (tfModel === undefined) {
			tfModel = await tf.loadLayersModel('models/tfjsmodel/model.json');
			// https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-webgpu
		}
	}

	/**
	 * Classifies hand gestures using TensorFlow model
	 * @param landmarks Flattened, normalized landmark coordinates
	 * @returns Array of probabilities for each supported gesture
	 */
	async function handGestureClassifier(landmarks: number[]): Promise<Float32Array> {
		if (tfModel === undefined) {
			await loadTF();
			if (tfModel === undefined) {
				throw new Error('Model not loaded');
			}
		}

		const input = tf.tensor(landmarks, [1, 42]);
		const output = tfModel.predict(input) as tf.Tensor;

		return output.dataSync() as Float32Array;
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
<div class="webcam_container">
	<div id="webcam_mirror">
		<!-- Video feed with mirroring -->
		<video id="webcam" autoplay playsinline><track kind="captions" src="" /></video>
		{#if !showVideo}
			<div class="video_block"></div>
		{/if}
		<!-- Overlay canvas for landmark visualization -->
		<canvas class="output_canvas" id="output_canvas" width="2000" height="1500"></canvas>
	</div>
</div>

<style>
	.webcam_container {
		display: flex;
		justify-content: left;
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
</style>
