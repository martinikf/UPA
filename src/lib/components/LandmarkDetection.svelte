<script lang="ts">
    // based on: https://codepen.io/mediapipe-preview/pen/gOKBGPN
    import { HandLandmarker, FilesetResolver, GestureRecognizer,  DrawingUtils, type HandLandmarkerResult} from "@mediapipe/tasks-vision";
    import { createEventDispatcher } from 'svelte';
    import { browser } from '$app/environment';

    const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ch']
    const msToNextPredict = 80;
    let lastVideoTime = -1;
    let results : HandLandmarkerResult | undefined;

    let videoHeight = 360;
    let videoWidth = 480;

    let handLandmarker : HandLandmarker | undefined;
    let webcamRunning: boolean = false;
    let tfliteModel : tflite.TFLiteModel | undefined;

    let loading_text_html : HTMLElement | null;

    if(browser){
        const video = document.getElementById("webcam") as HTMLVideoElement;
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
    }

    export function setSize(width: number, height: number){
        videoWidth = width;
        videoHeight = height;
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

        // getUsermedia parameters.
        const constraints = {
            video: true
        };

        // Activate the webcam stream.
        navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
            video.srcObject = stream;
            video.addEventListener("loadeddata", () => {predictWebcam(canvasElement, canvasCtx, video)});
        });
    }

    function loadingDone(){
        if(loading_text_html)
            loading_text_html.style.display = "none";
    }


    let lastTimeMs : number = 0;
    async function predictWebcam(canvasElement : HTMLCanvasElement, canvasCtx : CanvasRenderingContext2D, video : HTMLVideoElement) {
        const webcamElement = document.getElementById("webcam");

        loadingDone();

        if(canvasCtx === null || handLandmarker === undefined || video === null || webcamElement === null){
            return;
        }

        let startTimeMs = performance.now();
        if(startTimeMs - msToNextPredict < lastTimeMs){
            return window.requestAnimationFrame(() => {predictWebcam(canvasElement, canvasCtx, video)});
        }
        if (lastVideoTime !== video.currentTime) {
            console.log(startTimeMs - lastTimeMs + " ms"); // time to render one frame
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

            const abosluteLandmarks = calcAbsolutePositions(results.landmarks[0], video.videoWidth, video.videoHeight);

            //Convert landmarks to relative normalized coordtinates
            const relativeLandmarks = calcRelativeLandmarks(abosluteLandmarks);

            //Run ML model, get for each gesture its probability
            const probabilities = await handGestureClassifier(relativeLandmarks);

            let result : {[key: string]: number} = {}
            for(let i = 0; i < probabilities.length; i++){
                if(probabilities[i] > 0.2){
                    console.log("Gesture " + letters[i] + " has probability " + probabilities[i]);
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
        if(tfliteModel === undefined) {
            tflite.setWasmPath(
              'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.8/dist/'
            );
            tfliteModel = await tflite.loadTFLiteModel('models/keypoint_classifier.tflite');
            // https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-webgpu
            //tf.setBackend('webgpu'); // TODO: run ML on GPU
        }
    }

    async function handGestureClassifier(landmarks : number[]) : Promise<number[]>{

        if(tfliteModel === undefined){
           await loadTF();
        }

        const input = tf.tensor(landmarks, [1, 42]);
        const output = tfliteModel.predict(input);

        return await output.dataSync();
    }

</script>

<svelte:head>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-core"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-cpu"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite/dist/tf-tflite.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-webgpu/dist/tf-backend-webgpu.js"></script>
</svelte:head>

<div id="webcamDiv" style="--videoWidth: {videoWidth}; --videoHeight: {videoHeight}">
    <video id="webcam" autoplay playsinline><track kind="captions" src=""></video>
    <canvas class="output_canvas" id="output_canvas" width="1920" height="1080"></canvas>
    <div id="loading_text">Načítání...</div>
</div>

<style>
    #webcamDiv{
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1);
        width: calc(var(--videoWidth) * 1px);
        height: calc(var(--videoHeight) * 1px);
        position: relative;
    }

    #webcam{
        width: calc(var(--videoWidth) * 1px);
        height: calc(var(--videoHeight) * 1px);
    }

    #output_canvas{
        width: calc(var(--videoWidth) * 1px);
        height: calc(var(--videoHeight) * 1px);
        position: absolute;
        left: 0;
        top: 0;
    }

    #loading_text{
        position: absolute;
        top: 50%;
        right: 33%;
        transform: scaleX(-1);

        font-size: 48px;
        font-weight: bold;
        color: #a51c51;
    }
</style>