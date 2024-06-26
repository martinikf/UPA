<script lang="ts">
    // based on: https://codepen.io/mediapipe-preview/pen/gOKBGPN
    import { HandLandmarker, FilesetResolver, GestureRecognizer,  DrawingUtils, type HandLandmarkerResult} from "@mediapipe/tasks-vision";
    import { createEventDispatcher } from 'svelte';
    import { browser } from '$app/environment';
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';
    import type { LayersModel } from '@tensorflow/tfjs';

    const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ch']
    const msToNextPredict = 80;
    let lastVideoTime = -1;
    let results : HandLandmarkerResult | undefined;

    let handLandmarker : HandLandmarker | undefined;
    let webcamRunning: boolean = false;
    let tfModel : LayersModel | undefined;

    let showVideo : boolean = true;

    let loading_text_html : HTMLElement | null;

    let video : HTMLVideoElement | null = null;

    if(browser){
        onMount(() => {
            video = document.getElementById("webcam") as HTMLVideoElement;
            const canvasElement = document.getElementById("output_canvas") as HTMLCanvasElement;
            const canvasCtx = canvasElement.getContext("2d");

            loading_text_html = document.getElementById("loading_text");

            // Check if webcam access is supported.
            const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

            if (!hasGetUserMedia()) {
                console.warn("getUserMedia() is not supported by your browser");
            }

            if(video && canvasElement && canvasCtx){
                createHandLandmarker(canvasElement, canvasCtx, video);
                loadTF();
                predictWebcam(canvasElement, canvasCtx, video);
            }
        });
    }

    // https://stackoverflow.com/questions/50702662/passing-parent-method-to-child-in-svelte
    const dispatch = createEventDispatcher();

    function gestureRecognized(event : {[key: string]: number}){
        dispatch('gestureRecognized', event);
    }

    async function createHandLandmarker(canvasElement : HTMLCanvasElement, canvasCtx : CanvasRenderingContext2D, video : HTMLVideoElement){
        const vision = await FilesetResolver.forVisionTasks(
          "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
        );
        handLandmarker = await HandLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: `models/hand_landmarker.task`,
                delegate: "GPU"
            },
            runningMode: "VIDEO",
            numHands: 1
        });

        enableCam(canvasElement, canvasCtx, video);
    }

    // Enable the live webcam view and start detection.
    function enableCam(canvasElement : HTMLCanvasElement, canvasCtx : CanvasRenderingContext2D, video : HTMLVideoElement){
        webcamRunning = true;
        if (!handLandmarker) {
            console.log("Wait! objectDetector not loaded yet.");
            return;
        }

        // Activate the webcam stream.
        navigator.mediaDevices.getUserMedia({video: true }).then((stream) => {
            video.srcObject = stream;
            video.addEventListener("loadeddata", () => {predictWebcam(canvasElement, canvasCtx, video)});
        });
    }

    export function disableCam() {
        if (video && video.srcObject) {
            webcamRunning = false;
            let tracks = video.srcObject.getTracks();
            tracks[0].stop();
        }
    }

    function loadingDone(){
        if(loading_text_html)
            loading_text_html.style.display = "none";
    }


    let lastTimeMs : number = 0;
    async function predictWebcam(canvasElement : HTMLCanvasElement, canvasCtx : CanvasRenderingContext2D, video : HTMLVideoElement) {
        const webcamElement = document.getElementById("webcam");

        if(loading_text_html?.style.display !== "none")
            loadingDone();

        if(canvasCtx === null || handLandmarker === undefined || video === null || webcamElement === null){
            return;
        }

        let startTimeMs = performance.now();
        if(startTimeMs - msToNextPredict < lastTimeMs){
            return setTimeout(() => {predictWebcam(canvasElement, canvasCtx, video)}, msToNextPredict - (startTimeMs - lastTimeMs));
        }

        if (lastVideoTime !== video.currentTime) {
            //console.log(startTimeMs - lastTimeMs + " ms"); // time to render one frame
            lastTimeMs = startTimeMs;
            lastVideoTime = video.currentTime;
            results = handLandmarker.detectForVideo(video, startTimeMs);
        }

        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

        const drawingUtils = new DrawingUtils(canvasCtx);

        if (results && results.landmarks && results.landmarks.length > 0) {

            // draw landmarks and connections
            for (const landmark of results.landmarks) {
                drawLandmarks(drawingUtils, landmark);
            }

            const absoluteLandmarks = calcAbsolutePositions(results.landmarks[0], video.videoWidth, video.videoHeight);

            //Convert landmarks to relative normalized coordtinates
            const relativeLandmarks = calcRelativeLandmarks(absoluteLandmarks);

            //Run ML model, get for each gesture its probability
            const probabilities = await handGestureClassifier(relativeLandmarks);

            let result : {[key: string]: number} = {}
            for(let i = 0; i < probabilities.length; i++){
                if(probabilities[i] > 0.2){
                    //console.log("Gesture " + letters[i] + " has probability " + probabilities[i]);
                    result[letters[i]] = probabilities[i];
                }
            }

            gestureRecognized(result);
        }
        canvasCtx.restore();

        // Call this function again to keep predicting when the browser is ready.
        if (webcamRunning === true) {
            window.requestAnimationFrame(() => {predictWebcam(canvasElement, canvasCtx, video)});
        }
    }

    function drawLandmarks(drawingUtils : DrawingUtils, landmarks : { x: number, y:number, z:number }[]){
        drawingUtils.drawConnectors(landmarks, GestureRecognizer.HAND_CONNECTIONS, {
            color: "#00FF00",
            lineWidth: 5
        });
        drawingUtils.drawLandmarks(landmarks, {
            color: "#0000FF",
            lineWidth: 2
        });
    }

    // https://github.com/kinivi/hand-gesture-recognition-mediapipe
    function calcAbsolutePositions(landmarks : { x: number, y:number, z:number }[], imageWidth : number, imageHeight : number) : { x: number; y: number }[] {
        let newLandmarks = [];

        for (const landmark of landmarks){
            let x = Math.min( Math.floor(landmark.x * imageWidth), imageWidth - 1);
            let y = Math.min( Math.floor(landmark.y * imageHeight), imageHeight - 1);
            //let z = landmark.z;
            newLandmarks.push({x: x, y: y});
        }

        return newLandmarks;
    }

    function calcRelativeLandmarks(landmarks : { x: number; y: number }[]) : number[]{
        const tempLandmarkList = structuredClone(landmarks);

        let baseX: number = 0;
        let baseY: number = 0;

        for (let index = 0; index < tempLandmarkList.length; index++) {
            const landmarkPoint = tempLandmarkList[index];

            if (index === 0) {
                baseX = landmarkPoint.x;
                baseY = landmarkPoint.y;
            }

            tempLandmarkList[index].x = tempLandmarkList[index].x - baseX;
            tempLandmarkList[index].y = tempLandmarkList[index].y - baseY;
        }


        // Convert to a one-dimensional list
        let flattenedLandmarkList = [];
        for (let index = 0; index < tempLandmarkList.length; index++) {
            flattenedLandmarkList.push(tempLandmarkList[index].x);
            flattenedLandmarkList.push(tempLandmarkList[index].y);
        }

        // Normalization
        const absValues = flattenedLandmarkList.map(Math.abs);
        const maxValue: number = Math.max(...absValues);

        return flattenedLandmarkList.map((val) => val / maxValue);
    }

    async function loadTF(){
        if(tfModel === undefined) {
            tfModel = await tf.loadLayersModel('models/tfjsmodel/model.json');
            // https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-webgpu
        }
    }

    async function handGestureClassifier(landmarks : number[]) : Promise<number[]>{
        if(tfModel === undefined){
           await loadTF();
            if (tfModel === undefined){
                throw new Error("Model not loaded");
            }
        }

        const input = tf.tensor(landmarks, [1, 42]);
        const output = tfModel.predict(input);

        return await output.dataSync();
    }

    export function toggleShowVideo(){
        showVideo = !showVideo;
    }

</script>

<div class="webcam_container">
    <div id="webcam_mirror"> <!--  -->
        <video id="webcam" autoplay playsinline><track kind="captions" src=""></video>
        {#if !showVideo}
            <div class="video_block"></div>
        {/if}
        <canvas class="output_canvas" id="output_canvas" width="2000" height="1500"></canvas> <!-- used for drawing of lines, points and bounding box -->
        <div id="loading_text">Načítání...</div>
    </div>
</div>

<style>
    .webcam_container{
        display: flex;
        justify-content: left;
    }

    .video_block{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #444444;
    }

    #webcam_mirror{
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1);
        position: relative;
    }

    #webcam{
        width: 100%;
        height: 100%;
    }

    #output_canvas{
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
    }

    #loading_text{
        position: absolute;
        top: 50%;
        right: 33%;
        transform: scaleX(-1);

        font-size: 48px;
        font-weight: bold;
        color: #d9d9d9;
    }
</style>
